"""Fonctions de lecture du registre de conservation."""
from constants import CLE_LEGACY, CLE_LEGACY_LE, CLE_MOTIF_LEGACY


def filtrer(donnees, options):
    resultats = donnees.get("elements", [])
    for cle in ("tag", "categorie", "statut", "verdict", "id"):
        valeur = options.get(cle, "")
        if not valeur:
            continue
        if cle == "tag":
            resultats = [e for e in resultats if valeur in e.get("tags", [])]
        else:
            resultats = [e for e in resultats if str(e.get(cle, "")) == valeur]
    return resultats


def afficher(entrees):
    if not entrees:
        print("Aucun element trouve.")
        return
    for entree in entrees:
        # LE LEGACY SE VOIT EN LISANT (MO-431) : une decision enfouie dans le JSON
        # est une decision que personne ne lira -- `lire --id K-XXX` la REND avec
        # son motif et sa date, sans que le lecteur ait a deviner un champ.
        suffixe = ""
        if entree.get(CLE_LEGACY):
            suffixe = (" [LEGACY " + str(entree.get(CLE_LEGACY_LE, ""))
                       + " : " + str(entree.get(CLE_MOTIF_LEGACY, "")) + "]")
        print(
            entree.get("id", "") + " [" + entree.get("statut", "") + "] "
            + entree.get("categorie", "") + " " + entree.get("verdict", "")
            + " : " + entree.get("source", "") + suffixe
        )
