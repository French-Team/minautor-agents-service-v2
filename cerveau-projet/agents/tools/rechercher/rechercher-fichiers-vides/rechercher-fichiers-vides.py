#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
rechercher-fichiers-vides.py

Rechercher les fichiers markdown vides ou quasi vides.

Options:
  --seuil <n>      Taille minimale pour considerer un fichier comme vide (defaut: 5 lignes)
  --extensions     Extensions a chercher (defaut: md)
  --exclure        Dossiers a exclure (defaut: .git,node_modules,.agents)
  --verbose        Afficher les details
  --help           Afficher cette aide

Proprietaire : Buffy (outil partage)
Version : 0.2.0-py
Statut : prepare
"""

import io
import os
import sys

VERSION = "0.2.0-py"
STATUT = "prepare"


def afficher_aide():
    print("=== rechercher-fichiers-vides v%s ===" % VERSION)
    print("")
    print("Usage: rechercher-fichiers-vides.py [OPTIONS] [DOSSIER]")
    print("")
    print("Options :")
    print("  --seuil <n>      Taille minimale pour considerer un fichier comme vide (defaut: 5 lignes)")
    print("  --extensions     Extensions a chercher (defaut: md)")
    print("  --exclure        Dossiers a exclure (defaut: .git,node_modules,.agents)")
    print("  --verbose        Afficher les details")
    print("  --help           Afficher cette aide")


def compter_lignes_non_vides(fichier):
    """Compter les lignes non vides (ignorer les lignes vides et les lignes ---)."""
    nb = 0
    try:
        with io.open(fichier, "r", encoding="utf-8", errors="replace") as fh:
            for ligne in fh:
                if ligne.strip() == "":
                    continue
                if ligne.strip() == "---":
                    continue
                nb += 1
    except IOError:
        pass
    return nb


def main(argv):
    dossier = "."
    seuil = 5
    extensions = "md"
    exclure = ".git,node_modules,.agents"
    verbose = False
    help_demande = False

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--seuil" and i + 1 < len(argv):
            try:
                seuil = int(argv[i + 1])
            except ValueError:
                pass
            i += 2
            continue
        if arg == "--extensions" and i + 1 < len(argv):
            extensions = argv[i + 1]
            i += 2
            continue
        if arg == "--exclure" and i + 1 < len(argv):
            exclure = argv[i + 1]
            i += 2
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
            print("rechercher-fichiers-vides v%s (%s)" % (VERSION, STATUT))
            return 0
        dossier = arg
        i += 1

    if help_demande:
        afficher_aide()
        return 0

    if not os.path.isdir(dossier):
        print("[ERREUR] Le dossier n'existe pas : %s" % dossier)
        return 1

    print("=== Recherche de fichiers vides ===")
    print("Dossier : %s" % dossier)
    print("Seuil : %d lignes non vides" % seuil)
    print("Extensions : %s" % extensions)
    print("")

    ext_liste = [e.strip() for e in extensions.split(",") if e.strip()]
    excl_dirs = [d for d in exclure.split(",") if d]

    total_fichiers = 0
    fichiers_vides = 0
    fichiers_ok = 0

    for racine, dossiers, fichiers in os.walk(dossier):
        dossiers[:] = [d for d in dossiers if d not in excl_dirs and not d.startswith(".")]
        for nom in fichiers:
            if not any(nom.endswith("." + ext) for ext in ext_liste):
                continue
            chemin = os.path.join(racine, nom)
            if not os.path.isfile(chemin):
                continue
            total_fichiers += 1
            nb_non_vides = compter_lignes_non_vides(chemin)
            if nb_non_vides < seuil:
                fichiers_vides += 1
                nb_total = 0
                try:
                    with io.open(chemin, "r", encoding="utf-8", errors="replace") as fh:
                        nb_total = sum(1 for _ in fh)
                except IOError:
                    pass
                print("  [VIDE] %s" % chemin)
                if verbose:
                    print("        -> %d lignes au total, %d non vides" % (nb_total, nb_non_vides))
            else:
                fichiers_ok += 1
                if verbose:
                    print("  [OK] %s" % chemin)

    print("")
    print("=== Resume ===")
    print("Fichiers trouves : %d" % total_fichiers)
    print("Fichiers vides ou quasi vides : %d" % fichiers_vides)
    print("Fichiers avec contenu : %d" % fichiers_ok)

    if fichiers_vides > 0:
        print("")
        print("[ATTENTION] Des fichiers vides ont ete trouves")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
