#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
lire-fichier.py
Lire le contenu complet d'un fichier (avec options de plage).

Usage:
  lire-fichier.py [OPTIONS] <fichier>

Options:
  --debut N       Lire a partir de la ligne N
  --fin N         Lire jusqu'a la ligne N
  --lignes N      Lire les N premieres lignes
  --verbose       Afficher les details
  --version       Afficher la version
  --aide, -h      Afficher cette aide

Retour: 0 si succes, 1 si erreur.

Securite (round 3) :
  - octet nul dans le chemin -> refus explicite (exit 1)
  - lecture robuste : UTF-8 (BOM nettoye) puis fallback latin-1, jamais de crash
  - stdout force en UTF-8 : plus d'UnicodeEncodeError cp1252 sous Windows

Proprietaire : Buffy (outil partage)
Version : 0.4.1
Statut : prepare
"""

import argparse
import os
import sys

VERSION = "0.4.2"
STATUT = "prepare"

# Securite (round 3) : force la sortie en UTF-8 pour ne jamais crasher sur
# l'encodage de la console (cp1252 sous Windows avec des caracteres non-ASCII).
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass  # Python < 3.7 : la console gere l'encodage comme elle peut

# Couleurs ANSI
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[0;34m"
NC = "\033[0m"  # No Color


def verifier_nommage(nom_script):
    """Refuse l'execution si le script est renomme (protection du nommage)."""
    attendu = "lire-fichier.py"
    if nom_script != attendu:
        print(RED + "[ERREUR] Nom de fichier invalide : " + nom_script + NC)
        print(YELLOW + "  Attendu : " + attendu + NC)
        sys.exit(2)


def verifier_chemin_sur(chemin):
    """Securite (round 3) : refuse un chemin contenant un octet nul."""
    if "\x00" in chemin:
        print(RED + "[ERREUR] Chemin non sur (octet nul present)" + NC)
        sys.exit(1)


def decoder_ligne(octets):
    """Decode une ligne sans jamais crasher : UTF-8-sig (BOM nettoye) puis
    latin-1 en secours (decode toujours). Les lignes purement ASCII sont
    identiques dans les deux encodages : le resultat est donc exact."""
    try:
        return octets.decode("utf-8-sig")
    except UnicodeDecodeError:
        return octets.decode("latin-1")


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="lire-fichier.py",
        description="Lire le contenu complet d'un fichier.",
        add_help=False,
    )
    parser.add_argument("fichier", nargs="?", default=None,
                        help="Fichier a lire")
    parser.add_argument("--debut", type=int, default=None,
                        help="Lire a partir de la ligne N")
    parser.add_argument("--fin", type=int, default=None,
                        help="Lire jusqu'a la ligne N")
    parser.add_argument("--lignes", type=int, default=None,
                        help="Lire les N premieres lignes")
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
        print("lire-fichier.py v" + VERSION + " (" + STATUT + ")")
        return 0

    if args.fichier is None:
        print(RED + "[ERREUR] Aucun fichier specifie" + NC)
        construire_parser().print_help()
        return 1

    fichier = args.fichier
    verifier_chemin_sur(fichier)

    if not os.path.isfile(fichier):
        print(RED + "[ERREUR] Fichier non trouve: " + fichier + NC)
        return 1

    # Robustesse (round 4) : validation de la plage AVANT toute lecture.
    # Une plage invalide (--debut > --fin, ou borne < 1) est refusee avec un
    # message explicite : jamais de 0 silencieux avec une sortie vide.
    if args.lignes is not None and args.lignes < 1:
        print(RED + "[ERREUR] Plage invalide : --lignes doit etre >= 1 (recu: " +
              str(args.lignes) + ")" + NC)
        return 1
    if args.debut is not None and args.debut < 1:
        print(RED + "[ERREUR] Plage invalide : --debut doit etre >= 1 (recu: " +
              str(args.debut) + ")" + NC)
        return 1
    if args.fin is not None and args.fin < 1:
        print(RED + "[ERREUR] Plage invalide : --fin doit etre >= 1 (recu: " +
              str(args.fin) + ")" + NC)
        return 1
    if (args.debut is not None and args.fin is not None
            and args.debut > args.fin):
        print(RED + "[ERREUR] Plage invalide : --debut (" + str(args.debut) +
              ") > --fin (" + str(args.fin) + ")" + NC)
        return 1

    # LECTURE PARESSEUSE (performance round 2) : on ne lit que la plage
    # demandee, ligne par ligne, au lieu de charger tout le fichier en
    # memoire. --lignes 5 sur un fichier de 200k lignes ne lit que 5 lignes.
    # Securite (round 3) : iteration binaire + decodage robuste par ligne
    # (utf-8-sig puis latin-1), plus aucun crash d'encodage possible.
    if args.lignes is not None:
        # --lignes N : lire les N premieres lignes puis s'arreter
        debut, fin = 1, args.lignes
    elif args.debut is not None and args.fin is not None:
        debut, fin = args.debut, args.fin
    elif args.debut is not None:
        debut, fin = args.debut, None  # jusqu'a la fin
    elif args.fin is not None:
        debut, fin = 1, args.fin
    else:
        debut, fin = 1, None

    if args.verbose:
        # Compter les lignes uniquement si demande (lecture complete a ce
        # moment la, mais c'est explicite)
        try:
            with open(fichier, "rb") as f:
                total_lignes = sum(1 for _ in f)
            print(BLUE + "[INFO] Fichier: " + fichier +
                  " (" + str(total_lignes) + " lignes)" + NC)
        except OSError as e:
            print(RED + "[ERREUR] Lecture impossible: " + str(e) + NC)
            return 1

    try:
        with open(fichier, "rb") as f:
            for num, ligne in enumerate(f, 1):
                if num < debut:
                    continue
                if fin is not None and num > fin:
                    break
                print(decoder_ligne(ligne).rstrip("\r\n"))
    except OSError as e:
        print(RED + "[ERREUR] Lecture impossible: " + str(e) + NC)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
