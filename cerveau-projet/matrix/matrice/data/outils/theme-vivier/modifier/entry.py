"""Categorie modifier : orchestre la correction d'un theme existant (porte unique).

Interface entre main.py et les fonctions simples (modifier/fonctions.py).
Le theme garde SON id (les references restent valides), seuls les champs
fournis changent.
"""
from commun import charger_bdd, enregistrer_bdd, extraire_options
from constants import CATEGORIES
from modifier.fonctions import modifier_theme, trouver_theme

NOMS_OPTIONS = ("id", "but", "description", "categorie")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    identifiant = options.get("id", "")
    but = options.get("but", "")
    description = options.get("description")
    categorie = options.get("categorie", "").upper()

    if not identifiant:
        print('Usage : python main.py modifier --id TH-XXX [--but "..."] [--description "..."] [--categorie <categorie>]')
        return 2
    if but == "" and description is None and not categorie:
        print("REFUS : rien a modifier (fournir --but, --description ou --categorie).")
        return 2
    if categorie and categorie not in CATEGORIES:
        print("REFUS : categorie " + repr(categorie) + " hors liste fermee : " + ", ".join(CATEGORIES))
        return 1

    donnees = charger_bdd()
    index, theme = trouver_theme(donnees, identifiant)
    if index is None:
        print("Theme inconnu : " + identifiant)
        return 1
    modifier_theme(theme, but, description, categorie)
    empreinte = enregistrer_bdd(donnees)
    print(
        "Theme " + theme["id"] + " (" + theme["nom"] + ") modifie -- empreinte : "
        + empreinte[:16] + "..."
    )
    return 0