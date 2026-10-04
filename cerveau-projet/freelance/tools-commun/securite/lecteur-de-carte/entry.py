#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
entry.py - POINT D'ENTREE de lecteur-de-carte (P1 : orchestrateur).

La logique vit dans fonctions/coeur.py (protocole 14).
Auto-verification harnais (protocole 21) au demarrage.

Usage :
    python3 entry.py verifier --agent <agent> --cible <nom> [--type outil|combo]
    python3 entry.py lister --agent <agent>
    python3 entry.py aide

Proprietaire : Forge
Version : 0.1.0
"""

import os
import sys

_d = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _d)

# P10 : la racine se DETECTE via os_path, elle ne se compte pas
sys.path.insert(0, os.path.join(_d, "..", "..", "os_path", "fonctions"))
from racine import trouver_racine  # noqa: E402

# HARNAIS (PROTOCOLE 21) : l outil s auto-verifie en debut de traitement.
sys.path.insert(0, os.path.join(_d, "..", "..", "harnais", "fonctions"))
try:
    from harnais import verifier_outil
except ImportError:
    verifier_outil = None

sys.path.insert(0, os.path.join(_d, "fonctions"))
import coeur  # noqa: E402


if __name__ == "__main__":
    if verifier_outil is not None:
        verifier_outil(_d, agent="lecteur-de-carte")
    coeur.main()
