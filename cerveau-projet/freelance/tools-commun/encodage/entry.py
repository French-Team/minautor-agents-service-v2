#!/usr/bin/env python3
"""entry.py - encodage (P1 : orchestrateur)."""
import argparse, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonctions"))
from lire_ecrire import lire, ecrire, detecter

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("action", choices=["lire", "detecter"])
    p.add_argument("--chemin", required=True)
    a = p.parse_args()
    if a.action == "lire":
        print(lire(a.chemin))
    else:
        import json; print(json.dumps(detecter(a.chemin), indent=2))
