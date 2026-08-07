#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
valider-numerotation.py

Verifie que les tableaux d'etapes de mission des fiches agents
n'ont pas de doublons de numerotation (etape X x2).

Utilisation:
  valider-numerotation.py [OPTIONS] [FICHIER|DOSSIER]

Arguments:
  [FICHIER]  Verifier un fichier fiche agent (ex: buffy.md)
  [DOSSIER]  Verifier toutes les fiches d'un dossier (defaut: agents/)

Options:
  --agent <nom>   Verifier un seul agent (ex: --agent buffy)
  --verbose       Afficher les missions sans doublon
  --help          Afficher cette aide

Proprietaire : Vulcain (outil partage)
Version : 0.2.0-py
Statut : prepare
"""

import io
import os
import re
import sys

VERSION = "0.2.0-py"
STATUT = "prepare"

# Racine du projet : 5 niveaux au-dessus de ce script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.normpath(os.path.join(SCRIPT_DIR, "../../../../.."))

# Dossier par defaut : les fiches agents
DOSSIER_DEFAUT = os.path.join(RACINE, "cerveau-projet", "agents")

PATTERN_MISSION = re.compile(r"^### Mission : (.+)$")
PATTERN_NOUVELLE_SECTION = re.compile(r"^#{2,3} ")
PATTERN_TABLEAU_ETAPES = re.compile(r"^\| Etape \|")
PATTERN_LIGNE_ETAPE = re.compile(r"^\|\s*\*{0,2}([0-9]+)\*{0,2}\s*\|")


def afficher_aide():
    print("=== valider-numerotation v%s ===" % VERSION)
    print("")
    print("Verifie que les tableaux d'etapes de mission des fiches agents")
    print("n'ont pas de doublons de numerotation (etape X x2).")
    print("")
    print("Usage: valider-numerotation.py [OPTIONS] [FICHIER|DOSSIER]")
    print("")
    print("Arguments :")
    print("  [FICHIER]  Verifier un fichier fiche agent (ex: buffy.md)")
    print("  [DOSSIER]  Verifier toutes les fiches d'un dossier (defaut: agents/)")
    print("")
    print("Options :")
    print("  --agent <nom>   Verifier un seul agent (ex: --agent buffy)")
    print("  --verbose       Afficher les missions sans doublon")
    print("  --help          Afficher cette aide")
    print("")
    print("Exemples :")
    print("  valider-numerotation.py                         # Toutes les fiches agents")
    print("  valider-numerotation.py --agent buffy           # La fiche de Buffy")
    print("  valider-numerotation.py chemin/vers/fiche.md    # Une fiche precise")


def analyser_fichier(f):
    """Retourne la liste des doublons d'etapes dans un fichier fiche agent."""
    try:
        c = io.open(f, encoding="utf-8").read()
    except Exception:
        return ["fichier illisible: " + f]

    lignes = c.split("\n")
    in_mission = False
    mission = None
    in_etapes_table = False
    numeros = []
    doublons = []

    def finaliser():
        nonlocal in_mission, mission, in_etapes_table, numeros
        if in_mission and numeros:
            for num in sorted(set([n for n in numeros if numeros.count(n) > 1])):
                doublons.append(mission + " : etape " + num + " x" + str(numeros.count(num)))
        in_mission = False
        mission = None
        in_etapes_table = False
        numeros = []

    for l in lignes:
        m = PATTERN_MISSION.match(l)
        if m:
            finaliser()
            mission = m.group(1)
            in_mission = True
            in_etapes_table = False
            numeros = []
            continue
        if in_mission:
            if PATTERN_NOUVELLE_SECTION.match(l):
                finaliser()
                continue
            if PATTERN_TABLEAU_ETAPES.match(l):
                in_etapes_table = True
                continue
            m2 = PATTERN_LIGNE_ETAPE.match(l)
            if m2 and in_etapes_table:
                numeros.append(m2.group(1))
                continue
            if in_etapes_table and not l.strip().startswith("|"):
                in_etapes_table = False

    finaliser()
    return doublons


def lister_fiches(cible):
    """Retourne la liste des fichiers fiche agent a analyser."""
    if os.path.isfile(cible):
        return [cible]

    fichiers = []
    nom_dossier = os.path.basename(os.path.normpath(cible))
    fiche_directe = os.path.join(cible, nom_dossier + ".md")
    if os.path.isfile(fiche_directe):
        fichiers.append(fiche_directe)

    try:
        entrees = sorted(os.listdir(cible))
    except OSError:
        return fichiers

    for d in entrees:
        chemin = os.path.join(cible, d)
        if os.path.isdir(chemin):
            fiche = os.path.join(chemin, d + ".md")
            if os.path.isfile(fiche):
                fichiers.append(fiche)
    return fichiers


def main(argv):
    cible = DOSSIER_DEFAUT
    verbose = False

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--agent":
            if i + 1 < len(argv):
                cible = os.path.join(DOSSIER_DEFAUT, argv[i + 1])
                i += 1
        elif arg == "--verbose":
            verbose = True
        elif arg in ("--help", "-h"):
            afficher_aide()
            return 0
        elif arg == "--version":
            print("valider-numerotation v%s (%s)" % (VERSION, STATUT))
            return 0
        elif arg.startswith("-"):
            print("[ERREUR] Option inconnue : %s" % arg)
            afficher_aide()
            return 1
        else:
            cible = arg
        i += 1

    print("=== valider-numerotation v%s ===" % VERSION)
    print("Cible : %s" % cible)
    print("")

    if not os.path.exists(cible):
        print("[ERREUR] Le chemin n'existe pas : %s" % cible)
        return 1

    fiches = lister_fiches(cible)
    total_doublons = 0
    for f in fiches:
        doublons = analyser_fichier(f)
        if doublons:
            nom = os.path.basename(f)
            print("[DOUBLON] %s" % nom)
            for d in doublons:
                print("    - %s" % d)
            total_doublons += len(doublons)
        else:
            print("[OK] %s" % os.path.basename(f))

    print("---")
    print("Fichiers analyses : %d | Doublons detectes : %d" % (len(fiches), total_doublons))

    if total_doublons > 0:
        print("=== Resultat : DOUBLONS DETECTES ===")
        return 1
    print("=== Resultat : CONFORME (aucun doublon) ===")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
