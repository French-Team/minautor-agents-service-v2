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
    python main.py canoniser [--simuler oui]
                                   (REUNIT les cles non canoniques sur leur cle canonique :
                                   les deux histoires d un meme fichier sont fusionnees,
                                   sans perdre une entree -- le compte est le GARDE, et une
                                   migration qui perdrait une entree est REFUSEE ; EO-363)
    python main.py verifier [--auto-test]
                                   (l integrite ET la cle canonique ; --auto-test rejoue le
                                   cobaye et les contre-temoins sur des faits FABRIQUES)
"""
import sys

from canoniser.entry import executer as canoniser_executer
from corriger.entry import executer as corriger_executer
from lire.entry import executer as lire_executer
from noter.entry import executer as noter_executer
from verifier.entry import executer as verifier_executer

COMMANDES = {
    "noter": noter_executer,
    "corriger": corriger_executer,
    "lire": lire_executer,
    "canoniser": canoniser_executer,
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
