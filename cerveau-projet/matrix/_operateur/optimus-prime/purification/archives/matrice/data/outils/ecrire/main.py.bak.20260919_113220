"""Point d'entree global de l'outil ecrire.

Role : DIRIGER (parser la commande, router vers la categorie).
Aucune logique metier ici (convention-architecture-outils).

Usage :
    python main.py ecrire --fichier <chemin> --contenu "<texte|@fichier>" [--mode creer|remplacer|ajouter]
    python main.py ecrire --fichier <chemin> --contenu-fichier <chemin-source> [--mode ...]
    python main.py editer --fichier <chemin> --ancien "<old|@fichier>" --nouveau "<new|@fichier>"
    python main.py editer --fichier <chemin> --ancien-fichier <chemin> --nouveau-fichier <chemin>
"""
import sys

from ecrire.entry import executer as ecrire_executer
from editer.entry import executer as editer_executer

COMMANDES = {
    "ecrire": ecrire_executer,
    "editer": editer_executer,
}


def principal(arguments):
    if not arguments or arguments[0] not in COMMANDES:
        print(__doc__)
        return 2
    return COMMANDES[arguments[0]](arguments[1:])


if __name__ == "__main__":
    from sac_a_dos import envelopper
    sys.exit(envelopper(principal, sys.argv[1:]))
