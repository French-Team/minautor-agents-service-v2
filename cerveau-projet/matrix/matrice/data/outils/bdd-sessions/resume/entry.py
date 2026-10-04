"""Categorie resume : interface entre main.py et resume/fonctions.py."""
from resume.fonctions import lire_derniere


def executer(arguments):
    if "--derniere" in arguments:
        return lire_derniere()
    print('Usage : python main.py resume --derniere (la derniere session, lecture bornee)')
    return 2
