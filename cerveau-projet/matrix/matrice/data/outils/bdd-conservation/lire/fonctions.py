"""Fonctions de lecture du registre de conservation."""


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
        print(
            entree.get("id", "") + " [" + entree.get("statut", "") + "] "
            + entree.get("categorie", "") + " " + entree.get("verdict", "")
            + " : " + entree.get("source", "")
        )
