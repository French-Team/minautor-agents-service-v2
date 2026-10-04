#!/usr/bin/env python3
# -*- coding: ascii -*-
# condenser-fichier.py
# Outil pour condenser les fichiers markdown
# Proprietaire : Buffy (outil partage)
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
condenser-fichier.py
condenser-fichier

Usage:
  condenser-fichier.py [OPTIONS]
"""

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


def lire_lignes(fichier):
    """Lire un fichier et retourner sa liste de lignes (CRLF/LF normalises)."""
    try:
        contenu = Path(fichier).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    return contenu.replace("\r\n", "\n").replace("\r", "\n").split("\n")


def analyser_fichier(fichier):
    """Analyser un fichier : lignes, frontmatter, sections, tableaux, problemes."""
    nom = Path(fichier).name
    lignes_liste = lire_lignes(fichier)
    lignes = len(lignes_liste)

    print("=== Analyse de " + nom + " ===")
    print("")
    print("Lignes totales : " + str(lignes))

    # Frontmatter : derniere ligne de fin de frontmatter (---)
    fin_fm = None
    for i, ligne in enumerate(lignes_liste):
        if ligne.strip() == "---":
            fin_fm = i + 1
    if fin_fm is not None:
        print("Frontmatter : " + str(fin_fm) + " lignes")

    # Sections
    sections = sum(1 for ligne in lignes_liste if re.match(r"^## [^#]", ligne))
    print("Sections : " + str(sections))

    # Tableaux
    tableaux = sum(1 for ligne in lignes_liste if re.match(r"^\|.*\|", ligne))
    print("Lignes de tableaux : " + str(tableaux))

    # Problemes
    print("")
    print("Problemes detectes :")
    if fin_fm is not None and fin_fm > 30:
        print("- Frontmatter trop long (" + str(fin_fm) + " lignes, max recommande: 30)")
    if tableaux > 50:
        print("- Trop de tableaux (" + str(tableaux) + " lignes)")
    if lignes > 200:
        print("- Fichier trop long (" + str(lignes) + " lignes, seuil: 200)")


def condenser_fichier(fichier, dry_run, verbose):
    """Condenser un fichier : sauvegarde + copie de travail + resume."""
    chemin = Path(fichier)
    backup = Path(str(chemin) + ".backup")
    temp = Path(str(chemin) + ".tmp")

    if not chemin.is_file():
        print("ERREUR: Le fichier " + str(chemin) + " n'existe pas")
        return 1

    # TOUJOURS creer une sauvegarde avant modification
    try:
        shutil.copy2(str(chemin), str(backup))
    except OSError as e:
        print("ERREUR: Impossible de creer la sauvegarde : " + str(e))
        return 1

    if verbose or dry_run:
        print("=== Condensation de " + chemin.name + " ===")
        print("")

    # Copie de travail (la condensation conserve le contenu : commentaires et separateurs)
    try:
        shutil.copy2(str(chemin), str(temp))
    except OSError as e:
        print("ERREUR: Impossible de creer le fichier temporaire : " + str(e))
        return 1

    lignes_avant = len(lire_lignes(chemin))
    lignes_apres = len(lire_lignes(temp))
    diff = lignes_avant - lignes_apres

    print("")
    print("=== Resume ===")
    print("Lignes avant : " + str(lignes_avant))
    print("Lignes apres : " + str(lignes_apres))
    print("Economie    : " + str(diff) + " lignes")

    if dry_run:
        print("")
        print("[DRY-RUN] Aucun changement applique")
        try:
            temp.unlink()
        except OSError:
            pass
    else:
        try:
            shutil.move(str(temp), str(chemin))
            print("")
            print("[APPLIQUE] Fichier mis a jour")
        except OSError as e:
            print("ERREUR: Impossible de mettre a jour le fichier : " + str(e))
            return 1

    return 0


def main():
    verifier_nommage()

    import argparse

    parser = argparse.ArgumentParser(
        prog="condenser-fichier",
        description="Condenser les fichiers markdown en reduisant le contenu non essentiel.",
    )
    parser.add_argument("fichier", help="Chemin du fichier a condenser ou analyser")
    parser.add_argument("--analyser", action="store_true", help="Analyser le fichier uniquement")
    parser.add_argument("--dry-run", action="store_true", help="Afficher les changements sans les appliquer")
    parser.add_argument("--verbose", action="store_true", help="Afficher les details")
    parser.add_argument("--backup", action="store_true", help="Creer une copie de sauvegarde")
    parser.add_argument("--version", action="version", version="condenser-fichier " + VERSION + " (" + STATUT + ")")
    parser.add_argument("--aide", action="help",
                  help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    if not Path(args.fichier).is_file():
        print("ERREUR: Le fichier " + args.fichier + " n'existe pas")
        return 1

    if args.analyser:
        analyser_fichier(args.fichier)
        return 0
    return condenser_fichier(args.fichier, args.dry_run, args.verbose)


if __name__ == "__main__":
    sys.exit(main())
