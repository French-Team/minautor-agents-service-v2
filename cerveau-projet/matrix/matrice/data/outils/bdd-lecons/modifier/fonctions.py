"""Fonctions simples de la categorie modifier : une seule tache chacune."""


def trouver_entree(donnees, identifiant):
    """Retourne (index, entree) de la lecon portant cet id, ou (None, None)."""
    for index, entree in enumerate(donnees.get("lecons", [])):
        if entree.get("id") == identifiant:
            return index, entree
    return None, None


def modifier_entree(entree, contenu, source):
    """Remplace le contenu d'UNE lecon (meme id), horodate a jour."""
    entree["lecon"] = contenu
    entree["date"] = __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if source:
        entree["source"] = source
    return entree