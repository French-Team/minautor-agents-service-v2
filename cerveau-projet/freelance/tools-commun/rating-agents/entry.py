#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
entry.py - POINT D'ENTREE de rating-agents (P1 : orchestrateur).

Score numerique sur 100 : depart 50, penalite -1, felicitation +1.
Le score sert a IDENTIFIER les agents a problemes pour qu'ils soient REPARES.

Usage :
  python3 entry.py penalite  --agent <a> --motif "..." [--par X]
  python3 entry.py felicite  --agent <a> --motif "..." [--par X]
  python3 entry.py lister    [--agent <a>]
  python3 entry.py problemes [--seuil N]

Proprietaire : Forge
Version : 0.2.0
"""

import argparse
import sys

import os as _os
sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
                                 "fonctions"))

from score import enregistrer, evenements, score, problemes, \
    NOTATEURS, SCORE_DEPART

VERSION = "0.2.0"


def main():
    parser = argparse.ArgumentParser(description="rating-agents v%s" % VERSION)
    sub = parser.add_subparsers(dest="action")

    p_p = sub.add_parser("penalite", help="Penaliser un agent (-1)")
    p_p.add_argument("--agent", required=True)
    p_p.add_argument("--motif", required=True)
    p_p.add_argument("--par", default="stark")

    p_f = sub.add_parser("felicite", help="Feliciter un agent (+1)")
    p_f.add_argument("--agent", required=True)
    p_f.add_argument("--motif", required=True)
    p_f.add_argument("--par", default="stark")

    p_l = sub.add_parser("lister", help="Scores et historique")
    p_l.add_argument("--agent", default=None)

    p_pr = sub.add_parser("problemes", help="Agents sous le seuil (a reparer)")
    p_pr.add_argument("--seuil", type=int, default=None)

    args = parser.parse_args()

    if args.action in ("penalite", "felicite"):
        if args.par not in NOTATEURS:
            print("ERREUR: '%s' n'est pas notateur habilite (%s)"
                  % (args.par, ", ".join(NOTATEURS)))
            return 1
        entree, erreur = enregistrer(args.action, args.agent, args.motif,
                                     args.par)
        if erreur:
            print("ERREUR:", erreur)
            return 1
        signe = "-" if entree["delta"] < 0 else "+"
        print("[RATING] %s : %d %s%d -> %d (%s par %s)"
              % (entree["agent"], entree["score_avant"], signe,
                 abs(entree["delta"]), entree["score_apres"],
                 entree["type"], entree["par"]))
        return 0
    if args.action == "lister":
        agents = sorted(set(e["agent"] for e in evenements()))
        if args.agent:
            agents = [args.agent] if args.agent in agents or True else []
            events = evenements(args.agent)
            print("%s : score %d/100" % (args.agent, score(args.agent)))
            for e in events:
                signe = "-" if e["delta"] < 0 else "+"
                print("  [%s] %s%d -> %d : %s (%s)"
                      % (e["date"][:10], signe and "" or "", e["delta"],
                         e["score_apres"], e["motif"][:60], e["type"]))
            return 0
        for a in agents:
            print("%s : %d/100" % (a, score(a)))
        return 0
    if args.action == "problemes":
        probs = problemes(args.seuil)
        if not probs:
            print("Aucun agent sous le seuil de problemes.")
            return 0
        print("%d agent(s) a reparer :" % len(probs))
        for a, s in probs:
            print("  %s : %d/100" % (a, s))
        return 1
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
