"""Point d'entree global de l'espion-integrite.

Role : DIRIGER (parser la commande, router vers la categorie).
Aucune logique metier ici (convention-architecture-outils).

Usage :
    python main.py tour
    python main.py verifier
    python main.py rotation [--racine <matrix>] [--seuil <octets>] [--gardes <n>] [--force]
    python main.py boucle [--interval <secondes>]
    python main.py boucle arret
"""
import sys

from boucle.entry import executer as boucle_executer
from rotation.entry import executer as rotation_executer
from tour.entry import executer as tour_executer
from tour.entry import verifier as verifier_executer

COMMANDES = {
    "tour": tour_executer,
    "verifier": verifier_executer,
    "rotation": rotation_executer,
    "boucle": boucle_executer,
}


def principal(arguments):
    if not arguments or arguments[0] not in COMMANDES:
        print(__doc__)
        return 2
    return COMMANDES[arguments[0]](arguments[1:])


if __name__ == "__main__":
    sys.exit(principal(sys.argv[1:]))
