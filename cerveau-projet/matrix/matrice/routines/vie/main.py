"""Point d'entree global de l'activateur de vie de la Matrice.

Role : DIRIGER (parser la commande, router vers la categorie).
Aucune logique metier ici (convention-architecture-outils).

Usage :
    python main.py etat                       (etat des boucles : ARRET / ACTIVE / fantome nettoye)
    python main.py activer                    (lance veille-flux + espion-integrite en DETACHE invisible)
    python main.py activer --intervalle <s>   (lancement avec intervalle personnalise)
    python main.py server arret               (drapeau cooperatif du server matrice)
    python main.py server etat                (etat du server matrice)
"""
import sys

from activer import executer as activer_executer
from etat import executer as etat_executer
from server.entry import executer as server_executer

COMMANDES = {
    "activer": activer_executer,
    "etat": etat_executer,
    "server": server_executer,
}


def principal(arguments):
    if not arguments or arguments[0] not in COMMANDES:
        print(__doc__)
        return 2
    return COMMANDES[arguments[0]](arguments[1:])


if __name__ == "__main__":
    sys.exit(principal(sys.argv[1:]))
