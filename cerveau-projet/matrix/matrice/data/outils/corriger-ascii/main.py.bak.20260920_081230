"""Point d'entree global de l'outil corriger-ascii.

Role : DIRIGER (parser la commande, router vers la categorie).
Aucune logique metier ici (convention-architecture-outils).

Usage :
    python main.py verifier              (scan seul)
    python main.py corriger              (rapport sans ecrire)
    python main.py corriger --appliquer  (applique les corrections convertibles)
"""
import sys

from corriger.entry import executer as corriger_executer
from verifier.entry import executer as verifier_executer

COMMANDES = {
    "corriger": corriger_executer,
    "verifier": verifier_executer,
}


def principal(arguments):
    if not arguments or arguments[0] not in COMMANDES:
        print(__doc__)
        return 2
    return COMMANDES[arguments[0]](arguments)


if __name__ == "__main__":
    from sac_a_dos import envelopper
    sys.exit(envelopper(principal, sys.argv[1:]))
