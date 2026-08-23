#!/usr/bin/env python3
"""entry.py - exec (P1 : orchestrateur)."""
import argparse, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonctions"))
from lancer import lancer

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--timeout", type=int, default=60)
    p.add_argument("commande", nargs=argparse.REMAINDER)
    a = p.parse_args()
    print(json.dumps(lancer(a.commande, timeout=a.timeout), indent=2))
