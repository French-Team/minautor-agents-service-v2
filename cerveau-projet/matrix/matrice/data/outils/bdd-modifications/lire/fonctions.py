"""Fonctions simples de la categorie lire : une seule tache chacune."""


def filtrer(donnees, chemin=None, tag=None):
    """Retourne les fiches qui correspondent au chemin et/ou au tag.

    Aucun critere -> toutes les fiches.
    """
    resultats = {}
    for chemin_fiche, fiche in donnees.get("fichiers", {}).items():
        if chemin and chemin_fiche != chemin:
            continue
        if tag and tag not in fiche.get("tags", []):
            continue
        resultats[chemin_fiche] = fiche
    return resultats


def afficher(resultats):
    """Affiche les fiches (affichage console = le seul effet de bord assume)."""
    if not resultats:
        print("Aucune modification trouvee.")
        return
    for chemin_fiche, fiche in resultats.items():
        print(chemin_fiche + " (tags : " + ", ".join(fiche.get("tags", [])) + ")")
        for modification in fiche.get("modifications", []):
            print(
                "  ["
                + modification["date"]
                + "] "
                + modification["action"]
                + " : "
                + modification["detail"]
            )
