"""Fonctions communes a toutes les categories : ajouter une ligne, lire, options.

Chaque fonction fait UNE chose (convention-architecture-outils).
"""
import json

from constants import CHEMIN_BDD, ENCODAGE


def ajouter_ligne(entree):
    """Ajoute UNE ligne a la BDD (ajout seul : l'histoire n'est jamais reecrite)."""
    with open(CHEMIN_BDD, "a", encoding=ENCODAGE, newline="\n") as flux:
        flux.write(json.dumps(entree, ensure_ascii=True) + "\n")


def charger_lignes():
    """Retourne la liste des lignes valides de la BDD ([] si absente)."""
    if not CHEMIN_BDD.exists():
        return []
    lignes = []
    with open(CHEMIN_BDD, "r", encoding=ENCODAGE) as flux:
        for ligne in flux:
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                lignes.append(json.loads(ligne))
            except json.JSONDecodeError:
                continue
    return lignes


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
