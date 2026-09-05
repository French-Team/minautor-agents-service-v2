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
    '**Nom** : contenu' quelconques (+ lignes de continuation).
    Le resume est la concatenation de TOUS les champs dans leur ordre
    d apparition (aucune perte - PAC-7) ; si le bloc n a aucun champ
    structure, repli sur le corps brut du bloc (PAC-3 : le format v1
    reel utilise Contexte/Actions/Lecons/Mission/Livrables/Resultat,
    pas Tache/Erreur). La categorie est derivee du titre
    (ERREUR -> correction, sinon technique) ;
    source = chemin du fichier d origine.

    Deduplication par (agent, titre) EXACT - stable meme si le parse
    evolue (rejouabilite, PAC-8).

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
            if not titre:
                continue
            # extraire TOUS les champs structures (ordre d apparition)
            champs = []
            cle_courante = None
            for ligne in lignes[1:]:
                m = re.match(r"\*\*(.+?)\*\*\s*:?\s*(.*)", ligne.strip())
                if m:
                    cle_courante = m.group(1).strip().lower()
                    champs.append([cle_courante, []])
                    if m.group(2).strip():
                        champs[-1][1].append(m.group(2).strip())
                elif cle_courante and ligne.strip():
                    champs[-1][1].append(ligne.strip())
            # resume = tous les champs non vides, dans l ordre (PAC-7)
            parties = []
            for cle, valeurs in champs:
                contenu = " ".join(valeurs).strip()
                if contenu:
                    parties.append(cle.capitalize() + " : " + contenu)
            resume = " ".join(parties).strip()
            if not resume:
                # repli : corps brut du bloc (hors en-tete) - PAC-3
                resume = " ".join(l.strip() for l in lignes[1:]
                                   if l.strip()).strip()
            if not resume:
                continue
            # categorie derivee : ERREUR dans le titre -> correction,
            # sinon lecon positive -> technique
            categorie = ("correction" if "ERREUR" in (titre or "").upper()
                         else "technique")
            mots = (titre or "").replace("--", " ").lower()
            # deja importee ? (meme agent + meme titre exact)
            if _existe(agent, titre):
                continue
            enregistrer(agent, resume, categorie=categorie,
                        mots_cles=mots, source=chemin, titre=titre)
            importe += 1
    return importe


def _existe(agent, titre):
    """True si une lecon (agent, titre) exact existe deja en BDD.

    Cle stable pour la rejouabilite : independante de l evolution du
    parse de resume (PAC-8).
    """
    conn = connexion()
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM lecons WHERE agent = ? AND titre = ?",
                    (agent, titre))
        return cur.fetchone() is not None
    finally:
        conn.close()


# ------------------------------------------------------------------
# migration depuis lecons.db v1 (plan migration v1->v2, PAC-4/5/7/8)
# ------------------------------------------------------------------

