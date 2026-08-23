#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
lecteur-de-carte.py

Lecteur de carte - securite v2. Verifie si un agent est habilite a utiliser
un outil ou un combo. Les habilitations vivent dans cartes-data.json (D15).

Politique : tout agent non liste ou cible non autorisee = REFUSE.

Actions:
  verifier --agent <agent> --cible <nom> [--type outil|combo]
  lister   --agent <agent>
  aide

Proprietaire : Forge
Version : 0.1.0
Statut : actif
"""

import json
import os
import sys
from datetime import datetime

VERSION = "0.1.0"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.environ.get(
    "CARTES_DATA", os.path.join(BASE_DIR, "cartes-data.json"))


def charger_donnees():
    if not os.path.isfile(DATA_FILE):
        print("ERREUR: fichier de donnees introuvable: %s" % DATA_FILE)
        sys.exit(2)
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (ValueError, OSError) as e:
        print("ERREUR: fichier de donnees invalide: %s" % e)
        sys.exit(2)


def correspond(cible, motifs):
    """Wildcard simple : * en debut/fin de motif."""
    for motif in motifs:
        if motif == "*":
            return True
        if motif.startswith("*") and motif.endswith("*"):
            if motif.strip("*") in cible:
                return True
        elif motif.endswith("*"):
            if cible.startswith(motif[:-1]):
                return True
        elif motif == cible:
            return True
    return False


def verifier(agent, cible, type_cible):
    donnees = charger_donnees()
    carte = donnees.get("agents", {}).get(agent)
    if carte is None:
        print("REFUSE: agent '%s' sans carte (politique: %s)" % (
            agent, donnees.get("politique_defaut", "refuser")))
        return 1
    cle = "combos" if type_cible == "combo" else "outils"
    if correspond(cible, carte.get(cle, [])):
        print("ACCEDE: %s '%s' autorise pour '%s'" % (type_cible, cible, agent))
        return 0
    print("REFUSE: %s '%s' non autorise pour '%s'" % (type_cible, cible, agent))
    return 1


def lister(agent):
    donnees = charger_donnees()
    carte = donnees.get("agents", {}).get(agent)
    if carte is None:
        print("AUCUNE CARTE: '%s' n'est pas dans cartes-data.json" % agent)
        return 1
    print("Carte de '%s':" % agent)
    print("  outils : %s" % ", ".join(carte.get("outils", [])))
    print("  combos : %s" % ", ".join(carte.get("combos", [])))
    return 0


def aide():
    print("lecteur-de-carte v%s" % VERSION)
    print("Usage:")
    print("  lecteur-de-carte.py verifier --agent <agent> --cible <nom> "
          "[--type outil|combo]")
    print("  lecteur-de-carte.py lister --agent <agent>")
    print("Donnees: cartes-data.json (D15)")
    return 0


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("aide", "--help", "-h"):
        sys.exit(aide())
    action = args[0]
    opts = {"--agent": None, "--cible": None, "--type": "outil"}
    i = 1
    while i < len(args):
        if args[i] in opts and i + 1 < len(args):
            opts[args[i]] = args[i + 1]
            i += 2
        else:
            i += 1
    if action == "verifier":
        if not opts["--agent"] or not opts["--cible"]:
            print("ERREUR: --agent et --cible obligatoires")
            sys.exit(2)
        sys.exit(verifier(opts["--agent"], opts["--cible"], opts["--type"]))
    if action == "lister":
        if not opts["--agent"]:
            print("ERREUR: --agent obligatoire")
            sys.exit(2)
        sys.exit(lister(opts["--agent"]))
    print("ERREUR: action inconnue '%s'" % action)
    sys.exit(aide())


if __name__ == "__main__":
    main()
