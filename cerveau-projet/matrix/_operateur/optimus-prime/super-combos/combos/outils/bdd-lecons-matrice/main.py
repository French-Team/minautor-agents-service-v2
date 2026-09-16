#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bdd-lecons-matrice -- Porte unique des lecons matrice (lecons.json)

Point d'entree global. Dirige vers la categorie demandee.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# NOTE (L-017) : dossier a tiret = pas un package -> import direct, jamais "from bdd-lecons-matrice.entry import"
from entry import run as run_bdd_lecons_matrice


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nUsage:")
        print("  bdd-lecons-matrice ajouter \"<lecon>\" [--tags a,b] [--source S]")
        print("  bdd-lecons-matrice lister [--n 10]")
        print("  bdd-lecons-matrice chercher [--mot-cle M] [--tag T]")
        return 1

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == "ajouter":
        return run_bdd_lecons_matrice("ajouter", args)
    elif cmd == "lister":
        return run_bdd_lecons_matrice("lister", args)
    elif cmd == "chercher":
        return run_bdd_lecons_matrice("chercher", args)
    else:
        print(f"Commande inconnue: {cmd}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
