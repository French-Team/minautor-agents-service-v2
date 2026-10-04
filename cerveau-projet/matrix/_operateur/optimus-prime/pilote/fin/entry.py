"""Categorie fin : orchestre la cloture de la mission en cours.

Interface entre main.py et les fonctions simples (fin/fonctions.py).
"""
from commun import (charger_file, extraire_options, lire_bilan, lire_defauts,
                    lire_segments)
from constants import OPTION_DEFAUTS, OPTION_SEGMENT
from fin.fonctions import cloturer_mission

# --bilan : le texte direct (defaut). --bilan-fichier : le MEME recit, lu dans un
# fichier (EO-132) -- un argument traverse le shell, ou un accent grave EXECUTE du
# shell et disparait de la trace : mesure reelle, deux bilans troues (MO-142,
# MO-143), la friction declaree ponctuelle s'etant revelee RECURRENTE (friction 71).
# --defauts-fichier (R5, audit MO-174) : les DEFAUTS d'outil rencontres EN
# TRAVAILLANT, en JSONL STRUCTURE -- un objet par defaut, champs FERMES. Lus
# dans un FICHIER, pour la meme raison que le bilan (EO-132) : un argument
# traverse le shell, ou un accent grave EXECUTE du shell et disparait.
# --segment-fichier (MO-500, option C de l audit MO-499) : LE SEGMENT DE RAISONNEMENT
# du round -- un objet JSON par ligne, champs FERMES (`segment`, `tags` -- la
# `source` est posee par la CLOTURE, jamais par l agent). Lu dans un FICHIER, comme
# le bilan et les defauts. Son ABSENCE n'est pas une erreur : c'est le cas < NON >,
# que la cloture DIT (le silence est impossible).
NOMS_OPTIONS = ("bilan", "bilan-fichier", OPTION_DEFAUTS, OPTION_SEGMENT)


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    code, bilan, message = lire_bilan(options)
    if code != 0:
        print("REFUS : " + message)
        return 2
    if not bilan:
        print('Usage : python main.py fin --bilan "..." | --bilan-fichier <chemin>')
        print("        [--defauts-fichier <chemin.jsonl>]  (defauts d'OUTIL, R5)")
        print("        [--segment-fichier <chemin.jsonl>]  (segment de raisonnement :"
              " la cloture le DEPOSE, ou le DIT -- MO-500)")
        return 2
    code, defauts, message = lire_defauts((options.get(OPTION_DEFAUTS) or "").strip())
    if code != 0:
        print("REFUS : " + message)
        return 2
    # LA DEMANDE DE SEGMENT (MO-500) : lue AVANT la cloture, comme le bilan et les
    # defauts -- un fichier mal forme est REFUSE avant toute mutation.
    code, segments, message = lire_segments((options.get(OPTION_SEGMENT) or "").strip())
    if code != 0:
        print("REFUS : " + message)
        return 2
    return cloturer_mission(charger_file, bilan, defauts, segments)
