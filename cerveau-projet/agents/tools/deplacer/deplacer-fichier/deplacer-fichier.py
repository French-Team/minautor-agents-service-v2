#!/usr/bin/env python3
# deplacer-fichier.py
# Deplacer ou renommer un fichier vers une nouvelle destination
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
        prog="deplacer-fichier",
        description="Deplacer ou renommer un fichier vers une nouvelle destination.",
    )
    parser.add_argument("source", help="Fichier a deplacer ou renommer")
    parser.add_argument("destination", help="Nouveau chemin du fichier")
    parser.add_argument("--dry-run", action="store_true", help="Simuler sans deplacer")
    parser.add_argument("--verbose", action="store_true", help="Afficher les details")
    parser.add_argument("--version", action="version", version="deplacer-fichier " + VERSION + " (" + STATUT + ")")
    args = parser.parse_args()

    source = Path(args.source)
    destination = Path(args.destination)

    if not source.is_file():
        print(RED + "[ERREUR] Source non trouvee ou pas un fichier: " + args.source + NC)
        return 1

    if args.source == args.destination:
        print(YELLOW + "[INFO] Source et destination identiques, rien a faire" + NC)
        return 0

    if destination.exists():
        print(YELLOW + "[INFO] La destination existe deja, elle sera ecrasee: " + args.destination + NC)

    if args.verbose:
        print(BLUE + "[INFO] Source: " + args.source + NC)
        print(BLUE + "[INFO] Destination: " + args.destination + NC)

    if args.dry_run:
        print(YELLOW + "[DRY-RUN] Deplacement simule : " + args.source + " -> " + args.destination + NC)
        return 0

    # Creer le dossier parent de destination si besoin
    if not destination.parent.exists():
        try:
            destination.parent.mkdir(parents=True)
        except OSError as e:
            print(RED + "[ERREUR] Impossible de creer le dossier: " + str(destination.parent) + " : " + str(e) + NC)
            return 1

    try:
        shutil.move(str(source), str(destination))
    except OSError as e:
        print(RED + "[ERREUR] Le deplacement a echoue: " + str(e) + NC)
        return 1

    print(GREEN + "[OK] Fichier deplace : " + args.source + " -> " + args.destination + NC)
    return 0


if __name__ == "__main__":
    sys.exit(main())
