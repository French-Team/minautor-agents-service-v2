#!/usr/bin/env python3
# creer-fichier.py
# Creer un nouveau fichier avec verification
# Version : 0.2.0-py
# Statut : beta

# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
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


def main():
    verifier_nommage()

    import argparse

    parser = argparse.ArgumentParser(
        prog="creer-fichier",
        description="Creer un nouveau fichier avec verification.",
    )
    parser.add_argument("fichier", help="Chemin du fichier a creer")
    parser.add_argument("contenu", nargs="?", default="", help="Contenu du fichier (optionnel)")
    parser.add_argument("--forcer", action="store_true", help="Ecraser si le fichier existe deja")
    parser.add_argument("--dry-run", action="store_true", help="Simuler sans creer")
    parser.add_argument("--verbose", action="store_true", help="Afficher les details")
    parser.add_argument("--version", action="version", version="creer-fichier " + VERSION + " (" + STATUT + ")")
    args = parser.parse_args()

    fichier = Path(args.fichier)

    # Verifier si le fichier existe deja
    if fichier.is_file() and not args.forcer:
        print(RED + "[ERREUR] Le fichier existe deja: " + args.fichier + NC)
        print(YELLOW + "[INFO] Utiliser --forcer pour ecraser" + NC)
        return 1

    if args.dry_run:
        print(YELLOW + "[DRY-RUN] Creation de: " + args.fichier + NC)
        if args.contenu:
            print(YELLOW + "[DRY-RUN] Contenu: " + args.contenu + NC)
        return 0

    # Creer le repertoire parent si necessaire
    if not fichier.parent.exists():
        try:
            fichier.parent.mkdir(parents=True)
            if args.verbose:
                print(BLUE + "[INFO] Repertoire cree: " + str(fichier.parent) + NC)
        except OSError as e:
            print(RED + "[ERREUR] Impossible de creer le repertoire: " + str(e) + NC)
            return 1

    # Creer le fichier
    try:
        if args.contenu:
            # FIGER LF : open en mode texte avec newline='' (pas de traduction CRLF Windows)
            with open(fichier, "w", encoding="utf-8", newline="") as f:
                f.write(args.contenu + "\n")
        else:
            fichier.touch()
    except OSError as e:
        print(RED + "[ERREUR] Impossible de creer le fichier: " + str(e) + NC)
        return 1

    if args.verbose:
        print(GREEN + "[OK] Fichier cree: " + args.fichier + NC)

    return 0


if __name__ == "__main__":
    sys.exit(main())
