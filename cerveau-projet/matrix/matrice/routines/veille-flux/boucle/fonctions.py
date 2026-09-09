"""Fonctions simples de la categorie boucle : une seule tache chacune."""
import os
import time

from commun import ecrire_pid, lire_pid, supprimer_pid
from passe.entry import executer as passe_executer


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


def demarrer_boucle(vigile, intervalle_secondes):
    """Fait tourner la passe de veille toutes les N secondes.

    Protections : refuse de demarrer si une boucle vit deja (veille-flux.pid) --
    une seule veille a la fois.
    """
    pid_existant = lire_pid()
    if pid_existant is not None:
        print("REFUS : une boucle vit deja (PID " + str(pid_existant) + "). Une seule veille.")
        return 1

    ecrire_pid(os.getpid())
    mode = "vigile" if vigile else "relax"
    print(
        "Veille-flux demarree (mode " + mode + ", intervalle : " + str(intervalle_secondes)
        + "s). Arret : python main.py veille arret"
    )
    try:
        while True:
            arguments = ["--vigile"] if vigile else []
            passe_executer(arguments)
            if consommer_drapeau_arret():
                from commun import journaliser

                journaliser({"type": "arret", "motif": "drapeau"})
                break
            time.sleep(intervalle_secondes)
    finally:
        supprimer_pid()
    print("Veille terminee proprement.")
    return 0
