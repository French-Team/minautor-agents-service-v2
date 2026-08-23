# -*- coding: ascii -*-
"""fonctions/rappels.py - UNE tache : retourner les rappels pertinents
pour un contexte donne (D15 : les messages vivent dans rappels.json)."""

import json
import os
import sys

_sys_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "..", "os_path", "fonctions")
sys.path.insert(0, _sys_dir)
from racine import trouver_racine

RACINE = trouver_racine(__file__)
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "..", "rappels.json")


def charger():
    try:
        return json.loads(open(DATA_FILE, encoding="utf-8").read())["rappels"]
    except (OSError, ValueError, KeyError):
        return []


def pour(contexte):
    """Rappels dont le contexte correspond (exact ou partiel)."""
    contexte = contexte.lower().strip()
    resultats = []
    for r in charger():
        c = r.get("contexte", "").lower()
        if contexte and (c in contexte or contexte in c or contexte == "tout"):
            resultats.append(r)
    if not resultats and contexte:
        # aucun match exact : retourner tout (prudence > silence)
        resultats = charger()
    return resultats


def lister():
    return [(r.get("contexte"), r.get("message", "")[:70])
            for r in charger()]
