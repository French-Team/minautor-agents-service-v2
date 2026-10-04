"""Fonctions simples de la categorie lire : une seule tache chacune."""


def filtrer(donnees, tag=None):
    """Retourne les lecons qui portent le tag (toutes si aucun tag)."""
    lecons = donnees.get("lecons", [])
    if not tag:
        return lecons
    return [lecon for lecon in lecons if tag in lecon.get("tags", [])]


def afficher(lecons):
    """Affiche les lecons (affichage console = le seul effet de bord assume)."""
    if not lecons:
        print("Aucune lecon trouvee.")
        return
    for lecon in lecons:
        print(
            lecon["id"]
            + " [" + lecon["date"] + "] "
            + "(tags : " + ", ".join(lecon.get("tags", [])) + ") "
            + lecon["lecon"]
        )
