# -*- coding: ascii -*-
"""fonctions/historique.py v0.15.0 - Trois destinations (fichiers V2 separes,
   decision utilisateur 2026-08-26 : la v2 est l evolution de la v1, chaque
   session a SES fichiers - plus aucun partage v1/v2) :
1. AGENTS-activite-recente-v2.md : vue rapide (encart session-freelance,
   50 entrees max, raison tronquee a 80 car., UTF8+CRLF)
2. AGENTS-historique-v2.md : chronologie body v2 (100 dernieres actions,
   UTF8+CRLF)
3. historique.db (SQLite) : journal chronologique complet (texte integral,
   purge automatique apres 7 jours)
Les fichiers v1 (session-admin) sont geres par activer-agent-principal
(AGENTS-activite-recente.md + AGENTS-historique.md, ASCII+LF).
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# P10 : la racine se DETECTE via os_path, elle ne se compte pas
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "os_path", "fonctions"))
from racine import trouver_racine

RACINE = Path(trouver_racine(__file__))
ACTIVITE_FILE = RACINE / "AGENTS-activite-recente-v2.md"
GRADES_FILE = RACINE / "cerveau-projet" / "freelance" / "tools-commun" \
    / "grades" / "grades-v2.json"
AGENTS_FILE = Path(os.environ.get("AGENTS_FILE", str(RACINE / "AGENTS.md")))

# Import de la BDD (lazy pour ne pas casser si sqlite3 absent)
_bdd = None


def _get_bdd():
    global _bdd
    if _bdd is None:
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import historique_bdd as _hb
            _bdd = _hb
        except ImportError:
            pass
    return _bdd


MAX_ENTREES = 50  # entrees par encart (ancien : 10)
MAX_CORPS = 100  # entrees max dans le corps AGENTS-historique-v2.md
TRONCATURE_ENCART = 80  # raison tronquee dans l encart
HISTORIQUE_FILE = RACINE / "AGENTS-historique-v2.md"

# Grades et couleurs v2 (D15) : la colonne Grade de l encart affiche
# l emoji de la couleur du grade de l agent/routine (decision utilisateur
# 2026-08-26 : haut de grade = bleu/vert, bas de grade = rouge/orange,
# EDITH = rose). Les donnees vivent dans grades-v2.json, jamais en dur.
def _couleur_agent(agent: str) -> str:
    """Emoji couleur du grade d un agent ou d une routine (grades-v2.json)."""
    try:
        data = json.loads(GRADES_FILE.read_text(encoding="utf-8"))
    except Exception:
        return "\u26aa"  # blanc neutre si fichier indisponible
    grade = data.get("agents", {}).get(agent)
    if grade is None:
        grade = data.get("routines", {}).get(agent)
    if grade is None:
        return data.get("defaut", {}).get("emoji", "\u26aa")
    for e in data.get("echelle", []):
        if e.get("grade") == grade:
            return e.get("emoji", "\u26aa")
    return data.get("defaut", {}).get("emoji", "\u26aa")

# Convention v2 : UTF8 + CRLF (D4). Les fichiers -v2 sont en CRLF : on
# normalise la lecture en LF interne, on re-ecrit en CRLF explicite
# (sinon write_text double les \r sur Windows -> corruption).
def _lire(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").replace("\r\n", "\n")
    except FileNotFoundError:
        return ""


def _ecrire(path: Path, contenu: str):
    contenu = contenu.replace("\r\n", "\n").replace("\n", "\r\n")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(contenu)


def lire_nom_llm(session: str = "") -> str:
    """Lit le champ 'Nom LLM' du bloc session dans AGENTS.md (jamais de valeur en dur)."""
    try:
        contenu = AGENTS_FILE.read_text(encoding="utf-8")
    except FileNotFoundError:
        return "inconnu"
    lignes = contenu.split("\n")
    if session:
        debut = None
        for i, ligne in enumerate(lignes):
            if ligne.strip() == f"### Session : {session}":
                debut = i
                break
        if debut is None:
            return "inconnu"
        fin = debut
        while fin < len(lignes) and not lignes[fin].startswith("## "):
            fin += 1
        bloc = lignes[debut:fin]
    else:
        bloc = lignes
    for ligne in bloc:
        if "**Nom LLM**" in ligne:
            parties = [p.strip() for p in ligne.split("|")]
            for j, p in enumerate(parties):
                if p == "**Nom LLM**" and j + 1 < len(parties):
                    return parties[j + 1]
    return "inconnu"


def session_courante() -> str:
    """Session la plus recente du classeur v2 (fallback quand aucune
    session explicite n est passee : sans cela, l entree part dans le
    PREMIER encart - souvent session-admin - et evince ses lignes)."""
    try:
        _dir = os.path.join(RACINE, "cerveau-projet", "freelance",
                            "classeur", "fonctions")
        sys.path.insert(0, _dir)
        import classeur as c
        sessions = c.session_list()
        if sessions:
            return str(sessions[0].get("session", "")) if isinstance(
                sessions[0], dict) else str(sessions[0])
    except Exception:
        pass
    return ""


def historiser(agent: str, raison: str, type_action: str = "R", session: str = ""):
    """JARVIS enregistre une entree :
    1. Dans AGENTS-activite-recente-v2.md (encart vue rapide v2, 50 max)
    2. Dans AGENTS-historique-v2.md (corps chronologique v2, 100 max)
    3. Dans historique.db (BDD chronologique, 7 jours)
    """
    now = datetime.now()
    heure = now.strftime("%H:%M:%S.%f")[:-3]
    if not session:
        session = session_courante()
    llm = lire_nom_llm(session)

    # --- 1. ENCART dans AGENTS-activite-recente-v2.md ---
    _ecrire_encart(session, heure, agent, llm, type_action, raison)

    # --- 2. CORPS dans AGENTS-historique-v2.md (100 max) ---
    _ecrire_corps(now, agent, llm, type_action, raison)

    # --- 3. BDD SQLite (journal chronologique complet) ---
    bdd = _get_bdd()
    if bdd:
        bdd.ecrire(
            racine=str(RACINE),
            agent=agent,
            llm=llm,
            type_action=type_action,
            raison=raison,
            date_iso=now.strftime("%Y-%m-%dT%H:%M:%S")
        )

    print(f"[JARVIS] Historique: {agent} a {heure}")
    return True


def _ecrire_encart(session, heure, agent, llm, type_action, raison):
    """Ecrire dans l encart AGENTS-activite-recente-v2.md (vue rapide v2).
    Raison tronquee a TRONCATURE_ENCART car. Le texte complet est dans la BDD."""
    contenu = _lire(ACTIVITE_FILE)
    if not contenu:
        # Creer le fichier v2 avec l encart session-freelance vide
        contenu = (
            "---\n"
            "identite:\n"
            "  type: activite-recente-v2\n"
            "  appartient_a: freelance\n"
            "  commun: false\n"
            "  description: \"Vue rapide des activites recentes de la session-freelance (50 entrees max, UTF8+CRLF). Fichier separe de la v1 : AGENTS-activite-recente.md (ASCII+LF).\"\n"
            "---\n\n"
            "## Activites recentes -- session-freelance\n\n"
            "| Grade | Agent | Raison | Heure | id | Type |\n"
            "|-------|-------|--------|-------|----|------|\n"
        )
        _ecrire(ACTIVITE_FILE, contenu)

    lignes = contenu.split("\n")

    # Trouver l encart de la session
    entete_encart = f"## Activites recentes -- {session}"
    zone_debut = 0
    trouve_encart = False
    for i, ligne in enumerate(lignes):
        if ligne.strip() == entete_encart:
            zone_debut = i
            trouve_encart = True
            break
    if not trouve_encart:
        print(f"[JARVIS] ATTENTION: encart '{session}' introuvable "
              f"- premiere table utilisee")

    # Trouver le tableau
    idx_tableau = -1
    for i in range(zone_debut, len(lignes)):
        if "| Grade |" in lignes[i] and "| Agent |" in lignes[i]:
            idx_tableau = i
            break
    if idx_tableau == -1:
        print("[JARVIS] ERREUR: Section Activites recentes non trouvee")
        return False

    # Raison tronquee pour l encart + colonne Grade (emoji couleur)
    # ORDRE DES COLONNES (decision utilisateur 2026-08-26) :
    # Grade | Agent | Raison | Heure | id | Type
    raison_encart = raison if len(raison) <= TRONCATURE_ENCART else raison[:TRONCATURE_ENCART - 3] + "..."
    couleur = _couleur_agent(agent)
    nouvelle_entree = f"| {couleur} | {agent} | {raison_encart} | {heure} | {llm} | {type_action} |"

    # Inserer apres le separateur
    idx_separateur = idx_tableau + 1
    while idx_separateur < len(lignes) and not lignes[idx_separateur].startswith("|---"):
        idx_separateur += 1
    insert_pos = idx_separateur + 1
    lignes.insert(insert_pos, nouvelle_entree)

    # Limiter a MAX_ENTREES (debut_entrees = insert_pos : la NOUVELLE
    # entree compte dans le total, sinon le fichier derive a MAX+1 - bug
    # corrige 2026-08-26, l encart oscillait a 51 entrees)
    debut_entrees = insert_pos
    fin_entrees = debut_entrees
    while fin_entrees < len(lignes) and lignes[fin_entrees].startswith("| "):
        fin_entrees += 1
    nb_entrees = fin_entrees - debut_entrees
    if nb_entrees > MAX_ENTREES:
        # Les entrees sont triees plus recent en haut : les plus vieilles en BAS
        lignes = lignes[:fin_entrees - (nb_entrees - MAX_ENTREES)] + lignes[fin_entrees:]

    contenu = "\n".join(lignes)
    _ecrire(ACTIVITE_FILE, contenu)
    return True


def _ecrire_corps(maintenant, agent, llm, type_action, raison):
    """Journal chronologique : inserer '- HH:MM | id | TYPE | raison'
    dans le bloc '### agent' de la section '## JJ/MM/AAAA' de
    AGENTS-historique.md. Limite a MAX_CORPS entrees au total."""
    contenu = _lire(HISTORIQUE_FILE)
    if not contenu:
        return
    date_jour = maintenant.strftime("%d/%m/%Y")
    heure = maintenant.strftime("%H:%M:%S.%f")[:-3]
    ligne_entree = f"- {heure} | {llm} | {type_action} | {raison}"
    marqueur_jour = f"## {date_jour}"
    marqueur_agent = f"### {agent}"
    lignes = contenu.split("\n")
    # 1) trouver ou creer la section jour
    idx_jour = -1
    for i, ligne in enumerate(lignes):
        if ligne.strip() == marqueur_jour:
            idx_jour = i
            break
    if idx_jour == -1:
        # AGENTS-historique.md ne contient PLUS d encarts (decision 2026-08-26 :
        # les encarts vivent dans AGENTS-activite-recente.md). Inserer apres le
        # frontmatter (premier bloc '---') ou en debut de fichier.
        idx_ins = 0
        m_entete = re.search(r"^---\n.*?\n---\n", contenu, re.MULTILINE | re.DOTALL)
        if m_entete:
            idx_ins = m_entete.end()
        else:
            m_section = re.search(r"^## \d{2}/\d{2}/\d{4}", contenu, re.MULTILINE)
            if m_section:
                idx_ins = m_section.start()
        bloc_jour = ["", marqueur_jour, "", marqueur_agent, ligne_entree]
        for k, b in enumerate(bloc_jour):
            lignes.insert(idx_ins + k, b)
        contenu = "\n".join(lignes)
    else:
        # 2) trouver ou creer le bloc agent DANS la section jour
        fin_jour = len(lignes)
        for i in range(idx_jour + 1, len(lignes)):
            if lignes[i].strip().startswith("## ") and lignes[i].strip() != marqueur_jour:
                fin_jour = i
                break
        idx_agent = -1
        for i in range(idx_jour + 1, fin_jour):
            if lignes[i].strip() == marqueur_agent:
                idx_agent = i
                break
        if idx_agent == -1:
            # Creer le bloc agent avant la fin de la section jour
            idx_ins = fin_jour
            while idx_ins > idx_jour + 1 and lignes[idx_ins - 1].strip() == "":
                idx_ins -= 1
            bloc = ["", marqueur_agent, ligne_entree]
            for k, b in enumerate(bloc):
                lignes.insert(idx_ins + k, b)
        else:
            # Inserer apres le marqueur agent (plus recentes en haut)
            idx_ins = idx_agent + 1
            while idx_ins < fin_jour and lignes[idx_ins].strip() == "":
                idx_ins += 1
            lignes.insert(idx_ins, ligne_entree)
        contenu = "\n".join(lignes)
    # 3) limiter a MAX_CORPS entrees dans le corps (hors encarts) PUIS
    #    ECRIRE TOUJOURS le fichier (corrige 2026-08-26 : _ecrire_corps
    #    ne deleguait l ecriture qu a _limiter_corps, qui n ecrit QUE si
    #    le corps depasse MAX_CORPS -> toute entree ajoutee avec un corps
    #    <= 100 etait perdue).
    contenu = _limiter_corps(contenu)
    _ecrire(HISTORIQUE_FILE, contenu)


def _limiter_corps(contenu):
    """Limiter le corps chronologique a MAX_CORPS entrees.
    Compte les lignes '- ' (entrees) hors encarts, supprime les plus
    vieilles si depassement. RETOURNE le contenu limite (l ecriture est
    faite par _ecrire_corps)."""
    lignes = contenu.split("\n")
    # Trouver la fin des encarts (premiere section ## date)
    idx_debut_corps = 0
    for i, ligne in enumerate(lignes):
        if ligne.strip().startswith("## ") and not ligne.strip().startswith("## Activites") and not ligne.strip().startswith("---"):
            if "/" in ligne:  # ## JJ/MM/AAAA
                idx_debut_corps = i
                break
    # Compter les entrees dans le corps
    idx_entrees = []
    for i in range(idx_debut_corps, len(lignes)):
        if lignes[i].strip().startswith("- ") and " | " in lignes[i]:
            idx_entrees.append(i)
    if len(idx_entrees) <= MAX_CORPS:
        return contenu
    # Supprimer les plus vieilles. Le fichier est en ordre DECROISSANT
    # (plus recent en haut) : les plus vieilles sont a la FIN de la liste.
    # (corrige 2026-08-26 : on supprimait le debut = les plus recentes -
    # la nouvelle entree etait evincee des la premiere insertion).
    a_supprimer = len(idx_entrees) - MAX_CORPS
    indices_a_supprimer = sorted(idx_entrees[-a_supprimer:], reverse=True)
    for idx in indices_a_supprimer:
        del lignes[idx]
    return "\n".join(lignes)


def cmd_historiser(args):
    historiser(args.agent, args.raison, args.type,
               session=getattr(args, "session", ""))
