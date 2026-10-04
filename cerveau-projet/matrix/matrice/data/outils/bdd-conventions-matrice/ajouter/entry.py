"""Categorie ajouter : orchestre l'enregistrement d'une la convention taguee.

Interface entre main.py et les fonctions simples (ajouter/fonctions.py).
"""
from commun import charger_bdd, enregistrer_bdd, extraire_options, separer_tags
from ajouter.fonctions import ajouter_entree

NOMS_OPTIONS = ("convention", "tags", "source")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    contenu = options.get("convention", "")
    tags = separer_tags(options.get("tags", ""))
    source = options.get("source", "")

    if not contenu or not tags:
        print('Usage : python main.py ajouter --convention "..." --tags "a,b" [--source "..."]')
        return 2

    donnees = charger_bdd()
    entree = ajouter_entree(donnees, contenu, tags, source)
    empreinte = enregistrer_bdd(donnees)
    print(
        "La convention " + entree["id"] + " enregistree (tags : " + ", ".join(entree["tags"])
        + ") -- empreinte : " + empreinte[:16] + "..."
    )
    return 0
