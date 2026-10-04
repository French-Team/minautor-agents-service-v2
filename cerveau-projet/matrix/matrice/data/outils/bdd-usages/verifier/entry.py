"""Categorie verifier : controle structurel de la BDD des usages.

Chaque ligne doit etre un JSON valide avec les cles requises et des tags non vides.
Lecture seule : signale, ne repare jamais (code 0/1).
"""
from commun import charger_lignes
from constants import CLES_REQUISES


def executer(arguments):
    lignes = charger_lignes()
    if not lignes:
        print("BDD absente ou vide : rien a verifier (etat initial legitime).")
        return 0

    lignes_invalides = 0
    for numero, ligne in enumerate(lignes, 1):
        manquantes = [cle for cle in CLES_REQUISES if cle not in ligne]
        if manquantes:
            print("Ligne " + str(numero) + " : cles manquantes : " + ", ".join(manquantes))
            lignes_invalides += 1
        elif not ligne.get("tags"):
            print("Ligne " + str(numero) + " : tags vides (interdit).")
            lignes_invalides += 1

    if lignes_invalides:
        print("Verifier : " + str(lignes_invalides) + " ligne(s) invalide(s).")
        return 1
    print("Verifier : " + str(len(lignes)) + " ligne(s) valide(s), integrite structurelle OK.")
    return 0
