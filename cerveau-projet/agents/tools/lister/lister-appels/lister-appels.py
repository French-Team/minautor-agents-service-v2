#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lister-appels.py
Lister les appels de fonctions dans un fichier (sh/bash, py, js/ts).

Usage:
  lister-appels.py [OPTIONS] FICHIER

Options:
  --unique, -u    Afficher uniquement les appels uniques
  --verbose, -v   Afficher les details
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
    attendu = "lister-appels.py"
    if nom_script != attendu:
        print(RED + "[ERREUR] Nom de fichier invalide : " + nom_script + NC)
        print(YELLOW + "  Attendu : " + attendu + NC)
        sys.exit(2)


def extraire_appels_bash(lignes, unique):
    """Appels de fonctions bash : pattern nom() sur la ligne."""
    resultats = []
    for i, ligne in enumerate(lignes, 1):
        for m in re.finditer(r"[a-zA-Z_][a-zA-Z0-9_]*\(\)", ligne):
            nom = m.group(0)[:-2]
            resultats.append((i, nom, ligne.strip()))
    return resultats


def extraire_appels_parenthese(lignes, unique):
    """Appels de fonctions py/js/ts : pattern nom( sur la ligne."""
    resultats = []
    for i, ligne in enumerate(lignes, 1):
        for m in re.finditer(r"[a-zA-Z_][a-zA-Z0-9_]*\(", ligne):
            nom = m.group(0)[:-1]
            resultats.append((i, nom, ligne.strip()))
    return resultats


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="lister-appels.py",
        description="Lister les appels de fonctions dans un fichier.",
        add_help=False,
    )
    parser.add_argument("fichier", nargs="?", default=None,
                        help="Fichier a analyser")
    parser.add_argument("--unique", "-u", action="store_true",
                        help="Afficher uniquement les appels uniques")
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
        print("lister-appels.py v" + VERSION + " (" + STATUT + ")")
        return 0

    if args.fichier is None:
        print("Erreur: Aucun fichier specifie")
        print("Utilisez --aide pour l'aide")
        return 1

    fichier = args.fichier
    if not os.path.isfile(fichier):
        print("Erreur: Le fichier '" + fichier + "' n'existe pas")
        return 1

    print(BLUE + "[RECHERCHE] Appels de fonctions dans : " + fichier + NC)
    print("")

    extension = fichier.rsplit(".", 1)[-1].lower() if "." in fichier else ""
    if extension in ("sh", "bash"):
        print(BLUE + "Type : Script Bash" + NC)
        print("")
        try:
            with open(fichier, encoding="utf-8", errors="replace") as f:
                lignes = f.read().split("\n")
        except OSError:
            return 1
        resultats = extraire_appels_bash(lignes, args.unique)
        if args.unique:
            vus = []
            for _, nom, _ in resultats:
                if nom not in vus:
                    vus.append(nom)
            for nom in vus:
                print(GREEN + "[TELEPHONE] " + nom + NC)
        else:
            for num, nom, ligne in resultats:
                print(YELLOW + "Ligne " + str(num) + ":" + NC + " " + ligne)
    elif extension == "py":
        print(BLUE + "Type : Script Python" + NC)
        print("")
        try:
            with open(fichier, encoding="utf-8", errors="replace") as f:
                lignes = f.read().split("\n")
        except OSError:
            return 1
        resultats = extraire_appels_parenthese(lignes, args.unique)
        if args.unique:
            vus = []
            for _, nom, _ in resultats:
                if nom not in vus:
                    vus.append(nom)
            for nom in vus:
                print(GREEN + "[TELEPHONE] " + nom + NC)
        else:
            for num, nom, ligne in resultats:
                print(YELLOW + "Ligne " + str(num) + ":" + NC + " " + ligne)
    elif extension in ("js", "ts"):
        print(BLUE + "Type : Script JavaScript/TypeScript" + NC)
        print("")
        try:
            with open(fichier, encoding="utf-8", errors="replace") as f:
                lignes = f.read().split("\n")
        except OSError:
            return 1
        resultats = extraire_appels_parenthese(lignes, args.unique)
        if args.unique:
            vus = []
            for _, nom, _ in resultats:
                if nom not in vus:
                    vus.append(nom)
            for nom in vus:
                print(GREEN + "[TELEPHONE] " + nom + NC)
        else:
            for num, nom, ligne in resultats:
                print(YELLOW + "Ligne " + str(num) + ":" + NC + " " + ligne)
    else:
        print(YELLOW + "Type de fichier non pris en charge : " + extension + NC)
        print("Formats supportes : sh, bash, py, js, ts")
        return 1

    print("")
    print(BLUE + "Termine." + NC)
    return 0


if __name__ == "__main__":
    sys.exit(main())
