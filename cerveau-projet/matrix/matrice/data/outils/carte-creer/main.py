"""Point d'entree global de l'outil carte-creer (MO-430).

Role : DIRIGER (router la commande). Aucune logique metier ici.

Pose une CARTE D'IDENTITE en tete d'un document qui n'en a pas -- par la porte
ecrire uniquement (decision createur MO-430 : creer passe par la porte, le
garde de provenance -- controle attribution -- jauge chaque carte posee).

Usage :
    python main.py creer --fichier <chemin> --type <type> --appartient-a <nom>
                         [--commun true|false] [--liens "<c1>, <c2>"]
                         [--version <n>] [--date AAAA-MM-JJ] [--statut <etat>]
                         [--tags "<m1>, <m2>"] [--modele complet|minimal]
    python main.py            (cette aide, code 2)

Le MODELE de reference (matrice/templates/carte-identite) donne les champs ;
les cles obligatoires et le vocabulaire ferme viennent de la grammaire partagee
(matrice/data/commun/carte_identite.py).
"""
import sys

from creer.entry import executer_verbe

COMMANDES = {"creer": executer_verbe}
CODE_SANS_COMMANDE = 2


def principal(arguments):
    """Route vers la categorie du verbe, ou rend l'aide (code 2)."""
    if not arguments or arguments[0] not in COMMANDES:
        print(__doc__)
        return CODE_SANS_COMMANDE
    return COMMANDES[arguments[0]](arguments[1:])


if __name__ == "__main__":
    from sac_a_dos import envelopper

    sys.exit(envelopper(principal, sys.argv[1:]))
