"""Point d'entree global de l'outil passerelle-demandes.

Role : DIRIGER (parser la commande, router vers la categorie).
Aucune logique metier ici (convention-architecture-outils).

Usage :
    python main.py lire                  (LECTURE SEULE : lit, type, compte)
    python main.py deposer               (DRY : prepare et montre, n ecrit rien)
    python main.py deposer --confirmer   (WET : depose PAR LA PORTE)
"""
import sys

from deposer.entry import executer as deposer_executer
from lire.entry import executer as lire_executer

COMMANDES = {
    "lire": lire_executer,
    "deposer": deposer_executer,
}


def principal(arguments):
    if not arguments or arguments[0] not in COMMANDES:
        print(__doc__)
        return 2
    return COMMANDES[arguments[0]](arguments[1:])


if __name__ == "__main__":
    from sac_a_dos import envelopper
    sys.exit(envelopper(principal, sys.argv[1:]))
