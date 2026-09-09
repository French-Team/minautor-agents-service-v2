"""Fonctions communes de l'outil dupliquer-template : une seule tache chacune."""


def extraire_options(arguments, noms_connus):
    """Extrait les options --nom valeur d'une liste d'arguments (forme seulement)."""
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
