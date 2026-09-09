"""Categorie categoriser : pose la categorie d'un theme existant (liste fermee)."""
from commun import charger_bdd, enregistrer_bdd, extraire_options
from constants import CATEGORIES
from categoriser.fonctions import categoriser_theme

NOMS_OPTIONS = ("id", "categorie")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    identifiant = options.get("id", "")
    categorie = options.get("categorie", "").upper()
    if not identifiant or not categorie:
        print(
            "Usage : python main.py categoriser --id TH-XXX --categorie <"
            + "|".join(CATEGORIES) + ">"
        )
        return 2
    if categorie not in CATEGORIES:
        print("REFUS : categorie " + repr(categorie) + " hors liste fermee : " + ", ".join(CATEGORIES))
        return 1
    donnees = charger_bdd()
    entree, message = categoriser_theme(donnees, identifiant, categorie)
    if entree is None:
        print(message)
        return 1
    empreinte = enregistrer_bdd(donnees)
    print(
        "Theme " + entree["id"] + " (" + entree["nom"] + ") categorise : " + categorie
        + " -- empreinte : " + empreinte[:16] + "..."
    )
    return 0
