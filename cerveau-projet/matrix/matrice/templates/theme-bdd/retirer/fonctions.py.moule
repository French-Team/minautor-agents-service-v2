"""Fonctions simples de la categorie retirer : une seule tache chacune."""


def trouver_theme(themes, identifiant, nom):
    """Cherche UN theme par id exact OU par nom (casse ignoree). Retourne (index, theme)."""
    for index, theme in enumerate(themes):
        if identifiant and theme.get("id", "") == identifiant:
            return index, theme
        if nom and theme.get("nom", "").lower() == nom.lower():
            return index, theme
    return None, None


def retirer_theme(themes, index):
    """Retire le theme a l'index donne de la liste. Retourne l'entree retiree."""
    return themes.pop(index)
