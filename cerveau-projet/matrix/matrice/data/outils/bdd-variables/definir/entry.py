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

    if not cle or not tags:
        print('Usage : python main.py definir --cle <nom> --valeur "<valeur>" [--source "..."] --tags "a,b"')
        print('        (valeur vide acceptee pour la mise a jour d\'une cle existante : MO-093)')
        return 2

    donnees = charger_bdd()
    entree, creee = definir_variable(donnees, cle, valeur, source, tags)
    if creee and not valeur:
        # Une variable NOUVELLE sans valeur n'a pas de sens (MO-093 : c'est
        # ce cas vide qui poussait pause-session a ecrire hors porte).
        print("Refus : une variable NOUVELLE exige une valeur non vide (cle : " + cle + ")")
        return 2
    empreinte = enregistrer_bdd(donnees)
    action = "creee" if creee else "mise a jour"
    print(
        "Variable " + cle + " " + action + " (" + entree["id"] + ", statut " + entree["statut"]
        + ") -- empreinte : " + empreinte[:16] + "..."
    )
    return 0
