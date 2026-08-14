#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
lister-statuts.py
Lister les fichiers par statut (ebauche, prepare, dev, test, valide).

Usage:
  lister-statuts.py [chemin] [OPTIONS]

Options:
  --statut <statut>   Filtrer par statut (ebauche, prepare, dev, test, valide)
  --verbose           Afficher les details (resume par statut)
  --version           Afficher la version
  --aide, -h          Afficher cette aide

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

STATUTS = ("ebauche", "prepare", "dev", "test", "valide")


def verifier_nommage(nom_script):
    """Refuse l'execution si le script est renomme (protection du nommage)."""
    attendu = "lister-statuts.py"
    if nom_script != attendu:
        print(RED + "[ERREUR] Nom de fichier invalide : " + nom_script + NC)
        print(YELLOW + "  Attendu : " + attendu + NC)
        sys.exit(2)


def extraire_statut(basename):
    """Extrait le statut du nom de fichier (ASCII pur uniquement)."""
    m = re.search(r"\.(" + "|".join(STATUTS) + r")\.md$", basename)
    return m.group(1) if m else ""


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="lister-statuts.py",
        description="Lister les fichiers par statut.",
        add_help=False,
    )
    parser.add_argument("chemin", nargs="?", default=".",
                        help="Chemin a analyser (defaut: .)")
    parser.add_argument("--statut", default="",
                        help="Filtrer par statut (ebauche, prepare, dev, test, valide)")
    parser.add_argument("--verbose", action="store_true",
                        help="Afficher les details (resume par statut)")
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
        print("lister-statuts.py v" + VERSION + " (" + STATUT + ")")
        return 0

    chemin = args.chemin
    statut_filtre = args.statut

    if args.verbose:
        print("Recherche dans: " + chemin)
        if statut_filtre:
            print("Filtrage par statut: " + statut_filtre)
        print("---")

    fichiers_trouves = 0
    compteurs = {s: 0 for s in STATUTS}

    if os.path.isdir(chemin):
        for base, _, fichiers in os.walk(chemin):
            for nom in sorted(fichiers):
                if not nom.endswith(".md"):
                    continue
                fstatut = extraire_statut(nom)
                if not fstatut:
                    continue
                fichiers_trouves += 1
                compteurs[fstatut] = compteurs.get(fstatut, 0) + 1
                if not statut_filtre or fstatut == statut_filtre:
                    print(os.path.join(base, nom) + " | " + fstatut)

    if args.verbose:
        print("---")
        print("Resume:")
        print("  Total fichiers avec statut: " + str(fichiers_trouves))
        for s in STATUTS:
            print("  " + s + ": " + str(compteurs[s]))

    return 0


if __name__ == "__main__":
    sys.exit(main())
