"""Categorie tour : orchestre UNE passe de la vigie-portes.

Interface entre main.py et les fonctions simples (tour/fonctions.py).
"""
from pathlib import Path

from constants import REPERTOIRE_MATRIX
from tour.fonctions import executer_tour


def extraire_racine(arguments):
    """Racine matrix/ a controler (--racine <chemin>) ; defaut : celle du depot.

    --racine existe pour pouvoir PIEUGER le controle (lecon L-032 : un controle
    qu'on ne peut pas pieger ne prouve rien). C'est aussi ce qui permet de faire
    tourner la vigie sur un arbre cobaye sans toucher aux vraies donnees.
    """
    for index, morceau in enumerate(arguments):
        if morceau == "--racine" and index + 1 < len(arguments):
            return Path(arguments[index + 1]).resolve()
    return REPERTOIRE_MATRIX


def executer(arguments):
    """Lance la passe. --sans-signal = passe a BLANC.

    Une vigie doit pouvoir etre REGARDEE avant de tirer (premier lancement,
    diagnostic, essai sur un cobaye) : dans ce mode elle affiche et journalise
    mais ne depose RIEN dans l'inbox de la Matrice.
    """
    return executer_tour(extraire_racine(arguments), signaler_actif="--sans-signal" not in arguments)
