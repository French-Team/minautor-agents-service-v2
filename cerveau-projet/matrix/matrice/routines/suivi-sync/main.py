"""Routine de synchronisation du suivi-optimus.

A intervalles reguliers, lit l'inbox.jsonl et ecrit les missions terminees
dans le suivi-optimus. Tout comme veille-flux et espion-integrite, cette
routine est un processus de fond supervise par le serveur matrice.

Usage : python main.py [--once]
"""
import sys
import time
from pathlib import Path

from constants import (
    INTERVALLE_SECONDS,
    ENCODAGE,
    NOM_PID,
    CHEMIN_PID,
    CHEMIN_DRAPEAU_ARRET,
)

# data/commun est deja installe dans sys.path par constants (importe ci-dessus) :
# une seconde insertion ici etait un ordre en DOUBLE (et visait un dossier
# inexistant). Une seule source.
from attente import attendre  # noqa: E402


def ecrire_pid():
    """Note le PID de la routine."""
    try:
        CHEMIN_PID.write_text(str(__import__("os").getpid()) + "\n", encoding=ENCODAGE)
    except OSError:
        pass


def executer_once():
    """Une passe de synchronisation."""
    from commun import publier_passe, synchroniser

    nombre, messages = synchroniser()
    publier_passe(nombre, messages)
    if messages:
        print("[" + time.strftime("%H:%M:%S") + "] suivi-sync : " + " | ".join(messages))
    return 0 if nombre >= 0 else 1


def boucle():
    """Boucle de synchronization periodique avec arret cooperatif."""
    from commun import publier_passe, synchroniser

    # Cadence EFFECTIVE publiee a l'allumage : on la LIT, on ne l'attend pas.
    print("[" + time.strftime("%H:%M:%S") + "] suivi-sync : demarrage, cadence "
          + str(INTERVALLE_SECONDS) + "s")
    while True:
        nombre, messages = synchroniser()
        # L'etat de passe : le TEMOIN DE CADENCE (friction 28). Une passe qui
        # n'ecrit rien n'en est pas moins une passe : elle doit laisser l'heure.
        publier_passe(nombre, messages)
        if messages:
            print("[" + time.strftime("%H:%M:%S") + "] suivi-sync : " + " | ".join(messages))
        if CHEMIN_DRAPEAU_ARRET.exists():
            CHEMIN_DRAPEAU_ARRET.unlink()
            print("[" + time.strftime("%H:%M:%S") + "] suivi-sync : arret cooperatif")
            return 0
        # Attente DECOUPEE : le drapeau est vu en 2 s, pas au bout de la cadence.
        if attendre(INTERVALLE_SECONDS, CHEMIN_DRAPEAU_ARRET):
            CHEMIN_DRAPEAU_ARRET.unlink()
            print("[" + time.strftime("%H:%M:%S") + "] suivi-sync : arret cooperatif")
            return 0


def demander_arret():
    """Pose le drapeau d'arret sans tuer le processus."""
    CHEMIN_DRAPEAU_ARRET.write_text("arret\\n", encoding=ENCODAGE)
    print("Drapeau d'arret pose pour suivi-sync.")
    return 0


if __name__ == "__main__":
    import os
    arguments = sys.argv[1:]
    once = "--once" in arguments
    if arguments and arguments[0] == "arret":
        sys.exit(demander_arret())

    if once:
        # Passe unique (diagnostic) : AUCUN fichier PID.
        # MO-053 -- une passe --once lancee pendant que le demon tourne ecrivait
        # son PID puis l'EFFACAIT en sortant : le PID du demon disparaissait et
        # `vie etat` annoncait "suivi-sync : ARRET" alors que le processus vivait.
        # Un passage unique n'est pas un demon : il ne publie ni n'efface de PID.
        sys.exit(executer_once())

    ecrire_pid()
    boucle()
