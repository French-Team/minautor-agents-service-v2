"""Fonctions simples de la categorie modifier : une seule tache chacune."""


def trouver_entree(donnees, identifiant):
    """Retourne l'entree portant cet id, ou None."""
    for entree in donnees.get("conventions", []):
        if entree.get("id") == identifiant:
            return entree
    return None


def modifier_entree(entree, contenu, source, tags=None):
    """Remplace le TEXTE d'une convention (elle garde SON id et sa date de creation).

    L'id ne bouge jamais : les references restent valides (pour changer un id,
    c'est la porte `renommer`). La date de creation est conservee, la mise a
    jour est horodatee a part. `tags` (liste ou None) remplace les tags
    seulement s'il est fourni.
    """
    from datetime import datetime

    entree["convention"] = contenu
    entree["modifie_le"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if source:
        entree["source"] = source
    if tags:
        entree["tags"] = tags
    return entree
