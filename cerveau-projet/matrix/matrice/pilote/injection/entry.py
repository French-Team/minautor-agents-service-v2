"""Categorie injection : orchestre le statut et l'injection ordonnee.

Interface entre main.py et les fonctions simples (injection/fonctions.py).
"""
from commun import charger_file
from injection.fonctions import afficher_statut, enchainer, preparer_injection


def executer(arguments):
    if arguments and arguments[0] == "statut":
        return afficher_statut(charger_file())
    if arguments and arguments[0] == "injecter":
        return preparer_injection(charger_file)
    if arguments and arguments[0] == "enchainer":
        return enchainer(charger_file)
    print('Usage : python main.py statut | python main.py injecter | python main.py enchainer')
    return 2
