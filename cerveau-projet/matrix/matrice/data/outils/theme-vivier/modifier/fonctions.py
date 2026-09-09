"""Fonctions simples de la categorie modifier : une seule tache chacune."""
from datetime import datetime


def trouver_theme(donnees, identifiant):
    """Retourne (index, theme) par id EXACT ou nom (casse ignoree), ou (None, None)."""
    for index, theme in enumerate(donnees.get("themes", [])):
        if theme.get("id") == identifiant:
            return index, theme
    identifiant_bas = identifiant.lower()
    for index, theme in enumerate(donnees.get("themes", [])):
        if theme.get("nom", "").lower() == identifiant_bas:
            return index, theme
    return None, None


def modifier_theme(theme, but, description, categorie):
    """Met a jour les champs fournis du theme (meme id). Horodate a jour."""
    if but:
        theme["but"] = but
    if description is not None:
        theme["description"] = description
    if categorie:
        theme["categorie"] = categorie
    theme["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return theme