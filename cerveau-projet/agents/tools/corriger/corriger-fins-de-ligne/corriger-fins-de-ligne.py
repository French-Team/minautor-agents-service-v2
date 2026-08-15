#!/usr/bin/env python3
# -*- coding: ascii -*-
# corriger-fins-de-ligne.py
# Convertit les fins de ligne CRLF vers LF sur un fichier ou un dossier (--recursive)
# Version : 0.1.1
# Statut : prepare

# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
corriger-fins-de-ligne.py
corriger-fins-de-ligne

Usage:
  corriger-fins-de-ligne.py [OPTIONS]
"""

VERSION = "0.1.1"
STATUT = "prepare"

import argparse
import os
import re
import sys
from pathlib import Path

# Couleurs ANSI (desactivees si la sortie n'est pas un terminal)
if sys.stdout.isatty():
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    NC = "\033[0m"
else:
    RED = GREEN = YELLOW = NC = ""


def verifier_nommage():
    """Regle immuable : le nom du fichier doit commencer par le prefixe du dossier de categorie."""
    nom = Path(__file__).name
    dossier = Path(__file__).resolve().parent.name
    if not nom.startswith(dossier):
        print(RED + "[ERREUR] Nommage invalide : le fichier doit commencer par '" + dossier + "'" + NC)
        print("  Nom actuel : " + nom)
        sys.exit(2)


def _stats_fichier(chemin):
    """Retourne (nb_crlf, nb_lf) du fichier."""
    with open(chemin, "rb") as f:
        donnees = f.read()
    crlf = donnees.count(b"\r\n")
    lf = donnees.count(b"\n") - crlf
    return crlf, lf


def convertir_fichier(chemin, dry_run, verbose):
    """Convertit CRLF vers LF. Retourne (statut, crlf, lf).
    statut : 'converti' | 'deja_lf' | 'vide' | 'binaire' | 'erreur'
    """
    try:
        with open(chemin, "rb") as f:
            donnees = f.read()
    except OSError as e:
        return ("erreur", 0, 0, str(e))

    crlf = donnees.count(b"\r\n")
    lf = donnees.count(b"\n") - crlf

    if crlf == 0:
        return ("deja_lf", crlf, lf, "")

    # Detecter un fichier binaire (octet nul) : ne pas toucher
    if b"\x00" in donnees:
        return ("binaire", crlf, lf, "")

    # Convertir TOUS les CR avant un LF (gere aussi les sequences multi-CR
    # type \r\r\r\n qui resultent d'editions successives corrompues)
    nouveau = re.sub(rb"\r+\n", b"\n", donnees)

    if dry_run:
        return ("converti", crlf, lf, "")

    try:
        with open(chemin, "wb") as f:
            f.write(nouveau)
    except OSError as e:
        return ("erreur", crlf, lf, str(e))

    return ("converti", crlf, lf, "")


def collecter_fichiers(chemin, recursive):
    """Retourne la liste des fichiers texte a traiter."""
    p = Path(chemin)
    fichiers = []
    if p.is_file():
        fichiers.append(p)
    elif p.is_dir():
        if recursive:
            for racine, _, noms in os.walk(p):
                for nom in noms:
                    fp = Path(racine) / nom
                    if "__pycache__" in str(fp) or fp.suffix == ".pyc":
                        continue
                    fichiers.append(fp)
        else:
            for nom in p.iterdir():
                if nom.is_file():
                    fichiers.append(nom)
    return fichiers


def main():
    parser = argparse.ArgumentParser(
        description="Convertir les fins de ligne CRLF vers LF (fichier ou dossier)."
    )
    parser.add_argument("chemin", nargs="?", help="Fichier ou dossier a convertir")
    parser.add_argument("--recursive", action="store_true",
                        help="Traiter les sous-dossiers recursivement")
    parser.add_argument("--dry-run", action="store_true",
                        help="Simuler sans modifier")
    parser.add_argument("--verbose", action="store_true",
                        help="Afficher le detail de chaque fichier")
    parser.add_argument("--version", action="store_true",
                        help="Afficher la version")
    parser.add_argument("--aide", action="help",
                  help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    if args.version:
        print("corriger-fins-de-ligne " + VERSION)
        return 0

    verifier_nommage()

    if not args.chemin:
        parser.error("le chemin est obligatoire (ou utilisez --version)")

    if not os.path.exists(args.chemin):
        print(RED + "[ERREUR] Chemin introuvable : " + args.chemin + NC)
        return 2

    fichiers = collecter_fichiers(args.chemin, args.recursive)
    if not fichiers:
        print(YELLOW + "[AVERTISSEMENT] Aucun fichier a traiter." + NC)
        return 0

    stats = {"analyses": 0, "convertis": 0, "deja_lf": 0, "binaires": 0, "erreurs": 0}
    detail = []

    for fp in fichiers:
        statut, crlf, lf, msg = convertir_fichier(fp, args.dry_run, args.verbose)
        stats["analyses"] += 1
        if statut == "converti":
            stats["convertis"] += 1
            detail.append((fp, "converti", crlf))
        elif statut == "deja_lf":
            stats["deja_lf"] += 1
        elif statut == "binaire":
            stats["binaires"] += 1
        else:
            stats["erreurs"] += 1
            detail.append((fp, "erreur", msg))

    mode = "SIMULATION (dry-run)" if args.dry_run else "EXECUTION"
    print("=== corriger-fins-de-ligne " + VERSION + " -- " + mode + " ===")

    if args.verbose:
        for fp, statut, info in detail:
            if statut == "converti":
                print("  " + GREEN + "[CONVERTI] " + NC + str(fp) + " (CRLF: " + str(info) + ")")
            elif statut == "erreur":
                print("  " + RED + "[ERREUR] " + NC + str(fp) + " : " + str(info))

    print("---")
    print("Fichiers analyses : " + str(stats["analyses"]))
    print("Convertes (CRLF -> LF) : " + str(stats["convertis"]))
    print("Deja en LF : " + str(stats["deja_lf"]))
    print("Binaires ignores : " + str(stats["binaires"]))
    print("Erreurs : " + str(stats["erreurs"]))

    if stats["erreurs"] > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
