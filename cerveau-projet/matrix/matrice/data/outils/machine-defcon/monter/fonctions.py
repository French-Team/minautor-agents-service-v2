"""Fonctions simples de la categorie monter : une seule tache chacune."""
from constants import NIVEAUX, NIVEAUX_MONTABLES


def verifier_montee(courant, cible):
    """(code, message) : montee libre vers le haut, sauts permis (urgence)."""
    if cible not in NIVEAUX:
        return 1, "Niveau inconnu : l'echelle fermee est 1-5 (1 reserve)."
    if cible not in NIVEAUX_MONTABLES:
        return 1, (
            "Montee interdite vers defcon " + str(cible)
            + " : cibles possibles 3-5 (2 est le retour normal, 1 est reserve)."
        )
    if cible <= courant:
        return 1, (
            "Montee interdite : defcon courant = " + str(courant)
            + ", cible = " + str(cible) + " (la montee va vers le haut)."
        )
    return 0, ""
