"""Fonctions simples de la categorie lire : une seule tache chacune."""
# LA REGLE ASCII VIT A SON DOMICILE (EO-365 / MO-466) : la recherche normalise la
# CLE comme l ecriture la pose (M-076 ; L-029).
from texte_ascii import vers_ascii  # noqa: E402


def filtrer(donnees, chemin=None, tag=None):
    """Retourne les fiches qui correspondent au chemin et/ou au tag.

    Aucun critere -> toutes les fiches.
    """
    # LA RECHERCHE NORMALISE LA CLE COMME L ECRITURE LA POSE (EO-365 / MO-466) :
    # chercher un tag, c est chercher SA FORME ASCII -- sinon une cle ecrite avec un
    # accent resterait introuvable par son propre nom (mesure du 2026-09-22).
    tag = vers_ascii(tag) if tag else tag
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
