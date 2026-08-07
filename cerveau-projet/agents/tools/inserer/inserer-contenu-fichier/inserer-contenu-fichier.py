#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
inserer-contenu-fichier.py
Inserer du contenu a une position precise dans un fichier (apres un numero
de ligne donne).

Usage:
  inserer-contenu-fichier.py [OPTIONS] <fichier> <position> [contenu]

Arguments:
  <fichier>       Fichier a modifier
  <position>      Inserer APRES cette ligne (0 = au debut)
  [contenu]       Chaine a inserer (ou --fichier source)

Options:
  --fichier <src> Inserer le contenu d'un fichier source
  --dry-run       Simuler sans modifier
  --verbose       Afficher les details
  --version       Afficher la version
  --aide, -h      Afficher cette aide

Retour: 0 si succes, 1 si erreur.

Proprietaire : Buffy (outil partage)
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


def verifier_nommage(nom_script):
    """Refuse l'execution si le script est renomme (protection du nommage)."""
    attendu = "inserer-contenu-fichier.py"
    if nom_script != attendu:
        print(RED + "[ERREUR] Nom de fichier invalide : " + nom_script + NC)
        print(YELLOW + "  Attendu : " + attendu + NC)
        sys.exit(2)


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="inserer-contenu-fichier.py",
        description="Inserer du contenu a une position precise dans un fichier.",
        add_help=False,
    )
    parser.add_argument("fichier", nargs="?", default=None,
                        help="Fichier a modifier")
    parser.add_argument("position", nargs="?", default=None,
                        help="Inserer APRES cette ligne (0 = au debut)")
    parser.add_argument("contenu", nargs="?", default="",
                        help="Chaine a inserer (ou --fichier source)")
    parser.add_argument("--fichier", dest="source", default="",
                        help="Inserer le contenu d'un fichier source")
    parser.add_argument("--dry-run", action="store_true",
                        help="Simuler sans modifier")
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
        print("inserer-contenu-fichier.py v" + VERSION + " (" + STATUT + ")")
        return 0

    if args.fichier is None or args.position is None:
        print(RED + "[ERREUR] Fichier et position obligatoires" + NC)
        construire_parser().print_help()
        return 1

    fichier = args.fichier
    position = args.position

    if not os.path.isfile(fichier):
        print(RED + "[ERREUR] Fichier non trouve: " + fichier + NC)
        return 1

    if not position.isdigit():
        print(RED + "[ERREUR] La position doit etre un nombre: " + position + NC)
        return 1

    position = int(position)

    if args.source:
        if not os.path.isfile(args.source):
            print(RED + "[ERREUR] Fichier source non trouve: " + args.source + NC)
            return 1
    elif not args.contenu:
        print(RED + "[ERREUR] Aucun contenu a inserer (chaine ou --fichier)" + NC)
        construire_parser().print_help()
        return 1

    try:
        with open(fichier, encoding="utf-8", errors="replace") as f:
            lignes = f.read().split("\n")
    except OSError as e:
        print(RED + "[ERREUR] Lecture impossible: " + str(e) + NC)
        return 1

    # Normaliser : si le fichier finit par un saut de ligne, la derniere
    # entree est vide. On conserve cette convention (split conservateur).
    total_lignes = len(lignes)

    if position > total_lignes:
        print(YELLOW + "[INFO] La position (" + str(position) +
              ") depasse le nombre de lignes (" + str(total_lignes) + ")" + NC)
        print(YELLOW + "[INFO] Le contenu sera ajoute a la fin" + NC)
        position = total_lignes

    if args.verbose:
        print(BLUE + "[INFO] Fichier: " + fichier +
              " (" + str(total_lignes) + " lignes)" + NC)
        print(BLUE + "[INFO] Insertion apres la ligne " + str(position) + NC)

    if args.dry_run:
        print(YELLOW + "[DRY-RUN] Insertion simulee apres la ligne " +
              str(position) + " dans " + fichier + NC)
        return 0

    # Construire le contenu a inserer
    if args.source:
        try:
            with open(args.source, encoding="utf-8", errors="replace") as f:
                bloc = f.read().rstrip("\n")
        except OSError as e:
            print(RED + "[ERREUR] Lecture source impossible: " + str(e) + NC)
            return 1
    else:
        bloc = args.contenu

    # Inserer : avant = lignes 0..position ; bloc ; apres = position+1..fin
    avant = lignes[:position]
    apres = lignes[position:]
    nouvelles = avant + [bloc] + apres
    resultat = "\n".join(nouvelles)

    try:
        with open(fichier, "w", encoding="utf-8") as f:
            f.write(resultat)
    except OSError as e:
        print(RED + "[ERREUR] L'insertion a echoue: " + str(e) + NC)
        return 1

    print(GREEN + "[OK] Contenu insere apres la ligne " + str(position) +
          " dans " + fichier + NC)
    return 0


if __name__ == "__main__":
    sys.exit(main())