def migrer_depuis_lecons_db(chemin_v1, dry_run=False):
    """Migrer les lecons du lecons.db v1 vers la BDD v2 (bdd-lecons).

    Schema v1 : id/date/agent/domaine/tags/titre/lecon/mission/outils/verdict
    Schema v2 : id/date/agent/categorie/titre/resume/mots_cles/source

    Mapping :
      - date    -> date (texte tel quel)
      - agent   -> agent
      - titre   -> titre
      - lecon   -> resume (texte complet de la lecon)
      - domaine -> mots_cles (enrichi des tags)
      - tags    -> mots_cles
      - verdict -> prefixe "[verdict: X] " dans resume si present (PAC-7 :
                   aucune perte silencieuse)
      - mission/outils -> fusionnes dans resume en fin de texte (format
                   parseable "[mission: ...] [outils: ...]") - pas de perte
      - source  -> 'v1-lecons.db'
      - categorie derivee du domaine/verdict (defaut 'correction')

    REJOUABILITE (PAC-8) : transaction SQLite (BEGIN/COMMIT, rollback sur
    erreur) + deduplication applicative par (agent, titre, date) - une lecon
    deja presente en v2 (meme agent + meme titre + meme date) n est PAS
    re-inseree. Lancer 2x = meme resultat.

    COMPTAGES DYNAMIQUES (PAC-5) : affiche SELECT COUNT source puis cible.

    Retourne le nombre de lecons importees.
    """
    import sqlite3 as _sqlite
    if not os.path.isfile(chemin_v1):
        raise ValueError("lecons.db v1 introuvable : %s" % chemin_v1)
    # comptage source (dynamique)
    conn_v1 = _sqlite.connect(chemin_v1)
    try:
        nb_source = conn_v1.execute(
            "SELECT COUNT(*) FROM lecons").fetchone()[0]
    finally:
        conn_v1.close()
    # deja presentes en v2 (pour la deduplication)
    deja = set()
    for l in lister(n=100000):
        deja.add((l["agent"], l["titre"], l["date"]))
    conn_v1 = _sqlite.connect(chemin_v1)
    conn_v1.row_factory = _sqlite.Row
    lignes = []
    try:
        cur = conn_v1.execute(
            "SELECT date, agent, domaine, tags, titre, lecon, mission, "
            "outils, verdict FROM lecons ORDER BY id")
        for r in cur:
            lignes.append(dict(r))
    finally:
        conn_v1.close()
    importe = 0
    # deja en v2 parmi les lignes source (pour l affichage dry-run)
    deja_parmi_source = sum(1 for l in lignes if (
        (l.get("agent") or "").strip(),
        (l.get("titre") or "").strip(),
        (l.get("date") or "").strip()) in deja)
    if dry_run:
        print("[migration] dry-run : %d lecons source, %d deja en v2, "
              "%d a importer"
              % (nb_source, deja_parmi_source,
                 nb_source - deja_parmi_source))
        return 0
    conn = connexion()
    try:
        conn.execute("BEGIN")
        for r in lignes:
            agent = (r.get("agent") or "").strip()
            date = (r.get("date") or "").strip()
            lecon = (r.get("lecon") or "").strip()
            if not agent or not lecon:
                continue
            titre = (r.get("titre") or "").strip()
            # titre vide : derive du debut de la lecon (titre_auto) -
            # jamais de perte (PAC-7)
            if not titre:
                titre = titre_auto(lecon)
            # dedup APRES derivation du titre (rejeu idempotent)
            clef = (agent, titre, date)
            if clef in deja:
                continue
            # resume : lecon + verdict + mission + outils (aucune perte)
            resume = lecon
            verdict = (r.get("verdict") or "").strip()
            mission = (r.get("mission") or "").strip()
            outils = (r.get("outils") or "").strip()
            if verdict:
                resume += " [verdict: %s]" % verdict
            if mission:
                resume += " [mission: %s]" % mission
            if outils:
                resume += " [outils: %s]" % outils
            # mots_cles : domaine + tags
            domaine = (r.get("domaine") or "").strip()
            tags = (r.get("tags") or "").strip()
            mots = ", ".join(x for x in (domaine, tags) if x)
            # categorie derivee du domaine/verdict (defaut correction)
            domaine_l = domaine.lower()
            if any(m in domaine_l for m in ("test", "non-regression")):
                categorie = "technique"
            elif any(m in domaine_l for m in ("outil", "outils", "cli")):
                categorie = "outil"
            elif any(m in domaine_l for m in ("protocole", "regle", "regles")):
                categorie = "protocole"
            elif "carte" in domaine_l or "parcours" in domaine_l:
                categorie = "carte"
            elif any(m in domaine_l for m in ("audit", "controle",
                                              "verification", "verif")):
                categorie = "processus"
            elif "correction" in domaine_l or "corrig" in domaine_l:
                categorie = "correction"
            elif any(m in domaine_l for m in ("migration", "creation",
                                              "conception", "formation",
                                              "education", "redaction")):
                categorie = "autre"
            else:
                categorie = "correction"
            # insertion (INSERT OR IGNORE logique : dedup deja faite)
            cur = conn.cursor()
            cur.execute(
                "INSERT OR IGNORE INTO lecons (date, agent, categorie, "
                "titre, resume, mots_cles, source) VALUES (?,?,?,?,?,?,?)",
                (date, agent, categorie, titre, resume, mots,
                 "v1-lecons.db"))
            if cur.rowcount:
                importe += 1
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    nb_cible = compter()
    print("[migration] %d lecons importees de lecons.db v1 "
          "(source=%d, cible=%d)" % (importe, nb_source, nb_cible))
    return importe


