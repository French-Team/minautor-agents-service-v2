"""Point d entree global de l outil bdd-conservation."""
import sys

from ajouter.entry import executer as ajouter_executer
from lire.entry import executer as lire_executer
from verifier.entry import executer as verifier_executer

COMMANDES = {
    "proposer": ajouter_executer,
    "classer": ajouter_executer,
    "decider": ajouter_executer,
    "manifeste": lire_executer,
    "verifier": verifier_executer,
}


def principal(arguments):
    if not arguments or arguments[0] not in COMMANDES:
        print(__doc__)
        print("Usage : proposer | classer | decider | lire | manifeste | verifier")
        return 2
    return COMMANDES[arguments[0]](arguments)


if __name__ == "__main__":
    from sac_a_dos import envelopper
    sys.exit(envelopper(principal, sys.argv[1:]))
