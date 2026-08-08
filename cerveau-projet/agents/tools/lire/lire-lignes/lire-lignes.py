#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
lire-lignes.py
Lire des lignes specifiques d'un fichier (par numero ou plage).

Usage:
  lire-lignes.py [OPTIONS] <fichier> <debut> [fin]

Arguments:
  <fichier>       Fichier a lire
  <debut>         Numero de la premiere ligne (1 = debut)
  [fin]           Numero de la derniere ligne (defaut = debut)

Options:
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
    attendu = "lire-lignes.py"
    if nom_script != attendu:
        print(RED + "[ERREUR] Nom de fichier invalide : " + nom_script + NC)
        print(YELLOW + "  Attendu : " + attendu + NC)
        sys.exit(2)


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="lire-lignes.py",
        description="Lire des lignes specifiques d'un fichier (par numero ou plage).",
        add_help=False,
    )
    parser.add_argument("fichier", nargs="?", default=None,
                        help="Fichier a lire")
    parser.add_argument("debut", nargs="?", default=None,
                        help="Numero de la premiere ligne (1 = debut)")
    parser.add_argument("fin", nargs="?", default=None,
                        help="Numero de la derniere ligne (defaut = debut)")
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
        print("lire-lignes.py v" + VERSION + " (" + STATUT + ")")
        return 0

    if args.fichier is None or args.debut is None:
        print(RED + "[ERREUR] Fichier et numero de ligne obligatoires" + NC)
        construire_parser().print_help()
        return 1

    fichier = args.fichier
    if not os.path.isfile(fichier):
        print(RED + "[ERREUR] Fichier non trouve: " + fichier + NC)
        return 1

    if not args.debut.isdigit():
        print(RED + "[ERREUR] Le debut doit etre un nombre: " + args.debut + NC)
        return 1
    debut = int(args.debut)

    fin = args.fin if args.fin is not None else args.debut
    if not fin.isdigit():
        print(RED + "[ERREUR] La fin doit etre un nombre: " + fin + NC)
        return 1
    fin = int(fin)

    if debut < 1:
        print(RED + "[ERREUR] Le debut doit etre >= 1" + NC)
        return 1

    if fin < debut:
        print(RED + "[ERREUR] La fin (" + str(fin) +
              ") doit etre >= au debut (" + str(debut) + ")" + NC)
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
        print(BLUE + "[INFO] Lecture des lignes " + str(debut) +
              " a " + str(fin) + NC)
        print("---")

    if debut > total_lignes:
        print(YELLOW + "[INFO] Le fichier n'a que " + str(total_lignes) +
              " lignes, rien a afficher" + NC)
        return 0

    for i in range(debut - 1, min(fin, total_lignes)):
        print(lignes[i])

    return 0


if __name__ == "__main__":
    sys.exit(main())
