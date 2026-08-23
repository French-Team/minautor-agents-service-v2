# -*- coding: ascii -*-
"""fonctions/commun.py - elements partages des combos JARVIS (v0.1.0)."""

import json
import os
from datetime import datetime

from lib_lecture import lire_texte
from racine import trouver_racine

RACINE = trouver_racine(__file__)

# noms des agents (D15 : source = jarvis-data.json)
_jarvis_data = json.loads(lire_texte(
    "cerveau-projet/freelance/tools-commun/jarvis/jarvis-data.json") or "{}")
AGENTS_CONNUS = [a["nom"] for a in _jarvis_data.get("agents", [])
                 if isinstance(a, dict) and "nom" in a]


def reponse(combo, besoin, travail, placeholder):
    """Temps 3 : reponse structuree prete pour Stark (mode placeholder)."""
    return {
        "combo": combo,
        "besoin": besoin,
        "statut": "PLACEHOLDER",
        "travail_prevu": travail,
        "reponse_placeholder": placeholder,
        "date": datetime.now().isoformat(timespec="seconds"),
    }
