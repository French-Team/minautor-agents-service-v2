"""Categorie montrer : le CONTENU d un element de la zone, par son nom.

Interface entre main.py et la fonction simple (montrer/fonctions.py).
"""

from pathlib import Path

from commun import _options
from constants import ZONE
from montrer.fonctions import montrer

NOMS_OPTIONS = ("zone",)


def executer(arguments):
    options, positionnels, refus = _options(arguments, NOMS_OPTIONS)
    if refus:
        print(refus)
        return 2
    if len(positionnels) != 1:
        print("REFUS : montrer exige UN nom, par exemple montrer m-378-bilan.txt.")
        return 2
    zone = Path(options.get("zone") or ZONE)
    code, texte = montrer(zone, positionnels[0])
    print(texte)
    return code
