"""Categorie etat : affiche l'etat des routines supervisees.

La table nom -> PID ET la liste des routines viennent de constants.py (UNE
SEULE definition chacune, partagees avec le serveur : deux tables = deux
verites, cf. bug MO-043 ou l'ajout d'une routine faisait planter l'etat avec
un KeyError). L'etat ne reassemble plus la liste : il IMPORTE `BOUCLES`.

Chaque ligne porte aussi la cadence DECLAREE par la routine, LUE a sa source
(`CADENCE_PAR_NOM` dit seulement ou la lire). C'est ce qui permet de VERIFIER
sans ATTENDRE : on lit 300 s / 900 s au lieu de patienter 15 minutes pour voir
si la routine bat a son rythme (attendre n'est pas verifier, 2026-09-13).

Le SERVEUR est affiche aussi, et compte dans le verdict : des routines vivantes
avec un serveur mort, c'est une Matrice qui n'est plus conduite. L'etat ne doit
jamais dire "sain" dans ce cas (le garde muet du selecteur a deja coute une
journee).
"""
from constants import BOUCLES, PID_PAR_NOM
from fonctions import cadence_declaree, etat_boucle, lire_pid, processus_vivant
from server.entry import CHEMIN_PID_SERVER


def _etat_serveur():
    """Retourne (ligne, actif) pour le server matrice."""
    pid_serveur = lire_pid(CHEMIN_PID_SERVER)
    if pid_serveur is not None and processus_vivant(pid_serveur):
        return "serveur matrice : ACTIVE (PID " + str(pid_serveur) + ")", True
    if CHEMIN_PID_SERVER.exists():
        CHEMIN_PID_SERVER.unlink()
        return "serveur matrice : ARRET (PID fantome " + str(pid_serveur) + " nettoye)", False
    return "serveur matrice : ARRET", False


def executer(arguments):
    print("Etat des boucles de fond de la Matrice :")
    codes = 0
    for nom, chemin_routine in BOUCLES:
        ligne, _ = etat_boucle(nom, chemin_routine, PID_PAR_NOM[nom])
        cadence = cadence_declaree(nom, chemin_routine)
        if cadence is None:
            ligne += " | cadence : ILLISIBLE"
        else:
            ligne += " | cadence declaree : " + str(cadence) + "s"
        print("  " + ligne)
        if "ACTIVE" in ligne:
            codes += 1

    ligne_serveur, serveur_actif = _etat_serveur()
    print("  " + ligne_serveur)

    if codes == len(BOUCLES) and serveur_actif:
        print("La Matrice vit (serveur + " + str(len(BOUCLES)) + " routines actives).")
    elif codes == 0 and not serveur_actif:
        print("La Matrice dort (serveur et routines arretes).")
    elif not serveur_actif:
        print(
            "ATTENTION : le SERVEUR est arrete -- " + str(codes) + "/" + str(len(BOUCLES))
            + " routines vivent sans surveillance : personne ne les relancera."
        )
    else:
        print(
            "La Matrice vit partiellement (" + str(codes) + "/" + str(len(BOUCLES))
            + " routines actives)."
        )
    return 0
