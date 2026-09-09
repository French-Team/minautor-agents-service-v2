"""Fonctions simples de la categorie noter : une seule tache chacune."""
from datetime import datetime

from constants import SECTIONS, TAILLE_SECTION


def separer_tags(chaine_tags):
    """Transforme "a, b" en ["a", "b"] (chaine vide -> liste vide)."""
    if not chaine_tags:
        return []
    return [morceau.strip() for morceau in chaine_tags.split(",") if morceau.strip()]


def section_connue(nom):
    """Retourne True si ce nom de section est pre-declare (structure figee)."""
    return nom in SECTIONS


def deposer_activite(donnees, section, detail, tags):
    """Depose UNE activite en tete de SA section, puis applique la rotation.

    Retourne l'entree deposee.
    """
    entree = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "detail": detail,
        "tags": tags,
    }
    sections = donnees.setdefault("sections", {})
    liste = sections.setdefault(section, [])
    liste.insert(0, entree)
    del liste[TAILLE_SECTION:]
    return entree
