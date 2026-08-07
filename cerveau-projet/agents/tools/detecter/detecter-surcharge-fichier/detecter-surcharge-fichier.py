#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
detecter-surcharge-fichier.py
Detecte les fichiers markdown qui grossissent trop (en nombre de lignes).

Seuil de tolerance: 200 a 250 lignes. Au-dela, le fichier est signale en
surcharge.

Usage:
  detecter-surcharge-fichier.py [dossier] [options]

Options:
  --seuil <n>         Seuil de lignes (defaut: 250, tolerance 200-250)
  --recursive, -r     Analyser recursivement les sous-dossiers
  --version           Afficher la version
  --aide, -h          Afficher cette aide

Retour: 0 si aucun fichier en surcharge, 1 sinon.

Proprietaire : Vulcain (outil partage)
Version : 0.2.0-py
Statut : beta
"""

import argparse
import os
import sys

VERSION = "0.2.0-py"
STATUT = "beta"

# Couleurs ANSI
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[0;34m"
NC = "\033[0m"  # No Color

SEUIL_DEFAUT = 250
SEUIL_MIN = 200
SEUIL_MAX = 250


def compter_lignes(chemin):
    """Compte le nombre de lignes d'un fichier."""
    with open(chemin, encoding="utf-8", errors="replace") as f:
        return sum(1 for _ in f)


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="detecter-surcharge-fichier.py",
        description="Detecte les fichiers markdown qui grossissent trop (seuil 200-250 lignes).",
        add_help=False,
    )
    parser.add_argument("dossier", nargs="?", default=".",
                        help="Dossier a analyser (defaut: .)")
    parser.add_argument("--seuil", type=int, default=SEUIL_DEFAUT,
                        help="Seuil de lignes (defaut: 250, tolerance 200-250)")
    parser.add_argument("--recursive", "-r", action="store_true",
                        help="Analyser recursivement les sous-dossiers")
    parser.add_argument("--version", action="store_true",
                        help="Afficher la version")
    parser.add_argument("--aide", "-h", action="store_true",
                        help="Afficher cette aide")
    return parser


def main(argv=None):
    args = construire_parser().parse_args(argv)

    if args.aide:
        construire_parser().print_help()
        return 0
    if args.version:
        print("detecter-surcharge-fichier.py v" + VERSION + " (" + STATUT + ")")
        return 0

    # Normaliser le seuil dans la tolerance 200-250
    seuil = args.seuil
    if seuil < SEUIL_MIN:
        seuil = SEUIL_MIN
        print(YELLOW + "[INFO] Seuil releve a " + str(SEUIL_MIN) +
              " (tolerance 200-250)" + NC)
    elif seuil > SEUIL_MAX:
        seuil = SEUIL_MAX
        print(YELLOW + "[INFO] Seuil abaisse a " + str(SEUIL_MAX) +
              " (tolerance 200-250)" + NC)

    dossier = args.dossier
    if not os.path.isdir(dossier):
        print(RED + "[ERREUR] Dossier non trouve : " + dossier + NC)
        return 2

    print(BLUE + "=== Detection de surcharge dans " + dossier + " ===" + NC)
    print("Seuil : " + str(seuil) + " lignes")
    print("")

    trouble = 0
    total = 0

    if args.recursive:
        candidats = []
        for racine, _, fichiers in os.walk(dossier):
            for nom in sorted(fichiers):
                if nom.endswith(".md"):
                    candidats.append(os.path.join(racine, nom))
    else:
        candidats = [os.path.join(dossier, nom)
                     for nom in sorted(os.listdir(dossier))
                     if nom.endswith(".md") and os.path.isfile(os.path.join(dossier, nom))]

    for chemin in sorted(candidats):
        total += 1
        lignes = compter_lignes(chemin)
        if lignes > seuil:
            print(YELLOW + "[ATTENTION] " + chemin + " : " +
                  str(lignes) + " lignes" + NC)
            trouble += 1

    print("")
    print(BLUE + "=== Resume ===" + NC)
    print("Fichiers analyses : " + str(total))
    print("En surcharge : " + str(trouble))

    if trouble == 0:
        print(GREEN + "[OK] Aucun fichier en surcharge" + NC)
        return 0
    else:
        print(RED + "[ERREUR] " + str(trouble) +
              " fichier(s) en surcharge" + NC)
        return 1


if __name__ == "__main__":
    sys.exit(main())
