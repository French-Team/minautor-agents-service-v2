"""Categorie verifier : controle structurel du journal global (sans empreinte).

Interface entre main.py et les fonctions simples (verifier/fonctions.py).
"""
from commun import charger_lignes
from verifier.fonctions import verifier_structure


def executer(arguments):
    lignes = charger_lignes()
    succes, message = verifier_structure(lignes)
    print(message)
    return 0 if succes else 1
