"""Categorie retirer : sortie PROPRE du vrac (M-058) ET des files (MO-035).

Une mission classee a tort (doublon d'une mission deja executee) doit pouvoir
sortir de sa file : sinon le brin la ressert a chaque tissage.

Interface entre main.py et les fonctions simples (retirer/fonctions.py).
"""
from stockage import charger_entonnoir, enregistrer_entonnoir, verifier_famille
from retirer.fonctions import recomposer_brin, retirer_des_files, retirer_du_vrac


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
        print('Usage : python main.py retirer --id EO-XXX')
        return 2

    # Famille d'ids verifiee AVANT de toucher l'etat : sans ce controle en tete,
    # l'echec des deux retraits etait resume en "Mission inconnue", ce qui fait
    # passer un id de l'AUTRE entonnoir pour une faute de frappe (l'ecart etait
    # donc masque par le message d'erreur).
    code, message = verifier_famille(identifiant)
    if code != 0:
        print(message)
        return code

    etat = charger_entonnoir()
    code, message = retirer_du_vrac(etat, identifiant)
    if code != 0:
        # Pas au vrac : la mission est peut-etre classee (echelon 1-2).
        code, message = retirer_des_files(etat, identifiant)
        if code != 0:
            message = "Mission inconnue a l'entonnoir (vrac et files) : " + identifiant
        else:
            nb = recomposer_brin(etat)
            message += " -- brin recompose : " + str(nb) + " mission(s)."
    if code == 0:
        enregistrer_entonnoir(etat)
    print(message)
    return code
