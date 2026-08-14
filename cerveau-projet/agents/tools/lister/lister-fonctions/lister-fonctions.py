#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
lister-fonctions.py
Lister les fonctions definies dans un fichier (bash, python, js).

Usage:
  lister-fonctions.py [OPTIONS] FICHIER

Options:
  --type TYPE     Type de fichier: bash, python, js (defaut: auto)
  --version       Afficher la version
  --aide, -h      Afficher cette aide

Retour: 0 si succes, 1 si erreur.

Proprietaire : Vulcain (outil partage)
Version : 0.2.0-py
Statut : beta
"""

import argparse
import os
import re
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
    attendu = "lister-fonctions.py"
    if nom_script != attendu:
        print(RED + "[ERREUR] Nom de fichier invalide : " + nom_script + NC)
        print(YELLOW + "  Attendu : " + attendu + NC)
        sys.exit(2)


def lister_bash(lignes):
    """Fonctions bash : nom() { en debut de ligne."""
    resultats = []
    for i, ligne in enumerate(lignes, 1):
        m = re.match(r"^\s*([a-zA-Z_][a-zA-Z0-9_]*)\(\)\s*\{", ligne)
        if m:
            resultats.append((i, m.group(1)))
    return resultats


def lister_python(lignes):
    """Fonctions python : def nom( en debut de ligne."""
    resultats = []
    for i, ligne in enumerate(lignes, 1):
        m = re.match(r"^\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", ligne)
        if m:
            resultats.append((i, m.group(1)))
    return resultats


def lister_js(lignes):
    """Fonctions js : function nom( en debut de ligne."""
    resultats = []
    for i, ligne in enumerate(lignes, 1):
        m = re.match(r"^\s*function\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", ligne)
        if m:
            resultats.append((i, m.group(1)))
    return resultats


def detecter_type(fichier):
    """Detecte le type de script par extension."""
    ext = fichier.rsplit(".", 1)[-1].lower() if "." in fichier else ""
    if ext in ("sh", "bash"):
        return "bash"
    if ext == "py":
        return "python"
    if ext in ("js", "jsx", "ts", "tsx"):
        return "js"
    return "bash"  # Par defaut


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="lister-fonctions.py",
        description="Lister les fonctions definies dans un fichier.",
        add_help=False,
    )
    parser.add_argument("fichier", nargs="?", default=None,
                        help="Fichier a analyser")
    parser.add_argument("--type", default="auto",
                        help="Type de fichier: bash, python, js (defaut: auto)")
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
        print("lister-fonctions.py v" + VERSION + " (" + STATUT + ")")
        return 0

    if args.fichier is None:
        print("Erreur: Aucun fichier specifie")
        print("Utilisez --aide pour l'aide")
        return 1

    fichier = args.fichier
    if not os.path.isfile(fichier):
        print("Erreur: Le fichier '" + fichier + "' n'existe pas")
        return 1

    type_script = args.type if args.type != "auto" else detecter_type(fichier)

    print(BLUE + "[RECHERCHE] Fonctions dans : " + fichier + NC)
    print("")

    try:
        with open(fichier, encoding="utf-8", errors="replace") as f:
            lignes = f.read().split("\n")
    except OSError:
        return 1

    if type_script == "bash":
        resultats = lister_bash(lignes)
    elif type_script == "python":
        resultats = lister_python(lignes)
    elif type_script == "js":
        resultats = lister_js(lignes)
    else:
        print("Type non supporte: " + type_script)
        return 1

    for num, nom in resultats:
        print(str(num) + ":" + nom)
    return 0


if __name__ == "__main__":
    sys.exit(main())
