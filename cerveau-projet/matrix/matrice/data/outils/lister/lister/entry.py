"""Categorie lister : orchestre le listage d'un dossier.

Interface entre main.py et les fonctions simples (lister/fonctions.py).
"""
from commun import extraire_options
from lister.fonctions import executer_lister

NOMS_OPTIONS = ("dossier", "filtre", "recursif", "json")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    dossier = options.get("dossier", "")
    filtre = options.get("filtre", "")
    recursif = "recursif" in options
    as_json = "json" in options

    if not dossier:
        print("Usage : python main.py lister --dossier <chemin> [--filtre <glob>] [--recursif] [--json]")
        print("Ex : python main.py lister --dossier cerveau-projet/matrix/matrice/data/outils --recursif --filtre *.py")
        return 2
    return executer_lister(dossier, filtre, recursif, as_json)
