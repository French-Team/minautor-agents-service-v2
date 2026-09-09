"""Point d'entree global du pilote.

Role : DIRIGER (parser la commande, router vers la categorie).
Aucune logique metier ici (convention-architecture-outils).

Usage :
    python main.py file
    python main.py charger --theme <nom> --objectif "..."
    python main.py transformer --id M-00X --theme <nom> --objectif "..."
    python main.py statut
    python main.py injecter
    python main.py fin --bilan "..."   (la mission suivante reste en attente)
    python main.py file consommer      (echelon 4 : tete du brin -> file du pilote)
    python main.py checklist --id M-XXX (checklist de la mission, selon son type)
"""
import sys

from checklist.entry import executer as checklist_executer
from file.entry import executer as file_executer
from injection.entry import executer as injection_executer
from fin.entry import executer as fin_executer

COMMANDES = {
    "file": file_executer,
    "charger": file_executer,
    "lot": file_executer,
    "transformer": file_executer,
    "statut": injection_executer,
    "injecter": injection_executer,
    "enchainer": injection_executer,
    "fin": fin_executer,
    "checklist": checklist_executer,
}


def principal(arguments):
    if not arguments or arguments[0] not in COMMANDES:
        print(__doc__)
        return 2
    # Le verbe est transmis aux categories qui en gerent plusieurs (file/charger).
    return COMMANDES[arguments[0]](arguments)


if __name__ == "__main__":
    sys.exit(principal(sys.argv[1:]))
