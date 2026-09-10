"""Constantes de la routine suivi-sync (pour le serveur matrice).

Le serveur utilise ces constantes pour lancer et superviser la routine
suivi-sync comme les autres routines (veille-flux, espion-integrite).
"""
from pathlib import Path

REPERTOIRE_VIE = Path(__file__).resolve().parent
REPERTOIRE_ROUTINES = REPERTOIRE_VIE.parent
REPERTOIRE_SUIVI_SYNC = REPERTOIRE_ROUTINES / "suivi-sync"

# La routine suivi-sync est supervisee par le serveur.
BOUCLES_SUIVI_SYNC = (("suivi-sync", REPERTOIRE_SUIVI_SYNC),)

# PID file de la routine.
NOM_PID_SUIVI_SYNC = "suivi-sync.pid"

# Commande de boucle de la routine (ses propres verbes).
def commander_suivi_sync(nom):
    """Retourne les arguments de boucle de la routine."""
    return ["main.py"]


def pid_de_suivi_sync(nom):
    """Retourne le nom de fichier PID de la routine."""
    return NOM_PID_SUIVI_SYNC
