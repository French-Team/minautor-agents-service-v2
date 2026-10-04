"""Categorie marquer-obsolete : appose le marquage obsolete SUR AJOUT.

Interface entre main.py et les fonctions simples (obsolete/fonctions.py).
"""
from commun import ajouter_ligne, charger_lignes, extraire_options
from noter.fonctions import prochain_id
from obsolete.fonctions import deja_obsolete, fabriquer_marqueur, id_existe

NOMS_OPTIONS = ("id", "motif")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    cible = options.get("id", "")
    motif = options.get("motif", "")

    if not cible:
        print('Usage : python main.py marquer-obsolete --id H-XXX [--motif "..."]')
        return 2

    lignes = charger_lignes()
    if not id_existe(lignes, cible):
        print("Identifiant inconnu : " + cible + " (aucun evenement ne porte cet id).")
        return 2
    if deja_obsolete(lignes, cible):
        print("Deja obsolete : " + cible + " est deja vise par un marquage.")
        return 2

    marqueur = fabriquer_marqueur(prochain_id(lignes), cible, motif)
    ajouter_ligne(marqueur)
    print("Marquage " + marqueur["id"] + " appose : " + cible + " devient obsolete (sur ajout, entree originale intacte).")
    return 0
