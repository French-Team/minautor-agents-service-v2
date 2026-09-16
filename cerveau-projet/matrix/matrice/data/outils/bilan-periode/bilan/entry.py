"""Categorie bilan : collecte les 4 sources horodatees et presente le bilan."""
from bilan.fonctions import (
    afficher_bilan,
    collecter_activites,
    collecter_defcon,
    collecter_missions_par_source,
    collecter_usages,
)
from commun import analyser_periode, borne_periode
from constants import CHEMINS_HISTORIQUES, CHEMIN_ACTIVITES, CHEMIN_DEFCON, CHEMIN_USAGES


def executer(arguments):
    options = {}
    index = 0
    while index < len(arguments):
        if arguments[index] == "--periode" and index + 1 < len(arguments):
            options["--periode"] = arguments[index + 1]
            index += 2
        else:
            index += 1
    if "--periode" not in options:
        print('Usage : python main.py bilan --periode <1h|heures|24h|3j|semaine|mois>')
        return 2
    heures, message = analyser_periode(options["--periode"])
    if heures is None:
        print(message)
        return 2

    borne = borne_periode(heures)
    # TOUS les AVAL de missions (cameleon + optimus) : voir SOURCES_HISTORIQUES.
    missions = collecter_missions_par_source(CHEMINS_HISTORIQUES, borne)
    usages = collecter_usages(CHEMIN_USAGES, borne)
    activites = collecter_activites(CHEMIN_ACTIVITES, borne)
    transitions = collecter_defcon(CHEMIN_DEFCON, borne)
    return afficher_bilan(options["--periode"], heures, missions, usages, activites, transitions)
