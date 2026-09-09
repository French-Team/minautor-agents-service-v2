"""Categorie ajouter : orchestre l'enregistrement d'une lecon taguee.

Interface entre main.py et les fonctions simples (ajouter/fonctions.py).
"""
from commun import charger_bdd, enregistrer_bdd, extraire_options
from ajouter.fonctions import ajouter_lecon, separer_tags

NOMS_OPTIONS = ("lecon", "tags", "source")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    lecon = options.get("lecon", "")
    tags = separer_tags(options.get("tags", ""))
    source = options.get("source", "")

    if not lecon or not tags:
        print('Usage : python main.py ajouter --lecon "..." --tags "a,b" [--source "..."]')
        return 2

    donnees = charger_bdd()
    entree = ajouter_lecon(donnees, lecon, tags, source)
    empreinte = enregistrer_bdd(donnees)
    print(
        "Lecon " + entree["id"] + " enregistree (tags : " + ", ".join(entree["tags"])
        + ") -- empreinte : " + empreinte[:16] + "..."
    )
    return 0
