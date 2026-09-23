"""Categorie verifier : orchestre les 3 controles du marbre conventions.

Interface entre main.py et les fonctions simples (verifier/fonctions.py).
"""
from verifier.fonctions import executer_verification


def executer(arguments):
    print("== verifier-conventions ==")
    total = executer_verification()
    if total:
        print("Resultat : " + str(total) + " ecart(s).")
        return 1
    print("Resultat : aucun ecart. Marbre conventions conforme.")
    return 0
