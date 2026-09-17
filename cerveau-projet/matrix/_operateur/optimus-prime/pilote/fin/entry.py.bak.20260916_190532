"""Categorie fin : orchestre la cloture de la mission en cours.

Interface entre main.py et les fonctions simples (fin/fonctions.py).
"""
from commun import charger_file, extraire_options
from fin.fonctions import cloturer_mission

NOMS_OPTIONS = ("bilan",)


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    bilan = options.get("bilan", "")
    if not bilan:
        print('Usage : python main.py fin --bilan "..."')
        return 2
    return cloturer_mission(charger_file, bilan)
