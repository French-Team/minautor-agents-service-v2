"""Fonctions simples de la categorie ajouter : une seule tache chacune."""
from datetime import datetime


def separer_tags(chaine_tags):
    """Transforme "a, b" en ["a", "b"] (chaine vide -> liste vide)."""
    if not chaine_tags:
        return []
    return [morceau.strip() for morceau in chaine_tags.split(",") if morceau.strip()]


def prochain_id(donnees):
    """Calcule l'identifiant de la prochaine entree (compteur incremente)."""
    donnees["compteur"] = donnees.get("compteur", 0) + 1
    return "C-" + str(donnees["compteur"]).zfill(3)


def ajouter_entree(donnees, contenu, tags, source):
    """Ajoute UNE entree taguee a la liste. Ne touche a rien d'autre."""
    entree = {
        "id": prochain_id(donnees),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "convention": contenu,
        "tags": tags,
        "source": source,
    }
    donnees.setdefault("conventions", []).append(entree)
    return entree
