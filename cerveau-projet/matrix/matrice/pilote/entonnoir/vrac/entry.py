"""Categorie vrac : l'echelon 0 -- deposer une mission brute, proposer son type.

Interface entre main.py et les fonctions simples (vrac/fonctions.py).
"""
from listes import URGENCES
from stockage import charger_entonnoir, enregistrer_entonnoir
from vrac.fonctions import deposer_vrac, proposer_type, proposer_urgence


def extraire_options(arguments, noms_connus):
    """Voir le CONTRAT du domicile partage (EO-158) : options CONSOMMEES ici."""
    from options import extraire_options as repartir  # domicile partage (EO-158)
    return repartir(arguments, noms_connus)


NOMS_OPTIONS = ("theme", "objectif", "urgence", "source")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    theme = options.get("theme", "")
    objectif = options.get("objectif", "")
    urgence = proposer_urgence(options.get("urgence", ""))
    source = options.get("source", "createur")

    if not theme or not objectif:
        print('Usage : python main.py deposer --theme "..." --objectif "..." [--urgence bloquante|haute|normale|basse] [--source veille|createur]')
        return 2
    if urgence not in URGENCES:
        print("Urgence inconnue : " + urgence + " (urgences fermees : " + ", ".join(URGENCES) + ")")
        return 2

    etat = charger_entonnoir()
    identifiant = deposer_vrac(etat, theme, objectif, urgence, source)
    type_propose, mot_cle = proposer_type(theme, objectif)
    enregistrer_entonnoir(etat)
    print(
        "Mission " + identifiant + " deposee au vrac (urgence " + urgence
        + ", source " + source + ") -- type propose : " + type_propose
        + ("" if not mot_cle else " (mot-cle : " + mot_cle + ")")
    )
    return 0
