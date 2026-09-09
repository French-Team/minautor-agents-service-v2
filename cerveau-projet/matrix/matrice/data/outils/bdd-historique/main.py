"""Point d'entree global de l'outil bdd-historique.

Role : DIRIGER (parser la commande, router vers la categorie).
Aucune logique metier ici (convention-architecture-outils).

Usage :
    python main.py noter --type <type> --detail "..." --tags "a,b"
    python main.py lire [--type <t>] [--tag <t>] [--depuis AAAA-MM-JJ] [--tout]
    python main.py marquer-obsolete --id H-XXX [--motif "..."]
    python main.py verifier
"""
import sys

from lire.entry import executer as lire_executer
from obsolete.entry import executer as obsolete_executer
from noter.entry import executer as noter_executer
from verifier.entry import executer as verifier_executer

COMMANDES = {
    "noter": noter_executer,
    "lire": lire_executer,
    "marquer-obsolete": obsolete_executer,
    "verifier": verifier_executer,
}


def principal(arguments):
    if not arguments or arguments[0] not in COMMANDES:
        print(__doc__)
        return 2
    return COMMANDES[arguments[0]](arguments[1:])


if __name__ == "__main__":
    from sac_a_dos import envelopper
    sys.exit(envelopper(principal, sys.argv[1:]))
