"""Fonctions simples de la categorie noter : une seule tache chacune."""
from datetime import datetime


def separer_liste(chaine):
    """Transforme "a, b" en ["a", "b"] (chaine vide -> liste vide)."""
    if not chaine:
        return []
    return [morceau.strip() for morceau in chaine.split(",") if morceau.strip()]


def construire_evenement(mission, theme, action, detail, fichiers, portes, duree_s):
    """Construit UN evenement de la trace (format valide par le createur, M-084)."""
    evenement = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mission": mission,
        "theme": theme,
        "action": action,
        "detail": detail,
        "fichiers": fichiers,
        "portes": portes,
        "duree_s": duree_s,
    }
    return evenement