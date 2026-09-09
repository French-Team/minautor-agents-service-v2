"""Fonctions simples de la categorie descendre : une seule tache chacune."""
from constants import DESCENTES_PERMISES, NIVEAU_NORMAL


def verifier_descente(courant, cible):
    """(code, message) : descente stricte UN echelon a la fois (5->4, 4->3)."""
    if courant == NIVEAU_NORMAL:
        return 1, "Deja au niveau normal (defcon 2) : rien a descendre."
    if (courant, cible) in DESCENTES_PERMISES:
        return 0, ""
    if courant == 3 and cible == 2:
        return 1, "La descente 3 -> 2 passe par 'valider' (la validation clot def3)."
    return 1, (
        "Descente stricte UN echelon a la fois : permises 5 -> 4 et 4 -> 3 ; "
        "3 -> 2 = 'valider'."
    )
