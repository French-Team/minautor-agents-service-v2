#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
detecter-erreur-statut.py
Detecte les fichiers dont le statut ne correspond pas a leur contenu.

Evalue la maturite d'un fichier markdown (lignes, frontmatter, sections,
tableaux, code, listes, liens) puis compare le statut recommande au statut
porte par le nom du fichier (ebauche, prepare, dev, test, valide).

Usage:
  detecter-erreur-statut.py [dossier] [options]

Options:
  --statut <statut>   Filtrer par statut (ebauche, prepare, dev, test, valide)
  --verbose           Afficher les details
  --version           Afficher la version
  --aide, -h          Afficher cette aide

Retour: 0 si aucune erreur de statut, 1 sinon.

Proprietaire : Vulcain (outil partage)
Version : 0.2.0-py
Statut : beta
"""

import argparse
import os
import re
import sys

VERSION = "0.2.0-py"
STATUT = "beta"

# Couleurs ANSI
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[0;34m"
NC = "\033[0m"  # No Color

# Statuts valides et leur ordre
STATUTS = ["ebauche", "prepare", "dev", "test", "valide"]
ORDRE = {s: i + 1 for i, s in enumerate(STATUTS)}


def extraire_statut(fichier):
    """Extrait le statut porte par le nom du fichier."""
    basename = os.path.basename(fichier)
    m = re.search(r"\.(ebauche|prepare|dev|test|valide)\.md$", basename)
    return m.group(1) if m else None


def evaluer_maturite(chemin):
    """Evalue la maturite d'un contenu markdown (0 a 15)."""
    try:
        with open(chemin, encoding="utf-8") as f:
            contenu = f.read()
    except (OSError, UnicodeDecodeError):
        return 0

    lignes = contenu.split("\n")
    maturite = 0
    nb_lignes = len(lignes)
    nb_sections = len(re.findall(r"^## ", contenu, flags=re.MULTILINE))
    nb_liens = len(re.findall(r"\[.*\]\(.*\)", contenu))

    # 1. Nombre de lignes
    if nb_lignes > 50:
        maturite += 3
    elif nb_lignes > 20:
        maturite += 2
    elif nb_lignes > 10:
        maturite += 1

    # 2. Presence de frontmatter
    if lignes and lignes[0].strip().startswith("---"):
        maturite += 1

    # 3. Nombre de sections
    if nb_sections > 5:
        maturite += 3
    elif nb_sections > 3:
        maturite += 2
    elif nb_sections > 1:
        maturite += 1

    # 4. Presence de tableaux
    if re.search(r"^\|.*\|", contenu, flags=re.MULTILINE):
        maturite += 1

    # 5. Presence de code
    if "```" in contenu:
        maturite += 1

    # 6. Presence de listes
    if re.search(r"^- ", contenu, flags=re.MULTILINE):
        maturite += 1

    # 7. Liens internes
    if nb_liens > 5:
        maturite += 2
    elif nb_liens > 2:
        maturite += 1

    return maturite


def statut_recommande(maturite):
    """Determine le statut recommande selon la maturite."""
    if maturite >= 10:
        return "valide"
    if maturite >= 7:
        return "test"
    if maturite >= 5:
        return "dev"
    if maturite >= 3:
        return "prepare"
    return "ebauche"


def analyser_fichier(chemin, verbose):
    """Analyse un fichier et retourne (erreur, infos) ou (None, None)."""
    statut_actuel = extraire_statut(chemin)
    if not statut_actuel:
        return None, None
    maturite = evaluer_maturite(chemin)
    statut_recom = statut_recommande(maturite)
    ordre_actuel = ORDRE.get(statut_actuel, 0)
    ordre_recom = ORDRE.get(statut_recom, 0)

    if ordre_recom > ordre_actuel:
        erreur = "sous-statut"
    elif ordre_recom < ordre_actuel:
        erreur = "sur-statut"
    else:
        erreur = "aucune"

    if erreur == "aucune":
        return None, None

    return erreur, {
        "nom": os.path.basename(chemin),
        "statut_actuel": statut_actuel,
        "maturite": maturite,
        "statut_recom": statut_recom,
    }


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="detecter-erreur-statut.py",
        description="Detecte les fichiers dont le statut ne correspond pas a leur contenu.",
        add_help=False,
    )
    parser.add_argument("dossier", nargs="?", default=".",
                        help="Dossier a analyser (defaut: .)")
    parser.add_argument("--statut", choices=STATUTS, default=None,
                        help="Filtrer par statut (ebauche, prepare, dev, test, valide)")
    parser.add_argument("--verbose", action="store_true",
                        help="Afficher les details")
    parser.add_argument("--version", action="store_true",
                        help="Afficher la version")
    parser.add_argument("--aide", "-h", action="store_true",
                        help="Afficher cette aide")
    return parser


def main(argv=None):
    args = construire_parser().parse_args(argv)

    if args.aide:
        construire_parser().print_help()
        return 0
    if args.version:
        print("detecter-erreur-statut.py v" + VERSION + " (" + STATUT + ")")
        return 0

    dossier = args.dossier
    if not os.path.isdir(dossier):
        print(RED + "[ERREUR] Dossier non trouve : " + dossier + NC)
        return 2

    erreurs_totales = 0
    fichiers_analyses = 0

    print(BLUE + "=== Detection des erreurs de statut ===" + NC)
    print("Dossier : " + dossier)
    if args.statut:
        print("Filtre : " + args.statut)
    print("")

    for racine, _, fichiers in os.walk(dossier):
        for nom in sorted(fichiers):
            if not nom.endswith(".md"):
                continue
            chemin = os.path.join(racine, nom)
            fstatut = extraire_statut(chemin)
            if not fstatut:
                continue
            if args.statut and fstatut != args.statut:
                continue
            fichiers_analyses += 1
            erreur, infos = analyser_fichier(chemin, args.verbose)
            if erreur:
                erreurs_totales += 1
                print(RED + "[ERREUR] " + infos["nom"] + NC)
                print("   Statut actuel : " + infos["statut_actuel"])
                print("   Maturite : " + str(infos["maturite"]) + "/15")
                print("   Statut recommande : " + infos["statut_recom"])
                print(YELLOW + "   -> Devrait etre au statut '" +
                      infos["statut_recom"] + "'" + NC)
                print("")

    print(BLUE + "=== Resume ===" + NC)
    print("Fichiers analyses : " + str(fichiers_analyses))
    print("Erreurs detectees : " + str(erreurs_totales))

    if erreurs_totales == 0:
        print("")
        print(GREEN + "[OK] Aucune erreur de statut detectee" + NC)
        return 0
    else:
        print("")
        print(RED + "[ERREUR] " + str(erreurs_totales) +
              " erreur(s) de statut detectee(s)" + NC)
        return 1


if __name__ == "__main__":
    sys.exit(main())
