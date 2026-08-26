#!/usr/bin/env python3
"""entry.py - encodage (P1 : orchestrateur)."""
import argparse, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonctions"))
from lire_ecrire import lire, ecrire, detecter


# HARNAIS (PROTOCOLE 21) : l outil s auto-verifie en debut de traitement.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "harnais", "fonctions"))
try:
    from harnais import verifier_outil
    _CHEMIN_OUTIL = os.path.dirname(os.path.abspath(__file__))
except ImportError:
    verifier_outil = None

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("action", choices=["lire", "detecter"])
    p.add_argument("--chemin", required=True)
    a = p.parse_args()
    if verifier_outil is not None:
        verifier_outil(_CHEMIN_OUTIL, agent="encodage")
    if a.action == "lire":
        print(lire(a.chemin))
    else:
        import json; print(json.dumps(detecter(a.chemin), indent=2))
