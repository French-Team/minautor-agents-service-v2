#!/usr/bin/env python3
# -*- coding: ascii -*-
"""entry.py - harnais-jarvis : harnais de COMPORTEMENT du serveur JARVIS.

Sous-commandes :
  verifier  detecte les ecarts de comportement ET alerte Vision (inbox)
  sante     detecte SANS alerter (consultation)
  journal   affiche les alertes deja envoyees (dedup)
  aide      rappel d usage

Le harnais scanne les files JARVIS en lecture seule, applique les regles
de harnais-jarvis-data.json (D15) et alerte le destinataire (vision) --
le seul habilite a modifier JARVIS.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "fonctions"))
from harnais_jarvis import (verifier_comportement, rapport,
                            JOURNAL_PATH, VERSION)

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
    p = argparse.ArgumentParser(prog="harnais-jarvis",
                                description="Harnais de comportement JARVIS")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("verifier")
    sub.add_parser("sante")
    sub.add_parser("journal")
    sub.add_parser("aide")
    args = p.parse_args()
    if verifier_outil is not None and args.cmd not in (None,):
        verifier_outil(_CHEMIN_OUTIL, agent="harnais-jarvis")
    if not args.cmd or args.cmd == "aide":
        p.print_help()
        return 0

    if args.cmd == "verifier":
        ecarts, nouveaux = verifier_comportement(alerter=True)
        print("=== HARNAIS-JARVIS v%s : COMPORTEMENT ===" % VERSION)
        for ligne in rapport(ecarts):
            print("  %s" % ligne)
        print("---")
        print("%d ecart(s) detecte(s), %d nouveau(x) alerte(s) a Vision"
              % (len(ecarts), len(nouveaux)))
    elif args.cmd == "sante":
        ecarts, _ = verifier_comportement(alerter=False)
        print("=== HARNAIS-JARVIS v%s : SANTE (sans alerte) ===" % VERSION)
        for ligne in rapport(ecarts):
            print("  %s" % ligne)
    elif args.cmd == "journal":
        print("=== ALERTES DEJA ENVOYEES (dedup) ===")
        if not os.path.isfile(JOURNAL_PATH):
            print("  (aucune alerte)")
            return 0
        with open(JOURNAL_PATH, encoding="utf-8") as fh:
            lignes = [json.loads(l) for l in fh if l.strip()]
        for e in lignes[-20:]:
            print("  %s [%s] %s (%s)" % (e["date"], e["severite"],
                                         e["type"], e["cle"][:50]))
        print("  --- %d alerte(s) au total ---" % len(lignes))
    return 0


if __name__ == "__main__":
    sys.exit(main())
