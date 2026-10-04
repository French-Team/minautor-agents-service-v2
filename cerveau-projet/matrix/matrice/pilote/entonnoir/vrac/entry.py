"""Categorie vrac : l'echelon 0 -- deposer une mission brute, proposer son type.

Interface entre main.py et les fonctions simples (vrac/fonctions.py).
"""
from listes import URGENCES
from titre import est_theme_du_vivier
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

    # LE TITRE N'EST PAS UNE ETIQUETTE (mesure 2026-09-23, deux items reels cote
    # operateur) : un `--theme` qui EST un nom du vivier est une CONFUSION DE
    # CHAMPS -- le titre de la demande serait perdu et la file afficherait
    # l'etiquette. Refus DIRECTIONNEL, AVANT toute ecriture.
    if est_theme_du_vivier(theme):
        print("REFUS : --theme est le TITRE de la demande (texte libre), pas une etiquette.")
        print("  " + repr(theme) + " est un THEME DU VIVIER : c'est le ROLE de la mission qui le porte.")
        print('  Titre attendu, par exemple : --theme "Reparer la file qui affiche une etiquette"')
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
