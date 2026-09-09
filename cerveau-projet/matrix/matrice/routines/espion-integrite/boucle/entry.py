"""Categorie boucle : orchestre la veille en arriere-plan et l'arret propre.

Interface entre main.py et les fonctions simples (boucle/fonctions.py).
"""
from boucle.fonctions import arret_demande, demarrer_boucle, poser_drapeau_arret
from constants import INTERVALLE_DEFAUT_SECONDES


def executer(arguments):
    if arret_demande(arguments):
        return poser_drapeau_arret()

    intervalle = INTERVALLE_DEFAUT_SECONDES
    for index, morceau in enumerate(arguments):
        if morceau == "--interval" and index + 1 < len(arguments):
            intervalle = int(arguments[index + 1])

    return demarrer_boucle(intervalle)
