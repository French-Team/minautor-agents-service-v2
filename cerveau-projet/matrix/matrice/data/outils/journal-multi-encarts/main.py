"""Point d'entree global de l'outil journal-multi-encarts.

Role : DIRIGER (parser la commande, router vers la categorie).
Aucune logique metier ici (convention-architecture-outils).

Usage :
    python main.py construire            (regenere le journal depuis les BDD)
    python main.py lire                  (affiche le journal entier)
    python main.py lire --encart <nom>   (affiche UN encart)
"""
import sys

from construire.entry import executer as construire_executer
from lire.entry import executer as lire_executer

COMMANDES = {
    "construire": construire_executer,
    "lire": lire_executer,
}


def principal(arguments):
    if not arguments or arguments[0] not in COMMANDES:
        print(__doc__)
        return 2
    return COMMANDES[arguments[0]](arguments[1:])


if __name__ == "__main__":
    from sac_a_dos import envelopper
    sys.exit(envelopper(principal, sys.argv[1:]))