"""Point d'entree global de l'outil theme-vivier.

Role : DIRIGER (parser la commande, router vers la categorie).
Aucune logique metier ici (convention-architecture-outils).

Usage :
    python main.py ajouter --nom "NOM DU THEME" --categorie <SYSTEME|PERSONNALITE|QUESTION|GOUVERNANCE> --but "..." [--description "..."]
    python main.py lire [--nom "NOM"] [--categorie CATEGORIE]
    python main.py categoriser --id "TH-XXX" --categorie <CATEGORIE>
    python main.py retirer --id "TH-XXX" (ou --nom "NOM DU THEME")
    python main.py verifier
"""
import sys

from ajouter.entry import executer as ajouter_executer
from categoriser.entry import executer as categoriser_executer
from lire.entry import executer as lire_executer
from retirer.entry import executer as retirer_executer
from verifier.entry import executer as verifier_executer

COMMANDES = {
    "ajouter": ajouter_executer,
    "lire": lire_executer,
    "categoriser": categoriser_executer,
    "retirer": retirer_executer,
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
