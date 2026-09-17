"""Fonctions simples de la categorie noter : une seule tache chacune."""
from datetime import datetime

from constants import PREFIXE_ID, TYPE_MARQUEUR


# CONTRAT DE TRANSPORT des listes (frictions 72 et 73) : les tags voyagent joints
# par un caractere qui vit dans son DOMICILE (data/commun/transport_listes.py) --
# cette fonction le CONSOMME au lieu de le recopier, comme les dix autres portes de
# BDD (M-076 ; L-100/L-102 : une forme recopiee derive en silence).
from transport_listes import decouper_liste  # noqa: E402


def separer_tags(chaine_tags):
    """Transforme "a, b" en ["a", "b"] -- le separateur vient de son domicile."""
    return decouper_liste(chaine_tags)


def prochain_id(lignes):
    """Retourne le prochain identifiant H-XXX (maximum existant + 1).

    Le prefixe vient de constants.py PREFIXE_ID (CV-009), et la lecture d'un id
    existant se fait sur la MEME longueur que lui : recopier "H-" et "[2:]" a
    cote d'une constante, c'est deux verites qui peuvent diverger.
    """
    maximum = 0
    for ligne in lignes:
        identifiant = ligne.get("id", "")
        if isinstance(identifiant, str) and identifiant.startswith(PREFIXE_ID):
            try:
                maximum = max(maximum, int(identifiant[len(PREFIXE_ID):]))
            except ValueError:
                continue
    return PREFIXE_ID + str(maximum + 1).zfill(3)


def ids_obsoletes(lignes):
    """Retourne l'ensemble des ids vises par un marquage obsolete (ajout seul)."""
    vises = set()
    for ligne in lignes:
        if ligne.get("type") == TYPE_MARQUEUR and ligne.get("cible"):
            vises.add(ligne["cible"])
    return vises


def est_doublon_actif(lignes, type_evenement, detail):
    """Retourne True si un evenement ACTIF porte deja ce type + ce detail."""
    obsoletes = ids_obsoletes(lignes)
    for ligne in lignes:
        if ligne.get("id") in obsoletes:
            continue
        if ligne.get("type") == type_evenement and ligne.get("detail") == detail:
            return True
    return False


def fabriquer_entree(identifiant, type_evenement, detail, tags):
    """Fabrique UNE entree d'evenement {id, date, type, detail, tags}."""
    return {
        "id": identifiant,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": type_evenement,
        "detail": detail,
        "tags": tags,
    }
