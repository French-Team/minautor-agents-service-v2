# -*- coding: ascii -*-
"""fonctions/bdd_lecons.py - BDD des lecons v2 (SQLite, D10).

La BDD des lecons v2 (decision D10, proposition-v2.md) : lecons CLASSEES,
CATEGORISEES, consultables comme une bible au moment du besoin.

Stockage SQLite (modele du classeur v2 : rapide, consultation immediate) :
  - Table lecons : id, date, agent, categorie, titre, resume, mots_cles, source
  - Chaque lecon est enregistree via l outil (id auto, date auto, titre auto)
  - Consultation : lister (20 dernieres) / chercher (--mot-cle, --categorie, --agent)

Format d une lecon (spec mission 27253d81) :
  {id, date, agent, categorie(outil|protocole|processus|carte|correction|technique|autre),
   titre(auto: debut du resume), resume, mots_cles[], source}

Regles :
  - La BDD est le SEUL stockage (pas de fichier markdown pour les lecons).
  - Les agents n ecrivent PLUS leurs lecons dans corrections.md : ils les
    enregistrent ici via l outil bdd-lecons (source = fichier d origine pour
    les lecons migrees).
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

_sys_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "..", "os_path", "fonctions")
sys.path.insert(0, _sys_dir)
from racine import trouver_racine

RACINE = trouver_racine(__file__)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "lecons.db")
DB_PATH = os.path.abspath(DB_PATH)

CATEGORIES = ("outil", "protocole", "processus", "carte", "correction",
              "technique", "autre")

SCHEMA = """
CREATE TABLE IF NOT EXISTS lecons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT DEFAULT '',
    agent TEXT DEFAULT '',
    categorie TEXT DEFAULT 'autre',
    titre TEXT DEFAULT '',
    resume TEXT DEFAULT '',
    mots_cles TEXT DEFAULT '',
    source TEXT DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_lecons_date ON lecons(date);
CREATE INDEX IF NOT EXISTS idx_lecons_agent ON lecons(agent);
CREATE INDEX IF NOT EXISTS idx_lecons_categorie ON lecons(categorie);
"""


def connexion():
    """Ouvrir une connexion (creer la BDD + schema si absents)."""
    dossier = os.path.dirname(DB_PATH)
    if not os.path.isdir(dossier):
        os.makedirs(dossier, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    conn.commit()
    return conn


def timestamp():
    """Horodatage millisecondes (3 chiffres, parite v0.7.3 v1)."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def titre_auto(resume, limite=70):
    """Titre auto : debut du resume (premiere phrase ou 70 caracteres)."""
    resume = (resume or "").strip()
    if not resume:
        return ""
    coupure = resume.find(". ")
    if 0 < coupure < limite:
        return resume[:coupure + 1].strip()
    return resume[:limite].rstrip().strip()


def _mots_cles_norm(mots_cles):
    """Normaliser la liste de mots-cles (str csv ou liste) en csv."""
    if isinstance(mots_cles, (list, tuple)):
        return ",".join(m.strip() for m in mots_cles if m.strip())
    if isinstance(mots_cles, str):
        return ",".join(m.strip() for m in mots_cles.split(",") if m.strip())
    return ""


# ------------------------------------------------------------------
# enregistrer / lister / chercher
# ------------------------------------------------------------------

def enregistrer(agent, resume, categorie="correction", mots_cles="",
                source="bdd-lecons", titre=None):
    """Enregistrer une lecon (id auto, date auto, titre auto sauf si fourni).

    Retourne le dictionnaire de la lecon creee.
    """
    agent = (agent or "").strip()
    resume = (resume or "").strip()
    if not agent or not resume:
        raise ValueError("agent et resume sont obligatoires")
    if categorie not in CATEGORIES:
        categorie = "autre"
    titre = (titre or "").strip() or titre_auto(resume)
    mots = _mots_cles_norm(mots_cles)
    date = timestamp()
    conn = connexion()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO lecons (date, agent, categorie, titre, resume, "
            "mots_cles, source) VALUES (?,?,?,?,?,?,?)",
            (date, agent, categorie, titre, resume, mots, source))
        conn.commit()
        lecon_id = cur.lastrowid
    finally:
        conn.close()
    return {"id": lecon_id, "date": date, "agent": agent,
            "categorie": categorie, "titre": titre, "resume": resume,
            "mots_cles": mots, "source": source}


