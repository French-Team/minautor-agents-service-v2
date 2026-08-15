#!/usr/bin/env python3
# -*- coding: ascii -*-
# changer-statut.py
# Change le statut d'un fichier en le renommant selon la convention
# Proprietaire : Janus (outil partage)
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
changer-statut.py
changer-statut

Usage:
  changer-statut.py [OPTIONS]
"""

VERSION = "0.2.0-py"
STATUT = "beta"

import os
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

STATUTS_VALIDES = ("ebauche", "prepare", "dev", "test", "valide")


def verifier_nommage():
    """Regle immuable : le nom du fichier doit commencer par le prefixe du dossier de categorie."""
    nom = Path(__file__).name
    dossier = Path(__file__).resolve().parent.name
    if not nom.startswith(dossier):
        print(RED + "[ERREUR] Nommage invalide : le fichier doit commencer par '" + dossier + "'" + NC)
        print("  Nom actuel : " + nom)
        sys.exit(2)


def extraire_parties(fichier):
    """Extraire nom, id, class, statut du nom de fichier (separateur = point)."""
    basename = Path(fichier).stem  # retire l'extension .md
    parties = basename.split(".")
    if len(parties) < 4:
        return None
    statut = parties[-1]
    class_ = parties[-2]
    id_ = parties[-3]
    nom = ".".join(parties[:-3])
    return {"nom": nom, "id": id_, "class": class_, "statut": statut}


def incrementer_class(class_):
    """Incrementer le class et le formater sur 2 chiffres."""
    try:
        return "%02d" % (int(class_) + 1)
    except ValueError:
        return None


def trouver_liens(fichier):
    """Trouver les liens markdown qui pointent vers ce fichier dans le dossier et sous-dossiers."""
    dossier = Path(fichier).resolve().parent
    basename = Path(fichier).name
    motif = "]" + basename + "]"
    liens = []
    for p in dossier.rglob("*"):
        if p.is_file() and p.suffix == ".md":
            try:
                contenu = p.read_text(encoding="utf-8", errors="replace")
                for ligne in contenu.splitlines():
                    if motif in ligne:
                        liens.append(str(p) + ": " + ligne.strip())
            except OSError:
                continue
    return liens


def construire_parser():
    import argparse

    parser = argparse.ArgumentParser(
        prog="changer-statut",
        description="Change le statut d'un fichier en le renommant selon la convention.",
    )
    parser.add_argument("fichier", help="Chemin du fichier a renommer")
    parser.add_argument(
        "statut",
        help="Nouveau statut : ebauche, prepare, dev, test, valide",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Afficher les changements sans les appliquer",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Forcer le changement meme si des liens pointent vers le fichier",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Afficher les details",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="changer-statut " + VERSION + " (" + STATUT + ")",
    )
    return parser


def main():
    verifier_nommage()
    parser = construire_parser()
    parser.add_argument("--aide", action="help",
                  help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    fichier = Path(args.fichier)
    nouveau_statut = args.statut

    print(BLUE + "=== Changement de statut ===" + NC)
    print("Fichier : " + str(fichier))
    print("Nouveau statut : " + nouveau_statut)
    print("")

    # 1. Verifier que le fichier existe
    if not fichier.is_file():
        print(RED + "[ERREUR] Fichier non trouve : " + str(fichier) + NC)
        return 1

    # 2. Verifier que le nouveau statut est valide
    if nouveau_statut not in STATUTS_VALIDES:
        print(RED + "[ERREUR] Statut invalide : " + nouveau_statut + NC)
        print("  Statuts valides : " + ", ".join(STATUTS_VALIDES))
        return 1

    # 3. Extraire les parties du nom
    parties = extraire_parties(fichier)
    if parties is None:
        print(RED + "[ERREUR] Impossible d'extraire les parties du nom de fichier" + NC)
        print("  Format attendu : [type]-[theme].[id].[class].[statut].md")
        return 1

    nom_sans_statut = parties["nom"]
    id_ = parties["id"]
    class_actuel = parties["class"]
    statut_actuel = parties["statut"]

    # 4. Incrementer le class
    nouveau_class = incrementer_class(class_actuel)
    if nouveau_class is None:
        print(RED + "[ERREUR] Class invalide : " + class_actuel + NC)
        return 1

    # 5. Construire le nouveau nom
    nouveau_nom = nom_sans_statut + "." + id_ + "." + nouveau_class + "." + nouveau_statut + ".md"
    nouveau_chemin = fichier.parent / nouveau_nom

    print(BLUE + "--- Details ---" + NC)
    print("Nom actuel : " + fichier.name)
    print("Nom nouveau : " + nouveau_nom)
    print("Class : " + class_actuel + " -> " + nouveau_class)
    print("Statut : " + statut_actuel + " -> " + nouveau_statut)
    print("")

    # 6. Verifier si des liens pointent vers ce fichier
    print(BLUE + "--- Verification des liens ---" + NC)
    liens = trouver_liens(fichier)
    if liens:
        print(YELLOW + "[ATTENTION] Des liens pointent vers ce fichier :" + NC)
        for lien in liens[:5]:
            print("  " + lien)
        print("")
        if not args.force:
            print(RED + "[ERREUR] Utiliser --force pour ignorer les liens" + NC)
            return 1
    else:
        print(GREEN + "[OK] Aucun lien trouve" + NC)

    # 7. Verifier que le nouveau nom n'existe pas deja
    if nouveau_chemin.exists():
        print(RED + "[ERREUR] Le fichier existe deja : " + str(nouveau_chemin) + NC)
        return 1

    # 8. Appliquer le changement
    print("")
    if args.dry_run:
        print(YELLOW + "[DRY-RUN] Changement non applique" + NC)
        print("  Renommer : " + fichier.name + " -> " + nouveau_nom)
    else:
        try:
            shutil.move(str(fichier), str(nouveau_chemin))
            print(GREEN + "[OK] Fichier renomme avec succes" + NC)
            print("  " + fichier.name + " -> " + nouveau_nom)
        except OSError as e:
            print(RED + "[ERREUR] Erreur lors du renommage : " + str(e) + NC)
            return 1

    print("")
    print(GREEN + "=== Termine ===" + NC)
    return 0


if __name__ == "__main__":
    sys.exit(main())
