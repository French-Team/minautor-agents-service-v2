"""Entree de boucle de la routine suivi-sync.

Appelee par le serveur matrice pour lancer la routine en mode boucle.
"""
import sys
from pathlib import Path

REPERTOIRE_ROUTINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPERTOIRE_ROUTINE.parent / "data" / "commun"))


def executer(arguments):
    """Lance la routine en mode boucle."""
    from lancement import lancer_invisible

    nom_routine = REPERTOIRE_ROUTINE.name
    arguments_boucle = [str(REPERTOIRE_ROUTINE / "main.py")]
    pid, duree_ms = lancer_invisible(REPERTOIRE_ROUTINE, arguments_boucle)

    print("[" + __import__("time").strftime("%H:%M:%S") + "] " + nom_routine + " lance (PID " + str(pid) + ", " + str(duree_ms) + " ms)")
    return 0
