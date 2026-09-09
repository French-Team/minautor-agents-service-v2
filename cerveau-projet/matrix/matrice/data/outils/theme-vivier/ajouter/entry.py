"""Categorie ajouter : orchestre l'enregistrement d'un theme.

Interface entre main.py et les fonctions simples (ajouter/fonctions.py).
"""
from commun import charger_bdd, enregistrer_bdd, extraire_options
from constants import CATEGORIES
from ajouter.fonctions import ajouter_theme

NOMS_OPTIONS = ("nom", "but", "description", "categorie")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    nom = options.get("nom", "")
    but = options.get("but", "")
    description = options.get("description", "")
    categorie = options.get("categorie", "").upper()

    if not nom or not but or not categorie:
        print('Usage : python main.py ajouter --nom "NOM" --categorie <'
              + "|".join(CATEGORIES) + '> --but "..." [--description "..."]')
        return 2
    if categorie not in CATEGORIES:
        print("REFUS : categorie " + repr(categorie) + " hors liste fermee : " + ", ".join(CATEGORIES))
        return 1

    donnees = charger_bdd()
    entree, doublon = ajouter_theme(donnees, nom, but, description, categorie)
    if doublon:
        print("ECART : un theme porte deja ce nom (unicite du nom, casse ignoree).")
        return 2
    empreinte = enregistrer_bdd(donnees)
    print(
        "Theme " + entree["id"] + " (" + entree["nom"] + ") enregistre -- empreinte : "
        + empreinte[:16] + "..."
    )
    return 0
