"""Fonctions simples de la categorie ajouter : une seule tache chacune."""
from datetime import datetime

from constants import LARGEUR_NUMERO, PREFIXE_ID


def prochain_id(donnees):
    """Calcule l'identifiant de la prochaine entree (compteur incremente).

    Le prefixe vient de constants.py (PREFIXE_ID = CV-), jamais recopie ici.
    """
    donnees["compteur"] = donnees.get("compteur", 0) + 1
    return PREFIXE_ID + str(donnees["compteur"]).zfill(LARGEUR_NUMERO)


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
