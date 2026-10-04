#!/usr/bin/env python3
# -*- coding: ascii -*-
# deplacer-fichier.py
# Deplacer ou renommer un fichier vers une nouvelle destination
# Version : 0.3.1
# Statut : prepare

# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
deplacer-fichier.py
deplacer-fichier

Usage:
  deplacer-fichier.py [OPTIONS]
"""

VERSION = "0.3.1"
STATUT = "prepare"

import shutil
import sys
from pathlib import Path

# Securite (round 3) : force la sortie en UTF-8 pour ne jamais crasher sur
# l'encodage de la console (cp1252 sous Windows avec des caracteres non-ASCII).
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass  # Python < 3.7 : la console gere l'encodage comme elle peut

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
    parser.add_argument("--forcer", action="store_true",
                        help="Ecraser la destination si elle existe deja")
    parser.add_argument("--backup", action="store_true",
                        help="Sauvegarder la destination existante en .bak avant ecrasement")
    parser.add_argument("--dry-run", action="store_true", help="Simuler sans deplacer")
    parser.add_argument("--verbose", action="store_true", help="Afficher les details")
    parser.add_argument("--version", action="version", version="deplacer-fichier " + VERSION + " (" + STATUT + ")")
    parser.add_argument("--aide", action="help",
                  help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    source = Path(args.source)
    destination = Path(args.destination)

    # Securite (round 3) : octet nul dans les chemins -> refus explicite
    if "\x00" in args.source or "\x00" in args.destination:
        print(RED + "[ERREUR] Chemin non sur (octet nul present)" + NC)
        return 1

    # Securite (round 3) : refus de traverser un lien symbolique (source ou
    # destination) : deplacer ecrirait/ecraserait a travers le lien.
    if source.is_symlink() or destination.is_symlink():
        print(RED + "[ERREUR] Chemin est un lien symbolique (refus securite): " +
              args.source + " -> " + args.destination + NC)
        return 1

    if not source.is_file():
        print(RED + "[ERREUR] Source non trouvee ou pas un fichier: " + args.source + NC)
        return 1

    if args.source == args.destination:
        print(YELLOW + "[INFO] Source et destination identiques, rien a faire" + NC)
        return 0

    # Protection : destination existante -> refus sans --forcer (echec explicite)
    if destination.exists():
        if not args.forcer:
            print(RED + "[ERREUR] La destination existe deja: " + args.destination + NC)
            print(YELLOW + "[INFO] Utiliser --forcer pour ecraser, ou --backup pour sauvegarder avant" + NC)
            return 1
        if args.backup:
            shutil.copy2(str(destination), str(destination) + ".bak")
            if args.verbose:
                print(BLUE + "[INFO] Sauvegarde: " + str(destination) + ".bak" + NC)

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
