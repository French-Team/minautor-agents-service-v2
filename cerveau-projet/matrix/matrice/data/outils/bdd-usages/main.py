"""Point d'entree global de l'outil bdd-usages.

Role : DIRIGER (parser la commande, router vers la categorie).
Aucune logique metier ici (convention-architecture-outils).

Usage :
    python main.py noter --outil <nom> --commande <verbe> --code <n> [--duree <ms>] --tags "a,b"
    python main.py lire [--outil <nom>] [--tag <tag>]
    python main.py rotation [--racine <matrix>] (borne le journal en ARCHIVANT ses anciens)
    python main.py verifier
"""
import sys

import constants  # noqa: F401  -- installe data/commun dans sys.path (motif M-076)

# T1 de la chaine PB-002 : cet outil est le SEUL qui n entre pas par le sac a dos
# (`envelopper`), donc le refus de l OPTION EN TETE lui incombe ICI -- il CONSOMME
# le message du domicile (options.py), il ne le recopie jamais (M-076).
from options import nom_de_l_outil, refuser_option_en_tete

from lire.entry import executer as lire_executer
from noter.entry import executer as noter_executer
from rotation.entry import executer as rotation_executer
from verifier.entry import executer as verifier_executer

COMMANDES = {
    "noter": noter_executer,
    "lire": lire_executer,
    "rotation": rotation_executer,
    "verifier": verifier_executer,
}


def principal(arguments):
    code_tete = refuser_option_en_tete(arguments, nom_de_l_outil(), commandes=COMMANDES)
    if code_tete:
        return code_tete
    if not arguments or arguments[0] not in COMMANDES:
        print(__doc__)
        return 2
    return COMMANDES[arguments[0]](arguments[1:])


if __name__ == "__main__":
    sys.exit(principal(sys.argv[1:]))
