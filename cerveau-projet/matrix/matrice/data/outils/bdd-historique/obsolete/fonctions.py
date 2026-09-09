"""Fonctions simples de la categorie marquer-obsolete : une seule tache chacune."""
from datetime import datetime

from constants import TYPE_MARQUEUR


def id_existe(lignes, identifiant):
    """Retourne True si cet identifiant d'evenement existe dans le journal."""
    return any(ligne.get("id") == identifiant for ligne in lignes)


def deja_obsolete(lignes, identifiant):
    """Retourne True si cet identifiant est deja vise par un marquage."""
    return any(
        ligne.get("type") == TYPE_MARQUEUR and ligne.get("cible") == identifiant
        for ligne in lignes
    )


def fabriquer_marqueur(identifiant, cible, motif):
    """Fabrique UN marquage obsolete (SUR AJOUT : la cible n'est jamais reecrite)."""
    marqueur = {
        "id": identifiant,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": TYPE_MARQUEUR,
        "cible": cible,
        "tags": ["obsolete"],
    }
    if motif:
        marqueur["motif"] = motif
    return marqueur
