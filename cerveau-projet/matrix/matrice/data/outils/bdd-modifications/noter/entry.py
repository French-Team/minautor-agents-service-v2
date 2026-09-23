"""Categorie noter : orchestre l'enregistrement d'une modification.

Interface entre main.py et les fonctions simples (noter/fonctions.py).
"""
from commun import canoniser_cle, charger_bdd, enregistrer_bdd, extraire_options
from constants import ACTIONS_PERMISES
from noter.fonctions import ajouter_modification, separer_tags, valider_action

NOMS_OPTIONS = ("fichier", "action", "detail", "tags")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    chemin_fichier = options.get("fichier", "")
    action = options.get("action", "modifie")
    detail = options.get("detail", "")
    tags = separer_tags(options.get("tags", ""))

    if not chemin_fichier or not detail:
        print('Usage : python main.py noter --fichier <chemin> --action <action> --detail "..." --tags "a,b"')
        return 2
    if not valider_action(action, ACTIONS_PERMISES):
        print("Action inconnue : " + action + " (permises : " + ", ".join(ACTIONS_PERMISES) + ")")
        return 2

    # EO-363 : la cle s ECRIT dans SA forme canonique. Une forme NON canonique se
    # DIT (elle ne se refuse pas : c est la MEME cible, dite autrement) -- et deux
    # histoires pour un seul fichier ne peuvent plus naitre.
    cle = canoniser_cle(chemin_fichier)
    if cle != chemin_fichier:
        print("CLE CANONISEE (EO-363) : " + chemin_fichier + " -> " + cle
              + " (forme relative a la racine de la Matrice)")
    chemin_fichier = cle

    donnees = charger_bdd()
    ajouter_modification(donnees, chemin_fichier, action, detail, tags)
    empreinte = enregistrer_bdd(donnees)
    print("Note enregistree pour " + chemin_fichier + " (empreinte : " + empreinte[:16] + "...)")
    return 0
