#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
rechercher-fichier.py

Verifier si un fichier existe. Retourne 0 si le fichier existe, 1 sinon.

Options:
  --verbose   Afficher le resultat
  --help      Afficher cette aide

Proprietaire : Buffy (outil partage)
Version : 0.2.0-py
Statut : prepare
"""

import os
import sys

VERSION = "0.2.0-py"
STATUT = "prepare"


def afficher_aide():
    print("=== rechercher-fichier v%s ===" % VERSION)
    print("")
    print("Usage: rechercher-fichier.py [OPTIONS] <fichier>")
    print("")
    print("Retourne 0 si le fichier existe, 1 sinon.")
    print("")
    print("Options :")
    print("  --verbose   Afficher le resultat")
    print("  --help      Afficher cette aide")


def main(argv):
    fichier = ""
    verbose = False
    help_demande = False

    for arg in argv:
        if arg in ("--verbose", "-v"):
            verbose = True
        elif arg in ("--help", "--aide", "-h"):
            help_demande = True
        elif arg == "--version":
            print("rechercher-fichier v%s (%s)" % (VERSION, STATUT))
            return 0
        else:
            fichier = arg

    if help_demande:
        afficher_aide()
        return 0

    if not fichier:
        print("ERREUR: Aucun fichier specifie", file=sys.stderr)
        return 1

    if os.path.isfile(fichier):
        if verbose:
            print("Existe: %s" % fichier)
        return 0
    else:
        if verbose:
            print("Inexistant: %s" % fichier)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
