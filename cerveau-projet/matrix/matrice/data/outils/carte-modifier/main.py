"""Point d'entree global de l'outil carte-modifier (MO-430).

Role : DIRIGER (router la commande). Aucune logique metier ici.

Change UN champ de la carte d un document (valeur remplacee, champ insere s il
absente, champ retire avec --supprimer) -- par la porte ecrire uniquement
(decision createur MO-430 : modifier passe par la porte, le garde de
provenance -- controle attribution -- jauge chaque carte modifiee). Le bloc
RESULTAT est valide par le DOMICILE (carte_identite) AVANT toute ecriture.

Usage :
    python main.py modifier --fichier <chemin> --cle <nom> --valeur <valeur>
    python main.py modifier --fichier <chemin> --cle <nom> --supprimer
    python main.py            (cette aide, code 2)

Pour remplacer la carte ENTIERE : carte-editer. Pour poser une carte absente :
carte-creer.
"""
import sys

from modifier.entry import executer_verbe

COMMANDES = {"modifier": executer_verbe}
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
