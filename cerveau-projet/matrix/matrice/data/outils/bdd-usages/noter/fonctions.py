"""Fonctions simples de la categorie noter : une seule tache chacune."""
from datetime import datetime


def separer_tags(chaine_tags):
    """Transforme "a, b" en ["a", "b"] (chaine vide -> liste vide)."""
    if not chaine_tags:
        return []
    return [morceau.strip() for morceau in chaine_tags.split(",") if morceau.strip()]


def fabriquer_entree(outil, commande, code, duree, detail, tags):
    """Fabrique UNE entree d'usage {date, outil, commande, code, duree, detail, tags}."""
    entree = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "outil": outil,
        "commande": commande,
        "code": code,
        "tags": tags,
    }
    if duree is not None:
        entree["duree_ms"] = duree
    if detail:
        entree["detail"] = detail
    return entree
