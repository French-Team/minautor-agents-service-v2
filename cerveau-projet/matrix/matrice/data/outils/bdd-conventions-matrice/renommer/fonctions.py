"""Fonctions simples de la categorie renommer : une seule tache chacune."""
import re
from datetime import datetime

MOTIF_ID = re.compile(r"^[A-Z]{1,4}-[0-9]{3}$")


def id_valide(identifiant):
    """Vrai si l'identifiant respecte la forme <PREFIXE>-<NNN> (ex : CV-007)."""
    return bool(MOTIF_ID.match(identifiant or ""))


def trouver_entree(donnees, identifiant):
    """Retourne l'entree portant cet id, ou None."""
    for entree in donnees.get("conventions", []):
        if entree.get("id") == identifiant:
            return entree
    return None


def id_deja_pris(donnees, identifiant):
    """Vrai si une entree porte deja cet id (collision refusee)."""
    return trouver_entree(donnees, identifiant) is not None


def renommer_entree(donnees, ancien, nouveau):
    """Renomme l'IDENTIFIANT d'une entree et laisse la trace du renommage.

    Le contenu, les tags, la date et la source ne bougent pas : renommer
    n'est pas reecrire (lecon L-030). L'entree porte desormais d'ou elle vient.
    """
    entree = trouver_entree(donnees, ancien)
    entree["id"] = nouveau
    entree["ancien_id"] = ancien
    entree["renomme_le"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return entree
