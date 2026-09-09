"""Categorie definir : orchestre la creation ou la mise a jour d'une variable.

Interface entre main.py et les fonctions simples (definir/fonctions.py).
"""
from commun import charger_bdd, enregistrer_bdd, extraire_options
from definir.fonctions import definir_variable, separer_tags

NOMS_OPTIONS = ("cle", "valeur", "source", "tags")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    cle = options.get("cle", "")
    valeur = options.get("valeur", "")
    source = options.get("source", "")
    tags = separer_tags(options.get("tags", ""))

    if not cle or not valeur or not tags:
        print('Usage : python main.py definir --cle <nom> --valeur "<valeur>" [--source "..."] --tags "a,b"')
        return 2

    donnees = charger_bdd()
    entree, creee = definir_variable(donnees, cle, valeur, source, tags)
    empreinte = enregistrer_bdd(donnees)
    action = "creee" if creee else "mise a jour"
    print(
        "Variable " + cle + " " + action + " (" + entree["id"] + ", statut " + entree["statut"]
        + ") -- empreinte : " + empreinte[:16] + "..."
    )
    return 0
