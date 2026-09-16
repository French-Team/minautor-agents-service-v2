"""Point d'entree global de l'outil lister.

Role : DIRIGER (parser la commande, router vers la categorie).
Aucune logique metier ici (convention-architecture-outils).

Usage :
    python main.py lister --dossier <chemin> [--filtre <glob>] [--recursif] [--json]
"""
import sys

from lister.entry import executer as lister_executer

COMMANDES = {
    "lister": lister_executer,
}


def principal(arguments):
    if not arguments or arguments[0] not in COMMANDES:
        print(__doc__)
        return 2
    return COMMANDES[arguments[0]](arguments[1:])


if __name__ == "__main__":
    from sac_a_dos import envelopper
    sys.exit(envelopper(principal, sys.argv[1:]))
