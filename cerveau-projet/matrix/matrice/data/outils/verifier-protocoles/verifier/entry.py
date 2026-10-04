"""Categorie verifier : orchestre les 3 controles du marbre protocoles.

Interface entre main.py et les fonctions simples (verifier/fonctions.py).
"""
from verifier.fonctions import executer_verification

USAGE = "Usage : python main.py verifier"
# Ce VERBE ne declare AUCUNE option : le domicile refuse donc tout --xxx et le
# NOMME (T2 de PB-002). Avant, la liste d arguments etait ignoree en entier --
# une option fautive disparaissait et le scan rendait son resultat comme si de
# rien n etait (L-055 : un defaut muet se lit comme un fait).
OPTIONS = ()


def executer(arguments):
    from options import extraire_options
    extraire_options(arguments, OPTIONS, outil="verifier-protocoles", usage=USAGE)
    print("== verifier-protocoles ==")
    total = executer_verification()
    if total:
        print("Resultat : " + str(total) + " ecart(s).")
        return 1
    print("Resultat : aucun ecart. Marbre protocoles conforme.")
    return 0
