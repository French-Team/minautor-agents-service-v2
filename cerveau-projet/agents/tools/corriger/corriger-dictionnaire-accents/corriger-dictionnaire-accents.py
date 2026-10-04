#!/usr/bin/env python3
# -*- coding: ascii -*-
# corriger-dictionnaire-accents.py
# Outil pour detecter et corriger les accents et caracteres non-ASCII
# Conforme a la regle regles-emojis-ascii.md
# Version : 0.2.2-py
# Statut : beta

# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
corriger-dictionnaire-accents.py
corriger-dictionnaire-accents

Usage:
  corriger-dictionnaire-accents.py [OPTIONS]
"""

VERSION = "0.2.2-py"
STATUT = "beta"

import difflib
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


def lire_dictionnaire(dict_file):
    """Lire le dictionnaire (lignes 'accent|remplacement', ignorer # et vides)."""
    replacements = []
    try:
        with Path(dict_file).open(encoding="utf-8") as df:
            for line in df:
                line = line.rstrip("\n").rstrip("\r")
                if not line or line.startswith("#"):
                    continue
                if "|" in line:
                    accent, repl = line.split("|", 1)
                    if accent:
                        replacements.append((accent, repl))
    except OSError:
        pass
    return replacements


def main():
    verifier_nommage()

    import argparse

    parser = argparse.ArgumentParser(
        prog="corriger-dictionnaire-accents",
        description="Detecter et corriger les accents et caracteres non-ASCII via le dictionnaire.",
    )
    parser.add_argument("fichier", help="Fichier a corriger")
    parser.add_argument("--dry-run", action="store_true", help="Afficher les changements sans les appliquer")
    parser.add_argument("--verbose", action="store_true", help="Afficher les details")
    parser.add_argument("--dictionnaire", default=None, help="Chemin vers le dictionnaire (defaut: celui de l'outil)")
    parser.add_argument("--version", action="version", version="corriger-dictionnaire-accents " + VERSION + " (" + STATUT + ")")
    parser.add_argument("--aide", action="help",
                  help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    if args.dictionnaire:
        dict_file = Path(args.dictionnaire)
    else:
        dict_file = Path(__file__).resolve().parent / "corriger-dictionnaire-accents.txt"

    fichier = Path(args.fichier)
    if not fichier.is_file():
        print(RED + "[ERREUR] Fichier non trouve: " + args.fichier + NC)
        return 1

    if not dict_file.is_file():
        print(RED + "[ERREUR] Dictionnaire non trouve: " + str(dict_file) + NC)
        return 1

    print("[INFO] Correction des accents et caracteres non-ASCII")
    print("Fichier: " + args.fichier)
    print("Dictionnaire: " + str(dict_file))
    print("")

    replacements = lire_dictionnaire(dict_file)

    try:
        original = fichier.read_text(encoding="utf-8")
    except OSError as e:
        print(RED + "[ERREUR] Lecture impossible: " + str(e) + NC)
        return 1

    content = original
    total_changes = 0
    for accent, repl in replacements:
        count = content.count(accent)
        if count > 0:
            content = content.replace(accent, repl)
            total_changes += count
            if args.verbose:
                print("[OK] Remplace: '" + accent + "' -> '" + repl + "' (" + str(count) + " occurrences)")

    non_ascii = sum(1 for c in content if ord(c) > 127)

    if args.dry_run:
        if total_changes > 0:
            diff = list(difflib.unified_diff(
                original.splitlines(True),
                content.splitlines(True),
                fromfile=args.fichier,
                tofile=args.fichier + " (corrige)",
                lineterm="",
            ))
            for line in diff[:50]:
                print(line)
            if len(diff) > 50:
                print("... (" + str(len(diff) - 50) + " lignes de diff en plus)")
        print("")
        print("[INFO] Total: " + str(total_changes) + " occurrences modifiees")
        print("[INFO] Caracteres non-ASCII restants: " + str(non_ascii))
        print("[INFO] Aucune modification appliquee (dry-run)")
    else:
        if total_changes > 0:
            backup = args.fichier + ".bak"
            try:
                Path(backup).write_text(original, encoding="utf-8", newline="")
                fichier.write_text(content, encoding="utf-8", newline="")
            except OSError as e:
                print(RED + "[ERREUR] Ecriture impossible: " + str(e) + NC)
                return 1
            print("[OK] " + str(total_changes) + " occurrences modifiees")
            print("[INFO] Sauvegarde creee: " + backup)
            print("[INFO] Caracteres non-ASCII restants: " + str(non_ascii))
        else:
            print("[OK] Aucun accent ou caractere non-ASCII detecte")

    return 0


if __name__ == "__main__":
    sys.exit(main())
