"""Categorie urgencer : echelon 3 -- poser le niveau d'urgence d'une mission.

Interface entre main.py et les fonctions simples (urgencer/fonctions.py).
"""
from stockage import charger_entonnoir, enregistrer_entonnoir
from urgencer.fonctions import urgencer_mission


def extraire_options(arguments, noms_connus):
    """Voir le CONTRAT du domicile partage (EO-158) : options CONSOMMEES ici."""
    from options import extraire_options as repartir  # domicile partage (EO-158)
    return repartir(arguments, noms_connus)


NOMS_OPTIONS = ("id", "urgence")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    identifiant = options.get("id", "")
    urgence = options.get("urgence", "")
    if not identifiant or not urgence:
        print('Usage : python main.py urgencer --id E-XXX --urgence <bloquante|haute|normale|basse>')
        return 2
    etat = charger_entonnoir()
    code, message = urgencer_mission(etat, identifiant, urgence)
    if code == 0:
        enregistrer_entonnoir(etat)
    print(message)
    return code
