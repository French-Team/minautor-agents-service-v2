"""Fonctions simples de la categorie lire : une seule tache chacune."""


def filtrer(donnees, nom=None, categorie=None):
    """Retourne les themes filtres par nom (casse ignoree) ET/OU par categorie."""
    themes = donnees.get("themes", [])
    if nom:
        nom_bas = nom.lower()
        themes = [theme for theme in themes if theme.get("nom", "").lower() == nom_bas]
    if categorie:
        categorie_haute = categorie.upper()
        themes = [theme for theme in themes if theme.get("categorie", "").upper() == categorie_haute]
    return themes


def afficher(themes):
    """Affiche les themes (affichage console = le seul effet de bord assume)."""
    if not themes:
        print("Aucun theme trouve.")
        return
    for theme in themes:
        print(
            theme["id"]
            + " [" + theme.get("categorie", "sans-categorie") + "] "
            + theme["nom"] + " -- " + theme["but"]
            + (" (" + theme["description"] + ")" if theme.get("description") else "")
        )
