"""Point d'entree global du pilote.

Role : DIRIGER (parser la commande, router vers la categorie).
Detecte les mots-cles et lance le pilote Optimus si necessaire.
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
    python main.py mission --action <debut|pendant|fin> [--id ID] [--theme THEME] [--bilan BILAN]
    python main.py detecter --texte "ma demande avec [bug]"
    python main.py mots-cles
"""
import sys

from checklist.entry import executer as checklist_executer
from file.entry import executer as file_executer
from injection.entry import executer as injection_executer
from fin.entry import executer as fin_executer
from detecteur.entry import executer as detecter_executer

COMMANDES = {
    "file": file_executer,
    "charger": file_executer,
    "lot": file_executer,
    "transformer": file_executer,
    "statut": injection_executer,
    "injecter": injection_executer,
    "enchainer": injection_executer,
    "mission": injection_executer,
    "fin": fin_executer,
    "checklist": checklist_executer,
    "detecter": detecter_executer,
    "mots-cles": detecter_executer,
}


def principal(arguments):
    if not arguments or arguments[0] not in COMMANDES:
        print(__doc__)
        return 2
    # Le verbe est transmis aux categories qui en gerent plusieurs (file/charger).
    return COMMANDES[arguments[0]](arguments)


if __name__ == "__main__":
    sys.exit(principal(sys.argv[1:]))
