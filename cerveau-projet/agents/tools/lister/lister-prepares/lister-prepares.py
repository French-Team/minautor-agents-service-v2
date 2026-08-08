#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
lister-prepares.py
Lister les fichiers 'prepare' et verifier l'existence des specs associees.

Usage:
  lister-prepares.py [DOSSIER] [OPTIONS]

Options:
  --creer-spec   Proposer de creer les specs manquantes
  --verbose      Afficher les details
  --version      Afficher la version
  --aide, -h     Afficher cette aide

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
    attendu = "lister-prepares.py"
    if nom_script != attendu:
        print(RED + "[ERREUR] Nom de fichier invalide : " + nom_script + NC)
        print(YELLOW + "  Attendu : " + attendu + NC)
        sys.exit(2)


def extraire_statut(basename):
    """Extrait le statut du nom de fichier."""
    m = re.search(r"\.(" + "|".join(STATUTS) + r")\.md$", basename)
    return m.group(1) if m else ""


def extraire_nom(basename):
    """Extrait le nom sans le statut."""
    return re.sub(r"\.(" + "|".join(STATUTS) + r")\.md$", "", basename)


def verifier_spec(fichier):
    """Cherche une spec associee. Retourne (existe, chemin)."""
    nom = extraire_nom(os.path.basename(fichier))
    dossier = os.path.dirname(fichier)

    # Remonter pour trouver spec/
    current = dossier
    while current not in (".", "/", ""):
        dossier_spec = os.path.join(current, "spec")
        if os.path.isdir(dossier_spec):
            for base, _, fichiers in os.walk(dossier_spec):
                for fn in fichiers:
                    if fn.startswith("spec-" + nom) and fn.endswith(".md"):
                        return True, os.path.join(base, fn)
            break
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent

    # Spec dans le meme dossier
    if os.path.isdir(dossier):
        for fn in sorted(os.listdir(dossier)):
            if fn.startswith("spec-" + nom) and fn.endswith(".md"):
                return True, os.path.join(dossier, fn)

    return False, ""


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="lister-prepares.py",
        description="Lister les fichiers 'prepare' et verifier l'existence des specs.",
        add_help=False,
    )
    parser.add_argument("dossier", nargs="?", default=".",
                        help="Dossier a analyser (defaut: .)")
    parser.add_argument("--creer-spec", action="store_true",
                        help="Proposer de creer les specs manquantes")
    parser.add_argument("--verbose", action="store_true",
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
        print("lister-prepares.py v" + VERSION + " (" + STATUT + ")")
        return 0

    dossier = args.dossier
    print(BLUE + "=== Fichiers 'prepare' ===" + NC)
    print("Dossier : " + dossier)
    print("")

    fichiers_trouves = 0
    specs_manquantes = 0

    if os.path.isdir(dossier):
        for base, _, fichiers in os.walk(dossier):
            for nom in sorted(fichiers):
                if not nom.endswith(".md"):
                    continue
                statut = extraire_statut(nom)
                if statut != "prepare":
                    continue
                fichiers_trouves += 1
                fichier = os.path.join(base, nom)
                spec_existe, spec_chemin = verifier_spec(fichier)
                if spec_existe:
                    print(GREEN + "[OK] " + os.path.basename(fichier) + NC)
                    if args.verbose:
                        print("     Spec : " + spec_chemin)
                else:
                    print(YELLOW + "[SANS SPEC] " + os.path.basename(fichier) + NC)
                    specs_manquantes += 1
                    if args.creer_spec:
                        print("     " + BLUE + "-> Proposer de creer une spec" + NC)

    print("")
    print(BLUE + "=== Resume ===" + NC)
    print("Fichiers 'prepare' trouves : " + str(fichiers_trouves))
    print("Specs manquantes : " + str(specs_manquantes))

    if specs_manquantes > 0 and args.creer_spec:
        print("")
        print(YELLOW + "Des specs sont a creer pour les fichiers 'prepare'." + NC)
        print("Utiliser le template : cerveau-projet/pense-betes/specs/spec-template.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
