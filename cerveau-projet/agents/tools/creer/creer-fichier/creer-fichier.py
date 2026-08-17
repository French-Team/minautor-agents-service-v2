#!/usr/bin/env python3
# -*- coding: ascii -*-
# creer-fichier.py
# Creer un nouveau fichier avec verification
# Version : 0.3.2
# Statut : prepare

# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
creer-fichier.py
creer-fichier

Usage:
  creer-fichier.py [OPTIONS]
"""

VERSION = "0.3.2"
STATUT = "prepare"

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
        prog="creer-fichier",
        description="Creer un nouveau fichier avec verification.",
    )
    parser.add_argument("fichier", help="Chemin du fichier a creer")
    parser.add_argument("contenu", nargs="?", default="", help="Contenu du fichier (optionnel)")
    parser.add_argument("--forcer", action="store_true", help="Ecraser si le fichier existe deja")
    parser.add_argument("--backup", action="store_true", help="Sauvegarder le fichier existant en .bak avant ecrasement")
    parser.add_argument("--dry-run", action="store_true", help="Simuler sans creer")
    parser.add_argument("--verbose", action="store_true", help="Afficher les details")
    parser.add_argument("--version", action="version", version="creer-fichier " + VERSION + " (" + STATUT + ")")
    parser.add_argument("--aide", action="help",
                  help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    fichier = Path(args.fichier)

    # Securite (round 3) : octet nul dans le chemin -> refus explicite
    if "\x00" in args.fichier:
        print(RED + "[ERREUR] Chemin non sur (octet nul present)" + NC)
        return 1

    # Securite (round 3) : refus de creer/ecraser a travers un lien symbolique
    if fichier.is_symlink():
        print(RED + "[ERREUR] Chemin est un lien symbolique (refus securite): " +
              args.fichier + NC)
        return 1

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

    # Sauvegarde avant ecrasement (--forcer + --backup)
    if fichier.is_file() and args.forcer and args.backup:
        try:
            import shutil
            shutil.copy2(str(fichier), str(fichier) + ".bak")
            if args.verbose:
                print(BLUE + "[INFO] Sauvegarde: " + str(fichier) + ".bak" + NC)
        except OSError as e:
            print(RED + "[ERREUR] Sauvegarde impossible: " + str(e) + NC)
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

    # MESSAGES INFORMATIONNELS (regle immuable v0.3.0)
    print("")
    print(YELLOW + "=== MESSAGES POUR L AGENT ===" + NC)
    print("  > fichier cree : s il s agit d un OUTIL, ajouter l entree index-tools.md + catalogue + .md de doc obligatoire + assignation a un agent")
    print("  > fichier cree : s il s agit d un RAPPORT, le placer dans le dossier de l agent (jamais a la racine)")
    print("  > fichier cree : verifier les fichiers qui le referencent (tests, index, docs)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
