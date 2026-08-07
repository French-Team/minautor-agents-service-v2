#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
supprimer-dossier.py

Supprimer un dossier recursivement (avec protections).

Options:
  --force         Executer la suppression (sans : dry-run)
  --verbose       Afficher les details
  --help          Afficher cette aide

Protections:
  - Refus des chemins sensibles (/, ., .., racine du projet, tools/)
  - Dry-run par defaut : il faut --force pour supprimer reellement

Proprietaire : Buffy (outil partage)
Version : 0.2.0-py
Statut : prepare
"""

import os
import shutil
import sys

VERSION = "0.2.0-py"
STATUT = "prepare"

CHEMINS_SENSIBLES = {"", "/", ".", "..", "./", "../"}
DOSSIER_OUTILS = "cerveau-projet/agents/tools"


def afficher_aide():
    print("=== supprimer-dossier v%s ===" % VERSION)
    print("")
    print("Usage: supprimer-dossier.py [OPTIONS] <dossier>")
    print("")
    print("Arguments :")
    print("  <dossier>       Dossier a supprimer (recursif)")
    print("")
    print("Options :")
    print("  --force         Executer la suppression (sans : dry-run)")
    print("  --verbose       Afficher les details")
    print("  --help          Afficher cette aide")
    print("")
    print("Exemples :")
    print("  supprimer-dossier.py dossier-temporaire          # Dry-run")
    print("  supprimer-dossier.py --force dossier-temporaire  # Suppression reelle")


def main(argv):
    dossier = ""
    force = False
    verbose = False
    help_demande = False

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--force":
            force = True
            i += 1
            continue
        if arg in ("--verbose", "-v"):
            verbose = True
            i += 1
            continue
        if arg in ("--help", "--aide", "-h"):
            help_demande = True
            i += 1
            continue
        if arg == "--version":
            print("supprimer-dossier v%s (%s)" % (VERSION, STATUT))
            return 0
        if dossier:
            print("[ERREUR] Trop d'arguments: %s" % arg)
            afficher_aide()
            return 1
        dossier = arg
        i += 1

    if help_demande:
        afficher_aide()
        return 0

    if not dossier:
        print("[ERREUR] Aucun dossier specifie")
        afficher_aide()
        return 1

    if not os.path.isdir(dossier):
        print("[ERREUR] Dossier non trouve ou pas un dossier: %s" % dossier)
        return 1

    # Normaliser le chemin (supprimer les / finaux)
    dossier = dossier.rstrip("/\\")

    # PROTECTION : chemins sensibles absolument interdits
    if dossier in CHEMINS_SENSIBLES:
        print("[ERREUR] Suppression interdite de ce chemin sensible: %s" % dossier)
        return 1

    # PROTECTION : ne pas supprimer la racine du projet ni le dossier des outils
    cible_abs = os.path.abspath(dossier)
    if cible_abs == os.path.abspath("."):
        print("[ERREUR] Refus : ce dossier est la racine du projet")
        return 1
    if cible_abs == os.path.abspath(DOSSIER_OUTILS):
        print("[ERREUR] Refus : ce dossier contient les outils partages")
        return 1

    nb_fichiers = 0
    nb_dossiers = 0
    for racine, dossiers, fichiers in os.walk(dossier):
        nb_fichiers += len(fichiers)
        nb_dossiers += len(dossiers)

    if verbose:
        print("[INFO] Dossier cible: %s" % dossier)
        print("[INFO] Contenu: %d fichiers, %d sous-dossiers" % (nb_fichiers, nb_dossiers))

    if not force:
        print("[DRY-RUN] Aucune suppression effectuee (utiliser --force pour executer)")
        print("[INFO] %d fichiers et %d dossiers seraient supprimes" % (nb_fichiers, nb_dossiers))
        return 0

    try:
        shutil.rmtree(dossier)
    except OSError:
        print("[ERREUR] La suppression a echoue")
        return 1

    print("[OK] Dossier supprime : %s (%d fichiers, %d dossiers)" % (dossier, nb_fichiers, nb_dossiers))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
