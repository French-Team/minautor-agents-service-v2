"""Categorie verifier : orchestre les 3 controles du marbre protocoles.

Interface entre main.py et les fonctions simples (verifier/fonctions.py).
"""
from verifier.fonctions import executer_verification


def executer(arguments):
    print("== verifier-protocoles ==")
    total = executer_verification()
    if total:
        print("Resultat : " + str(total) + " ecart(s).")
        return 1
    print("Resultat : aucun ecart. Marbre protocoles conforme.")
    return 0
