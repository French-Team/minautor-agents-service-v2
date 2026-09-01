# -*- coding: ascii -*-
"""fonctions/files.py - Files de missions pour Oracle (v1).

Une mission en attente est stockee dans files/<file>.jsonl.
Files : asap (prioritaire), normale, plus-tard, attente (missions
interrompues, transposition de la file-attente v2 - decision utilisateur
2026-08-29 : mise en attente de la mission en cours lors d un inter-round).

Chaque mission : {id, date, mission, statut, agent}
Statuts : EN_ATTENTE -> PRISE -> TERMINEE
"""

import json
import uuid
from datetime import datetime
from pathlib import Path

FILES_DIR = Path(__file__).parent.parent / "files"
FILES_DIR.mkdir(exist_ok=True)

FILES_VALIDES = ["asap", "normale", "plus-tard", "attente"]


def _file_path(nom):
    """Chemin vers le fichier de file."""
    if nom not in FILES_VALIDES:
        return None
    return FILES_DIR / f"{nom}.jsonl"


def ajouter(mission, file="asap", agent=""):
    """Ajouter une mission dans la file, sans duplicata en attente."""
    chemin = _file_path(file)
    if chemin is None:
        return None, f"file invalide '{file}' (valides: {', '.join(FILES_VALIDES)})"
    mission_norm = " ".join((mission or "").split()).casefold()
    for ligne in chemin.read_text(encoding="utf-8").splitlines() if chemin.exists() else []:
        try:
            ancien = json.loads(ligne)
        except ValueError:
            continue
        if (ancien.get("statut") == "EN_ATTENTE"
                and ancien.get("agent", "").strip().casefold() == (agent or "").strip().casefold()
                and " ".join((ancien.get("mission", "")).split()).casefold() == mission_norm):
            return ancien, "doublon: mission deja en attente"
    entree = {
        "id": uuid.uuid4().hex[:8],
        "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "mission": mission,
        "statut": "EN_ATTENTE",
        "agent": agent,
    }
    with open(chemin, "a", encoding="utf-8") as f:
        f.write(json.dumps(entree, ensure_ascii=False) + "\n")
    return entree, None


def prendre(file="asap"):
    """Prendre la premiere mission en attente (FIFO)."""
    chemin = _file_path(file)
    if chemin is None:
        return None, f"file invalide '{file}'"
    if not chemin.exists():
        return None, None
    lignes = [l.strip() for l in chemin.read_text(encoding="utf-8").splitlines() if l.strip()]
    for i, l in enumerate(lignes):
        try:
            e = json.loads(l)
            if e.get("statut") == "EN_ATTENTE":
                e["statut"] = "PRISE"
                lignes[i] = json.dumps(e, ensure_ascii=False)
                with open(chemin, "w", encoding="utf-8") as f:
                    f.write("\n".join(lignes) + "\n")
                return e, None
        except ValueError:
            continue
    return None, None


def terminer(id_mission, file="asap"):
    """Marquer une mission comme terminee."""
    chemin = _file_path(file)
    if chemin is None:
        return None, f"file invalide '{file}'"
    if not chemin.exists():
        return None, "mission introuvable"
    lignes = [l.strip() for l in chemin.read_text(encoding="utf-8").splitlines() if l.strip()]
    for i, l in enumerate(lignes):
        try:
            e = json.loads(l)
            if e.get("id") == id_mission:
                e["statut"] = "TERMINEE"
                lignes[i] = json.dumps(e, ensure_ascii=False)
                with open(chemin, "w", encoding="utf-8") as f:
                    f.write("\n".join(lignes) + "\n")
                return e, None
        except ValueError:
            continue
    return None, "mission introuvable"


def lister(file=None):
    """Lister les missions (toutes les files si file=None)."""
    resultats = []
    files = FILES_VALIDES if file is None else [file]
    for nom in files:
        chemin = _file_path(nom)
        if chemin is None or not chemin.exists():
            continue
        for l in chemin.read_text(encoding="utf-8").splitlines():
            if not l.strip():
                continue
            try:
                e = json.loads(l)
                e["_file"] = nom
                resultats.append(e)
            except ValueError:
                continue
    return resultats


def en_attente_count(file=None):
    """Nombre de missions en attente."""
    return sum(1 for m in lister(file) if m.get("statut") == "EN_ATTENTE")


def cmd_mission_ajouter(args):
    """Ajouter une mission dans une file."""
    entree, erreur = ajouter(args.mission, file=args.file, agent=getattr(args, "agent", ""))
    if erreur:
        if erreur.startswith("doublon:"):
            print(f"[ORACLE] Mission deja en attente: {entree['id']} ({args.file})")
        else:
            print(f"[ORACLE] ERREUR: {erreur}")
        return
    print(f"[ORACLE] Mission ajoutee: {entree['id']} ({args.file})")


