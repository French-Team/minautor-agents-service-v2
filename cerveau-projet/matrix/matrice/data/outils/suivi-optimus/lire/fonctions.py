"""Fonctions simples de la categorie lire : une seule tache chacune."""


def filtrer(evenements, mission=None, action=None):
    """Retourne les evenements qui correspondent (tous si aucun filtre)."""
    resultats = list(evenements)
    if mission:
        resultats = [e for e in resultats if e.get("mission", "") == mission]
    if action:
        resultats = [e for e in resultats if e.get("action", "") == action]
    return resultats


def derniers(evenements, n):
    """Retourne les `n` derniers evenements (tous si n est nul ou absent)."""
    if not n:
        return evenements
    return evenements[-n:]


def afficher(evenements):
    """Affiche les evenements (affichage console = le seul effet de bord assume)."""
    if not evenements:
        print("Aucun evenement trouve.")
        return
    for evenement in evenements:
        morceaux = [
            str(evenement.get("date", "?")),
            "mission " + str(evenement.get("mission", "-")),
            "action " + str(evenement.get("action", "?")),
            str(evenement.get("detail", "")),
        ]
        if evenement.get("fichiers"):
            morceaux.append("fichiers [" + ", ".join(evenement["fichiers"]) + "]")
        if evenement.get("portes"):
            morceaux.append("portes [" + ", ".join(evenement["portes"]) + "]")
        if evenement.get("duree_s"):
            morceaux.append("duree " + str(evenement["duree_s"]) + "s")
        print(" | ".join(morceaux))