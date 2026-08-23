# -*- coding: ascii -*-
"""fonctions/noter.py - enregistrer une note de palier (v0.1.0)."""

import json
import os
import sys
from datetime import datetime

_sys_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "..", "os_path", "fonctions")
sys.path.insert(0, _sys_dir)
from racine import trouver_racine
from paliers import palier_valide, est_baisse

RACINE = trouver_racine(__file__)
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "..", "notes-agents.jsonl")


def noter(agent, palier, motif, par):
    """Enregistrer une note {date, agent, palier_avant, palier_apres,
    motif, par}. Retourne (entree, erreur)."""
    if not palier_valide(palier):
        return None, ("palier invalide '%s'. Paliers: OR/SILVER/COPPER "
                      "(hausse) A_REVOIR/A_REPARER/DECLASSE (baisse)" % palier)
    if not motif or len(motif.strip()) < 5:
        return None, "motif obligatoire (min 5 caracteres) - une note sans raison ne sert a rien"
    avant = palier_actuel(agent)
    entree = {
        "date": datetime.now().isoformat(timespec="seconds"),
        "agent": agent,
        "palier_avant": avant,
        "palier_apres": palier,
        "sens": "BAISSE" if est_baisse(palier) else "HAUSSE",
        "motif": motif.strip(),
        "par": par,
    }
    with open(DATA_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entree, ensure_ascii=False) + "\n")
    return entree, None


def palier_actuel(agent):
    """Dernier palier connu d'un agent (None si jamais note)."""
    if not os.path.isfile(DATA_FILE):
        return None
    dernier = None
    with open(DATA_FILE, encoding="utf-8") as f:
        for ligne in f:
            try:
                e = json.loads(ligne)
            except ValueError:
                continue
            if e.get("agent") == agent:
                dernier = e.get("palier_apres")
    return dernier


def lister(agent=None):
    """Toutes les notes (filtrees par agent optionnel)."""
    if not os.path.isfile(DATA_FILE):
        return []
    resultats = []
    with open(DATA_FILE, encoding="utf-8") as f:
        for ligne in f:
            try:
                e = json.loads(ligne)
            except ValueError:
                continue
            if agent is None or e.get("agent") == agent:
                resultats.append(e)
    return resultats


def problemes():
    """Agents dont le dernier palier est un palier de baisse."""
    vus = {}
    for e in lister():
        vus[e["agent"]] = e
    return [e for e in vus.values() if est_baisse(e.get("palier_apres", ""))]
