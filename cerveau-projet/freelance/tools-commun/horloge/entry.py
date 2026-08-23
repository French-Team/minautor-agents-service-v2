#!/usr/bin/env python3
"""entry.py - horloge (P1 : orchestrateur)."""
import argparse, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonctions"))
from horloge import maintenant, date_fichier, date_tableau, heure_historique

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("format", choices=["message", "fichier", "tableau", "historique"])
    a = p.parse_args()
    print({"message": maintenant, "fichier": date_fichier,
           "tableau": date_tableau, "historique": heure_historique}[a.format]())
