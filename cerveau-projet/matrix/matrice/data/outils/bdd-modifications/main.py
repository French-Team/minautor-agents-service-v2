"""Point d'entree global de l'outil bdd-modifications.

Role : DIRIGER (parser la commande, router vers la categorie).
Aucune logique metier ici (convention-architecture-outils).

Usage :
    python main.py noter --fichier <chemin> --action <action> --detail "..." --tags "a,b"
    python main.py lire  [--fichier <chemin>] [--tag <tag>]
    python main.py corriger --fichier <chemin> --extrait "<texte du detail>" --tags "a,b" [--motif "..."] [--index N]
                                   (reattribue UNE entree EN PLACE : date, action et detail
                                   conserves, anciens tags traces dans l entree, puis la porte
                                   RECALCULE l empreinte -- EO-155)
    python main.py verifier
"""
import sys

from corriger.entry import executer as corriger_executer
from lire.entry import executer as lire_executer
from noter.entry import executer as noter_executer
from verifier.entry import executer as verifier_executer

COMMANDES = {
    "noter": noter_executer,
    "corriger": corriger_executer,
    "lire": lire_executer,
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
