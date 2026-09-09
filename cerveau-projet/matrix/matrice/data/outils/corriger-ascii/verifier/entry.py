"""Categorie verifier : scan seul des ecarts ASCII (capacite de conversion affichee).

Interface entre main.py et les fonctions simples (verifier/fonctions.py).
"""
from verifier.fonctions import executer_verification


def executer(arguments):
    print("== corriger-ascii : verifier (scan seul) ==")
    total = executer_verification()
    return 1 if total else 0
