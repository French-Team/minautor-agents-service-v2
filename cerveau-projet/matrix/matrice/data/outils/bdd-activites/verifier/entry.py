"""Categorie verifier : integrite structurelle + empreinte des activites-recentes.

Interface entre main.py et les fonctions simples (verifier/fonctions.py).
"""
from commun import calculer_empreinte_si_existe, charger_bdd, lire_empreinte
from constants import CHEMIN_BDD
from verifier.fonctions import verifier_structure


def executer(arguments):
    donnees = charger_bdd()
    succes, message = verifier_structure(donnees)
    if not succes:
        print(message)
        return 1
    empreinte_enregistree = lire_empreinte()
    empreinte_reelle = calculer_empreinte_si_existe(CHEMIN_BDD)
    if empreinte_enregistree is None or empreinte_reelle is None:
        print("Verifier : BDD absente ou sans etalon (jamais encore ecrite par la porte unique).")
        return 1
    if empreinte_reelle != empreinte_enregistree:
        print("ECART D'INTEGRITE : empreinte reelle differente de l'etalon (fichier modifie hors porte unique).")
        return 1
    print(message + " Empreinte OK (" + empreinte_reelle[:16] + "...).")
    return 0
