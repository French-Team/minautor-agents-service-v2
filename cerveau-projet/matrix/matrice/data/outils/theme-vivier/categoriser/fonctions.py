"""Fonctions simples de la categorie categoriser : une seule tache chacune."""


def trouver_theme(themes, identifiant):
    """Retourne le theme portant cet id (TH-XXX), ou None si inconnu."""
    for theme in themes:
        if theme.get("id") == identifiant:
            return theme
    return None


def categoriser_theme(donnees, identifiant, categorie):
    """Met a jour la categorie du theme de cet id (en place). Retourne (entree, message)."""
    theme = trouver_theme(donnees.get("themes", ()), identifiant)
    if theme is None:
        return None, "Theme inconnu : " + identifiant
    theme["categorie"] = categorie
    return theme, ""
