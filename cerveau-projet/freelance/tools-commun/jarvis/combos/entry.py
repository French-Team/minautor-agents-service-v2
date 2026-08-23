#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: jarvis
#   commun: false
"""
entry.py

POINT D'ENTREE des combos JARVIS (P1 : orchestrateur, aucune logique metier).
Chaque combo vit dans fonctions/ (une tache par fonction).

Usage :
  python3 entry.py <ETAT|CHERCHE|RAPPELLE|RESUME|?> [besoin...]
  python3 entry.py aide

Protocole Stark->JARVIS : objet 'JARVIS <COMMANDE> [args]'
Contrat   : combos/protocole-placeholder.md

Proprietaire : Vision (perimetre JARVIS)
Version : 0.4.0
"""

import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
sys.path.insert(0, os.path.join(BASE, "fonctions"))

from fonctions.etat import combo_etat
from fonctions.cherche import combo_cherche
from fonctions.rappelle import combo_rappelle
from fonctions.resume import combo_resume
from fonctions.question_libre import combo_question_libre

VERSION = "0.4.0"


def dispatch(combo, besoin):
    """Router le combo vers SA fonction (une tache par module)."""
    if combo == "ETAT":
        return combo_etat(besoin)
    if combo == "CHERCHE":
        return combo_cherche(besoin)
    if combo == "RAPPELLE":
        return combo_rappelle(besoin)
    if combo == "RESUME":
        return combo_resume(besoin)
    if combo in ("?", "QUESTION"):
        return combo_question_libre(besoin)
    return None


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("aide", "--help", "-h"):
        print("combos JARVIS v%s - point d'entree unique (P1)" % VERSION)
        print("Usage: entry.py <ETAT|CHERCHE|RAPPELLE|RESUME|?> [besoin...]")
        print("Protocole Stark->JARVIS : objet 'JARVIS <COMMANDE> [args]'")
        return 0
    import json
    resultat = dispatch(args[0].upper(),
                        " ".join(args[1:]) if len(args) > 1 else "(non precise)")
    if resultat is None:
        print("ERREUR: combo inconnu '%s'. Combos: ETAT CHERCHE RAPPELLE RESUME ?"
              % args[0].upper())
        return 1
    print(json.dumps(resultat, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
