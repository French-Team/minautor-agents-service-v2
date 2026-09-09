"""Server MATRICE (E-056, M-081) : orchestrateur de vie des routines.

2 etages du server de demarrage voulu par le createur :
  - server 'matrice' : CE processus (boucle de fond invisible). Il possede
    le lancement : chaque routine est lancee/relancee PAR LUI, jamais en
    direct. Il relance toute boucle morte (reprise apres crash/redemarrage).
  - server 'routine' : chaque routine (veille-flux, espion-integrite) est
    un fils du server : son cycle de vie passe par le server.

Exigeance createur : le redemarrage d'une routine est INVISIBLE (aucune
fenetre console). Toute relance passe par le motif partage lancement.py
(CREATE_NO_WINDOW + SW_HIDE sur Windows).

Usage : python server-matrice.py [--interval <secondes>] [--once]
Arret  : drapeau cooperatif (fichier server-matrice-arret.txt).
"""
import sys
import time
from pathlib import Path

REPERTOIRE_SERVER = Path(__file__).resolve().parent
sys.path.insert(0, str(REPERTOIRE_SERVER))
sys.path.insert(0, str(REPERTOIRE_SERVER.parent.parent / "data" / "commun"))

from constants import BOUCLES, NOM_PID_ESPION, NOM_PID_VEILLE, ENCODAGE  # noqa: E402
from fonctions import etat_boucle  # noqa: E402
from lancement import lancer_invisible  # noqa: E402
from server.entry import CHEMIN_DRAPEAU_ARRET, CHEMIN_PID_SERVER  # noqa: E402

INTERVALLE_DEFAUT_SECONDES = 60


def pid_de(nom):
    """Retourne le nom de fichier PID d'une boucle connue."""
    return NOM_PID_VEILLE if nom == "veille-flux" else NOM_PID_ESPION


def commander(nom):
    """Retourne les arguments de boucle de la routine (ses propres verbes)."""
    return ["veille", "--boucle"] if nom == "veille-flux" else ["boucle"]


def relancer_si_morte(nom, chemin_routine, intervalle):
    """Relance la boucle si morte ; retourne (action, pid, duree_ms)."""
    _, pid = etat_boucle(nom, chemin_routine, pid_de(nom))
    if pid is not None:
        return "vivant", pid, 0
    pid_nouveau, duree_ms = lancer_invisible(chemin_routine, commander(nom) + ["--interval", str(intervalle)])
    return "RELANCEE", pid_nouveau, duree_ms


def ecrire_pid_server(pid):
    """Note le PID du server (atomique simple : petit fichier, LF forces)."""
    CHEMIN_PID_SERVER.write_text(str(pid) + "\n", encoding=ENCODAGE)


def boucle_principale(intervalle, once=False):
    """Boucle de surveillance : relance toute routine morte, jamais de fenetre."""
    pid = None  # place par le bloc principal (voir plus bas)
    while True:
        if CHEMIN_DRAPEAU_ARRET.exists():
            CHEMIN_DRAPEAU_ARRET.unlink()
            print("Drapeau d'arret recu : le server matrice s'arrete proprement.")
            return 0
        actions = []
        for nom, chemin_routine in BOUCLES:
            action, _, duree_ms = relancer_si_morte(nom, chemin_routine, intervalle)
            if action == "RELANCEE":
                actions.append(nom + " (relancee en " + str(duree_ms) + " ms)")
        if actions:
            print("[" + time.strftime("%H:%M:%S") + "] server matrice : " + ", ".join(actions))
        if once:
            return 0
        time.sleep(intervalle)


if __name__ == "__main__":
    import os

    arguments = sys.argv[1:]
    intervalle = INTERVALLE_DEFAUT_SECONDES
    once = "--once" in arguments
    if "--interval" in arguments:
        intervalle = int(arguments[arguments.index("--interval") + 1])
    ecrire_pid_server(os.getpid())
    code = boucle_principale(intervalle, once)
    # En mode --once (sonde), le PID du VRAI server n'est pas retire : seul
    # le server en boucle possede son cycle de vie (garde garde-fou).
    if not once and CHEMIN_PID_SERVER.exists():
        CHEMIN_PID_SERVER.unlink()
    sys.exit(code)
