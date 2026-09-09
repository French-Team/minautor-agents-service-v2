"""Categorie server : le server matrice -- surveillance des routines en boucle.

Le server VIT ICI ( meme dossier que l'activateur de vie). Une seule
instance (garde PID), lancement par la porte officielle ci-dessous :
  demarrage direct : python server_matrice.py
  arret cooperatif : python main.py server arret
  etat             : python main.py server etat
"""
from constants import ENCODAGE
from pathlib import Path

REPERTOIRE_SERVER = Path(__file__).resolve().parent
NOM_PID_SERVER = "server-matrice.pid"
CHEMIN_PID_SERVER = REPERTOIRE_SERVER / NOM_PID_SERVER
NOM_DRAPEAU_ARRET = "server-matrice-arret.txt"
CHEMIN_DRAPEAU_ARRET = REPERTOIRE_SERVER / NOM_DRAPEAU_ARRET


def executer(arguments):
    if arguments and arguments[0] == "arret":
        CHEMIN_DRAPEAU_ARRET.write_text("arret demande\n", encoding=ENCODAGE)
        print("Drapeau d'arret pose : le server matrice s'arretera apres son cycle courant.")
        return 0
    if arguments and arguments[0] == "etat":
        if CHEMIN_PID_SERVER.exists():
            print("server matrice : ACTIVE (PID " + CHEMIN_PID_SERVER.read_text(encoding=ENCODAGE).strip() + ")")
        else:
            print("server matrice : ARRET (demarrage : python server_matrice.py)")
        return 0
    print(__doc__)
    return 2
