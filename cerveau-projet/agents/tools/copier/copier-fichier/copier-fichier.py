#!/usr/bin/env python3
# copier-fichier.py
# Copier un fichier vers une destination
# Version : 0.2.0-py
# Statut : beta

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


def main():
    verifier_nommage()

    import argparse

    parser = argparse.ArgumentParser(
        prog="copier-fichier",
        description="Copier un fichier vers une destination.",
    )
    parser.add_argument("source", help="Fichier source")
    parser.add_argument("destination", help="Fichier de destination")
    parser.add_argument("--forcer", action="store_true", help="Ecraser si la destination existe")
    parser.add_argument("--dry-run", action="store_true", help="Simuler sans copier")
    parser.add_argument("--verbose", action="store_true", help="Afficher les details")
    parser.add_argument("--version", action="version", version="copier-fichier " + VERSION + " (" + STATUT + ")")
    args = parser.parse_args()

    source = Path(args.source)
    destination = Path(args.destination)

    if not source.is_file():
        print(RED + "[ERREUR] Source non trouvee: " + str(source) + NC)
        return 1

    if destination.exists() and not args.forcer:
        print(RED + "[ERREUR] Destination existe deja: " + str(destination) + NC)
        print(YELLOW + "[INFO] Utiliser --forcer pour ecraser" + NC)
        return 1

    if args.dry_run:
        print(YELLOW + "[DRY-RUN] Copie: " + str(source) + " -> " + str(destination) + NC)
        return 0

    # Creer le repertoire parent si necessaire
    if not destination.parent.exists():
        try:
            destination.parent.mkdir(parents=True)
        except OSError as e:
            print(RED + "[ERREUR] Impossible de creer le dossier parent: " + str(e) + NC)
            return 1

    try:
        shutil.copy2(str(source), str(destination))
    except OSError as e:
        print(RED + "[ERREUR] La copie a echoue: " + str(e) + NC)
        return 1

    if args.verbose:
        print(GREEN + "[OK] Copie: " + str(source) + " -> " + str(destination) + NC)

    return 0


if __name__ == "__main__":
    sys.exit(main())
