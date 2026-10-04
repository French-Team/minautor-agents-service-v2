"""Fonctions simples de la categorie modifier : une seule tache chacune."""


def trouver_entree(donnees, identifiant):
    """Retourne (index, entree) de la lecon portant cet id, ou (None, None)."""
    for index, entree in enumerate(donnees.get("lecons", [])):
        if entree.get("id") == identifiant:
            return index, entree
    return None, None


def modifier_entree(entree, contenu, source, tags=None):
    """Modifie UNE lecon (meme id) ; horodate a jour.

    `tags` (demande createur 2026-09-26) : quand il est FOURNI, il REMPLACE les
    tags. Une lecon dont les tags sont trop SPECIFIQUES n est jamais servie -- le
    plafond classe par pertinence (tags presents dans le vocabulaire de mission),
    et mesure du 2026-09-26 : L-176 servi 71/134 missions. Un `tags` vide ou absent
    NE TOUCHE a rien (un appel sans --tags garde les anciens : on ne vide pas des
    tags par accident). Un `contenu` vide ne touche pas non plus la lecon : on peut
    donc changer les TAGS SEULS, sans reecrire le texte.
    """
    if contenu:
        entree["lecon"] = contenu
    if source:
        entree["source"] = source
    if tags:
        entree["tags"] = list(tags)
    entree["date"] = __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return entree