"""Categorie retiqueter : poser ou REPARER les ETIQUETTES d'un item -- categorie et/ou
role -- puis recomposer le brin.

Interface entre main.py et les fonctions simples (retiqueter/fonctions.py).
"""
from retiqueter.fonctions import retiqueter_mission
from stockage import charger_entonnoir, enregistrer_entonnoir
from tresse.fonctions import marquer_brin, tresser


def extraire_options(arguments, noms_connus):
    """Voir le CONTRAT du domicile partage (EO-158) : options CONSOMMEES ici."""
    from options import extraire_options as repartir  # domicile partage (EO-158)
    return repartir(arguments, noms_connus)


NOMS_OPTIONS = ("id", "categorie", "role")

USAGE = ("Usage : python main.py retiqueter --id EO-XXX "
         "[--categorie <nom>] [--role <THEME du vivier>]")
AIDE = ("  au moins une etiquette : la CATEGORIE (liste fermee de SON type) et/ou le ROLE "
        "(vivier) -- le classement POSE, retiqueter REPOSE.")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    identifiant = options.get("id", "")
    role = options.get("role", "")
    categorie = options.get("categorie", "")
    if not identifiant or not (role or categorie):
        print(USAGE)
        print(AIDE)
        return 2
    etat = charger_entonnoir()
    code, message = retiqueter_mission(etat, identifiant, role, categorie)
    if code != 0:
        if message:
            print(message)
        return code
    # Le brin est RECOMPOSE dans le meme geste : un role pose sans retressage
    # laisserait la tete du brin porter l'ancien role, donc l'ancien blocage.
    etat["brin"] = marquer_brin(tresser(etat.get("files", {})))
    enregistrer_entonnoir(etat)
    print(message)
    print("Brin recompose : " + str(len(etat["brin"])) + " mission(s).")
    return 0
