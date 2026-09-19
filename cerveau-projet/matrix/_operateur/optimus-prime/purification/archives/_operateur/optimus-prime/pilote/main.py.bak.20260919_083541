"""Point d'entree global du pilote OPTIMUS (Flux 2, MO-001).

Pilote dedie _operateur/optimus-prime/pilote/ (Flux 2, invisible cameleon).
Miroir du pilote cameleon (matrice/pilote/) mais isole : meme interface,
file/historique/entonnoir/intercom dedies, prefix MO-001, vivier partage+prive.
Role : DIRIGER (parser la commande, router vers la categorie).
Aucune logique metier ici (convention-architecture-outils).

Usage :
    python main.py file
    python main.py charger --theme <nom> --type <t> --objectif "..."   (le TYPE
                                       est EXIGE : EO-120, sans lui la mission nait
                                       sans posture et la checklist perd son specifique)
    python main.py transformer --id MO-00X --theme <nom> --objectif "..."
    python main.py retiqueter --id MO-00X [--theme <nom>] [--type <t>]   (corrige le
                                       theme et/ou le TYPE, quel que soit le statut --
                                       trace conservee)
    python main.py statut
    python main.py injecter
    python main.py fin --bilan "..."   (la mission suivante reste en attente)
                                       --bilan-fichier <chemin> lit le MEME recit
                                       dans un fichier (EO-132) : un argument
                                       traverse le shell, ou un accent grave
                                       EXECUTE du shell et troue la trace
    python main.py file consommer      (echelon 4 : tete du brin -> file du pilote)
    python main.py enregistrer --id MO-XXX --theme <nom> [--type <t>] --objectif "..."
                                       --bilan "..."   (le TYPE est ACCEPTE EN OPTION --
                                       jamais exige : une porte de reparation ne refuse pas
                                       de reparer ; sans lui, la porte le DIT)
                                       (mission DEJA TERMINEE menee hors file :
                                       ecrit la file ET le journal, debut + fin)
    python main.py checklist --id MO-XXX [--reconstruire] (checklist selon le type ;
                                       --reconstruire l'enregistre si elle manque)
    python main.py mission --action <debut|pendant|fin> [--id ID] [--theme THEME] [--bilan BILAN]
    python main.py profil [--guider|--remplir]
"""
import sys

from checklist.entry import executer as checklist_executer
from file.entry import executer as file_executer
from injection.entry import executer as injection_executer
from fin.entry import executer as fin_executer
from filtrer.entry import executer as filtrer_executer
from profil.entry import executer as profil_executer

COMMANDES = {
    "file": file_executer,
    "charger": file_executer,
    "lot": file_executer,
    "transformer": file_executer,
    "retiqueter": file_executer,
    "enregistrer": file_executer,
    "statut": injection_executer,
    "injecter": injection_executer,
    "enchainer": injection_executer,
    "mission": injection_executer,
    "fin": fin_executer,
    "checklist": checklist_executer,
    "filtrer": filtrer_executer,
    "profil": profil_executer,
}


def principal(arguments):
    if not arguments or arguments[0] not in COMMANDES:
        print(__doc__)
        return 2
    # Le verbe est transmis aux categories qui en gerent plusieurs (file/charger).
    return COMMANDES[arguments[0]](arguments)


if __name__ == "__main__":
    sys.exit(principal(sys.argv[1:]))
