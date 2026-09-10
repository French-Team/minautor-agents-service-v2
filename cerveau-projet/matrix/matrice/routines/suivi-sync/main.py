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
    REPERTOIRE_ROUTINE,
    INTERVALLE_SECONDS,
    ENCODAGE,
    NOM_PID,
    CHEMIN_PID,
)

sys.path.insert(0, str(REPERTOIRE_ROUTINE.parent / "data" / "commun"))


def ecrire_pid():
    """Note le PID de la routine."""
    try:
        CHEMIN_PID.write_text(str(__import__("os").getpid()) + "\n", encoding=ENCODAGE)
    except OSError:
        pass


def executer_once():
    """Une passe de synchronisation."""
    from commun import synchroniser

    nombre, messages = synchroniser()
    if messages:
        print("[" + time.strftime("%H:%M:%S") + "] suivi-sync : " + " | ".join(messages))
    return 0 if nombre >= 0 else 1


def boucle():
    """Boucle de synchronization periodique."""
    from commun import synchroniser

    while True:
        nombre, messages = synchroniser()
        if messages:
            print("[" + time.strftime("%H:%M:%S") + "] suivi-sync : " + " | ".join(messages))
        time.sleep(INTERVALLE_SECONDS)


if __name__ == "__main__":
    import os
    arguments = sys.argv[1:]
    once = "--once" in arguments

    ecrire_pid()
    if once:
        code = executer_once()
        try:
            CHEMIN_PID.unlink()
        except OSError:
            pass
        sys.exit(code)
    else:
        boucle()
