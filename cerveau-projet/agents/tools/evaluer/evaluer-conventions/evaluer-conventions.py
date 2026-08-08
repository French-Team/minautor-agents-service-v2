#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
evaluer-conventions.py
Evalue le respect des conventions : nommage, ASCII, format.

Produit un rapport markdown sur stdout avec un score /100.

Usage:
  evaluer-conventions.py [DOSSIER]

Retour: 0 toujours (outil d'evaluation, rapport sur stdout).

Proprietaire : Themis (outil partage)
Version : 0.2.0-py
Statut : beta
"""

import argparse
import os
import sys

VERSION = "0.2.0-py"
STATUT = "beta"

# Couleurs ANSI
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
NC = "\033[0m"  # No Color


def verifier_nommage(nom_script):
    """Refuse l'execution si le script est renomme (protection du nommage)."""
    attendu = "evaluer-conventions.py"
    if nom_script != attendu:
        print(RED + "[ERREUR] Nom de fichier invalide : " + nom_script + NC)
        print(YELLOW + "  Attendu : " + attendu + NC)
        sys.exit(2)


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="evaluer-conventions.py",
        description="Evalue le respect des conventions.",
        add_help=False,
    )
    parser.add_argument("dossier", nargs="?", default=".",
                        help="Racine du projet (defaut: .)")
    parser.add_argument("--version", action="store_true",
                        help="Afficher la version")
    parser.add_argument("--aide", "-h", action="store_true",
                        help="Afficher cette aide")
    return parser


def est_ascii(chaine):
    """True si tous les caracteres sont ASCII."""
    return all(ord(c) < 128 for c in chaine)


