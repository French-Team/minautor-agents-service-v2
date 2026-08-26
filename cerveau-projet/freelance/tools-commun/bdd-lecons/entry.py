#!/usr/bin/env python3
# -*- coding: ascii -*-
"""entry.py - bdd-lecons v2 (BDD SQLite, D10) : interface CLI directe.

Sous-commandes :
  enregistrer <resume> --agent <nom> [--categorie C] [--mots-cles csv] [--source S]
  lister [--n N]
  chercher [--mot-cle M] [--categorie C] [--agent A]
  compter

La BDD est le SEUL stockage des lecons v2 : les agents n ecrivent plus
leurs lecons dans corrections.md, ils les enregistrent ici (id auto,
date auto, titre auto).
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "fonctions"))
from bdd_lecons import (enregistrer, lister, chercher, compter, CATEGORIES)

# HARNAIS (PROTOCOLE 21) : chaque outil v2 s auto-verifie en debut de
# traitement. Le harnais emet un signal OK/WARN/ERR/CRIT et guide l agent.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "harnais", "fonctions"))
try:
    from harnais import verifier_outil
    _CHEMIN_OUTIL = os.path.dirname(os.path.abspath(__file__))
except ImportError:
    verifier_outil = None


def main():
    p = argparse.ArgumentParser(prog="bdd-lecons",
                                description="BDD des lecons v2 (D10, bible)")
    sub = p.add_subparsers(dest="cmd")

    pe = sub.add_parser("enregistrer")
    pe.add_argument("resume")
    pe.add_argument("--agent", required=True)
    pe.add_argument("--categorie", default="correction",
                    choices=list(CATEGORIES))
    pe.add_argument("--mots-cles", default="")
    pe.add_argument("--source", default="bdd-lecons")

    pl = sub.add_parser("lister")
    pl.add_argument("--n", type=int, default=20)

    pc = sub.add_parser("chercher")
    pc.add_argument("--mot-cle", default="")
    pc.add_argument("--categorie", default="")
    pc.add_argument("--agent", default="")

    sub.add_parser("compter")

    args = p.parse_args()
    if verifier_outil is not None and args.cmd not in (None,):
        verifier_outil(_CHEMIN_OUTIL, agent="bdd-lecons")
    if not args.cmd:
        p.print_help()
        return 0

    if args.cmd == "enregistrer":
        lecon = enregistrer(agent=args.agent, resume=args.resume,
                            categorie=args.categorie,
                            mots_cles=args.mots_cles, source=args.source)
        print("[bdd-lecons] LECON ENREGISTREE : id=%s, categorie=%s, "
              "titre=%s" % (lecon["id"], lecon["categorie"], lecon["titre"]))
    elif args.cmd == "lister":
        print(json.dumps(lister(args.n), ensure_ascii=False, indent=1))
    elif args.cmd == "chercher":
        print(json.dumps(chercher(mot_cle=args.mot_cle,
                                  categorie=args.categorie,
                                  agent=args.agent),
                         ensure_ascii=False, indent=1))
    elif args.cmd == "compter":
        print("[bdd-lecons] %s lecon(s) en BDD" % compter())
    return 0


if __name__ == "__main__":
    sys.exit(main())
