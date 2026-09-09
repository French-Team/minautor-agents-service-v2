"""Categorie retirer : orchestre la sortie d'un theme du registre.

Interface entre main.py et les fonctions simples (retirer/fonctions.py).
"""
from commun import charger_bdd, enregistrer_bdd, extraire_options
from retirer.fonctions import trouver_theme, retirer_theme

NOMS_OPTIONS = ("id", "nom")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    identifiant = options.get("id", "")
    nom = options.get("nom", "")

    if not identifiant and not nom:
        print('Usage : python main.py retirer --id "TH-XXX" (ou --nom "NOM DU THEME")')
        return 2

    donnees = charger_bdd()
    themes = donnees.get("themes", [])
    index, theme = trouver_theme(themes, identifiant, nom)
    if theme is None:
        print("ECART : aucun theme ne porte cet id ni ce nom (registre intact).")
        return 2
    retire = retirer_theme(themes, index)
    empreinte = enregistrer_bdd(donnees)
    print(
        "Theme " + retire["id"] + " (" + retire["nom"] + ") retire -- empreinte : "
        + empreinte[:16] + "..."
    )
    return 0
