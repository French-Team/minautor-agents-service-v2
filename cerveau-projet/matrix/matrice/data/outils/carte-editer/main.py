"""Point d'entree global de l'outil carte-editer (MO-430).

Role : DIRIGER (router la commande). Aucune logique metier ici.

Remplace la CARTE ENTIERE d un document par un nouveau front-matter fourni --
par la porte ecrire uniquement (decision createur MO-430 : editer passe par la
porte, le garde de provenance -- controle attribution -- jauge chaque carte
remplacee). Le nouveau bloc est valide par le DOMICILE (carte_identite) AVANT
toute ecriture : une carte non conforme n est jamais posee.

Usage :
    python main.py editer --fichier <chemin> --nouveau-fichier <chemin>
    python main.py            (cette aide, code 2)

Pour changer UN champ : carte-modifier. Pour poser une carte absente :
carte-creer.
"""
import sys

from editer.entry import executer_verbe

COMMANDES = {"editer": executer_verbe}
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
