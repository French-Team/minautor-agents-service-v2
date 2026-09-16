"""Categorie verifier : scan seul des ecarts ASCII (capacite de conversion affichee).

Interface entre main.py et les fonctions simples (verifier/fonctions.py).
"""
from corriger.fonctions import resumer_exemptions
from verifier.fonctions import executer_verification


def executer(arguments):
    print("== corriger-ascii : verifier (scan seul) ==")
    total = executer_verification()
    # Les EXEMPTES sont RAPPORTES : un fichier hors du champ de reecriture est un
    # angle mort mesure, et un angle mort tu est un angle mort qu'on croit couvert.
    for ligne in resumer_exemptions():
        print(ligne)
    return 1 if total else 0
