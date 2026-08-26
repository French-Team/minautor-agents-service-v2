#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""entry.py - Classeur v2 (BDD SQLite) : interface CLI directe.

Sous-commandes (parite avec les sous-commandes jarvis.py) :
  variable-set <nom> <valeur> [--source S]
  variable-get <nom>
  variable-list
  session-set <session> [--id ID] [--agent AGENT]
  session-get <session>
  session-list
  agent-set <nom> [--statut S] [--mission M]
  agent-get <nom>
  agent-list
  utilisateur-set <champ> <valeur>
  utilisateur-list
  etat
  exporter
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "fonctions"))
from classeur import (variable_set, variable_get, variable_list,
                      session_set, session_get, session_list,
                      agent_set, agent_get, agent_list,
                      utilisateur_set, utilisateur_list,
                      etat_complet, exporter_json)

# HARNAIS (PROTOCOLE 21) : chaque outil v2 s auto-verifie en debut de
# traitement. Le harnais emet un signal OK/WARN/ERR/CRIT et guide l agent.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "tools-commun", "harnais", "fonctions"))
try:
    from harnais import verifier_outil
    _CHEMIN_OUTIL = os.path.dirname(os.path.abspath(__file__))
except ImportError:
    verifier_outil = None


def main():
    p = argparse.ArgumentParser(prog="classeur-v2",
                                description="Classeur v2 (BDD SQLite)")
    sub = p.add_subparsers(dest="cmd")

    pv = sub.add_parser("variable-set")
    pv.add_argument("nom")
    pv.add_argument("valeur")
    pv.add_argument("--source", default="classeur-v2")

    pg = sub.add_parser("variable-get")
    pg.add_argument("nom")

    sub.add_parser("variable-list")

    ps = sub.add_parser("session-set")
    ps.add_argument("session")
    ps.add_argument("--id", dest="id_llm", default="")
    ps.add_argument("--agent", default="")

    psg = sub.add_parser("session-get")
    psg.add_argument("session")

    sub.add_parser("session-list")

    pa = sub.add_parser("agent-set")
    pa.add_argument("nom")
    pa.add_argument("--statut", default="")
    pa.add_argument("--mission", default="")

    pag = sub.add_parser("agent-get")
    pag.add_argument("nom")

    sub.add_parser("agent-list")

    pu = sub.add_parser("utilisateur-set")
    pu.add_argument("champ")
    pu.add_argument("valeur")

    sub.add_parser("utilisateur-list")

    sub.add_parser("etat")
    sub.add_parser("exporter")

    args = p.parse_args()
    if verifier_outil is not None and args.cmd not in (None,):
        verifier_outil(_CHEMIN_OUTIL, agent="classeur-v2")
    if not args.cmd:
        p.print_help()
        return 0

    if args.cmd == "variable-set":
        variable_set(args.nom, args.valeur, source=args.source)
        print("[classeur-v2] variable %s ecrite" % args.nom)
    elif args.cmd == "variable-get":
        v = variable_get(args.nom)
        print(json.dumps(v, ensure_ascii=False) if v else "ABSENTE")
    elif args.cmd == "variable-list":
        print(json.dumps(variable_list(), ensure_ascii=False, indent=1))
    elif args.cmd == "session-set":
        session_set(args.session, id_llm=args.id_llm, agent=args.agent)
        print("[classeur-v2] session %s ecrite" % args.session)
    elif args.cmd == "session-get":
        s = session_get(args.session)
        print(json.dumps(s, ensure_ascii=False) if s else "ABSENTE")
    elif args.cmd == "session-list":
        print(json.dumps(session_list(), ensure_ascii=False, indent=1))
    elif args.cmd == "agent-set":
        agent_set(args.nom, statut=args.statut, mission=args.mission)
        print("[classeur-v2] agent %s ecrit" % args.nom)
    elif args.cmd == "agent-get":
        a = agent_get(args.nom)
        print(json.dumps(a, ensure_ascii=False) if a else "ABSENT")
    elif args.cmd == "agent-list":
        print(json.dumps(agent_list(), ensure_ascii=False, indent=1))
    elif args.cmd == "utilisateur-set":
        utilisateur_set(args.champ, args.valeur)
        print("[classeur-v2] champ utilisateur %s ecrit" % args.champ)
    elif args.cmd == "utilisateur-list":
        print(json.dumps(utilisateur_list(), ensure_ascii=False, indent=1))
    elif args.cmd == "etat":
        print(json.dumps(etat_complet(), ensure_ascii=False, indent=1))
    elif args.cmd == "exporter":
        print(json.dumps(exporter_json(), ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())