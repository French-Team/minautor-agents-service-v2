"""Categorie preparer : PREPARER la liste des outils d une mission (EO-313).

Interface entre main.py et les fonctions simples (preparer/fonctions.py).
"""
from preparer.fonctions import preparer_outils
from stockage import charger_entonnoir, enregistrer_entonnoir
from tresse.fonctions import marquer_brin, tresser


def extraire_options(arguments, noms_connus):
    """Voir le CONTRAT du domicile partage (EO-158) : options CONSOMMEES ici."""
    from options import extraire_options as repartir  # domicile partage (EO-158)
    return repartir(arguments, noms_connus)


NOMS_OPTIONS = ("id", "outils")

USAGE = ("Usage : python main.py preparer --id EO-XXX --outils <nom1,nom2,...>")
AIDE = ("  la liste est DECLAREE (jamais devinee) et VALIDEE a la pose contre le catalogue des"
        " briques que l injection sait servir : un nom non servable REFUSE l ecriture."
        " La chaine vide (--outils \"\") VIDE la liste, et le repli par TYPE s applique alors"
        " a l injection.")


def executer(arguments):
    """Pose la liste des outils sur l ITEM, puis RECOMPOSE le brin.

    Le retressage est dans le MEME geste : le brin porte des COPIES des items, donc
    une liste posee sans retressage ne serait pas celle que le pont enverrait a la
    mission (meme raison que retiqueter, MO-213 -- sans lui, la tete du brin
    porterait l ancienne liste, donc l ancien comportement).
    """
    options = extraire_options(arguments, NOMS_OPTIONS)
    identifiant = options.get("id", "")
    sans_valeur = list(options.get("__sans_valeur__") or [])
    if not identifiant or "--outils" not in arguments or "outils" in sans_valeur:
        print(USAGE)
        print(AIDE)
        if "outils" in sans_valeur:
            print("  REFUS : --outils attend une valeur -- une liste, ou la chaine vide pour"
                  " VIDER (une option privee de valeur n est jamais avalee en silence).")
        return 2
    etat = charger_entonnoir()
    code, message = preparer_outils(etat, identifiant, options.get("outils", ""))
    if code != 0:
        if message:
            print(message)
        return code
    etat["brin"] = marquer_brin(tresser(etat.get("files", {})))
    enregistrer_entonnoir(etat)
    print(message)
    print("Brin recompose : " + str(len(etat["brin"])) + " mission(s).")
    return 0
