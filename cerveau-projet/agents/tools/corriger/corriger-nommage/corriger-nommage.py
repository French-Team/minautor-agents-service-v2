#!/usr/bin/env python3
# corriger-nommage.py
# Corriger le nommage des fichiers selon les conventions
# Version : 0.2.0-py
# Statut : beta

VERSION = "0.2.0-py"
STATUT = "beta"

import re
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


def renommer(fichier, nouveau_nom, dry_run):
    """Renommer le fichier si le nouveau nom differe, avec verification."""
    basename = fichier.name
    if basename == nouveau_nom:
        print("  " + GREEN + "[OK] Aucune correction necessaire" + NC)
        return 0

    print("  " + YELLOW + "[ATTENTION] Correction necessaire :" + NC)
    print("    Actuel : " + basename)
    print("    Nouveau : " + nouveau_nom)

    if dry_run:
        print("  " + YELLOW + "Mode dry-run : aucun fichier modifie" + NC)
        return 0

    chemin_complet = fichier.parent / nouveau_nom
    if chemin_complet.exists():
        print("  " + RED + "[ERREUR] Le fichier destination existe deja" + NC)
        return 1

    try:
        shutil.move(str(fichier), str(chemin_complet))
        print("  " + GREEN + "[OK] Fichier renomme" + NC)
        return 0
    except OSError as e:
        print("  " + RED + "[ERREUR] Echec du renommage : " + str(e) + NC)
        return 1


def corriger_protocole(fichier, dry_run):
    basename = fichier.name
    print(BLUE + "[OUTIL] Correction du nommage : " + basename + NC)
    print("")

    # Format : [nom].[major].[minor].[statut].md
    parties = basename.split(".")
    if len(parties) < 5:
        print("  " + RED + "[ERREUR] Format invalide : " + basename + NC)
        print("    Impossible de corriger automatiquement")
        return 1

    nouveau_nom = ".".join(parties) if basename.endswith(".md") else basename + ".md"
    # Le format attendu est deja nom.majeur.mineur.statut.md
    return renommer(fichier, basename, dry_run)


def corriger_agent(fichier, dry_run):
    basename = fichier.name
    print(BLUE + "[OUTIL] Correction du nommage : " + basename + NC)
    print("")

    # Format : nom-agent.md (minuscules)
    if re.match(r"^[a-z]+\.md$", basename):
        print("  " + GREEN + "[OK] Aucune correction necessaire" + NC)
        return 0

    nom = basename[:-3]
    nouveau_nom = nom + ".md"
    return renommer(fichier, nouveau_nom, dry_run)


def corriger_outil(fichier, dry_run):
    basename = fichier.name
    print(BLUE + "[OUTIL] Correction du nommage : " + basename + NC)
    print("")

    # Format : nom-outil.sh ou nom-outil.md (minuscules + tirets)
    if re.match(r"^[a-z-]+\.(sh|md)$", basename):
        print("  " + GREEN + "[OK] Aucune correction necessaire" + NC)
        return 0

    stem = basename.rsplit(".", 1)[0]
    ext = basename.rsplit(".", 1)[1]
    nouveau_nom = stem + "." + ext
    return renommer(fichier, nouveau_nom, dry_run)


def corriger_convention(fichier, dry_run):
    basename = fichier.name
    print(BLUE + "[OUTIL] Correction du nommage : " + basename + NC)
    print("")

    # Format : convention-nom.md
    if re.match(r"^convention-[a-z-]+\.md$", basename):
        print("  " + GREEN + "[OK] Aucune correction necessaire" + NC)
        return 0

    nom = basename[:-3]
    nom = re.sub(r"^convention-", "", nom)
    nouveau_nom = "convention-" + nom + ".md"
    return renommer(fichier, nouveau_nom, dry_run)


def main():
    verifier_nommage()

    import argparse

    parser = argparse.ArgumentParser(
        prog="corriger-nommage",
        description="Corriger le nommage des fichiers selon les conventions.",
    )
    parser.add_argument("fichier", help="Chemin du fichier a corriger")
    parser.add_argument("--type", required=True, choices=["protocole", "agent", "outil", "convention"],
                        help="Type de fichier (protocole, agent, outil, convention)")
    parser.add_argument("--dry-run", action="store_true", help="Simuler sans modifier")
    parser.add_argument("--verbose", action="store_true", help="Afficher les details")
    parser.add_argument("--version", action="version", version="corriger-nommage " + VERSION + " (" + STATUT + ")")
    args = parser.parse_args()

    fichier = Path(args.fichier)
    if not fichier.is_file():
        print("Erreur: Le fichier '" + args.fichier + "' n'existe pas")
        return 1

    if args.type == "protocole":
        return corriger_protocole(fichier, args.dry_run)
    elif args.type == "agent":
        return corriger_agent(fichier, args.dry_run)
    elif args.type == "outil":
        return corriger_outil(fichier, args.dry_run)
    elif args.type == "convention":
        return corriger_convention(fichier, args.dry_run)
    return 1


if __name__ == "__main__":
    sys.exit(main())
