"""Point d'entree global de la routine veille-flux.

Role : DIRIGER (parser la commande, router vers la categorie).
Aucune logique metier ici (convention-architecture-outils).

Usage :
    python main.py veille              (une passe RELAX : corriger-ascii + py_compile)
    python main.py veille --vigile     (une passe VIGILE : + les 3 verifiers du marbre)
    python main.py veille --boucle     (surveillance continue, refus de double lancement)
    python main.py veille --boucle --vigile
    python main.py veille --boucle --intervalle <secondes>
    python main.py veille arret        (drapeau d'arret cooperatif, zero processus tue)
    python main.py rotation            (borne journal-veille.txt en ARCHIVANT ses anciens)
"""
import sys

from boucle.entry import executer as boucle_executer
from passe.entry import executer as passe_executer
from rotation.entry import executer as rotation_executer


def principal(arguments):
    if arguments and arguments[0] == "rotation":
        # Verbe de la categorie rotation : il ne fait pas une passe, il borne le
        # journal en deplacant ses evenements anciens dans une archive datee.
        return rotation_executer(arguments[1:])
    if not arguments or arguments[0] != "veille":
        print(__doc__)
        return 2
    reste = arguments[1:]
    if "--boucle" in reste:
        return boucle_executer(reste)
    if reste and reste[0] == "arret":
        # 'arret' est un verbe de la BOUCLE (drapeau cooperatif), jamais une passe.
        return boucle_executer(reste)
    return passe_executer(reste)


if __name__ == "__main__":
    sys.exit(principal(sys.argv[1:]))
