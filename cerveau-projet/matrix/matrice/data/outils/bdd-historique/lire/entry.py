"""Categorie lire : orchestre la consultation filtree du journal global.

Interface entre main.py et les fonctions simples (lire/fonctions.py).
"""
from commun import charger_lignes, extraire_options
from lire.fonctions import afficher, filtrer

NOMS_OPTIONS = ("type", "tag", "depuis", "tout")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    lignes = charger_lignes()
    tout = "--tout" in arguments or options.get("tout") == "true"
    evenements = filtrer(
        lignes,
        options.get("type"),
        options.get("tag"),
        options.get("depuis"),
        tout,
    )
    afficher(evenements)
    return 0
