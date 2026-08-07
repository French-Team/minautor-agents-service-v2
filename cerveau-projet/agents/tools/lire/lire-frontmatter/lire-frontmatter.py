#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lire-frontmatter.py
Extraire le frontmatter YAML en tete d'un fichier markdown.

Usage:
  lire-frontmatter.py [OPTIONS] <fichier>

Options:
  --champ <nom>   Afficher uniquement la valeur d'un champ (ex: statut)
  --verbose       Afficher les details (presence/absence)
  --version       Afficher la version
  --aide, -h      Afficher cette aide

Retour: 0 si succes, 1 si erreur (fichier absent ou champ absent).

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
    attendu = "lire-frontmatter.py"
    if nom_script != attendu:
        print(RED + "[ERREUR] Nom de fichier invalide : " + nom_script + NC)
        print(YELLOW + "  Attendu : " + attendu + NC)
        sys.exit(2)


def extraire_frontmatter(lignes):
    """Extrait le bloc frontmatter (--- en ligne 1 et ligne de cloture)."""
    if not lignes or lignes[0].strip() != "---":
        return []
    bloc = []
    for ligne in lignes[1:]:
        if ligne.strip() == "---":
            break
        bloc.append(ligne)
    return bloc


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="lire-frontmatter.py",
        description="Extraire le frontmatter YAML en tete d'un fichier markdown.",
        add_help=False,
    )
    parser.add_argument("fichier", nargs="?", default=None,
                        help="Fichier markdown a analyser")
    parser.add_argument("--champ", default="",
                        help="Afficher uniquement la valeur d'un champ (ex: statut)")
    parser.add_argument("--verbose", action="store_true",
                        help="Afficher les details (presence/absence)")
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
        print("lire-frontmatter.py v" + VERSION + " (" + STATUT + ")")
        return 0

    if args.fichier is None:
        print(RED + "[ERREUR] Fichier obligatoire" + NC)
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

    bloc = extraire_frontmatter(lignes)

    if not bloc:
        if args.verbose:
            print(YELLOW + "[INFO] Pas de frontmatter detecte en tete de " +
                  fichier + NC)
        return 0

    if args.champ:
        valeur = ""
        for ligne in bloc:
            if ligne.startswith(args.champ + ":"):
                valeur = ligne.split(":", 1)[1].strip()
                break
        if not valeur:
            if args.verbose:
                print(YELLOW + "[ERREUR] Champ '" + args.champ +
                      "' absent du frontmatter" + NC)
            return 1
        print(valeur)
        return 0

    print("\n".join(bloc))
    return 0


if __name__ == "__main__":
    sys.exit(main())
