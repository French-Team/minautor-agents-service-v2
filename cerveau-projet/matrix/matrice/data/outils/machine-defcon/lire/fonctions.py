"""Fonctions simples de la categorie lire : une seule tache chacune."""
from constants import NIVEAUX, NIVEAU_NORMAL, NOMS_NIVEAUX


def composer_etat(niveau):
    """Retourne la ligne d'etat du niveau courant."""
    ligne = "defcon = " + str(niveau) + " -- " + NOMS_NIVEAUX.get(niveau, "inconnu")
    if niveau == NIVEAU_NORMAL:
        ligne = ligne + " [ETAT NORMAL]"
    return ligne


def composer_echelle():
    """Retourne les lignes de l'echelle fermee (5 = max)."""
    lignes = []
    for n in sorted(NIVEAUX, reverse=True):
        lignes.append("  defcon " + str(n) + " : " + NOMS_NIVEAUX[n])
    return lignes
