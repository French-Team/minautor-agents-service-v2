"""Categorie classer : echelons 1-2 -- ranger par TYPE puis par CATEGORIE.

Interface entre main.py et les fonctions simples (classer/fonctions.py).
"""
from stockage import charger_entonnoir, enregistrer_entonnoir
from classer.fonctions import classer_mission


def extraire_options(arguments, noms_connus):
    """Voir le CONTRAT du domicile partage (EO-158) : options CONSOMMEES ici."""
    from options import extraire_options as repartir  # domicile partage (EO-158)
    return repartir(arguments, noms_connus)


NOMS_OPTIONS = ("id", "type", "categorie")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    identifiant = options.get("id", "")
    type_cible = options.get("type", "")
    if not identifiant or not type_cible:
        print('Usage : python main.py classer --id E-XXX --type <dev|reparation|doc|audit> [--categorie <nom>]')
        return 2

    categorie = options.get("categorie", "")
    etat = charger_entonnoir()
    code, message = classer_mission(etat, identifiant, type_cible, categorie)
    if code == 0:
        enregistrer_entonnoir(etat)
    print(message)
    return code
