"""Fonctions simples de la categorie corriger : une seule tache chacune."""
from datetime import datetime


def trouver_entree(donnees, identifiant):
    """L entree qui porte CET identifiant, ou None -- comparaison EXACTE, jamais un proche."""
    for entree in donnees.get("segments", []):
        if entree.get("id") == identifiant:
            return entree
    return None


def corriger_tags(entree, tags, motif):
    """Corrige les TAGS d une entree EN PLACE : rien d autre ne bouge.

    L id, la date, le segment et la source sont CONSERVES : une correction n est pas une
    reecriture, et une entree reecrite perdrait sa place dans l histoire. Les ANCIENS tags
    sont TRACES dans l entree, avec la date et le motif -- une correction qui effacerait sa
    trace se lirait comme une entree nee juste. Mesure du 2026-09-28 (MO-502) : les tags de
    RS-004 ont ete abimes a la cloture et restaient abimes, faute d un verbe de correction.
    MEME discipline que bdd-modifications.corriger (EO-155).
    """
    anciens = list(entree.get("tags", []))
    entree["tags"] = list(tags)
    entree.setdefault("corrections", []).append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "anciens_tags": anciens,
        "motif": motif,
    })
    return anciens
