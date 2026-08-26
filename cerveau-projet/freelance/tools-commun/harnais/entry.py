#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""entry.py - Harnais v2 : verifier un outil ou un script temporaire.

Usage:
  python3 entry.py outil <chemin_outil> [--agent A]
  python3 entry.py script <chemin_script> [--agent A] [--type test]
  python3 entry.py aide
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "fonctions"))
from harnais import (verifier_outil, verifier_script, executer_script,
                     signal, VERSION)


def main():
    p = argparse.ArgumentParser(prog="harnais-v2",
                                description="Harnais v2 (conformite outils + scripts temporaires)")
    sub = p.add_subparsers(dest="cmd")

    po = sub.add_parser("outil", help="Verifier la conformite d un outil v2")
    po.add_argument("chemin_outil")
    po.add_argument("--agent", default="")

    ps = sub.add_parser("script", help="Proteger un script temporaire")
    ps.add_argument("chemin_script")
    ps.add_argument("--agent", default="", help="Agent qui execute (OBLIGATOIRE - config verifications)")
    ps.add_argument("--raison", default="", help="Raison/mission (OBLIGATOIRE - config verifications)")
    ps.add_argument("--type", default="test")

    pe = sub.add_parser("exec", help="Executer un script temporaire (AVANT -> PENDANT -> APRES)")
    pe.add_argument("chemin_script")
    pe.add_argument("--agent", default="", help="Agent qui execute (OBLIGATOIRE)")
    pe.add_argument("--raison", default="", help="Raison/mission (OBLIGATOIRE)")
    pe.add_argument("--timeout", type=int, default=60, help="Timeout d execution (s)")

    sub.add_parser("aide", help="Aide + signaux")

    args = p.parse_args()
    if not args.cmd:
        p.print_help()
        return 0

    if args.cmd == "outil":
        rc = verifier_outil(args.chemin_outil, agent=args.agent)
        print("")
        print("== Harnais v2 (outil) : rc=%d %s ==" % (rc, "CONFORME" if rc == 0 else "A TRAITER"))
        return rc
    elif args.cmd == "script":
        rc = verifier_script(args.chemin_script, agent=args.agent,
                             raison=getattr(args, "raison", ""),
                             type_script=args.type)
        print("")
        print("== Harnais v2 (script) : rc=%d %s ==" % (rc, "PROTEGE" if rc == 0 else "A TRAITER"))
        return rc
    elif args.cmd == "exec":
        rc = executer_script(args.chemin_script, agent=args.agent,
                             raison=getattr(args, "raison", ""),
                             timeout=args.timeout)
        print("")
        print("== Harnais v2 (exec) : rc=%d %s ==" % (rc, "REUSSI" if rc == 0 else "ECHEC"))
        return rc
    elif args.cmd == "aide":
        print("Harnais v2 v%s" % VERSION)
        print("Signaux :")
        for niveau, info in [("OK", "[SIG OK] tout est conforme - continue"),
                             ("WARN", "[SIG WARN] anomalie mineure - continue mais signale"),
                             ("ERR", "[SIG ERR] erreur - STOPPE et corrige"),
                             ("CRIT", "[SIG CRIT] critique - arret immediat")]:
            print("  %s %s" % (niveau, info))
        print("")
        print("Commandes :")
        print("  harnais outil <chemin_outil>   # conformite d un outil v2")
        print("  harnais script <chemin>        # protection script temporaire")
    return 0


if __name__ == "__main__":
    sys.exit(main())