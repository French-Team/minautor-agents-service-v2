"""Fonctions simples de la categorie noter : une seule tache chacune."""
from datetime import datetime

from constants import SECTIONS, TAILLE_SECTION


# CONTRAT DE TRANSPORT des listes (frictions 72 et 73) : les tags voyagent joints
# par un caractere qui vit dans son DOMICILE (data/commun/transport_listes.py) --
# cette fonction le CONSOMME au lieu de le recopier, comme les dix autres portes de
# BDD (M-076 ; L-100/L-102 : une forme recopiee derive en silence).
from transport_listes import decouper_liste  # noqa: E402


def separer_tags(chaine_tags):
    """Transforme "a, b" en ["a", "b"] -- le separateur vient de son domicile."""
    return decouper_liste(chaine_tags)


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
