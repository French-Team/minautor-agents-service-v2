"""Categorie retirer : sortie PROPRE du vrac (M-058).

Interface entre main.py et les fonctions simples (retirer/fonctions.py).
"""
from stockage import charger_entonnoir, enregistrer_entonnoir
from retirer.fonctions import retirer_du_vrac


def extraire_options(arguments, noms_connus):
    """Extrait les options --nom valeur (nom local : pas de collision avec le pilote)."""
    options = {}
    index = 0
    while index < len(arguments):
        morceau = arguments[index]
        if morceau.startswith("--") and morceau[2:] in noms_connus:
            if index + 1 < len(arguments):
                options[morceau[2:]] = arguments[index + 1]
            index += 2
        else:
            index += 1
    return options


NOMS_OPTIONS = ("id",)


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    identifiant = options.get("id", "")
    if not identifiant:
        print('Usage : python main.py retirer --id E-XXX')
        return 2

    etat = charger_entonnoir()
    code, message = retirer_du_vrac(etat, identifiant)
    if code == 0:
        enregistrer_entonnoir(etat)
    print(message)
    return code
