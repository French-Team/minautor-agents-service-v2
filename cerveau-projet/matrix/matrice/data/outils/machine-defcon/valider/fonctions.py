"""Fonctions simples de la categorie valider : une seule tache chacune."""
from constants import NIVEAU_NORMAL


def verifier_validation(courant):
    """(code, message) : la validation clot def3 (defcon 3 -> 2 uniquement)."""
    if courant == 3:
        return 0, ""
    if courant == NIVEAU_NORMAL:
        return 1, "Deja au niveau normal (defcon 2) : rien a valider."
    return 1, (
        "La validation ne s'applique qu'a defcon 3 (cloture de la periode de "
        "surveillance) : courant = defcon " + str(courant) + "."
    )
