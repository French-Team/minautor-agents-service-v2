"""Categorie lire : orchestre la consultation du classeur-variables.

Interface entre main.py et les fonctions simples (lire/fonctions.py).
"""
from commun import charger_bdd, extraire_options
from lire.fonctions import afficher, filtrer

NOMS_OPTIONS = ("cle", "tag")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    donnees = charger_bdd()
    resultats = filtrer(donnees, options.get("cle"), options.get("tag"))
    afficher(resultats)
    return 0
