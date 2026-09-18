"""Categorie urgencer : echelon 3 -- poser le niveau d'urgence d'une mission.

Interface entre main.py et les fonctions simples (urgencer/fonctions.py).
"""
from stockage import charger_entonnoir, enregistrer_entonnoir
from urgencer.fonctions import urgencer_mission


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


NOMS_OPTIONS = ("id", "urgence")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    identifiant = options.get("id", "")
    urgence = options.get("urgence", "")
    if not identifiant or not urgence:
        print('Usage : python main.py urgencer --id EO-XXX --urgence <bloquante|haute|normale|basse>')
        return 2
    etat = charger_entonnoir()
    code, message = urgencer_mission(etat, identifiant, urgence)
    if code == 0:
        enregistrer_entonnoir(etat)
    print(message)
    return code
