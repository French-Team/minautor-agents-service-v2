"""Categorie lire : orchestre la consultation des activites-recentes.

Interface entre main.py et les fonctions simples (lire/fonctions.py).
"""
from commun import charger_bdd, extraire_options
from lire.fonctions import afficher, filtrer

NOMS_OPTIONS = ("section", "tag")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    donnees = charger_bdd()
    couples = filtrer(donnees, options.get("section"), options.get("tag"))
    afficher(couples)
    return 0
