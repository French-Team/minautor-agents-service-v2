"""Fonctions communes a toutes les categories : charger, ajouter, options.

Chaque fonction fait UNE chose (convention-architecture-outils).
"""
import json

from constants import CHEMIN_BDD, ENCODAGE


def charger_lignes():
    """Retourne la liste des lignes JSON du journal (ajout seul, sans empreinte)."""
    if not CHEMIN_BDD.exists():
        return []
    lignes = []
    with open(CHEMIN_BDD, "r", encoding=ENCODAGE) as flux:
        for ligne in flux:
            ligne = ligne.strip()
            if ligne:
                lignes.append(json.loads(ligne))
    return lignes


def ajouter_ligne(entree):
    """Ajoute UNE ligne au journal (en ajout seul, jamais modifie a posteriori)."""
    with open(CHEMIN_BDD, "a", encoding=ENCODAGE) as flux:
        flux.write(json.dumps(entree, ensure_ascii=True) + "\n")


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