def main(argv=None):
    verifier_nommage(os.path.basename(sys.argv[0]))
    args = construire_parser().parse_args(argv)

    if args.aide:
        construire_parser().print_help()
        return 0
    if args.version:
        print("evaluer-conventions.py v" + VERSION + " (" + STATUT + ")")
        return 0

    dossier = args.dossier
    print("=== evaluer-conventions v" + VERSION + " ===")
    print("Cible : " + dossier)
    print("")

    if not os.path.isdir(dossier):
        print(RED + "[ERREUR] Le dossier n'existe pas : " + dossier + NC)
        return 1

    total = 0
    ok = 0
    erreurs = 0
    avertissements = 0

    print("# Rapport evaluer-conventions")
    print("")

    cerveau = os.path.join(dossier, "cerveau-projet")

    # 1. Nommage des fichiers de contenu (statuts)
    print("## Nommage des statuts")
    total += 1
    nb_bad = 0
    if os.path.isdir(cerveau):
        for base, _, fichiers in os.walk(cerveau):
            for nom in fichiers:
                if nom.endswith(".md") and not est_ascii(nom):
                    nb_bad += 1
    if nb_bad > 0:
        print("| ERREUR | Fichiers avec accents dans les statuts | " +
              str(nb_bad) +
              " fichier(s) avec des caracteres non-ASCII dans le nom (ex: .prepare-accentue.) |")
        erreurs += 1
    else:
        print("| OK | Fichiers avec accents dans les statuts | Aucun accent dans les noms de fichiers |")
        ok += 1

    # 2. Conformite ASCII (hors exceptions)
    print("")
    print("## Conformite ASCII (hors exceptions)")
    total += 1
    nb_non_ascii = 0
    if os.path.isdir(cerveau):
        for base, _, fichiers in os.walk(cerveau):
            base_norm = base.replace("\\", "/")
            if "/exemples/" in base_norm + "/":
                continue
            for nom in fichiers:
                if not (nom.endswith(".md") or nom.endswith(".sh")):
                    continue
                if nom.startswith("dictionnaire-") and nom.endswith(".txt"):
                    continue
                if nom == "regles-emojis-ascii.md":
                    continue
                chemin = os.path.join(base, nom)
                try:
                    with open(chemin, encoding="utf-8", errors="replace") as f:
                        contenu = f.read()
                    if not est_ascii(contenu):
                        nb_non_ascii += 1
                except (OSError, IOError):
                    continue
    if nb_non_ascii > 0:
        print("| AVERTISSEMENT | Fichiers avec caracteres non-ASCII | " +
              str(nb_non_ascii) + " fichier(s) restant(s) |")
        avertissements += 1
    else:
        print("| OK | Fichiers avec caracteres non-ASCII | Tous conformes |")
        ok += 1

    # 3. Bandeau EXCEPTION VOLONTAIRE
    print("")
    print("## Bandeaux EXCEPTION VOLONTAIRE")
    total += 1
    dictionnaires_ok = 0
    if os.path.isdir(cerveau):
        for base, _, fichiers in os.walk(cerveau):
            for nom in fichiers:
                if nom.startswith("dictionnaire-") and nom.endswith(".txt"):
                    chemin = os.path.join(base, nom)
                    with open(chemin, encoding="utf-8", errors="replace") as f:
                        contenu = f.read()
                    if "EXCEPTION VOLONTAIRE" in contenu:
                        dictionnaires_ok += 1
                    else:
                        print("| ERREUR | Bandeau manquant | `" + chemin + "` |")
                        erreurs += 1
    if dictionnaires_ok > 0:
        print("| OK | Bandeaux dictionnaires | " + str(dictionnaires_ok) +
              " dictionnaire(s) avec bandeau |")
        ok += 1

    # 4. Dossier exemples exclu des outils
    print("")
    print("## Exclusion du dossier exemples")
    total += 1
    chemins_exclusion = [
        os.path.join(cerveau, "agents", "tools", "valider",
                     "valider-conformite-ascii", "valider-conformite-ascii.sh"),
        os.path.join(cerveau, "agents", "tools", "rechercher",
                     "rechercher-accents-sensibles", "rechercher-accents-sensibles.sh"),
        os.path.join(cerveau, "agents", "tools", "corriger",
                     "corriger-emojis", "corriger-emojis.sh"),
    ]
    exclus = 0
    for chemin in chemins_exclusion:
        try:
            with open(chemin, encoding="utf-8", errors="replace") as f:
                if "exemples" in f.read():
                    exclus += 1
        except (OSError, IOError):
            continue
    if exclus == 3:
        print("| OK | Exclusion exemples | 3 outils sur 3 excluent le dossier |")
        ok += 1
    else:
        print("| ERREUR | Exclusion exemples | Un ou plusieurs outils n'excluent pas exemples |")
        erreurs += 1

    # 5. Format des fichiers agents (.md presents)
    print("")
    print("## Format des fichiers agents")
    total += 1
    agents_dir = os.path.join(cerveau, "agents")
    agents_avec_fiche = 0
    agents_sans_fiche = []
    if os.path.isdir(agents_dir):
        for nom in sorted(os.listdir(agents_dir)):
            chemin = os.path.join(agents_dir, nom)
            if not os.path.isdir(chemin) or nom == "tools":
                continue
            if os.path.isfile(os.path.join(chemin, nom + ".md")):
                agents_avec_fiche += 1
            else:
                agents_sans_fiche.append(nom)
    if not agents_sans_fiche:
        print("| OK | Fiches agents | " + str(agents_avec_fiche) +
              " agent(s) avec fiche |")
        ok += 1
    else:
        print("| ERREUR | Fiches agents | Agents sans fiche :" +
              " ".join(agents_sans_fiche) + " |")
        erreurs += 1

    # Resume
    print("")
    print("## Resume")
    print("")
    print("- Total elements verifies : " + str(total))
    print("- OK : " + str(ok))
    print("- Erreurs : " + str(erreurs))
    print("- Avertissements : " + str(avertissements))
    print("")
    score = (ok * 100 // total) if total > 0 else 0
    print("Score conventions : " + str(score) + "/100")

    return 0


if __name__ == "__main__":
    sys.exit(main())
