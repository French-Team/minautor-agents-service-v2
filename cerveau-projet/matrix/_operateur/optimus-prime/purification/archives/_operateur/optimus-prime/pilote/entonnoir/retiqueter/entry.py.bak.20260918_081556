"""Categorie retiqueter : poser le ROLE d'un item, puis recomposer le brin.

Interface entre main.py et les fonctions simples (retiqueter/fonctions.py).
"""
from retiqueter.fonctions import retiqueter_mission
from stockage import charger_entonnoir, enregistrer_entonnoir
from tresse.fonctions import marquer_brin, tresser


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


NOMS_OPTIONS = ("id", "role")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    identifiant = options.get("id", "")
    role = options.get("role", "")
    if not identifiant or not role:
        print('Usage : python main.py retiqueter --id EO-XXX --role <THEME du vivier>')
        return 2
    etat = charger_entonnoir()
    code, message = retiqueter_mission(etat, identifiant, role)
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
