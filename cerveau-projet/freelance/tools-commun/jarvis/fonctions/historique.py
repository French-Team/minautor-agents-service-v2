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
    # Encart = vue RAPIDE : raison tronquee a 80 caracteres (r[:77] + '...')
    # pour la lisibilite du tableau. Le texte COMPLET reste dans le corps
    # chronologique (_ecrire_corps ci-dessous) : rien n est perdu.
    raison_encart = raison if len(raison) <= 80 else raison[:77] + "..."
    nouvelle_entree = f"| {heure} | {agent} | {llm} | {type_action} | {raison_encart} |"
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
    contenu = "\n".join(lignes)
    # JOURNAL CHRONOLOGIQUE (v0.12.1) : en PLUS de l encart, chaque
    # entree est ecrite dans le corps (## JJ/MM/AAAA / ### agent /
    # - HH:MM | id | TYPE | raison). Sans cela, tout ce qui sort de
    # l encart (10 lignes max) est PERDU : la tracabilite longue est
    # impossible. Structure identique a celle de la v1 pour coexister
    # dans le meme fichier.
    contenu = _ecrire_corps(contenu, now, agent, llm, type_action, raison)
    HISTORIQUE_FILE.write_text(contenu, encoding="utf-8")
    print(f"[JARVIS] Historique: {agent} a {heure}")
    return True


def _ecrire_corps(contenu, maintenant, agent, llm, type_action, raison):
    """Journal chronologique : inserer '- HH:MM | id | TYPE | raison'
    dans le bloc '### agent' de la section '## JJ/MM/AAAA'. Cree la
    section jour et le bloc agent s ils n existent pas. La colonne porte
    l ID LLM (comme l encart), pas le nom de l agent : c est le format
    timeline de la v1 qui coexiste dans AGENTS-historique.md."""
    date_jour = maintenant.strftime("%d/%m/%Y")
    heure = maintenant.strftime("%H:%M:%S.%f")[:12]
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
        # section jour absente : creer apres les encarts (fin du bloc
        # '---' qui suit le dernier encart, sinon fin du fichier)
        idx_ins = len(lignes)
        for i, ligne in enumerate(lignes):
            if ligne.strip() == "## Activites recentes -- session-admin":
                # la section jour doit etre APRES tous les encarts
                idx_ins = len(lignes)
            if ligne.strip().startswith("## ") and i > 0:
                idx_ins = i
        if idx_ins == len(lignes) or idx_ins == 0:
            lignes.append("")
            lignes.append(marqueur_jour)
            idx_jour = len(lignes) - 1
        else:
            while idx_ins < len(lignes) and lignes[idx_ins].strip() == "":
                idx_ins += 1
            lignes.insert(idx_ins, "")
            lignes.insert(idx_ins, marqueur_jour)
            idx_jour = idx_ins
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
        # creer le bloc agent : insere apres la section jour (apres les
        # lignes vides qui suivent le titre), avant la prochaine section
        idx_ins = fin_jour
        if lignes[idx_ins - 1].strip() == "":
            idx_ins -= 1
        while idx_ins > idx_jour and lignes[idx_ins - 1].strip() == "":
            idx_ins -= 1
        bloc = ["", marqueur_agent, ligne_entree]
        for k, b in enumerate(bloc):
            lignes.insert(idx_ins + k, b)
        return "\n".join(lignes)
    # 3) inserer l entree dans le bloc agent (les plus recentes en HAUT)
    idx_ins = idx_agent + 1
    while idx_ins < fin_jour and lignes[idx_ins].strip() == "":
        idx_ins += 1
    if idx_ins < fin_jour and lignes[idx_ins].strip().startswith("- "):
        lignes.insert(idx_ins, ligne_entree)
    else:
        lignes.insert(idx_agent + 1, ligne_entree)
    return "\n".join(lignes)


def cmd_historiser(args):
    historiser(args.agent, args.raison, args.type,
               session=getattr(args, "session", ""))