def cmd_mission_prendre(args):
    """Prendre la premiere mission en attente."""
    entree, erreur = prendre(args.file)
    if erreur:
        print(f"[ORACLE] ERREUR: {erreur}")
        return
    if entree is None:
        print(f"[ORACLE] Aucune mission en attente dans '{args.file}'")
        return
    print(f"[ORACLE] Mission {entree['id']} prise:")
    print(f"  Date: {entree['date']}")
    print(f"  Mission: {entree['mission']}")


# Cartes de deduction de l agent cible depuis le TEXTE de la mission,
# quand la mission est deposee sans champ `agent` explicite. Decision
# utilisateur 2026-08-29 : Oracle choisit l agent habilite puis historise
# son DEBUT a sa place et lance le pilote.
_CARTE_AGENT = [
    # Alerte de coordination (v1) : un ETAT URGENT / P1 non-acquittes doit
    # revenir a ORACLE (coordinateur de la coordination) qui declenche le
    # super-combo purge-p1 pour distribuer les P1 a chaque destinataire,
    # au lieu du fallback vague cerberus (lecon 2026-08-30). Placee en
    # TETE : prioritaire sur toute autre carte.
    (["etat urgent", "p1 non-acquitte", "p1 non acquitte",
      "purge p1", "alerts de coordination", "coordination v1"],
     "oracle"),
    (["test", "non-regression", "non regression", "ecrire/executer",
      "lancer les tests"], "morpheus"),
    (["outil", "creer/modifier un outil", "optimiser un outil", "construire"],
     "vulcain"),
    (["inventaire", "audit", "verification", "evaluation", "evaluer"],
     "themis"),
    (["pense-bete", "pense bete"], "athena"),
    (["spec"], "promethee"),
    (["todo"], "minerve"),
    (["readme", "muse de l histoire"], "clio"),
    (["orthographe", "vocabulaire", "fautes"], "hermes"),
    (["workspace", "nettoyer", "residus"], "hygie"),
    (["contradiction", "incoherence"], "argus"),
    (["gardien", "marbre", "zone protegee"], "gardien"),
    (["git"], "hades"),
    (["revision strategique", "prioriser"], "socrate"),
    (["documentation v2", "freelance"], "ferrari"),
]


def deduire_agent(mission, agent_explicite=""):
    """Deviner l agent cible d une mission : champ agent explicite sinon
    deduction par mots-cles sur le texte. Retourne (agent, source)."""
    agent = (agent_explicite or "").strip().lower()
    if agent:
        return agent, "champ-agent"
    texte = (mission or "").lower()
    for mots, cible in _CARTE_AGENT:
        if any(m in texte for m in mots):
            return cible, "deduction"
    return "cerberus", "inconnu"


def relais(file="asap"):
    """Prendre (PRISE) la premiere mission en attente pour la relayer a
    l agent cible. Retourne (entree, erreur). La mission garde son champ
    `agent` (deduit si absent) pour que Oracle sache a qui l envoyer.
    """
    entree, erreur = prendre(file)
    if erreur or entree is None:
        return entree, erreur
    agent, source = deduire_agent(entree.get("mission",
                                              ""), entree.get("agent", ""))
    entree["agent"] = agent
    entree["agent_source"] = source
    return entree, None


def cmd_mission_terminer(args):
    """Terminer une mission."""
    entree, erreur = terminer(args.id, file=args.file)
    if erreur:
        print(f"[ORACLE] ERREUR: {erreur}")
        return
    print(f"[ORACLE] Mission {args.id} terminee")


def cmd_mission_lister(args):
    """Lister les missions.
    v0.6.0 (Verrou bleu) : filtres optionnels --statut et --agent. Par
    defaut comportement inchange (liste toutes les missions de la file).
    Un --statut en MAJUSCULE insensible a la casse, l agent filtre aussi
    en minuscules (l agent peut porter la casse du nom)."""
    file = getattr(args, "file", None)
    filtre_statut = getattr(args, "statut", None)
    filtre_agent = getattr(args, "filtre_agent", None)
    missions = lister(file)
    if missions and filtre_statut:
        missions = [m for m in missions
                    if m.get("statut", "").upper() == filtre_statut.upper()]
    if missions and filtre_agent:
        missions = [m for m in missions
                    if m.get("agent", "").lower() == filtre_agent.lower()]
    if not missions:
        print("[ORACLE] Aucune mission")
        return
    en_attente = sum(1 for m in missions if m.get("statut") == "EN_ATTENTE")
    print(f"[ORACLE] {len(missions)} mission(s), {en_attente} en attente:")
    for m in missions:
        statut = m.get("statut", "?")
        marqueur = " *" if statut == "EN_ATTENTE" else ""
        print(f"  [{m['_file']:10s}] {m['id']} {statut}{marqueur} : {m['mission'][:60]}")
