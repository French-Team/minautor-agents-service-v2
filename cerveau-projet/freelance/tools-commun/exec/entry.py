#!/usr/bin/env python3
"""entry.py - exec (P1 : orchestrateur)."""
import argparse, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonctions"))
from lancer import lancer

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
    p.add_argument("--timeout", type=int, default=60)
    p.add_argument("commande", nargs=argparse.REMAINDER)
    a = p.parse_args()
    if verifier_outil is not None:
        verifier_outil(_CHEMIN_OUTIL, agent="exec")
    print(json.dumps(lancer(a.commande, timeout=a.timeout), indent=2))
