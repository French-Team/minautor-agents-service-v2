"""Point d'entree global de l'outil bilan-periode.

Role : DIRIGER (parser la commande, router vers la categorie).
Aucune logique metier ici (convention-architecture-outils).

Usage :
    python main.py bilan --periode <1h|heures|24h|3j|semaine|mois>

Bilan LECTURE SEULE des BDD horodatees sur une periode fermee :
missions terminees, usages d'outils, activites recentes, transitions defcon.
"""
import sys

from bilan.entry import executer as bilan_executer

COMMANDES = {
    "bilan": bilan_executer,
}


def principal(arguments):
    if not arguments or arguments[0] not in COMMANDES:
        print(__doc__)
        return 2
    return COMMANDES[arguments[0]](arguments[1:])


if __name__ == "__main__":
    from sac_a_dos import envelopper
    sys.exit(envelopper(principal, sys.argv[1:]))