def lister(n=20):
    """Lister les n dernieres lecons (par date decroissante)."""
    conn = connexion()
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, date, agent, categorie, titre, resume, "
                    "mots_cles, source FROM lecons ORDER BY id DESC LIMIT ?",
                    (n,))
        return [_ligne(r) for r in cur.fetchall()]
    finally:
        conn.close()


def chercher(mot_cle="", categorie="", agent=""):
    """Chercher des lecons par mot-cle (resume/titre/mots_cles),
    categorie et/ou agent. Retourne les plus recentes d abord."""
    conn = connexion()
    try:
        cur = conn.cursor()
        requete = ("SELECT id, date, agent, categorie, titre, resume, "
                   "mots_cles, source FROM lecons WHERE 1=1")
        params = []
        if mot_cle:
            requete += (" AND (resume LIKE ? OR titre LIKE ? OR mots_cles LIKE ?)")
            motif = "%" + mot_cle + "%"
            params += [motif, motif, motif]
        if categorie:
            requete += " AND categorie = ?"
            params.append(categorie)
        if agent:
            requete += " AND agent = ?"
            params.append(agent)
        requete += " ORDER BY id DESC"
        cur.execute(requete, params)
        return [_ligne(r) for r in cur.fetchall()]
    finally:
        conn.close()


def compter():
    """Nombre total de lecons (utile pour la migration)."""
    conn = connexion()
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM lecons")
        return cur.fetchone()[0]
    finally:
        conn.close()


def _ligne(r):
    """Convertir une ligne SQLite en dictionnaire."""
    return {"id": r[0], "date": r[1], "agent": r[2], "categorie": r[3],
            "titre": r[4], "resume": r[5], "mots_cles": r[6], "source": r[7]}


# ------------------------------------------------------------------
# migration depuis les corrections.md (import unique)
# ------------------------------------------------------------------

def migrer_depuis_corrections(chemins):
    """Importer les lecons [LECON] des corrections.md dans la BDD.

    Format parse : '##/### [LECON] <date> -- <titre>' puis champs
    '**Tache**', '**Erreur**', '**Lecon**', '**Pourquoi**',
    '**Cause racine**', '**Correction**'.
    Le resume est la concatenation des champs cles ; la categorie est
    derivee du titre (ERREUR -> correction, sinon technique) ;
    source = chemin du fichier d origine.

    Retourne le nombre de lecons importees (0 si aucune nouvelle).
    """
    import re
    importe = 0
    for chemin in chemins:
        if not os.path.isfile(chemin):
            continue
        agent = os.path.basename(os.path.dirname(chemin))
        with open(chemin, "r", encoding="utf-8-sig") as f:
            texte = f.read()
        blocs = re.split(r"(?m)^#{2,3}\s+\[LECON\]", texte)
        for bloc in blocs[1:]:
            lignes = bloc.splitlines()
            entete = lignes[0].strip() if lignes else ""
            m_date = re.match(r"([0-9]{4}-[0-9]{2}-[0-9]{2})", entete)
            date = m_date.group(1) if m_date else ""
            titre = entete[len(date):].lstrip(" -").strip() if date else entete
            # extraire les champs cles
            champs = {}
            cle_courante = None
            for ligne in lignes[1:]:
                m = re.match(r"\*\*(.+?)\*\*\s*:?\s*(.*)", ligne.strip())
                if m:
                    cle_courante = m.group(1).lower()
                    champs.setdefault(cle_courante, [])
                    if m.group(2).strip():
                        champs[cle_courante].append(m.group(2).strip())
                elif cle_courante and ligne.strip():
                    champs[cle_courante].append(ligne.strip())
            # construire le resume (sans double deux-points)
            parties = []
            for cle in ("tache", "erreur", "lecon", "pourquoi",
                        "cause racine", "correction"):
                if cle in champs:
                    contenu = " ".join(champs[cle]).strip()
                    if contenu:
                        parties.append(cle.capitalize() + " : " + contenu)
            resume = " ".join(parties).strip()
            if not resume:
                continue
            # categorie derivee : ERREUR dans le titre -> correction,
            # sinon lecon positive -> technique
            categorie = ("correction" if "ERREUR" in (titre or "").upper()
                         else "technique")
            mots = (titre or "").replace("--", " ").lower()
            # deja importee ? (meme agent + meme debut de resume)
            deja = chercher(agent=agent, mot_cle=titre_auto(resume, 40))
            if any(deja):
                continue
            enregistrer(agent, resume, categorie=categorie,
                        mots_cles=mots, source=chemin, titre=titre)
            importe += 1
    return importe
