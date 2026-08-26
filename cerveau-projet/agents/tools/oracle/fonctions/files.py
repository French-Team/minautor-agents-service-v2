# -*- coding: ascii -*-
"""fonctions/files.py - Files de missions pour Oracle (v1).

Une mission en attente est stockee dans files/<file>.jsonl.
Files : asap (prioritaire), normale, plus-tard.

Chaque mission : {id, date, mission, statut, agent}
Statuts : EN_ATTENTE -> PRISE -> TERMINEE
"""

import json
import uuid
from datetime import datetime
from pathlib import Path

FILES_DIR = Path(__file__).parent.parent / "files"
FILES_DIR.mkdir(exist_ok=True)

FILES_VALIDES = ["asap", "normale", "plus-tard"]


def _file_path(nom):
    """Chemin vers le fichier de file."""
    if nom not in FILES_VALIDES:
        return None
    return FILES_DIR / f"{nom}.jsonl"


def ajouter(mission, file="asap", agent=""):
    """Ajouter une mission dans la file."""
    chemin = _file_path(file)
    if chemin is None:
        return None, f"file invalide '{file}' (valides: {', '.join(FILES_VALIDES)})"
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


def cmd_mission_terminer(args):
    """Terminer une mission."""
    entree, erreur = terminer(args.id, file=args.file)
    if erreur:
        print(f"[ORACLE] ERREUR: {erreur}")
        return
    print(f"[ORACLE] Mission {args.id} terminee")


def cmd_mission_lister(args):
    """Lister les missions."""
    file = getattr(args, "file", None)
    missions = lister(file)
    if not missions:
        print("[ORACLE] Aucune mission")
        return
    en_attente = sum(1 for m in missions if m.get("statut") == "EN_ATTENTE")
    print(f"[ORACLE] {len(missions)} mission(s), {en_attente} en attente:")
    for m in missions:
        statut = m.get("statut", "?")
        marqueur = " *" if statut == "EN_ATTENTE" else ""
        print(f"  [{m['_file']:10s}] {m['id']} {statut}{marqueur} : {m['mission'][:60]}")
