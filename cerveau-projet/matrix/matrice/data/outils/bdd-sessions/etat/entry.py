"""Categorie etat : interface entre main.py et etat/fonctions.py (MO-121).

Aucune option : l'etat est un FAIT, pas une interrogation. Le lecteur BORNE
du moteur partage fait tout le travail (L-068, M-076).
"""
from etat.fonctions import afficher_etat


def executer(arguments):
    return afficher_etat()
