"""Categorie server : le server matrice -- surveillance des routines en boucle.

Le server VIT ICI ( meme dossier que l'activateur de vie). Une seule
instance (garde PID), lancement par la porte officielle ci-dessous :
  demarrage direct : python server_matrice.py
  arret cooperatif : python main.py server arret
  etat             : python main.py server etat
"""
from constants import ENCODAGE, NOM_DRAPEAU_SERVER, NOM_PID_SERVER
from pathlib import Path

from fonctions import lire_pid, processus_vivant  # noqa: E402

REPERTOIRE_SERVER = Path(__file__).resolve().parent
CHEMIN_PID_SERVER = REPERTOIRE_SERVER / NOM_PID_SERVER
CHEMIN_DRAPEAU_ARRET = REPERTOIRE_SERVER / NOM_DRAPEAU_SERVER


def executer(arguments):
    if arguments and arguments[0] == "arret":
        pid = lire_pid(CHEMIN_PID_SERVER)
        if pid is None or not processus_vivant(pid):
            if CHEMIN_PID_SERVER.exists():
                CHEMIN_PID_SERVER.unlink()
            print("server matrice deja arrete.")
            return 0
        CHEMIN_DRAPEAU_ARRET.write_text("arret demande\n", encoding=ENCODAGE)
        print("Drapeau d'arret pose : le server matrice s'arretera apres son cycle courant.")
        return 0
    if arguments and arguments[0] == "etat":
        pid = lire_pid(CHEMIN_PID_SERVER)
        if pid is not None and not processus_vivant(pid):
            CHEMIN_PID_SERVER.unlink()
            print("server matrice : ARRET (PID fantome " + str(pid) + " nettoye)")
            return 0
        if pid is not None:
            print("server matrice : ACTIVE (PID " + str(pid) + ")")
            return 0
        print("server matrice : ARRET (demarrage : python server_matrice.py)")
        return 0
    print(__doc__)
    return 2
