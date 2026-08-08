#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
valider-cartes-decision.py

Verifie que les agents respectent leur CARTE DE DECISION. Depuis la v0.2.0
(allegement des fiches), la carte de decision d'un agent est son PARCOURS JSON
(agents/<agent>/parcours/parcours-<agent>.json) : c'est la SOURCE DE VERITE du
guidage. Cet outil valide la structure et les references d'un parcours.

Validations d'un parcours :
  1. Le fichier parcours-<agent>.json existe
  2. Le JSON est valide (json.load)
  3. Structure : cles top-level identite + parcours + cases presentes
  4. parcours.case_depart existe et designe une case reelle
  5. Chaque case a un type valide (question/indice/controle/fin)
  6. References valides : suivant et vers des branches pointent vers des cases
  7. La case c0 est une question de relecture honnete (Pattern 4, spec v0.2.9)

Utilisation:
  valider-cartes-decision.py --agent <nom>
  valider-cartes-decision.py --tous
  valider-cartes-decision.py --fichier <chemin.json>

Proprietaire : Vulcain (outil partage)
Version : 0.3.0
Statut : prepare
"""

import io
import json
import os
import sys

VERSION = "0.3.0"
STATUT = "prepare"

AGENTS_DIR = "cerveau-projet/agents"
TYPES_VALIDES = ("question", "indice", "controle", "fin")


def afficher_aide():
    print("=== valider-cartes-decision v%s ===" % VERSION)
    print("")
    print("Verifie la carte de decision d'un agent = son PARCOURS JSON (source de verite).")
    print("")
    print("Usage: valider-cartes-decision.py [options]")
    print("")
    print("Options:")
    print("  --agent <nom>          Verifier le parcours d'un agent specifique")
    print("  --tous                 Verifier les parcours de tous les agents")
    print("  --fichier <chemin>     Verifier un fichier parcours JSON specifique")
    print("  --aide                 Afficher cette aide")
    print("")
    print("Exemples:")
    print("  valider-cartes-decision.py --agent buffy")
    print("  valider-cartes-decision.py --tous")
    print("  valider-cartes-decision.py --fichier cerveau-projet/agents/buffy/parcours/parcours-buffy.json")


def lister_agents():
    """Tous les dossiers agents qui ont un dossier parcours/."""
    agents = []
    if not os.path.isdir(AGENTS_DIR):
        return agents
    for nom in sorted(os.listdir(AGENTS_DIR)):
        dossier = os.path.join(AGENTS_DIR, nom)
        if os.path.isdir(dossier) and os.path.isdir(os.path.join(dossier, "parcours")):
            agents.append(nom)
    return agents


def chemin_parcours_agent(agent):
    return os.path.join(AGENTS_DIR, agent, "parcours", "parcours-" + agent + ".json")


def valider_parcours(contenu, nom_display):
    """Valide un parcours JSON. Retourne 0 si conforme, 1 sinon."""
    print("=== Verification %s ===" % nom_display)
    print("")

    try:
        donnees = json.loads(contenu)
    except ValueError as e:
        print("1. JSON valide")
        print("   [ERREUR] JSON invalide : %s" % e)
        print("")
        print("=== Resultat : NON CONFORME ===")
        return 1

    erreurs = []
    controles_ok = []

    # 1. JSON valide
    controles_ok.append("1. JSON valide")
    print("1. JSON valide")
    print("   [OK] JSON parse sans erreur")

    # 2. Structure : identite + parcours + cases
    manquantes = [c for c in ("identite", "parcours", "cases") if c not in donnees]
    print("2. Structure (identite + parcours + cases)")
    if manquantes:
        print("   [ERREUR] Cles manquantes : %s" % ", ".join(manquantes))
        erreurs.append("structure")
    else:
        controles_ok.append("2. Structure (identite + parcours + cases)")
        print("   [OK] Cles top-level presentes")
        identite = donnees["identite"]
        if identite.get("type") != "parcours":
            print("   [ERREUR] identite.type doit etre 'parcours' (trouve: %s)"
                  % identite.get("type"))
            erreurs.append("identite.type")
        else:
            print("   [OK] identite.type = parcours")

    # 3. case_depart
    print("3. Case de depart (case_depart)")
    parcours = donnees.get("parcours", {})
    cases = donnees.get("cases", {})
    case_depart = parcours.get("case_depart")
    if not case_depart:
        print("   [ERREUR] parcours.case_depart manquante")
        erreurs.append("case_depart")
    elif case_depart not in cases:
        print("   [ERREUR] case_depart '%s' introuvable dans cases" % case_depart)
        erreurs.append("case_depart")
    else:
        controles_ok.append("3. Case de depart (case_depart)")
        print("   [OK] case_depart '%s' existe" % case_depart)

    # 4. Types de cases valides
    print("4. Types de cases (question/indice/controle/fin)")
    types_invalides = []
    for cid, case in cases.items():
        typ = case.get("type")
        if typ not in TYPES_VALIDES:
            types_invalides.append("%s:%s" % (cid, typ))
    if types_invalides:
        print("   [ERREUR] Types invalides : %s" % ", ".join(types_invalides[:5]))
        erreurs.append("types")
    else:
        controles_ok.append("4. Types de cases")
        print("   [OK] %d cases, tous types valides" % len(cases))

    # 5. References valides (suivant + vers des branches)
    print("5. References (suivant + branches.vers)")
    refs_cassees = []
    for cid, case in cases.items():
        suivant = case.get("suivant")
        if suivant and suivant not in cases:
            refs_cassees.append("%s.suivant->%s" % (cid, suivant))
        for b in case.get("branches") or []:
            vers = b.get("vers")
            if vers and vers not in cases:
                refs_cassees.append("%s.branche->%s" % (cid, vers))
    if refs_cassees:
        print("   [ERREUR] References cassees : %s" % ", ".join(refs_cassees[:5]))
        erreurs.append("references")
    else:
        controles_ok.append("5. References")
        print("   [OK] Toutes les references pointent vers des cases existantes")

    # 6. Case c0 = question de relecture honnete (Pattern 4)
    print("6. Case c0 de relecture honnete (Pattern 4)")
    c0 = cases.get("c0")
    if c0 is None:
        print("   [ERREUR] Case c0 absente")
        erreurs.append("c0")
    elif c0.get("type") != "question":
        print("   [ERREUR] c0 doit etre de type question (relecture)")
        erreurs.append("c0")
    else:
        question = (c0.get("question") or "").lower()
        if "memoire" not in question:
            print("   [ATTENTION] c0 est une question mais ne semble pas poser la question de relecture")
        controles_ok.append("6. Case c0 de relecture")
        print("   [OK] c0 est une question de relecture")

    print("")
    if erreurs:
        print("=== Resultat : NON CONFORME (%d erreur(s)) ===" % len(erreurs))
        return 1
    print("=== Resultat : CONFORME ===")
    return 0


def verifier_parcours_fichier(chemin, nom_display):
    """Verifie un fichier parcours JSON (ou signale qu'une fiche .md n'est plus la cible)."""
    if not os.path.isfile(chemin):
        print("=== Verification %s : %s ===" % (nom_display, chemin))
        print("")
        print("ERREUR : Le fichier %s n'existe pas" % chemin)
        return 1

    if chemin.endswith(".md"):
        print("=== Verification %s : %s ===" % (nom_display, chemin))
        print("")
        print("NOTE : la carte de decision ne vit plus dans la fiche .md")
        print("(allegement v0.2.0). La SOURCE DE VERITE est le parcours JSON :")
        print("  agents/<agent>/parcours/parcours-<agent>.json")
        print("Utiliser --agent <nom> ou --fichier <parcours.json>.")
        print("")
        print("=== Resultat : NON CONFORME (mauvaise cible) ===")
        return 1

    try:
        with io.open(chemin, encoding="utf-8") as fh:
            contenu = fh.read()
    except Exception:
        print("=== Verification %s : %s ===" % (nom_display, chemin))
        print("")
        print("ERREUR : Impossible de lire le fichier %s" % chemin)
        return 1

    return valider_parcours(contenu, nom_display)


def verifier_agent(agent):
    chemin = chemin_parcours_agent(agent)
    return verifier_parcours_fichier(chemin, "de l'agent %s" % agent)


def verifier_tous():
    print("=== Verification de tous les agents ===")
    print("")

    agents = lister_agents()
    conformes = 0
    total = 0

    for agent in agents:
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
        return verifier_parcours_fichier(argv[1], "du fichier")

    print("ERREUR : Option inconnue '%s'" % argv[0])
    afficher_aide()
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
