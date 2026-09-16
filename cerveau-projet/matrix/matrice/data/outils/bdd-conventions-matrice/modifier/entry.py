"""Categorie modifier : orchestre la correction d'une convention existante (porte unique).

Interface entre main.py et les fonctions simples (modifier/fonctions.py).
La convention garde SON id (les references restent valides), seul son texte
change -- pour changer un id, c'est la porte `renommer`.
"""
from commun import charger_bdd, enregistrer_bdd, extraire_options, separer_tags
from modifier.fonctions import modifier_entree, trouver_entree

NOMS_OPTIONS = ("id", "convention", "source", "tags")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    identifiant = options.get("id", "")
    contenu = options.get("convention", "")
    source = options.get("source", "")
    tags = separer_tags(options.get("tags", ""))

    if not identifiant or not contenu:
        print('Usage : python main.py modifier --id CV-XXX --convention "..." [--tags "a,b"] [--source "..."]')
        return 2

    donnees = charger_bdd()
    entree = trouver_entree(donnees, identifiant)
    if entree is None:
        print("Convention inconnue : " + identifiant)
        return 1
    modifier_entree(entree, contenu, source, tags)
    empreinte = enregistrer_bdd(donnees)
    print("Convention " + identifiant + " modifiee -- empreinte : " + empreinte[:16] + "...")
    return 0
