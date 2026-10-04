"""Point d'entree global de l'outil rendre-graphe.

Role : DIRIGER (parser la commande, router vers la categorie).
Aucune logique metier ici (convention-architecture-outils).

Usage :
    python main.py mermaid [--source parcours|vivier|arbre] [--theme <NOM>]
                           [--arbre <fichier.json>] [--sortie <fichier>] [--appliquer]
    python main.py svg (--mermaid <fichier.mmd> | [--source parcours|vivier|arbre])
                        [--theme <NOM>] [--arbre <fichier.json>] [--sortie <fichier>]
                        [--appliquer]
    python main.py verifier [--source parcours|vivier|arbre] [--theme <NOM>]
                            [--arbre <fichier.json>]
"""
import sys

from mermaid.entry import executer as mermaid_executer
from svg.entry import executer as svg_executer
from verifier.entry import executer as verifier_executer

COMMANDES = {
    "mermaid": mermaid_executer,
    "svg": svg_executer,
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
