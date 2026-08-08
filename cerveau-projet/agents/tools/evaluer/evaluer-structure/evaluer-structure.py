#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
evaluer-structure.py
Evalue la structure du cerveau-projet : dossiers, fichiers critiques, arborescence.

Produit un rapport markdown sur stdout avec un score /100.

Usage:
  evaluer-structure.py [DOSSIER]

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

AGENTS = ["cerberus", "buffy", "athena", "atlas", "clio", "janus",
          "minerve", "morpheus", "promethee", "vulcain", "themis"]

CATEGORIES_OUTILS = [
    "ajouter", "analyser", "changer", "combos", "condenser", "copier",
    "corriger", "creer", "decomposer", "deplacer", "detecter", "ecrire",
    "editer", "evaluer", "generateurs", "gerer", "inserer", "lire",
    "lister", "mettre-a-jour", "nettoyer", "rechercher", "supprimer",
    "valider", "verifier", "tester",
]


def verifier_nommage(nom_script):
    """Refuse l'execution si le script est renomme (protection du nommage)."""
    attendu = "evaluer-structure.py"
    if nom_script != attendu:
        print(RED + "[ERREUR] Nom de fichier invalide : " + nom_script + NC)
        print(YELLOW + "  Attendu : " + attendu + NC)
        sys.exit(2)


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="evaluer-structure.py",
        description="Evalue la structure du cerveau-projet.",
        add_help=False,
    )
    parser.add_argument("dossier", nargs="?", default=".",
                        help="Racine du projet (defaut: .)")
    parser.add_argument("--version", action="store_true",
                        help="Afficher la version")
    parser.add_argument("--aide", "-h", action="store_true",
                        help="Afficher cette aide")
    return parser


def compter_fichiers(chemin):
    """Compte les fichiers sous un dossier."""
    n = 0
    for base, _, fichiers in os.walk(chemin):
        n += len(fichiers)
    return n


def main(argv=None):
    verifier_nommage(os.path.basename(sys.argv[0]))
    args = construire_parser().parse_args(argv)

    if args.aide:
        construire_parser().print_help()
        return 0
    if args.version:
        print("evaluer-structure.py v" + VERSION + " (" + STATUT + ")")
        return 0

    dossier = args.dossier
    print("=== evaluer-structure v" + VERSION + " ===")
    print("Cible : " + dossier)
    print("")

    if not os.path.isdir(dossier):
        print(RED + "[ERREUR] Le dossier n'existe pas : " + dossier + NC)
        return 1

    total = 0
    ok = 0
    erreurs = 0
    avertissements = 0

    def evaluer(description, chemin, type_elem):
        nonlocal total, ok, erreurs
        total += 1
        present = (os.path.isfile(chemin) if type_elem == "fichier"
                   else os.path.isdir(chemin))
        if present:
            print("| OK | " + description + " | `" + chemin + "` |")
            ok += 1
        else:
            print("| ERREUR | " + description + " | `" + chemin +
                  "` MANQUANT |")
            erreurs += 1

    def evaluer_vide(description, chemin):
        nonlocal total, ok, avertissements
        if not os.path.isdir(chemin):
            return
        total += 1
        nb = compter_fichiers(chemin)
        if nb == 0:
            print("| AVERTISSEMENT | " + description + " | `" + chemin +
                  "` VIDE |")
            avertissements += 1
        else:
            print("| OK | " + description + " | `" + chemin + "` (" +
                  str(nb) + " fichiers) |")
            ok += 1

    print("# Rapport evaluer-structure")
    print("")
    print("| Statut | Description | Chemin |")
    print("|---|---|---|")

    # Dossiers critiques
    print("")
    print("## Dossiers critiques")
    cerveau = os.path.join(dossier, "cerveau-projet")
    evaluer("Point d'entree du cerveau", cerveau, "dossier")
    evaluer("Dossier agents", os.path.join(cerveau, "agents"), "dossier")
    evaluer("Dossier tools", os.path.join(cerveau, "agents", "tools"), "dossier")
    evaluer("Dossier pense-betes", os.path.join(cerveau, "pense-betes"), "dossier")
    evaluer("Dossier conventions",
            os.path.join(cerveau, "pense-betes", "conventions"), "dossier")
    evaluer("Dossier regles-immuables",
            os.path.join(cerveau, "pense-betes", "regles-immuables"), "dossier")
    evaluer("Dossier classeur-variables",
            os.path.join(cerveau, "agents", "classeur-variables"), "dossier")
    evaluer("Dossier exemples", os.path.join(cerveau, "exemples"), "dossier")

    # Fichiers critiques
    print("")
    print("## Fichiers critiques")
    evaluer("Point de demarrage", os.path.join(dossier, "demarrer.md"), "fichier")
    evaluer("Index agents", os.path.join(dossier, "AGENTS.md"), "fichier")
    evaluer("README", os.path.join(dossier, "README.md"), "fichier")
    evaluer("Index cerveau", os.path.join(cerveau, "index-cerveau.md"), "fichier")
    evaluer("Index agents (detail)",
            os.path.join(cerveau, "agents", "index-agents.md"), "fichier")
    evaluer("Template agent",
            os.path.join(cerveau, "agents", "fiche-agent-template.md"), "fichier")
    evaluer("Index regles",
            os.path.join(cerveau, "pense-betes", "regles-immuables",
                         "index-regles-immuables.md"), "fichier")
    evaluer("Regle emojis-ascii",
            os.path.join(cerveau, "pense-betes", "regles-immuables", "general",
                         "regles-emojis-ascii.md"), "fichier")
    evaluer("RVAV workflow",
            os.path.join(cerveau, "pense-betes", "regles-immuables", "general",
                         "rvav-workflow.md"), "fichier")
    evaluer("Historique agents", os.path.join(dossier, "AGENTS-historique.md"),
            "fichier")

    # Categories d'outils (par action)
    print("")
    print("## Categories d'outils")
    tools_dir = os.path.join(cerveau, "agents", "tools")
    for cat in CATEGORIES_OUTILS:
        evaluer("Categorie " + cat, os.path.join(tools_dir, cat), "dossier")

    # Dossiers agents
    print("")
    print("## Dossiers agents")
    for agent in AGENTS:
        evaluer("Agent " + agent, os.path.join(cerveau, "agents", agent),
                "dossier")

    # Contenu des dossiers outils (pas vides)
    print("")
    print("## Contenu des categories d'outils")
    for cat in CATEGORIES_OUTILS:
        evaluer_vide("Categorie " + cat, os.path.join(tools_dir, cat))

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
    print("Score structure : " + str(score) + "/100")

    return 0


if __name__ == "__main__":
    sys.exit(main())
