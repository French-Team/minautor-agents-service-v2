# -*- coding: ascii -*-
"""fonctions/core.py - fondations JARVIS : chemins, JSONL, agents (D15).

Une tache : fournir les primitives partagees par tous les modules.
"""

import json
from pathlib import Path

JARVIS_DIR = Path(__file__).parent.parent
INBOX_DIR = JARVIS_DIR / "inbox"
OUTBOX_DIR = JARVIS_DIR / "outbox"


def _charger_donnees_agents():
    """v0.1.1/D15 : agents = [{nom, role, fiche, corrections}, ...]."""
    chemin = Path(__file__).parent.parent / "jarvis-data.json"
    try:
        donnees = json.loads(chemin.read_text(encoding="utf-8"))["agents"]
    except (OSError, ValueError, KeyError):
        return {}
    return {a["nom"]: a for a in donnees if isinstance(a, dict) and "nom" in a}


AGENTS_INFOS = _charger_donnees_agents()
AGENTS_VALIDES = set(AGENTS_INFOS)


def get_inbox(agent: str) -> Path:
    return INBOX_DIR / f"{agent}.jsonl"


def get_outbox(agent: str) -> Path:
    return OUTBOX_DIR / f"{agent}.jsonl"


def lire_jsonl(path: Path) -> list:
    """Lire un fichier JSONL et retourner la liste de messages."""
    if not path.exists():
        return []
    messages = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    messages.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return messages


def ecrire_jsonl(path: Path, messages: list):
    """Ecrire une liste de messages en JSONL."""
    with open(path, "w", encoding="utf-8") as f:
        for msg in messages:
            f.write(json.dumps(msg, ensure_ascii=False) + "\n")


def ajouter_message(path: Path, message: dict):
    """Ajouter un message a la fin d'un fichier JSONL."""
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(message, ensure_ascii=False) + "\n")


def marquer_lu(agent, ids):
    """v0.5.0 : marquer lu+accuse une liste d'IDs dans l'inbox de l'agent
    ET l'outbox de chaque expediteur. Retourne le nb marques."""
    messages = lire_jsonl(get_inbox(agent))
    marques = 0
    expediteurs = {}
    for m in messages:
        if m.get("id") in ids and not m.get("lu"):
            m["lu"] = True
            m["accuse"] = True
            marques += 1
            expediteurs.setdefault(m.get("de"), []).append(m["id"])
    if marques:
        ecrire_jsonl(get_inbox(agent), messages)
        for exp, exp_ids in expediteurs.items():
            try:
                outbox_msgs = lire_jsonl(get_outbox(exp))
            except OSError:
                continue
            modifie = False
            for m in outbox_msgs:
                if m.get("id") in exp_ids and not m.get("lu"):
                    m["lu"] = True
                    m["accuse"] = True
                    modifie = True
            if modifie:
                ecrire_jsonl(get_outbox(exp), outbox_msgs)
    return marques
