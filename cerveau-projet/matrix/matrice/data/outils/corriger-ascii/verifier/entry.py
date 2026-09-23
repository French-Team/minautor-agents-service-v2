"""Categorie verifier : scan seul des ecarts ASCII (capacite de conversion affichee).

Interface entre main.py et les fonctions simples (verifier/fonctions.py).
"""
from corriger.fonctions import resumer_exemptions
from verifier.fonctions import executer_verification

USAGE = "Usage : python main.py verifier"
# Ce VERBE ne declare AUCUNE option : le domicile refuse donc tout --xxx (T2 de
# PB-002). Avant, la liste d arguments etait ignoree en entier -- une option
# fautive disparaissait et le scan rendait son resultat comme si de rien n etait.
OPTIONS = ()


def executer(arguments):
    from options import extraire_options
    extraire_options(arguments, OPTIONS, outil="corriger-ascii", usage=USAGE)
    print("== corriger-ascii : verifier (scan seul) ==")
    total = executer_verification()
    # Les EXEMPTES sont RAPPORTES : un fichier hors du champ de reecriture est un
    # angle mort mesure, et un angle mort tu est un angle mort qu'on croit couvert.
    for ligne in resumer_exemptions():
        print(ligne)
    return 1 if total else 0
