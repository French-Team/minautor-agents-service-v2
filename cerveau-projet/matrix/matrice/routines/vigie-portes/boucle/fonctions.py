"""Fonctions simples de la categorie boucle : une seule tache chacune."""
import os

from commun import ecrire_pid, journaliser, lire_pid, publier_cadence, supprimer_pid
from constants import CHEMIN_DRAPEAU_ARRET, REPERTOIRE_MATRIX
from rotation.entry import tourner_et_journaliser
from tour.entry import executer as tour_executer

# data/commun est installe dans sys.path par constants (importe juste au-dessus) :
# cet ordre d'import est volontaire, ne pas trier alphabetiquement.
from attente import attendre  # noqa: E402


def arret_demande(arguments):
    """Retourne True si la sous-commande est "arret"."""
    return bool(arguments) and arguments[0] == "arret"


def poser_drapeau_arret():
    """Pose le drapeau d'arret : la boucle s'arrete ELLE-MEME apres sa passe.

    Arret cooperatif : zero processus tue de l'exterieur, zero fantome.
    """
    CHEMIN_DRAPEAU_ARRET.write_text("arret\n", encoding="utf-8")
    print("Drapeau d'arret pose : la boucle s'arretera apres sa passe en cours.")
    return 0


def consommer_drapeau_arret():
    """Verifie le drapeau d'arret et le consomme s'il est pose."""
    if CHEMIN_DRAPEAU_ARRET.exists():
        CHEMIN_DRAPEAU_ARRET.unlink()
        return True
    return False


def demarrer_boucle(intervalle_secondes):
    """Fait tourner la passe de vigie toutes les N secondes.

    Protection : refuse de demarrer si une boucle vit deja (fichier PID).
    """
    pid_existant = lire_pid()
    if pid_existant is not None:
        print("REFUS : une boucle vit deja (PID " + str(pid_existant) + "). Une seule vigie.")
        return 1

    ecrire_pid(os.getpid())
    # La cadence EFFECTIVE est journalisee a l'allumage : on la LIT, on ne
    # l'attend pas (attendre n'est pas verifier -- parole du createur 2026-09-13).
    journaliser({"type": "demarrage", "intervalle": intervalle_secondes})
    # Cadence PUBLIEE dans un etat court : le journal etant rotationne, un
    # controle qui la chercherait dans le journal serait neutralise (L-040).
    publier_cadence(intervalle_secondes)
    print("Boucle demarree (intervalle : " + str(intervalle_secondes) + "s). "
          "Arret : python main.py boucle arret")
    try:
        while True:
            # Borne du journal AVANT la passe : le declenchement se LIT (taille
            # vs seuil des constantes), et un refus de rotation ne tue jamais la
            # passe (lecon L-026).
            tourner_et_journaliser(REPERTOIRE_MATRIX)
            tour_executer([])
            if consommer_drapeau_arret():
                journaliser({"type": "arret", "motif": "drapeau"})
                break
            # Attente DECOUPEE : un arret demande est vu en 2 s, meme avec une
            # cadence de 900 s. Le drapeau est consomme ici (un seul proprietaire).
            if attendre(intervalle_secondes, CHEMIN_DRAPEAU_ARRET):
                consommer_drapeau_arret()
                journaliser({"type": "arret", "motif": "drapeau"})
                break
    finally:
        supprimer_pid()
    print("Boucle terminee proprement.")
    return 0
