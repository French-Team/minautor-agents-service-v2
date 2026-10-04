"""Point d'entree global de l'outil lire.

Role : DIRIGER (parser la commande, router vers la categorie).
Aucune logique metier ici (convention-architecture-outils).

Usage :
    python main.py lire --fichier <chemin> [--lignes debut:fin] [--hash]
    python main.py lire --fichiers <c1,c2> [--lignes debut:fin] [--hash]
    python main.py lire --dossier <chemin> [--filtre *.py] [--recursif] [--hash]
"""
import sys

from lire.entry import executer as lire_executer

COMMANDES = {
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
