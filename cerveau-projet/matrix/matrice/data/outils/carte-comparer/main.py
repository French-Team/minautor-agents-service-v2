"""Point d'entree global de l'outil carte-comparer (MO-430).

Role : DIRIGER (router la commande). Aucune logique metier ici.

Juge une carte face a SON MODELE de reference : quels champs du modele sont
PRESENTS, et la carte est-elle CONFORME (memes jugements que le garde, venant
du domicile partage carte_identite). L outil est en LECTURE seule : il ne
change rien, il REND un rapport (decision createur MO-430 : comparer dit si la
carte est presente et conforme).

Usage :
    python main.py comparer                      (sans sujet : le CORPUS entier)
    python main.py comparer --fichier <chemin> [--modele complet|minimal]
    python main.py comparer --corpus [--dans <dossier>] [--modele ...]
    python main.py            (cette aide, code 2)

Codes : 0 = conforme, 1 = ecarts, 2 = refus d usage.
"""
import sys

from comparer.entry import executer_verbe

COMMANDES = {"comparer": executer_verbe}
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
