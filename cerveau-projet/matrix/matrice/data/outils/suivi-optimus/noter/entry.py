"""Categorie noter : orchestre l'enregistrement d'un evenement de la trace.

Interface entre main.py et les fonctions simples (noter/fonctions.py).
"""
from commun import ajouter_ligne, extraire_options
from constants import ACTIONS
from noter.fonctions import construire_evenement, separer_liste

NOMS_OPTIONS = ("mission", "theme", "action", "detail", "fichiers", "portes", "duree-s")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    mission = options.get("mission", "")
    theme = options.get("theme", "")
    action = options.get("action", "")
    detail = options.get("detail", "")
    fichiers = separer_liste(options.get("fichiers", ""))
    portes = separer_liste(options.get("portes", ""))
    duree_s = options.get("duree-s", "")

    if not action or not detail:
        print('Usage : python main.py noter --mission M-XXX --theme SUIVI --action <action> --detail "..."')
        return 2
    if action not in ACTIONS:
        print(
            "Action inconnue : " + repr(action)
            + " (actions fermees : " + ", ".join(ACTIONS) + ")"
        )
        return 2

    evenement = construire_evenement(mission, theme, action, detail, fichiers, portes, duree_s)
    empreinte = ajouter_ligne(evenement)
    print(
        "Evenement note (action : " + action
        + ", mission : " + (mission or "-")
        + ") -- empreinte : " + empreinte[:16] + "..."
    )
    return 0