#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lire-fichier.py
Lire le contenu complet d'un fichier (avec options de plage).

Usage:
  lire-fichier.py [OPTIONS] <fichier>

Options:
  --debut N       Lire a partir de la ligne N
  --fin N         Lire jusqu'a la ligne N
  --lignes N      Lire les N premieres lignes
  --verbose       Afficher les details
  --version       Afficher la version
  --aide, -h      Afficher cette aide

Retour: 0 si succes, 1 si erreur.

Proprietaire : Buffy (outil partage)
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
    attendu = "lire-fichier.py"
    if nom_script != attendu:
        print(RED + "[ERREUR] Nom de fichier invalide : " + nom_script + NC)
        print(YELLOW + "  Attendu : " + attendu + NC)
        sys.exit(2)


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="lire-fichier.py",
        description="Lire le contenu complet d'un fichier.",
        add_help=False,
    )
    parser.add_argument("fichier", nargs="?", default=None,
                        help="Fichier a lire")
    parser.add_argument("--debut", type=int, default=None,
                        help="Lire a partir de la ligne N")
    parser.add_argument("--fin", type=int, default=None,
                        help="Lire jusqu'a la ligne N")
    parser.add_argument("--lignes", type=int, default=None,
                        help="Lire les N premieres lignes")
    parser.add_argument("--verbose", action="store_true",
                        help="Afficher les details")
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
        print("lire-fichier.py v" + VERSION + " (" + STATUT + ")")
        return 0

    if args.fichier is None:
        print(RED + "[ERREUR] Aucun fichier specifie" + NC)
        construire_parser().print_help()
        return 1

    fichier = args.fichier
    if not os.path.isfile(fichier):
        print(RED + "[ERREUR] Fichier non trouve: " + fichier + NC)
        return 1

    try:
        with open(fichier, encoding="utf-8", errors="replace") as f:
            lignes = f.read().split("\n")
    except OSError as e:
        print(RED + "[ERREUR] Lecture impossible: " + str(e) + NC)
        return 1

    total_lignes = len(lignes)
    if args.verbose:
        print(BLUE + "[INFO] Fichier: " + fichier +
              " (" + str(total_lignes) + " lignes)" + NC)

    # Construire la plage de lecture
    debut, fin = 1, total_lignes
    if args.lignes is not None:
        fin = min(args.lignes, total_lignes)
    elif args.debut is not None and args.fin is not None:
        debut = max(args.debut, 1)
        fin = min(args.fin, total_lignes)
    elif args.debut is not None:
        debut = max(args.debut, 1)
    elif args.fin is not None:
        fin = min(args.fin, total_lignes)

    for i in range(debut - 1, min(fin, total_lignes)):
        print(lignes[i])

    return 0


if __name__ == "__main__":
    sys.exit(main())
