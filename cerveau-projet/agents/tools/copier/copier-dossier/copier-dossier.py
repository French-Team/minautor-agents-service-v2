#!/usr/bin/env python3
# copier-dossier.py
# Copier un dossier recursivement vers une destination
# Version : 0.2.0-py
# Statut : beta

# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION = "0.2.0-py"
STATUT = "beta"

import shutil
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


def compter_fichiers(source):
    """Compter le nombre de fichiers dans le dossier source (recursif)."""
    return sum(1 for p in source.rglob("*") if p.is_file())


def main():
    verifier_nommage()

    import argparse

    parser = argparse.ArgumentParser(
        prog="copier-dossier",
        description="Copier un dossier recursivement vers une destination.",
    )
    parser.add_argument("source", help="Dossier a copier (recursif)")
    parser.add_argument("destination", help="Dossier de destination")
    parser.add_argument("--dry-run", action="store_true", help="Simuler sans copier")
    parser.add_argument("--verbose", action="store_true", help="Afficher les details")
    parser.add_argument("--version", action="version", version="copier-dossier " + VERSION + " (" + STATUT + ")")
    args = parser.parse_args()

    source = Path(args.source)
    destination = Path(args.destination)

    if not source.is_dir():
        print(RED + "[ERREUR] Source non trouvee ou pas un dossier: " + str(source) + NC)
        return 1

    # Anti-boucle : la destination ne doit pas etre dans la source
    try:
        if source.resolve() in destination.resolve().parents:
            print(RED + "[ERREUR] La destination (" + str(destination) + ") est dans la source (" + str(source) + ")" + NC)
            return 1
    except OSError:
        pass

    if destination.exists():
        print(YELLOW + "[INFO] La destination existe deja: " + str(destination) + NC)
        print(YELLOW + "[INFO] Le contenu sera fusionne/ecrase" + NC)

    nb_fichiers = compter_fichiers(source)

    if args.verbose:
        print(BLUE + "[INFO] Source: " + str(source) + " (" + str(nb_fichiers) + " fichiers)" + NC)
        print(BLUE + "[INFO] Destination: " + str(destination) + NC)

    if args.dry_run:
        print(YELLOW + "[DRY-RUN] Copie simulee : " + str(source) + " -> " + str(destination) + " (" + str(nb_fichiers) + " fichiers)" + NC)
        return 0

    try:
        shutil.copytree(str(source), str(destination), dirs_exist_ok=True)
    except OSError as e:
        print(RED + "[ERREUR] La copie a echoue: " + str(e) + NC)
        return 1

    print(GREEN + "[OK] Copie terminee : " + str(source) + " -> " + str(destination) + NC)
    print(GREEN + "[INFO] " + str(nb_fichiers) + " fichiers copies" + NC)
    return 0


if __name__ == "__main__":
    sys.exit(main())
