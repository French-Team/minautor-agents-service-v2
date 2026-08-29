#!/usr/bin/env python3
"""entry.py - jsonl-store (P1 : orchestrateur)."""
import argparse, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonctions"))
from store import lire, filtrer


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
    p.add_argument("action", choices=["lire"])
    p.add_argument("--chemin", required=True)
    p.add_argument("--filtre", default="", help="cle=valeur")
    a = p.parse_args()
    if verifier_outil is not None:
        verifier_outil(_CHEMIN_OUTIL, agent="jsonl-store")
    crit = dict(kv.split("=", 1) for kv in a.filtre.split(",")) if a.filtre else {}
    print(json.dumps(filtrer(a.chemin, **crit), ensure_ascii=True, indent=2))
