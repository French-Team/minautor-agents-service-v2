"""Categorie modifier : orchestre la correction d'une lecon existante (porte unique).

Interface entre main.py et les fonctions simples (modifier/fonctions.py).
La lecon garde SON id (les references restent valides), seul son contenu change.
"""
from commun import charger_bdd, enregistrer_bdd, extraire_options
from modifier.fonctions import modifier_entree, trouver_entree

NOMS_OPTIONS = ("id", "lecon", "source")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    identifiant = options.get("id", "")
    contenu = options.get("lecon", "")
    source = options.get("source", "")

    if not identifiant or not contenu:
        print('Usage : python main.py modifier --id L-XXX --lecon "..." [--source "..."]')
        return 2

    donnees = charger_bdd()
    index, entree = trouver_entree(donnees, identifiant)
    if index is None:
        print("Lecon inconnue : " + identifiant)
        return 1
    modifier_entree(entree, contenu, source)
    empreinte = enregistrer_bdd(donnees)
    print(
        "Lecon " + identifiant + " modifiee -- empreinte : " + empreinte[:16] + "..."
    )
    return 0