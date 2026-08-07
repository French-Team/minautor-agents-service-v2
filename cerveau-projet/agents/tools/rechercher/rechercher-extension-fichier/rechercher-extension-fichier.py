#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
rechercher-extension-fichier.py

Extraire l'extension d'un fichier (ou verifier une extension).

Arguments:
  <fichier>       Fichier dont on veut l'extension

Options:
  --verifier <ext>  Verifier si le fichier a cette extension (retourne 0 si oui, 1 si non)
  --verbose       Afficher les details
  --help          Afficher cette aide

Proprietaire : Buffy (outil partage)
Version : 0.2.0-py
Statut : prepare
"""

import os
import sys

VERSION = "0.2.0-py"
STATUT = "prepare"


def afficher_aide():
    print("=== rechercher-extension-fichier v%s ===" % VERSION)
    print("")
    print("Usage: rechercher-extension-fichier.py [OPTIONS] <fichier>")
    print("")
    print("Arguments :")
    print("  <fichier>       Fichier dont on veut l'extension")
    print("")
    print("Options :")
    print("  --verifier <ext>  Verifier si le fichier a cette extension (retourne 0 si oui, 1 si non)")
    print("  --verbose       Afficher les details")
    print("  --help          Afficher cette aide")


def main(argv):
    fichier = ""
    verifier = ""
    verbose = False
    help_demande = False

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--verifier" and i + 1 < len(argv):
            verifier = argv[i + 1]
            i += 2
            continue
        if arg in ("--verbose", "-v"):
            verbose = True
        elif arg in ("--help", "--aide", "-h"):
            help_demande = True
        elif arg == "--version":
            print("rechercher-extension-fichier v%s (%s)" % (VERSION, STATUT))
            return 0
        else:
            if fichier:
                print("[ERREUR] Trop d'arguments: %s" % arg)
                afficher_aide()
                return 1
            fichier = arg
        i += 1

    if help_demande:
        afficher_aide()
        return 0

    if not fichier:
        print("[ERREUR] Fichier obligatoire")
        afficher_aide()
        return 1

    # Extraire l'extension (apres le dernier point, sans le point)
    base = os.path.basename(fichier)
    if "." in base:
        extension = base.rsplit(".", 1)[1]
    else:
        extension = ""

    if verbose:
        print("[INFO] Fichier: %s" % fichier)
        print("[INFO] Extension: %s" % (extension if extension else "aucune"))
        print("---")

    if verifier:
        if extension == verifier:
            if verbose:
                print("[OK] Le fichier a bien l'extension .%s" % verifier)
            return 0
        else:
            if verbose:
                print("[NON] Extension trouvee: %s (attendu: %s)" % (extension if extension else "aucune", verifier))
            return 1

    print(extension)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
