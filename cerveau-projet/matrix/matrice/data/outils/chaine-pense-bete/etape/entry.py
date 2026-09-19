"""Porte de la categorie ETAPE de la chaine pense-bete -> spec -> todo-list (EO-215, MO-224).

Cette categorie ne fabrique AUCUN fichier elle-meme : elle CONSOMME la porte
unique d'ecriture (data/outils/ecrire), le passage oblige du cerveau. Le VERBE
est valide ICI ; le geste vit dans fonctions.py (convention-architecture-outils).
"""
from etape.fonctions import USAGE_AVANCER, USAGE_ETAT, USAGE_NAITRE, executer_etape

VERBES = {
    "naitre": executer_etape,
    "avancer": executer_etape,
    "etat": executer_etape,
}
NOMS_OPTIONS = ("titre", "objectif", "id")


def executer(arguments):
    """Rend le code de sortie de l'outil : jamais un silence."""
    if not arguments or arguments[0] not in VERBES:
        print("Usage : " + USAGE_NAITRE)
        print("        " + USAGE_AVANCER)
        print("        " + USAGE_ETAT)
        return 2
    return VERBES[arguments[0]](arguments)
