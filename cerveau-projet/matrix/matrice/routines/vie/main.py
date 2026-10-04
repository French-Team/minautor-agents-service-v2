"""Point d'entree global de l'activateur de vie de la Matrice.

Role : DIRIGER (parser la commande, router vers la categorie).
Aucune logique metier ici (convention-architecture-outils).

Usage :
    python main.py etat                       (etat des boucles : ARRET / ACTIVE / fantome nettoye)
    python main.py activer                    (lance le server matrice, porte unique des routines)
    python main.py activer --intervalle <s>   (override EXPLICITE de la cadence de toutes les routines ;
                                               sans lui, chacune garde SON temps declare)
    python main.py server arret               (arret cooperatif du server et des routines)

La liste des routines supervisees n'est PAS ecrite ici : elle vit dans
`constants.py` (BOUCLES) et nulle part ailleurs.
    python main.py server etat                (etat du server matrice)
    python main.py service etat               (planning : cadences, modes, echeances)
    python main.py service tour [--racine X]  (UN tour du service : allume la routine
                                               DUE, recoit, transforme en message)
"""
import sys

from activer import executer as activer_executer
from etat import executer as etat_executer
from server.entry import executer as server_executer
from service.entry import executer as service_executer

COMMANDES = {
    "activer": activer_executer,
    "etat": etat_executer,
    "server": server_executer,
    "service": service_executer,
}


def principal(arguments):
    if not arguments or arguments[0] not in COMMANDES:
        print(__doc__)
        return 2
    return COMMANDES[arguments[0]](arguments[1:])


if __name__ == "__main__":
    sys.exit(principal(sys.argv[1:]))
