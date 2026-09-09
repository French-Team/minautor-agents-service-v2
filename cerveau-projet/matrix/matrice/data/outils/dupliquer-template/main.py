"""Point d'entree global de l'outil dupliquer-template.

Role : DIRIGER (parser la commande, router vers la categorie).
Aucune logique metier ici (convention-architecture-outils).

Usage :
    python main.py generer --moule <outil-bdd|theme-bdd> --nom <nom> [options du moule]

    moule outil-bdd (defaut) :
      --nom bdd-xxx --bdd xxx.json --prefixe X --liste xxx --champ xxx [--humain xxx]
    moule theme-bdd :
      --nom <nom-code> --prefixe X [--nom-affiche "NOM AFFICHE"]

Le generateur lit le moule templates/<moule>/ (JAMAIS un outil vivant),
traduit les jetons, verifie les sources EN MEMOIRE (py_compile + ASCII +
jeton residuel) et l'executable clone AVANT d'ecrire sur disque.
"""
import sys

from generer.entry import executer as generer_executer

COMMANDES = {
    "generer": generer_executer,
}


def principal(arguments):
    if not arguments or arguments[0] not in COMMANDES:
        print(__doc__)
        return 2
    return COMMANDES[arguments[0]](arguments[1:])


if __name__ == "__main__":
    from sac_a_dos import envelopper
    sys.exit(envelopper(principal, sys.argv[1:]))
