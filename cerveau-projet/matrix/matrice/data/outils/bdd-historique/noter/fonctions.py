"""Fonctions simples de la categorie noter : une seule tache chacune."""
from datetime import datetime

from constants import TYPE_MARQUEUR


def separer_tags(chaine_tags):
    """Transforme "a, b" en ["a", "b"] (chaine vide -> liste vide)."""
    if not chaine_tags:
        return []
    return [morceau.strip() for morceau in chaine_tags.split(",") if morceau.strip()]


def prochain_id(lignes):
    """Retourne le prochain identifiant H-XXX (maximum existant + 1)."""
    maximum = 0
    for ligne in lignes:
        identifiant = ligne.get("id", "")
        if isinstance(identifiant, str) and identifiant.startswith("H-"):
            try:
                maximum = max(maximum, int(identifiant[2:]))
            except ValueError:
                continue
    return "H-" + str(maximum + 1).zfill(3)


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
