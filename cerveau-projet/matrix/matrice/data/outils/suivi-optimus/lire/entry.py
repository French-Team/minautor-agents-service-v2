"""Categorie lire : orchestre la consultation de la trace suivi-optimus.

Interface entre main.py et les fonctions simples (lire/fonctions.py).
"""
from commun import extraire_options, lire_evenements
from lire.fonctions import afficher, derniers, filtrer

NOMS_OPTIONS = ("mission", "action", "n")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    evenements = lire_evenements()
    resultats = filtrer(
        evenements, mission=options.get("mission"), action=options.get("action")
    )
    if options.get("n"):
        try:
            resultats = derniers(resultats, int(options["n"]))
        except ValueError:
            pass
    afficher(resultats)
    return 0