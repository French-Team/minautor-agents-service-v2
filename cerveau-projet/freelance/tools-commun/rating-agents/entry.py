#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
entry.py - POINT D'ENTREE de rating-agents (P1 : orchestrateur).

Systeme de notation des agents v2 : paliers vers le HAUT (performance)
et vers le BAS (problemes a reparer). Le rating sert a IDENTIFIER quel
agent a des problemes pour qu'il soit REPARE.

Paliers :
  hausse : COPPER -> SILVER -> OR
  baisse : A_REVOIR -> A_REPARER -> DECLASSE

Usage :
  python3 entry.py noter --agent <agent> --palier <palier> --motif "..." [--par X]
  python3 entry.py lister [--agent <agent>]
  python3 entry.py problemes

Proprietaire : Forge
Version : 0.1.0
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "fonctions"))

from noter import noter, lister, problemes, palier_actuel
from paliers import NOTATEURS, HAUSSE, BAISSE

VERSION = "0.1.0"


def main():
    parser = argparse.ArgumentParser(description="rating-agents v%s" % VERSION)
    sub = parser.add_subparsers(dest="action")

    p_n = sub.add_parser("noter", help="Noter un agent (hausse ou baisse)")
    p_n.add_argument("--agent", required=True)
    p_n.add_argument("--palier", required=True,
                     help="OR/SILVER/COPPER ou A_REVOIR/A_REPARER/DECLASSE")
    p_n.add_argument("--motif", required=True)
    p_n.add_argument("--par", default="stark", help="Notateur")

    p_l = sub.add_parser("lister", help="Lister les notes")
    p_l.add_argument("--agent", default=None)

    sub.add_parser("problemes", help="Agents en palier de baisse")

    args = parser.parse_args()
    if args.action == "noter":
        if args.par not in NOTATEURS:
            print("ERREUR: '%s' n'est pas un notateur habilite (%s)"
                  % (args.par, ", ".join(NOTATEURS)))
            return 1
        entree, erreur = noter(args.agent, args.palier.upper(), args.motif,
                               args.par)
        if erreur:
            print("ERREUR:", erreur)
            return 1
        print("[RATING] %s note par %s : %s -> %s"
              % (entree["agent"], entree["par"], entree["palier_avant"],
                 entree["palier_apres"]))
        if entree["sens"] == "BAISSE":
            print("  ACTION REQUISE : agent a reparer "
                  "(A_REVOIR=education, A_REPARER/DECLASSE=mission de reparation)")
        return 0
    if args.action == "lister":
        for e in lister(args.agent):
            print("[%s] %s %s->%s par %s : %s"
                  % (e["date"][:10], e["agent"], e["palier_avant"],
                     e["palier_apres"], e["par"], e["motif"][:60]))
        return 0
    if args.action == "problemes":
        probs = problemes()
        if not probs:
            print("Aucun agent en palier de baisse.")
            return 0
        print("%d agent(s) a reparer :" % len(probs))
        for e in probs:
            print("  %s [%s] motif: %s" % (e["agent"], e["palier_apres"],
                                           e["motif"][:70]))
        return 1  # code non-zero = il y a du travail
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
