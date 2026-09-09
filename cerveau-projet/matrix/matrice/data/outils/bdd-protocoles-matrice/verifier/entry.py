"""Categorie verifier : orchestre le controle d'integrite de la BDD protocoles-matrice.json.

Interface entre main.py et les fonctions simples (verifier/fonctions.py).
"""
from commun import calculer_empreinte_si_existe, lire_empreinte
from constants import CHEMIN_BDD
from verifier.fonctions import verifier_integrite


def executer(arguments):
    empreinte_enregistree = lire_empreinte()
    empreinte_reelle = calculer_empreinte_si_existe(CHEMIN_BDD)
    succes, message = verifier_integrite(empreinte_reelle, empreinte_enregistree)
    print(message)
    return 0 if succes else 1
