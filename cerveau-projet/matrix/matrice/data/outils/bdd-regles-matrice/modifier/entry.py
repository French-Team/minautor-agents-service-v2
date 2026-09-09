"""Categorie modifier : orchestre la correction d'une regle existante (porte unique).

Interface entre main.py et les fonctions simples (modifier/fonctions.py).
La regle garde SON id (les references restent valides), seul son contenu change.
"""
from commun import charger_bdd, enregistrer_bdd, extraire_options
from modifier.fonctions import modifier_entree, trouver_entree

NOMS_OPTIONS = ("id", "regle", "source")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    identifiant = options.get("id", "")
    contenu = options.get("regle", "")
    source = options.get("source", "")

    if not identifiant or not contenu:
        print('Usage : python main.py modifier --id R-XXX --regle "..." [--source "..."]')
        return 2

    donnees = charger_bdd()
    index, entree = trouver_entree(donnees, identifiant)
    if index is None:
        print("Regle inconnue : " + identifiant)
        return 1
    modifier_entree(entree, contenu, source)
    empreinte = enregistrer_bdd(donnees)
    print(
        "Regle " + identifiant + " modifiee -- empreinte : " + empreinte[:16] + "..."
    )
    return 0