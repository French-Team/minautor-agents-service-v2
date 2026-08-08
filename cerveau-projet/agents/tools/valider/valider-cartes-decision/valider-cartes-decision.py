#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
valider-cartes-decision.py

Outil pour verifier que les agents respectent les cartes de decision :
section CARTE DE DECISION, tableau des missions, details des missions,
regles absolues.

Utilisation:
  valider-cartes-decision.py --agent <nom>
  valider-cartes-decision.py --tous
  valider-cartes-decision.py --fichier <chemin>

Proprietaire : Vulcain (outil partage)
Version : 0.2.0-py
Statut : prepare
"""

import io
import os
import sys

VERSION = "0.2.0-py"
STATUT = "prepare"

AGENTS_DIR = "cerveau-projet/agents"

AGENTS_DEFAUT = ["cerberus", "buffy", "atlas", "janus", "vulcain"]

CLE_SECTION = "CARTE DE DECISION"
CLE_TABLEAU = "Missions disponibles"
CLE_DETAILS = "Mission :"
CLE_REGLES = "REGLE ABSOLUE"


def afficher_aide():
    print("=== valider-cartes-decision v%s ===" % VERSION)
    print("")
    print("Usage: valider-cartes-decision.py [options]")
    print("")
    print("Options:")
    print("  --agent <nom>          Verifier un agent specifique")
    print("  --tous                 Verifier tous les agents")
    print("  --fichier <chemin>     Verifier un fichier specifique")
    print("  --aide                 Afficher cette aide")
    print("")
    print("Exemples:")
    print("  valider-cartes-decision.py --agent Buffy")
    print("  valider-cartes-decision.py --tous")
    print("  valider-cartes-decision.py --fichier cerveau-projet/agents/buffy/buffy.md")


def verifier_fichier(fichier, nom_display):
    """Verifier qu'un fichier contient les elements d'une carte de decision."""
    print("=== Verification %s : %s ===" % (nom_display, fichier))
    print("")

    if not os.path.isfile(fichier):
        print("ERREUR : Le fichier %s n'existe pas" % fichier)
        return 1

    try:
        with io.open(fichier, encoding="utf-8") as fh:
            contenu = fh.read()
    except Exception:
        print("ERREUR : Impossible de lire le fichier %s" % fichier)
        return 1

    controles = [
        ("1. Section Carte de Decision", CLE_SECTION, "Section presente", "Section manquante"),
        ("2. Tableau des missions", CLE_TABLEAU, "Tableau present", "Tableau manquant"),
        ("3. Details des missions", CLE_DETAILS, "Details presents", "Details manquants"),
        ("4. Regles absolues", CLE_REGLES, "Regles presentes", "Regles manquantes"),
    ]

    for titre, cle, ok_msg, err_msg in controles:
        print(titre)
        if cle in contenu:
            print("   [OK] %s" % ok_msg)
        else:
            print("   [ERREUR] %s" % err_msg)
            print("")
            print("=== Resultat : NON CONFORME ===")
            return 1

    print("")
    print("=== Resultat : CONFORME ===")
    return 0


def verifier_agent(agent):
    fichier = os.path.join(AGENTS_DIR, agent, agent + ".md")
    return verifier_fichier(fichier, "de l'agent %s" % agent)


def verifier_tous():
    print("=== Verification de tous les agents ===")
    print("")

    conformes = 0
    total = 0

    for agent in AGENTS_DEFAUT:
        if os.path.isdir(os.path.join(AGENTS_DIR, agent)):
            total += 1
            if verifier_agent(agent) == 0:
                conformes += 1
            print("")

    print("=== Resume ===")
    print("Agents verifies : %d" % total)
    print("Agents conformes : %d" % conformes)
    print("Agents non conformes : %d" % (total - conformes))
    return 0


def main(argv):
    if not argv:
        afficher_aide()
        return 1

    if argv[0] in ("--aide", "--help", "-h"):
        afficher_aide()
        return 0

    if argv[0] == "--version":
        print("valider-cartes-decision v%s (%s)" % (VERSION, STATUT))
        return 0

    if argv[0] == "--agent":
        if len(argv) < 2:
            print("ERREUR : Nom de l'agent manquant")
            afficher_aide()
            return 1
        return verifier_agent(argv[1])

    if argv[0] == "--tous":
        return verifier_tous()

    if argv[0] == "--fichier":
        if len(argv) < 2:
            print("ERREUR : Chemin du fichier manquant")
            afficher_aide()
            return 1
        return verifier_fichier(argv[1], "du fichier")

    print("ERREUR : Option inconnue '%s'" % argv[0])
    afficher_aide()
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
