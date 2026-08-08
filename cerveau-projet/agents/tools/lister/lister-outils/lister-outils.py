#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
lister-outils.py
Lister les outils partages du cerveau-projet, par categorie, avec l'etat
des scripts (.sh) et documentations (.md).

Usage:
  lister-outils.py [OPTIONS]

Options:
  --detail, -d        Afficher les details complets
  --categorie, -c     Filtrer par categorie
  --verbose, -v       Afficher les details
  --version           Afficher la version
  --aide, -h          Afficher cette aide

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
CYAN = "\033[0;36m"
NC = "\033[0m"  # No Color

TOOLS_DIR = "cerveau-projet/agents/tools"

# Categories exclues de la liste des outils
CATEGORIES_EXCLUES = ("combos", "tester")


def verifier_nommage(nom_script):
    """Refuse l'execution si le script est renomme (protection du nommage)."""
    attendu = "lister-outils.py"
    if nom_script != attendu:
        print(RED + "[ERREUR] Nom de fichier invalide : " + nom_script + NC)
        print(YELLOW + "  Attendu : " + attendu + NC)
        sys.exit(2)


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="lister-outils.py",
        description="Lister les outils partages du cerveau-projet.",
        add_help=False,
    )
    parser.add_argument("--detail", "-d", action="store_true",
                        help="Afficher les details complets")
    parser.add_argument("--categorie", "-c", default="",
                        help="Filtrer par categorie")
    parser.add_argument("--verbose", "-v", action="store_true",
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
        print("lister-outils.py v" + VERSION + " (" + STATUT + ")")
        return 0

    print(BLUE + "[LISTE] Liste des outils partages" + NC)
    print("")

    if not os.path.isdir(TOOLS_DIR):
        print(RED + "Erreur: Le dossier " + TOOLS_DIR + " n'existe pas" + NC)
        return 1

    total = 0
    avec_script = 0
    sans_script = 0

    categories = []
    if os.path.isdir(TOOLS_DIR):
        for nom in sorted(os.listdir(TOOLS_DIR)):
            if os.path.isdir(os.path.join(TOOLS_DIR, nom)) and \
                    nom not in CATEGORIES_EXCLUES:
                categories.append(nom)

    for cat in categories:
        if args.categorie and cat != args.categorie:
            continue
        cat_dir = os.path.join(TOOLS_DIR, cat)
        if not os.path.isdir(cat_dir):
            continue

        print(CYAN + "----------------------------------------" + NC)
        print(GREEN + "[CATEGORIE] " + cat + NC)
        print(CYAN + "----------------------------------------" + NC)

        for outil in sorted(os.listdir(cat_dir)):
            outil_dir = os.path.join(cat_dir, outil)
            if not os.path.isdir(outil_dir):
                continue
            tool_sh = os.path.join(outil_dir, outil + ".sh")
            tool_md = os.path.join(outil_dir, outil + ".md")

            print("  [OUTIL] " + outil)
            if os.path.isfile(tool_sh):
                print("    [OK] Script : Present")
                avec_script += 1
                if args.detail:
                    if os.access(tool_sh, os.X_OK):
                        print("    [EXECUTABLE] Oui")
                    else:
                        print("    [ATTENTION]  Executable : Non")
            else:
                print("    [ERREUR] Script : Absent")
                sans_script += 1

            if os.path.isfile(tool_md):
                print("    [DOCUMENTATION] Presente")
            else:
                print("    [ATTENTION]  Documentation : Absente")
            total += 1
            print("")

    print(CYAN + "----------------------------------------" + NC)
    print(BLUE + "Resume :" + NC)
    print("  [TOTAL] Outils : " + str(total))
    print("  [OK] Avec script : " + str(avec_script))
    print("  [ERREUR] Sans script : " + str(sans_script))
    print(CYAN + "----------------------------------------" + NC)
    return 0


if __name__ == "__main__":
    sys.exit(main())
