#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
rechercher-dossier.py

Verifier si un dossier existe.

Arguments:
  <chemin>        Chemin du dossier a verifier

Options:
  --verbose       Afficher les details
  --help          Afficher cette aide

Code de sortie:
  0 = le dossier existe
  1 = le dossier n'existe pas

Proprietaire : Buffy (outil partage)
Version : 0.2.0-py
Statut : prepare
"""

import os
import sys

VERSION = "0.2.0-py"
STATUT = "prepare"


def afficher_aide():
    print("=== rechercher-dossier v%s ===" % VERSION)
    print("")
    print("Usage: rechercher-dossier.py [OPTIONS] <chemin>")
    print("")
    print("Arguments :")
    print("  <chemin>        Chemin du dossier a verifier")
    print("")
    print("Options :")
    print("  --verbose       Afficher les details")
    print("  --help          Afficher cette aide")
    print("")
    print("Code de sortie :")
    print("  0 = le dossier existe")
    print("  1 = le dossier n'existe pas")


def main(argv):
    chemin = ""
    verbose = False
    help_demande = False

    for arg in argv:
        if arg in ("--verbose", "-v"):
            verbose = True
        elif arg in ("--help", "--aide", "-h"):
            help_demande = True
        elif arg == "--version":
            print("rechercher-dossier v%s (%s)" % (VERSION, STATUT))
            return 0
        else:
            if chemin:
                print("[ERREUR] Trop d'arguments: %s" % arg)
                afficher_aide()
                return 1
            chemin = arg

    if help_demande:
        afficher_aide()
        return 0

    if not chemin:
        print("[ERREUR] Aucun chemin specifie")
        afficher_aide()
        return 1

    if os.path.isdir(chemin):
        if verbose:
            print("[INFO] Chemin verifie: %s" % chemin)
        print("[OK] Le dossier existe : %s" % chemin)
        return 0
    else:
        if verbose:
            if os.path.exists(chemin):
                print("[INFO] Le chemin existe mais n'est pas un dossier")
            else:
                print("[INFO] Le chemin n'existe pas du tout")
        print("[ERREUR] Le dossier n'existe pas : %s" % chemin)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
