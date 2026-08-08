#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
ecrire-fichier.py
Ecrire ou ecraser le contenu d'un fichier. Supporte l'ecriture depuis un
argument ou depuis stdin.

Usage:
  ecrire-fichier.py [OPTIONS] <fichier> [contenu]

Options:
  --backup            Creer une sauvegarde .bak avant
  --dry-run           Simuler sans ecrire
  --verbose           Afficher les details
  --version           Afficher la version
  --aide, -h          Afficher cette aide

Exemples:
  ecrire-fichier.py fichier.md "# Nouveau contenu"
  echo "texte" | ecrire-fichier.py fichier.md -

Retour: 0 si succes, 1 si erreur.

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


def verifier_nommage(nom_script):
    """Refuse l'execution si le script est renomme (protection du nommage)."""
    attendu = "ecrire-fichier.py"
    if nom_script != attendu:
        print(RED + "[ERREUR] Nom de fichier invalide : " + nom_script + NC)
        print(YELLOW + "  Attendu : " + attendu + NC)
        sys.exit(2)


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="ecrire-fichier.py",
        description="Ecrire ou ecraser le contenu d'un fichier.",
        add_help=False,
    )
    parser.add_argument("fichier", nargs="?", default=None,
                        help="Chemin du fichier a ecrire")
    parser.add_argument("contenu", nargs="?", default="",
                        help="Contenu a ecrire (ou '-' pour lire depuis stdin)")
    parser.add_argument("--backup", action="store_true",
                        help="Creer une sauvegarde .bak avant")
    parser.add_argument("--dry-run", action="store_true",
                        help="Simuler sans ecrire")
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
        print("ecrire-fichier.py v" + VERSION + " (" + STATUT + ")")
        return 0

    if args.fichier is None:
        print(RED + "[ERREUR] Aucun fichier specifie" + NC)
        construire_parser().print_help()
        return 1

    fichier = args.fichier
    contenu = args.contenu

    # Lire le contenu depuis stdin si "-" ou si stdin est un pipe
    if contenu == "-" or (not contenu and not sys.stdin.isatty()):
        contenu = sys.stdin.read()

    if args.dry_run:
        print(YELLOW + "[DRY-RUN] Ecriture dans: " + fichier + NC)
        return 0

    # Sauvegarde si demandee et le fichier existe
    if args.backup and os.path.isfile(fichier):
        backup_path = fichier + ".bak"
        with open(fichier, "r", encoding="utf-8", errors="replace") as fsrc, \
                open(backup_path, "w", encoding="utf-8") as fdst:
            fdst.write(fsrc.read())
        if args.verbose:
            print(BLUE + "[INFO] Sauvegarde creee: " + backup_path + NC)

    # Ecrire
    try:
        if contenu:
            with open(fichier, "w", encoding="utf-8") as f:
                f.write(contenu)
        else:
            open(fichier, "a", encoding="utf-8").close()
    except OSError as e:
        print(RED + "[ERREUR] Impossible d'ecrire " + fichier +
              " : " + str(e) + NC)
        return 1

    if args.verbose:
        print(GREEN + "[OK] Fichier ecrit: " + fichier + NC)

    return 0


if __name__ == "__main__":
    sys.exit(main())
