#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
valider-relecture.py

Verifie que chaque fiche d'agent et son corrections.md contiennent
la regle de relecture, a chaque activation.

Utilisation:
  valider-relecture.py [OPTIONS]

Options :
  --agent <nom>     Verifier un seul agent
  --verbose         Afficher la ligne ou la regle a ete trouvee
  --help            Afficher cette aide

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

BASE_AGENTS = "cerveau-projet/agents"

# Mots-cles acceptes pour la regle de relecture dans UNE fiche d'agent
PATTERN_FICHE = re.compile(
    r"RELECTURE|relis MA fiche|relire sa fiche|sa fiche et SES corrections|"
    r"MA fiche et MES corrections",
    re.IGNORECASE
)

# Mots-cles acceptes pour la regle de relecture dans corrections.md
PATTERN_CORRECTIONS = re.compile(
    r"Relire sa fiche|relecture|relis MA fiche",
    re.IGNORECASE
)


def afficher_aide():
    print("=== valider-relecture v%s ===" % VERSION)
    print("")
    print("Verifie que chaque agent porte la regle de relecture de sa fiche")
    print("(fiche [agent].md + corrections.md), a chaque activation.")
    print("")
    print("Usage: valider-relecture.py [OPTIONS]")
    print("")
    print("Options :")
    print("  --agent <nom>     Verifier un seul agent")
    print("  --verbose         Afficher la ligne ou la regle a ete trouvee")
    print("  --help            Afficher cette aide")
    print("")
    print("Exemples :")
    print("  valider-relecture.py                          # Verifier tous les agents")
    print("  valider-relecture.py --agent buffy            # Verifier uniquement Buffy")
    print("  valider-relecture.py --verbose                # Avec le detail des regles trouvees")


def lire_contenu(fichier):
    try:
        with io.open(fichier, encoding="utf-8") as fh:
            return fh.read()
    except Exception:
        return ""


def ligne_regle(contenu, pattern):
    for i, l in enumerate(contenu.split("\n"), 1):
        if pattern.search(l):
            return i
    return 0


def verifier_agent(agent, verbose):
    base = os.path.join(BASE_AGENTS, agent)
    fiche = os.path.join(base, agent + ".md")
    corrections = os.path.join(base, "corrections.md")

    if not os.path.isfile(fiche):
        print("[MANQUE] %s : fiche absente (%s)" % (agent, fiche))
        return 1
    if not os.path.isfile(corrections):
        print("[MANQUE] %s : corrections absentes (%s)" % (agent, corrections))
        return 1

    c_fiche = lire_contenu(fiche)
    c_corr = lire_contenu(corrections)

    ok_fiche = bool(PATTERN_FICHE.search(c_fiche))
    ok_corr = bool(PATTERN_CORRECTIONS.search(c_corr))

    if ok_fiche and ok_corr:
        print("[OK] %s : fiche + corrections" % agent)
        if verbose:
            lf = ligne_regle(c_fiche, PATTERN_FICHE)
            lc = ligne_regle(c_corr, PATTERN_CORRECTIONS)
            print("      fiche: ligne %d | corrections: ligne %d" % (lf, lc))
        return 0

    print("[MANQUE] %s : fiche=%s corrections=%s" % (
        agent, "OK" if ok_fiche else "KO", "OK" if ok_corr else "KO"))
    if verbose:
        if not ok_fiche:
            print("      fiche: regle de relecture absente")
        if not ok_corr:
            print("      corrections: regle de relecture absente")
    return 1


def executer(agent_filtre, verbose):
    print("=== valider-relecture ===")
    if agent_filtre:
        print("Agent : %s" % agent_filtre)
    else:
        print("Agents : tous (dossier agents/)")
    print("")

    total = 0
    conformes = 0

    if agent_filtre:
        total = 1
        if verifier_agent(agent_filtre, verbose) == 0:
            conformes = 1
    else:
        if os.path.isdir(BASE_AGENTS):
            for nom in sorted(os.listdir(BASE_AGENTS)):
                chemin = os.path.join(BASE_AGENTS, nom)
                if not os.path.isdir(chemin):
                    continue
                if nom == "tools":
                    continue
                total += 1
                if verifier_agent(nom, verbose) == 0:
                    conformes += 1

    print("")
    print("=== Resume ===")
    print("Agents verifies : %d" % total)
    print("Conformes : %d" % conformes)

    if conformes == total:
        print("")
        print("[OK] Tous les agents portent la regle de relecture")
        return 0
    print("")
    print("[ERREUR] %d agent(s) sans regle de relecture complete" % (total - conformes))
    return 1


def main(argv):
    agent_filtre = ""
    verbose = False

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--agent":
            if i + 1 < len(argv):
                agent_filtre = argv[i + 1]
                i += 1
        elif arg == "--verbose":
            verbose = True
        elif arg in ("--help", "-h"):
            afficher_aide()
            return 0
        elif arg == "--version":
            print("valider-relecture v%s (%s)" % (VERSION, STATUT))
            return 0
        else:
            print("[ERREUR] Option inconnue : %s" % arg)
            afficher_aide()
            return 1
        i += 1

    return executer(agent_filtre, verbose)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
