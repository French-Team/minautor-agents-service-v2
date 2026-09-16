"""Point d'entree global de la vigie-portes (Flux 1, famille surveillance).

Role : DIRIGER (parser la commande, router vers la categorie).
Aucune logique metier ici (convention-architecture-outils).

But : surveiller les PORTES de la Matrice (les outils de matrice/data/outils/)
et CEUX QUI LES UTILISENT (journal d'usages). Une porte qui ne dit rien et une
porte qui va bien se ressemblent : cette vigie est le temoin qui les distingue.

Usage :
    python main.py tour [--racine <matrix>]   (une passe, affichee)
    python main.py rotation [--racine <matrix>]   (borne le journal en ARCHIVANT ses anciens)
    python main.py boucle [--interval <s>]
    python main.py boucle arret
"""
import sys

from boucle.entry import executer as boucle_executer
from rotation.entry import executer as rotation_executer
from tour.entry import executer as tour_executer

COMMANDES = {
    "tour": tour_executer,
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
