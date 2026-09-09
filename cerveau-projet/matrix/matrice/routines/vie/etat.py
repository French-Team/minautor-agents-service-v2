"""Categorie etat : affiche l'etat des boucles de fond (ARRET / ACTIVE / FANTOME nettoye)."""
from constants import BOUCLES, NOM_PID_ESPION, NOM_PID_VEILLE
from fonctions import etat_boucle


def executer(arguments):
    print("Etat des boucles de fond de la Matrice :")
    codes = 0
    for nom, chemin_routine in BOUCLES:
        nom_pid = NOM_PID_VEILLE if nom == "veille-flux" else NOM_PID_ESPION
        ligne, _ = etat_boucle(nom, chemin_routine, nom_pid)
        print("  " + ligne)
        if "ACTIVE" in ligne:
            codes += 1
    if codes == len(BOUCLES):
        print("La Matrice vit (toutes les boucles actives).")
    elif codes == 0:
        print("La Matrice dort (aucune boucle active).")
    return 0
