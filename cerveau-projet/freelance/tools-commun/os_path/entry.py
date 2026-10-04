#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
entry.py - POINT D'ENTREE de os_path (P1 : orchestrateur, zero logique).

os_path resout LA douleur recurrente des chemins :
- racine()     : DETECTE la racine du workspace (cherche AGENTS.md en
                 remontant) - plus jamais de "../.." comptes a la main
- resoudre()   : chemin relatif -> absolu, refus hors workspace
- localiser()  : retrouve un fichier par nom dans tout le workspace

Usage :
  python3 entry.py racine
  python3 entry.py resoudre <chemin-relatif>
  python3 entry.py existe   <chemin-relatif>
  python3 entry.py localiser <nom-fichier>

Proprietaire : Forge
Version : 0.1.0
"""

import os
import sys
# HARNAIS (PROTOCOLE 21) : l outil s auto-verifie en debut de traitement.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "harnais", "fonctions"))
try:
    from harnais import verifier_outil
    _CHEMIN_OUTIL = os.path.dirname(os.path.abspath(__file__))
except ImportError:
    verifier_outil = None

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "fonctions"))

from racine import trouver_racine
from resoudre import resoudre, existe
from localiser import localiser

VERSION = "0.1.0"


def main():
    if verifier_outil is not None:
        verifier_outil(_CHEMIN_OUTIL, agent="os-path")
    args = sys.argv[1:]
    if not args or args[0] in ("aide", "--help", "-h"):
        print("os_path v%s" % VERSION)
        print("Usage:")
        print("  entry.py racine")
        print("  entry.py resoudre <chemin-relatif>")
        print("  entry.py existe   <chemin-relatif>")
        print("  entry.py localiser <nom-fichier>")
        return 0
    action = args[0]
    if action == "racine":
        print(trouver_racine(depuis=os.path.abspath(__file__)))
        return 0
    if action in ("resoudre", "existe") and len(args) > 1:
        reel = resoudre(args[1])
        print(reel if action == "resoudre" else str(existe(args[1])))
        return 0 if reel else 1
    if action == "localiser" and len(args) > 1:
        for chemin in localiser(args[1]):
            print(chemin)
        return 0
    print("ERREUR: usage invalide (voir --help)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
