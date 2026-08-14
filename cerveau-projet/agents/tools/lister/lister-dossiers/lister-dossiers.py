#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
lister-dossiers.py
Lister les dossiers d'un chemin donne.

Usage:
  lister-dossiers.py [OPTIONS] [CHEMIN]

Options:
  --recursif, -r  Explorer les sous-dossiers
  --version       Afficher la version
  --aide, -h      Afficher cette aide

Retour: 0 si succes, 1 si erreur.

Proprietaire : Vulcain (outil partage)
Version : 0.2.0-py
Statut : beta
"""

import argparse
import os
import sys

VERSION = "0.2.0-py"
STATUT = "beta"

# Couleurs ANSI
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[0;34m"
NC = "\033[0m"  # No Color


def verifier_nommage(nom_script):
    """Refuse l'execution si le script est renomme (protection du nommage)."""
    attendu = "lister-dossiers.py"
    if nom_script != attendu:
        print(RED + "[ERREUR] Nom de fichier invalide : " + nom_script + NC)
        print(YELLOW + "  Attendu : " + attendu + NC)
        sys.exit(2)


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="lister-dossiers.py",
        description="Lister les dossiers d'un chemin.",
        add_help=False,
    )
    parser.add_argument("chemin", nargs="?", default=".",
                        help="Chemin du dossier (defaut: .)")
    parser.add_argument("--recursif", "-r", action="store_true",
                        help="Explorer les sous-dossiers")
    parser.add_argument("--version", action="store_true",
                        help="Afficher la version")
    parser.add_argument("--aide", "-h", action="store_true",
                        help="Afficher cette aide")
    return parser


def main(argv=None):
    verifier_nommage(os.path.basename(sys.argv[0]))
    args = construire_parser().parse_args(argv)

    if args.aide:
        construire_parser().print_help()
        return 0
    if args.version:
        print("lister-dossiers.py v" + VERSION + " (" + STATUT + ")")
        return 0

    chemin = args.chemin
    if not os.path.exists(chemin):
        print("Erreur: Le chemin '" + chemin + "' n'existe pas")
        return 1

    print(BLUE + "[DOSSIER] Dossiers dans : " + chemin + NC)
    print("")

    if args.recursif:
        for base, dossiers, _ in os.walk(chemin):
            for d in sorted(dossiers):
                print(os.path.join(base, d))
    else:
        if os.path.isdir(chemin):
            for nom in sorted(os.listdir(chemin)):
                if os.path.isdir(os.path.join(chemin, nom)):
                    print(nom)
        else:
            print("Erreur: Le chemin '" + chemin +
                  "' n'existe pas ou n'est pas un dossier")
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
