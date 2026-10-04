#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: forge
#   commun: true
"""
entry.py - POINT D'ENTREE de harnais-nr (P1 : orchestrateur).

Cadre de suites de NON-REGRESSION (v2 freelance). Chaque suite est un
dossier dans le repertoire declare au config (D15) avec SA config JSON ;
les tests sont des DONNEES, jamais du code.

Usage :
    python3 entry.py lister
    python3 entry.py executer --suite <nom> [--test <nom>]
    python3 entry.py executer --toutes [--rapport]

Proprietaire : Forge
Version : 0.1.0 (PHASE 1 - cadre ; les suites arrivent en phase 2)
"""

import argparse
import os
import sys

_d = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _d)

# P10 : la racine se DETECTE via os_path, elle ne se compte pas
sys.path.insert(0, os.path.join(_d, "..", "os_path", "fonctions"))
from racine import trouver_racine  # noqa: E402

# HARNAIS (PROTOCOLE 21) : l outil s auto-verifie en debut de traitement.
sys.path.insert(0, os.path.join(_d, "..", "harnais", "fonctions"))
try:
    from harnais import verifier_outil
except ImportError:
    verifier_outil = None

VERSION = "0.1.0"

sys.path.insert(0, os.path.join(_d, "fonctions"))
import moteur  # noqa: E402


def main():
    if verifier_outil is not None:
        verifier_outil(_d, agent="harnais-nr")
    parser = argparse.ArgumentParser(
        description="harnais-nr v%s - suites de non-regression" % VERSION)
    sub = parser.add_subparsers(dest="action")
    sub.add_parser("lister", help="Lister les suites et leurs tests")
    p_e = sub.add_parser("executer", help="Executer une suite (ou toutes)")
    p_e.add_argument("--suite", default=None,
                     help="Nom du dossier de la suite (ex: nr-jarvis)")
    p_e.add_argument("--test", default=None,
                     help="Restreindre a un seul test de la suite")
    p_e.add_argument("--toutes", action="store_true",
                     help="Executer toutes les suites actives")
    p_e.add_argument("--rapport", action="store_true",
                     help="Ecrire le rapport JSON complet")
    args = parser.parse_args()

    cfg = moteur.charger_config()
    if args.action == "lister":
        moteur.lister(cfg)
        return 0
    if args.action == "executer":
        if args.toutes:
            ok = moteur.executer_toutes(cfg, ecrire_rapport=args.rapport)
            return 0 if ok else 1
        if not args.suite:
            print("ERREUR: --suite <nom> ou --toutes requis")
            return 2
        ok = moteur.executer_suite(cfg, args.suite, args.test,
                                   ecrire_rapport=args.rapport)
        return 0 if ok else 1
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
