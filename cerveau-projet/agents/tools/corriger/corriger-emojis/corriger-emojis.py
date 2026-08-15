#!/usr/bin/env python3
# -*- coding: ascii -*-
# corriger-emojis.py
# Detecte et remplace les emojis par des symboles ASCII
# Proprietaire : Vulcain (outil partage)
# Version : 0.2.0-py
# Statut : beta

# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
corriger-emojis.py
corriger-emojis

Usage:
  corriger-emojis.py [OPTIONS]
"""

VERSION = "0.2.0-py"
STATUT = "beta"

import sys
from pathlib import Path

# Couleurs ANSI (desactivees si la sortie n'est pas un terminal)
if sys.stdout.isatty():
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    NC = "\033[0m"
else:
    RED = GREEN = YELLOW = BLUE = NC = ""


def verifier_nommage():
    """Regle immuable : le nom du fichier doit commencer par le prefixe du dossier de categorie."""
    nom = Path(__file__).name
    dossier = Path(__file__).resolve().parent.name
    if not nom.startswith(dossier):
        print(RED + "[ERREUR] Nommage invalide : le fichier doit commencer par '" + dossier + "'" + NC)
        print("  Nom actuel : " + nom)
        sys.exit(2)


def lire_dictionnaire(dict_file):
    """Lire le dictionnaire (lignes 'EMOJI|REMPLACEMENT', ignorer # et vides)."""
    replacements = []
    try:
        with Path(dict_file).open(encoding="utf-8") as df:
            for line in df:
                line = line.rstrip("\n").rstrip("\r")
                if not line or line.startswith("#"):
                    continue
                if "|" in line:
                    emoji, repl = line.split("|", 1)
                    if emoji:
                        replacements.append((emoji, repl))
    except OSError:
        pass
    return replacements


def executer_fichier(fichier, replacements, dry_run, verbose):
    """Detecter et remplacer les emojis dans un fichier. Retourne True si modifie."""
    try:
        content = Path(fichier).read_text(encoding="utf-8")
    except OSError as e:
        print(RED + "[ERREUR] Lecture impossible : " + str(e) + NC)
        return False

    present = []
    for emoji, repl in replacements:
        if emoji in content:
            present.append((emoji, repl, content.count(emoji)))

    if not present:
        if verbose:
            print("[OK] aucun emoji detecte")
        return False

    print("[ATTENTION] emojis detectes :")
    for emoji, repl, n in present:
        print("  " + emoji + " (x" + str(n) + ") -> " + repl)

    if dry_run:
        print("[DRY-RUN] Changements non appliques")
        return False

    # Appliquer les remplacements (le plus long d'abord pour eviter les conflits)
    for emoji, repl, n in sorted(present, key=lambda x: -len(x[0])):
        content = content.replace(emoji, repl)

    try:
        Path(fichier).write_text(content, encoding="utf-8", newline="")
    except OSError as e:
        print(RED + "[ERREUR] Ecriture impossible : " + str(e) + NC)
        return False

    print("[OK] " + str(len(present)) + " emoji(s) remplace(s)")
    return True


def main():
    verifier_nommage()

    import argparse

    parser = argparse.ArgumentParser(
        prog="corriger-emojis",
        description="Detecte et remplace les emojis par des symboles ASCII.",
    )
    parser.add_argument("cible", help="Fichier ou dossier a corriger")
    parser.add_argument("--dry-run", action="store_true", help="Afficher les changements sans les appliquer")
    parser.add_argument("--verbose", action="store_true", help="Afficher les details")
    parser.add_argument("--version", action="version", version="corriger-emojis " + VERSION + " (" + STATUT + ")")
    parser.add_argument("--aide", action="help",
                  help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    dict_file = Path(__file__).resolve().parent / "dictionnaire-emojis.txt"
    if not dict_file.is_file():
        print(RED + "[ERREUR] Dictionnaire non trouve : " + str(dict_file) + NC)
        return 1

    cible = Path(args.cible)
    if not cible.exists():
        print(RED + "[ERREUR] Cible non trouvee : " + args.cible + NC)
        return 1

    print(BLUE + "=== Correction des emojis ===" + NC)
    print("Cible : " + args.cible)
    print("Dictionnaire : " + str(dict_file))
    print("")

    replacements = lire_dictionnaire(dict_file)

    if cible.is_file():
        executer_fichier(cible, replacements, args.dry_run, args.verbose)
    elif cible.is_dir():
        nb_fichiers = 0
        nb_modifies = 0
        nb_errores = 0

        fichiers = []
        for ext in (".md", ".sh", ".py"):
            fichiers.extend(cible.rglob("*" + ext))
        # Exclure le dossier exemples
        fichiers = [f for f in fichiers if f.is_file() and "exemples" not in f.parts]

        for fichier in fichiers:
            nb_fichiers += 1
            if executer_fichier(fichier, replacements, args.dry_run, args.verbose):
                nb_modifies += 1

        print("")
        print(BLUE + "=== Resumer ===" + NC)
        print("Fichiers analyses : " + str(nb_fichiers))
        print("Fichiers modifies : " + str(nb_modifies))
        print("Erreurs : " + str(nb_errores))
    else:
        print(RED + "[ERREUR] Cible non trouvee : " + args.cible + NC)
        return 1

    print("")
    print(GREEN + "=== Termine ===" + NC)
    return 0


if __name__ == "__main__":
    sys.exit(main())
