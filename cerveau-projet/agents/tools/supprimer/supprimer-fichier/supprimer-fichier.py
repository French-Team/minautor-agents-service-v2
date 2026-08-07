#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
supprimer-fichier.py

Supprimer un fichier avec verification.

Options:
  --forcer         Supprimer sans confirmer
  --dry-run        Simuler sans supprimer
  --verbose        Afficher les details
  --help           Afficher cette aide

Proprietaire : Buffy (outil partage)
Version : 0.2.0-py
Statut : prepare
"""

import os
import sys

VERSION = "0.2.0-py"
STATUT = "prepare"


def afficher_aide():
    print("=== supprimer-fichier v%s ===" % VERSION)
    print("")
    print("Usage: supprimer-fichier.py [OPTIONS] <fichier>")
    print("")
    print("Options :")
    print("  --forcer         Supprimer sans confirmer")
    print("  --dry-run        Simuler sans supprimer")
    print("  --verbose        Afficher les details")
    print("  --help           Afficher cette aide")


def main(argv):
    fichier = ""
    forcer = False
    dry_run = False
    verbose = False
    help_demande = False

    for arg in argv:
        if arg == "--forcer":
            forcer = True
        elif arg == "--dry-run":
            dry_run = True
        elif arg in ("--verbose", "-v"):
            verbose = True
        elif arg in ("--help", "--aide", "-h"):
            help_demande = True
        elif arg == "--version":
            print("supprimer-fichier v%s (%s)" % (VERSION, STATUT))
            return 0
        else:
            fichier = arg

    if help_demande:
        afficher_aide()
        return 0

    if not fichier:
        print("[ERREUR] Aucun fichier specifie")
        afficher_aide()
        return 1

    if not os.path.isfile(fichier):
        print("[INFO] Fichier inexistant: %s" % fichier)
        return 0

    if dry_run:
        print("[DRY-RUN] Suppression: %s" % fichier)
        return 0

    os.remove(fichier)

    if verbose:
        print("[OK] Supprime: %s" % fichier)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
