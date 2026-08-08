#!/usr/bin/env python3
# corriger-liens.py
# Corrige les liens casses dans un fichier Markdown
# Version : 0.2.0-py
# Statut : beta

# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
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


def extraire_liens(contenu):
    """Extraire tous les liens markdown [texte](chemin)."""
    pattern = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")
    return pattern.findall(contenu)


def corriger_liens(fichier, dry_run, verbose):
    fichier_path = Path(fichier)
    dossier_fichier = fichier_path.parent

    print(BLUE + "[OUTIL] Correction des liens dans : " + fichier + NC)
    print(BLUE + "[DOSSIER] Repertoire du fichier : " + str(dossier_fichier) + NC)
    print("")

    # Creer une copie de sauvegarde
    if not dry_run:
        try:
            shutil.copy2(fichier, str(fichier_path) + ".backup")
            print(YELLOW + "[CHECKLIST] Copie de sauvegarde : " + str(fichier_path) + ".backup" + NC)
        except OSError as e:
            print(RED + "[ERREUR] Impossible de creer la sauvegarde : " + str(e) + NC)
            return 1

    try:
        contenu = Path(fichier).read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        print(RED + "[ERREUR] Impossible de lire le fichier : " + str(e) + NC)
        return 1

    liens = extraire_liens(contenu)

    if not liens:
        print(YELLOW + "Aucun lien Markdown trouve." + NC)
        return 0

    total = len(liens)
    print(BLUE + "Trouve " + str(total) + " lien(s) Markdown" + NC)
    print("")

    liens_valides = 0
    liens_corriges = 0

    for texte, chemin in liens:
        # Lien externe : on ne le corrige pas
        if re.match(r"^https?://", chemin):
            liens_valides += 1
            if verbose:
                print(YELLOW + "[LIEN] " + texte + " -> " + chemin + " (externe)" + NC)
            continue

        # Lien interne : verifier depuis le repertoire du fichier
        chemin_rel = chemin.split("#")[0]  # ignorer les ancres
        if not chemin_rel:
            liens_valides += 1
            continue

        cible = (dossier_fichier / chemin_rel).resolve()
        if cible.exists():
            liens_valides += 1
            if verbose:
                print(GREEN + "[OK] " + texte + " -> " + chemin + NC)
        else:
            print(RED + "[ERREUR] Lien casse : " + texte + " -> " + chemin + NC)
            print("   Chemin verifie : " + str(cible))
            print("  Suggestions :")
            print("    - Verifier le nom du fichier")
            print("    - Verifier le chemin")
            print("    - Creer le fichier manquant")
            liens_corriges += 1

    print("")
    print(BLUE + "Resume :" + NC)
    print(GREEN + "[OK] Liens valides : " + str(liens_valides) + NC)
    print(YELLOW + "[ATTENTION] Liens a corriger : " + str(liens_corriges) + NC)

    if dry_run:
        print(YELLOW + "Mode dry-run : aucun fichier modifie" + NC)
    else:
        print(GREEN + "Copie de sauvegarde : " + str(fichier_path) + ".backup" + NC)

    return 0


def main():
    verifier_nommage()

    import argparse

    parser = argparse.ArgumentParser(
        prog="corriger-liens",
        description="Corrige les liens casses dans un fichier Markdown.",
    )
    parser.add_argument("fichier", help="Fichier Markdown a corriger")
    parser.add_argument("--dry-run", action="store_true", help="Simuler sans modifier")
    parser.add_argument("--verbose", action="store_true", help="Afficher les details")
    parser.add_argument("--version", action="version", version="corriger-liens " + VERSION + " (" + STATUT + ")")
    args = parser.parse_args()

    fichier = Path(args.fichier)
    if not fichier.is_file():
        print("Erreur: Le fichier '" + args.fichier + "' n'existe pas")
        return 1

    return corriger_liens(args.fichier, args.dry_run, args.verbose)


if __name__ == "__main__":
    sys.exit(main())
