# -*- coding: ascii -*-
"""fonctions/historique.py - UNE tache : ecrire dans AGENTS-historique.md."""

import os
import sys
from datetime import datetime
from pathlib import Path

# P10 : la racine se DETECTE via os_path, elle ne se compte pas
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "os_path", "fonctions"))
from racine import trouver_racine

RACINE = Path(trouver_racine(__file__))
HISTORIQUE_FILE = RACINE / "AGENTS-historique.md"
AGENTS_FILE = Path(os.environ.get("AGENTS_FILE", str(RACINE / "AGENTS.md")))


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
    PREMIER encart d AGENTS-historique.md - souvent session-admin -
    et evince ses lignes par la fenetre glissante)."""
    try:
        _dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "..", "..", "classeur", "fonctions")
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
    """JARVIS enregistre une entree dans AGENTS-historique.md."""
    now = datetime.now()
    heure = now.strftime("%H:%M:%S.%f")[:12]
    if not session:
        session = session_courante()
    llm = lire_nom_llm(session)
    try:
        contenu = HISTORIQUE_FILE.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"[JARVIS] ERREUR: {HISTORIQUE_FILE} introuvable")
        return False
    lignes = contenu.split("\n")
    # Encarts SEPARES par session (demande utilisateur 2026-08-24) :
    # chercher la table DANS l'encart de la session, jamais avant.
    zone_debut = 0
    if session:
        entete_encart = f"## Activites recentes -- {session}"
        trouve_encart = False
        for i, ligne in enumerate(lignes):
            if ligne.strip() == entete_encart:
                zone_debut = i
                trouve_encart = True
                break
        if not trouve_encart:
            print(f"[JARVIS] ATTENTION: encart '{session}' introuvable "
                  f"- premiere table utilisee")
    idx_tableau = -1
    for i in range(zone_debut, len(lignes)):
        if "| Heure | Agent |" in lignes[i]:
            idx_tableau = i
            break
    if idx_tableau == -1:
        print("[JARVIS] ERREUR: Section Activites recentes non trouvee")
        return False
    nouvelle_entree = f"| {heure} | {agent} | {llm} | {type_action} | {raison} |"
    idx_separateur = idx_tableau + 1
    while idx_separateur < len(lignes) and not lignes[idx_separateur].startswith("|---"):
        idx_separateur += 1
    insert_pos = idx_separateur + 1
    lignes.insert(insert_pos, nouvelle_entree)
    debut_entrees = insert_pos + 1
    fin_entrees = debut_entrees
    while fin_entrees < len(lignes) and lignes[fin_entrees].startswith("| "):
        fin_entrees += 1
    nb_entrees = fin_entrees - debut_entrees
    if nb_entrees > 10:
        # les entrees sont triees plus recent en haut : les plus vieilles sont en BAS
        lignes = lignes[:fin_entrees - (nb_entrees - 10)] + lignes[fin_entrees:]
    HISTORIQUE_FILE.write_text("\n".join(lignes), encoding="utf-8")
    print(f"[JARVIS] Historique: {agent} a {heure}")
    return True


def cmd_historiser(args):
    historiser(args.agent, args.raison, args.type,
               session=getattr(args, "session", ""))
