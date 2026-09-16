#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verifier-selecteur.py -- Routine de verification du selecteur de flux

Verifie que le selecteur est coherant avec les processus en cours.
Detecte les incoherences (ex: flux1 actif mais watchdog flux2 demarre).

Usage: python verifier-selecteur.py [--verbose]
"""

import sys
import json
import subprocess
import argparse
from pathlib import Path
from datetime import datetime


# routines/selecteur-flux/ -> matrice/ (3 remontees, garde-foi L-006)
RACINE = Path(__file__).resolve().parent.parent.parent
if RACINE.name != "matrice":
    raise RuntimeError(
        "Structure inattendue : " + str(RACINE) + " n'est pas le dossier matrice/"
    )
SELECTEUR_PATH = RACINE / "data" / "selecteur-flux.json"
WATCHDOG_FLUX1_PID = RACINE.parent / "_operateur" / "optimus-prime" / "super-combos" / "combos" / "outils" / "watchdog-flux1.pid"
WATCHDOG_FLUX2_PID = RACINE.parent / "_operateur" / "optimus-prime" / "super-combos" / "combos" / "outils" / "watchdog-flux2.pid"


def load_selecteur() -> dict:
    """Charger le selecteur."""
    if SELECTEUR_PATH.exists():
        with open(SELECTEUR_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"flux_actif": None}


def verifier_processus(pid_file: Path) -> bool:
    """Verifier si un processus est en cours."""
    if not pid_file.exists():
        return False
    
    try:
        pid = int(pid_file.read_text().strip())
        result = subprocess.run(["tasklist", "/FI", f"PID eq {pid}"], capture_output=True, text=True)
        return str(pid) in result.stdout
    except:
        return False


def main():
    parser = argparse.ArgumentParser(description="Verifier le selecteur de flux")
    parser.add_argument("--verbose", action="store_true", help="Afficher les details")
    args = parser.parse_args()

    sel = load_selecteur()
    flux_actif = sel.get("flux_actif")
    
    # Verifier les watchdogs
    watchdog1_actif = verifier_processus(WATCHDOG_FLUX1_PID)
    watchdog2_actif = verifier_processus(WATCHDOG_FLUX2_PID)
    
    # Verifier la coherence
    problemes = []
    
    # Un flux SELECTIONNE sans son watchdog n'est pas conduit : c'est une
    # INCOHERENCE, pas un detail de --verbose. Ne le dire qu'en --verbose
    # laissait le selecteur repondre "Coherence: OK" avec un flux mort -- constat
    # MO-061 : flux2 selectionne, aucun watchdog, verdict OK.
    if flux_actif == "flux1":
        if watchdog2_actif:
            problemes.append("Watchdog Flux 2 actif alors que Flux 1 est selectionne")
        if not watchdog1_actif:
            problemes.append("Flux 1 selectionne mais son watchdog n'est PAS demarre")
    
    elif flux_actif == "flux2":
        if watchdog1_actif:
            problemes.append("Watchdog Flux 1 actif alors que Flux 2 est selectionne")
        if not watchdog2_actif:
            problemes.append("Flux 2 selectionne mais son watchdog n'est PAS demarre")
    
    else:
        if watchdog1_actif or watchdog2_actif:
            problemes.append("Aucun flux selectionne mais un watchdog est actif")
    
    # Afficher les problemes
    if problemes:
        print("INCOHERENCES DETECTEES:")
        for p in problemes:
            print(f"  - {p}")
        return 1
    
    if args.verbose:
        print(f"Selecteur: {flux_actif or 'AUCUN'}")
        print(f"Watchdog 1: {'ACTIF' if watchdog1_actif else 'INACTIF'}")
        print(f"Watchdog 2: {'ACTIF' if watchdog2_actif else 'INACTIF'}")
        print("Coherence: OK")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
