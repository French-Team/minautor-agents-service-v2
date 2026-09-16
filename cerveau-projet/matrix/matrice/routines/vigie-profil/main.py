"""Point d'entree global de la vigie-profil (Flux 1, famille orchestration).

Role : DIRIGER (parser la commande, router vers la categorie).
Aucune logique metier ici (convention-architecture-outils).

But : verifier si la fiche USER-PROFIL.md est remplie et, sinon, deposer
une ALERTE dans l'inbox de la Matrice (porte officielle : outil signaler).
La Matrice route l'alerte vers la maintenance, le pilote guide ensuite
l'agent sur le parcours USER-PROFIL pour remplir la fiche avec l'utilisateur.

Usage :
    python main.py tour
    python main.py rotation [--racine <matrix>]   (borne le journal en ARCHIVANT ses anciens)
    python main.py boucle [--interval <secondes>]
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
