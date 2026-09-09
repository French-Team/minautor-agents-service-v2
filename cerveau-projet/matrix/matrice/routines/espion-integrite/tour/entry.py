"""Categorie tour : orchestre UNE passe de surveillance.

Interface entre main.py et les fonctions simples (tour/fonctions.py).
Retourne 0 si rien a signaler, 1 si au moins un ECART.
"""
from constants import BDDS
from commun import journaliser
from tour.fonctions import surveiller_bdd

CHAPITRE_INTEGRITE = 1
CHAPITRE_PRESENCE = 2


def executer(arguments):
    ecarts = []
    for nom_bdd, faite in BDDS.items():
        constat = surveiller_bdd(nom_bdd, faite, CHAPITRE_INTEGRITE, CHAPITRE_PRESENCE)
        if constat["etat"] == "ECART":
            ecarts.append(nom_bdd)

    journaliser(
        {
            "type": "passe",
            "chapitres": [CHAPITRE_INTEGRITE, CHAPITRE_PRESENCE],
            "bdds_surveillees": len(BDDS),
            "ecarts": ecarts,
        }
    )
    if ecarts:
        print("ECARTS detectes : " + ", ".join(ecarts))
        return 1
    print("Passe complete : aucune alerte.")
    return 0
