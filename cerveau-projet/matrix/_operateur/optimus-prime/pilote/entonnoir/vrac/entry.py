"""Categorie vrac : l'echelon 0 -- deposer une mission brute, proposer son type.

Interface entre main.py et les fonctions simples (vrac/fonctions.py).
"""
from listes import URGENCES
from roles import CHAMP_ROLE, valider_role
from stockage import charger_entonnoir, enregistrer_entonnoir
from vrac.fonctions import deposer_vrac, proposer_type, proposer_urgence


def extraire_options(arguments, noms_connus):
    """Voir le CONTRAT du domicile partage (EO-158) : options CONSOMMEES ici."""
    from options import extraire_options as repartir  # domicile partage (EO-158)
    return repartir(arguments, noms_connus)


NOMS_OPTIONS = ("theme", "objectif", "urgence", "source", "role")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    theme = options.get("theme", "")
    objectif = options.get("objectif", "")
    urgence = proposer_urgence(options.get("urgence", ""))
    source = options.get("source", "createur")

    if not theme or not objectif:
        print('Usage : python main.py deposer --theme "..." --objectif "..." [--urgence bloquante|haute|normale|basse] [--source veille|createur] [--role THEME]')
        return 2
    if urgence not in URGENCES:
        print("Urgence inconnue : " + urgence + " (urgences fermees : " + ", ".join(URGENCES) + ")")
        return 2

    # `theme` = TITRE (libre) ; `role` = ROLE de la mission, valide contre le
    # VIVIER. Facultatif au depot : le classement le pose (L-061/MO-076).
    role = ""
    role_brut = options.get("role", "")
    if role_brut:
        code, canonical, ecart = valider_role(role_brut)
        if code != 0:
            return code
        if ecart:
            print(ecart)
        role = canonical

    etat = charger_entonnoir()
    identifiant = deposer_vrac(etat, theme, objectif, urgence, source, role)
    type_propose, mot_cle = proposer_type(theme, objectif)
    enregistrer_entonnoir(etat)
    print(
        "Mission " + identifiant + " deposee au vrac (urgence " + urgence
        + ", source " + source + ") -- type propose : " + type_propose
        + ("" if not mot_cle else " (mot-cle : " + mot_cle + ")")
        + (" -- role : " + role if role else " -- role : (pose au classement)")
    )
    return 0
