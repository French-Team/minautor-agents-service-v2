#!/usr/bin/env python3
"""entry.py - horloge (P1 : orchestrateur)."""
import argparse, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonctions"))
from horloge import maintenant, date_fichier, date_tableau, heure_historique

# HARNAIS (PROTOCOLE 21) : l outil s auto-verifie en debut de traitement.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "harnais", "fonctions"))
try:
    from harnais import verifier_outil
    _CHEMIN_OUTIL = os.path.dirname(os.path.abspath(__file__))
except ImportError:
    verifier_outil = None

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("format", choices=["message", "fichier", "tableau", "historique"])
    a = p.parse_args()
    if verifier_outil is not None:
        verifier_outil(_CHEMIN_OUTIL, agent="horloge")
    print({"message": maintenant, "fichier": date_fichier,
           "tableau": date_tableau, "historique": heure_historique}[a.format]())
