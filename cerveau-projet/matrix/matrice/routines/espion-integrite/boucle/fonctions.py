"""Fonctions simples de la categorie boucle : une seule tache chacune."""
import os
import time

from commun import ecrire_pid, journaliser, lire_pid, supprimer_pid
from tour.entry import executer as tour_executer


def arret_demande(arguments):
    """Retourne True si la sous-commande est "arret"."""
    return bool(arguments) and arguments[0] == "arret"


def poser_drapeau_arret():
    """Pose le drapeau d'arret : la boucle s'arrete ELLE-MEME apres sa passe en cours.

    Arret cooperatif : zero processus tue de l'exterieur, zero processus fantome.
    """
    from constants import CHEMIN_DRAPEAU_ARRET

    CHEMIN_DRAPEAU_ARRET.write_text("arret\n", encoding="utf-8")
    print("Drapeau d'arret pose : la boucle s'arretera apres sa passe en cours.")
    return 0


def consommer_drapeau_arret():
    """Verifie le drapeau d'arret et le consomme s'il est pose."""
    from constants import CHEMIN_DRAPEAU_ARRET

    if CHEMIN_DRAPEAU_ARRET.exists():
        CHEMIN_DRAPEAU_ARRET.unlink()
        return True
    return False


def demarrer_boucle(intervalle_secondes):
    """Fait tourner la passe de surveillance toutes les N secondes.

    Protections : refuse de demarrer si une boucle vit deja (espion.pid) --
    un seul espion a la fois.
    """
    pid_existant = lire_pid()
    if pid_existant is not None:
        print("REFUS : une boucle vit deja (PID " + str(pid_existant) + "). Un seul espion.")
        return 1

    ecrire_pid(os.getpid())
    print("Boucle demarree (intervalle : " + str(intervalle_secondes) + "s). Arret : python main.py boucle arret")
    try:
        while True:
            tour_executer([])
            if consommer_drapeau_arret():
                journaliser({"type": "arret", "motif": "drapeau"})
                break
            time.sleep(intervalle_secondes)
    finally:
        supprimer_pid()
    print("Boucle terminee proprement.")
    return 0
