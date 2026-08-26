#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
entry.py - POINT D'ENTREE de rappel (P1 : orchestrateur).

Le combo anti-dispersion : quand tu corriges quelque part, il te rappelle
QUOI AUTRE verifier. Les messages vivent dans rappels.json (D15).

Usage :
  python3 entry.py pour --contexte <contexte>
  python3 entry.py lister

Proprietaire : Forge
Version : 0.1.0
"""

import argparse
import json
import os
import sys
# HARNAIS (PROTOCOLE 21) : l outil s auto-verifie en debut de traitement.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "harnais", "fonctions"))
try:
    from harnais import verifier_outil
    _CHEMIN_OUTIL = os.path.dirname(os.path.abspath(__file__))
except ImportError:
    verifier_outil = None

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "fonctions"))
from rappels import pour, lister

VERSION = "0.1.0"


def main():
    if verifier_outil is not None:
        verifier_outil(_CHEMIN_OUTIL, agent="rappel")
    parser = argparse.ArgumentParser(description="rappel v%s" % VERSION)
    sub = parser.add_subparsers(dest="action")
    p_p = sub.add_parser("pour", help="Rappels pertinents pour un contexte")
    p_p.add_argument("--contexte", required=True,
                     help="ex: correction-regle, correction-outil, correction-fiche")
    sub.add_parser("lister", help="Lister tous les contextes de rappel")
    args = parser.parse_args()

    if args.action == "pour":
        resultats = pour(args.contexte)
        if not resultats:
            print("Aucun rappel disponible (verifier rappels.json).")
            return 1
        print(f"[RAPPEL] {len(resultats)} rappel(s) - il y a probablement "
              f"AILLEURS a corriger :")
        for r in resultats:
            print(f"  [{r.get('contexte')}] {r.get('message')}")
        return 0
    if args.action == "lister":
        for contexte, message in lister():
            print(f"  {contexte} : {message}")
        return 0
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
