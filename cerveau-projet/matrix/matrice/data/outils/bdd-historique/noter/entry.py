"""Categorie noter : orchestre le versement d'un evenement au journal global.

Interface entre main.py et les fonctions simples (noter/fonctions.py).
"""
from commun import ajouter_ligne, charger_lignes, extraire_options
from noter.fonctions import (
    fabriquer_entree,
    est_doublon_actif,
    prochain_id,
    separer_tags,
)

NOMS_OPTIONS = ("type", "detail", "tags")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    type_evenement = options.get("type", "")
    detail = options.get("detail", "")
    tags = separer_tags(options.get("tags", ""))

    if not type_evenement or not detail or not tags:
        print('Usage : python main.py noter --type <type> --detail "..." --tags "a,b"')
        return 2

    lignes = charger_lignes()
    if est_doublon_actif(lignes, type_evenement, detail):
        print("DOUBLON ACTIF refuse : un evenement de ce type avec ce detail existe deja (le marquer obsolete pour re-noter).")
        return 2

    entree = fabriquer_entree(prochain_id(lignes), type_evenement, detail, tags)
    ajouter_ligne(entree)
    print(
        "Evenement " + entree["id"] + " verse au journal (" + type_evenement
        + ") -- empreinte non applicable (journal ajout seul)"
    )
    return 0