# ------------------------------------------------------------------
# verification d integralite de la migration (PAC-6, commande --verifier)
# ------------------------------------------------------------------

def verifier_migration(chemin_v1):
    """Verifier l integralite de la migration v1 -> v2 (PAC-6).

    Controles :
      1. comptage dynamique : source (lecons.db v1) vs cible migree
         (source='v1-lecons.db' en v2) - parite globale ET par agent ;
      2. 0 doublon : aucune paire (agent, titre, date) en double en v2 ;
      3. echantillon de controle : 3 lecons affichees (source + cible).

    Retourne True si tous les controles passent.
    """
    import sqlite3 as _sqlite
    ok = True
    if not os.path.isfile(chemin_v1):
        print("[verifier] KO : lecons.db v1 introuvable : %s" % chemin_v1)
        return False
    # 1. comptage source (dynamique)
    conn_v1 = _sqlite.connect(chemin_v1)
    try:
        nb_source = conn_v1.execute(
            "SELECT COUNT(*) FROM lecons").fetchone()[0]
        cur = conn_v1.execute(
            "SELECT agent, COUNT(*) FROM lecons GROUP BY agent")
        par_agent_source = dict(cur.fetchall())
    finally:
        conn_v1.close()
    conn = connexion()
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM lecons WHERE source='v1-lecons.db'")
        nb_migre = cur.fetchone()[0]
        cur.execute("SELECT agent, COUNT(*) FROM lecons "
                    "WHERE source='v1-lecons.db' GROUP BY agent")
        par_agent_migre = dict(cur.fetchall())
        # 2. doublons (agent, titre, date) en v2
        cur.execute("SELECT COUNT(*) FROM (SELECT agent, titre, date, "
                    "COUNT(*) c FROM lecons GROUP BY agent, titre, date "
                    "HAVING c > 1)")
        doublons = cur.fetchone()[0]
        # 3. echantillon : 3 lecons migrees
        cur.execute("SELECT date, agent, titre FROM lecons "
                    "WHERE source='v1-lecons.db' ORDER BY id LIMIT 3")
        echantillon = cur.fetchall()
    finally:
        conn.close()
    print("[verifier] comptage : source v1 = %d, migrees v2 = %d"
          % (nb_source, nb_migre))
    if nb_source != nb_migre:
        ok = False
        print("[verifier] KO : ecart global source/cible (%d != %d)"
              % (nb_source, nb_migre))
    # parite par agent
    ecarts = {a: par_agent_source.get(a, 0) - par_agent_migre.get(a, 0)
              for a in set(par_agent_source) | set(par_agent_migre)
              if par_agent_source.get(a, 0) != par_agent_migre.get(a, 0)}
    if ecarts:
        ok = False
        print("[verifier] KO : ecarts par agent : %s" % ecarts)
    else:
        print("[verifier] parite par agent : OK (%d agents)"
              % len(par_agent_source))
    if doublons:
        ok = False
        print("[verifier] KO : %d doublon(s) (agent, titre, date) en v2"
              % doublons)
    else:
        print("[verifier] doublons : 0")
    print("[verifier] echantillon (3 premieres migrees) :")
    for date, agent, titre in echantillon:
        print("  - %s | %s | %s" % (date, agent, (titre or "")[:70]))
    if ok:
        print("[verifier] VERDICT : OK - migration integre (0 perte, "
              "0 doublon)")
    else:
        print("[verifier] VERDICT : KO")
    return ok
