"""Categorie fin : orchestre la cloture de la mission en cours.

Interface entre main.py et les fonctions simples (fin/fonctions.py).
"""
from commun import charger_file, extraire_options, lire_bilan
from fin.fonctions import cloturer_mission

# --bilan : le texte direct (defaut). --bilan-fichier : le MEME recit, lu dans un
# fichier (EO-132) -- un argument traverse le shell, ou un accent grave EXECUTE du
# shell et disparait de la trace : mesure reelle, deux bilans troues (MO-142,
# MO-143), la friction declaree ponctuelle s'etant revelee RECURRENTE (friction 71).
NOMS_OPTIONS = ("bilan", "bilan-fichier")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    code, bilan, message = lire_bilan(options)
    if code != 0:
        print("REFUS : " + message)
        return 2
    if not bilan:
        print('Usage : python main.py fin --bilan "..." | --bilan-fichier <chemin>')
        return 2
    return cloturer_mission(charger_file, bilan)
