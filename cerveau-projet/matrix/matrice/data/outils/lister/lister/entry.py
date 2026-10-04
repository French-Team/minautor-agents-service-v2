"""Categorie lister : orchestre le listage d'un dossier.

Interface entre main.py et les fonctions simples (lister/fonctions.py).
"""
from commun import extraire_options
from lister.fonctions import executer_lister

# --prive : la TRAPPE d ouverture des zones invisibles L-016, reservee a la
# Matrice (MO-152 : le listage etait ferme EN DUR -- inclure_invisible=False --
# donc la Matrice elle-meme ne pouvait plus lister une zone exclue).
NOMS_OPTIONS = ("dossier", "filtre", "recursif", "json", "prive")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    dossier = options.get("dossier", "")
    filtre = options.get("filtre", "")
    recursif = "recursif" in options
    as_json = "json" in options
    inclure_prive = "prive" in options

    if not dossier:
        print("Usage : python main.py lister --dossier <chemin> [--filtre <glob>] [--recursif] [--json]")
        print("Ex : python main.py lister --dossier cerveau-projet/matrix/matrice/data/outils --recursif --filtre *.py")
        print("       --prive : ouvre les zones invisibles L-016 (Matrice seule)")
        return 2
    return executer_lister(dossier, filtre, recursif, as_json, inclure_prive)
