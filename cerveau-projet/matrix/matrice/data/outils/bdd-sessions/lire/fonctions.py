"""Fonctions simples de la categorie lire : une seule tache chacune."""


def filtrer(donnees, tag=None):
    """Retourne les entrees qui portent le tag (toutes si aucun tag)."""
    entrees = donnees.get("sessions", [])
    if not tag:
        return entrees
    return [entree for entree in entrees if tag in entree.get("tags", [])]


def afficher(entrees):
    """Affiche les entrees (affichage console = le seul effet de bord assume)."""
    if not entrees:
        print("Aucune sessions trouvee.")
        return
    for entree in entrees:
        print(
            entree["id"]
            + " [" + entree["date"] + "] "
            + "(tags : " + ", ".join(entree.get("tags", [])) + ") "
            + entree["session"]
        )
