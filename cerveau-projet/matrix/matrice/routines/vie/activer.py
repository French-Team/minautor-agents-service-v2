"""Categorie activer : porte unique vers le server matrice.

Le server matrice est l'unique proprietaire du cycle de vie des routines.
Cette commande ne lance plus directement une routine : elle demarre le server,
qui adopte les routines existantes et lance les absentes.
La LISTE de ces routines vit dans `constants.py` (BOUCLES) et nulle part
ailleurs : l'enumerer ici serait une deuxieme table, donc une deuxieme verite.
"""
from constants import ENCODAGE
from fonctions import processus_vivant
from lancement import lancer_invisible
from pathlib import Path


REPERTOIRE_VIE = Path(__file__).resolve().parent
CHEMIN_PID_SERVER = REPERTOIRE_VIE / "server" / "server-matrice.pid"
NOM_DRAPEAU_SERVER = "server-matrice-arret.txt"
CHEMIN_DRAPEAU_SERVER = REPERTOIRE_VIE / "server" / NOM_DRAPEAU_SERVER


def executer(arguments):
    """Demarre le server matrice s'il n'est pas deja actif."""
    intervalle = None
    for index, morceau in enumerate(arguments):
        if morceau == "--intervalle" and index + 1 < len(arguments):
            intervalle = arguments[index + 1]

    if CHEMIN_PID_SERVER.exists():
        try:
            pid = int(CHEMIN_PID_SERVER.read_text(encoding=ENCODAGE).strip())
        except (ValueError, OSError):
            pid = None
        if processus_vivant(pid):
            print("Server matrice deja actif (PID " + str(pid) + ").")
            return 0
        CHEMIN_PID_SERVER.unlink()

    if CHEMIN_DRAPEAU_SERVER.exists():
        CHEMIN_DRAPEAU_SERVER.unlink()

    arguments_server = []
    if intervalle:
        arguments_server += ["--interval", intervalle]
    pid, duree_ms = lancer_invisible(
        REPERTOIRE_VIE,
        arguments_server,
        script="server_matrice.py",
    )
    print(
        "Server matrice lance (PID " + str(pid) + ", "
        + str(duree_ms) + " ms). Il possede les routines de BOUCLES."
    )
    return 0
