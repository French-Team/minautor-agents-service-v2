#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
rechercher-texte.py

Rechercher un pattern dans un fichier.

Arguments:
  <pattern>       Pattern a rechercher
  <fichier>       Fichier a analyser

Options:
  --insensible     Ignorer la casse
  --numeros        Afficher les numeros de ligne
  --inverser       Afficher les lignes qui ne matchent pas
  --compter        Compter les occurrences
  --verbose        Afficher les details
  --help           Afficher cette aide

Proprietaire : Buffy (outil partage)
Version : 0.2.0-py
Statut : prepare
"""

import io
import os
import re
import sys

VERSION = "0.2.0-py"
STATUT = "prepare"


def afficher_aide():
    print("=== rechercher-texte v%s ===" % VERSION)
    print("")
    print("Usage: rechercher-texte.py [OPTIONS] <pattern> <fichier>")
    print("")
    print("Options :")
    print("  --insensible     Ignorer la casse")
    print("  --numeros        Afficher les numeros de ligne")
    print("  --inverser       Afficher les lignes qui ne matchent pas")
    print("  --compter        Compter les occurrences")
    print("  --verbose        Afficher les details")
    print("  --help           Afficher cette aide")


def main(argv):
    pattern = ""
    fichier = ""
    insensible = False
    numeros = False
    inverser = False
    compter = False
    verbose = False
    help_demande = False

    for arg in argv:
        if arg == "--insensible":
            insensible = True
        elif arg == "--numeros":
            numeros = True
        elif arg == "--inverser":
            inverser = True
        elif arg == "--compter":
            compter = True
        elif arg in ("--verbose", "-v"):
            verbose = True
        elif arg in ("--help", "--aide", "-h"):
            help_demande = True
        elif arg == "--version":
            print("rechercher-texte v%s (%s)" % (VERSION, STATUT))
            return 0
        else:
            if not pattern:
                pattern = arg
            elif not fichier:
                fichier = arg

    if help_demande:
        afficher_aide()
        return 0

    if not pattern or not fichier:
        print("[ERREUR] Pattern et fichier requis")
        afficher_aide()
        return 1

    if not os.path.isfile(fichier):
        print("[ERREUR] Fichier non trouve: %s" % fichier)
        return 1

    try:
        if insensible:
            regex = re.compile(re.escape(pattern), re.IGNORECASE)
        else:
            regex = re.compile(re.escape(pattern))
        with io.open(fichier, "r", encoding="utf-8", errors="replace") as fh:
            lignes = fh.readlines()
    except (IOError, re.error):
        print("[ERREUR] Impossible de lire le fichier: %s" % fichier)
        return 1

    resultats = []
    for i, ligne in enumerate(lignes, 1):
        contenu = ligne.rstrip("\r\n")
        matche = bool(regex.search(contenu))
        if inverser:
            matche = not matche
        if matche:
            resultats.append((i, contenu))

    if compter:
        nb = len(resultats)
        if verbose:
            print("%d occurrences dans %s" % (nb, fichier))
        else:
            print(nb)
        return 0

    for i, contenu in resultats:
        if numeros:
            print("%d:%s" % (i, contenu))
        else:
            print(contenu)

    return 0 if resultats else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
