"""Categorie lire : lecture filtree de la BDD des usages.

Interface entre main.py et les fonctions simples (pas de fonctions.py ici :
2 filtres, 1 affichage -- convention action minimale).
"""
from commun import charger_lignes, extraire_options

NOMS_OPTIONS = ("outil", "tag")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    filtre_outil = options.get("outil", "")
    filtre_tag = options.get("tag", "")

    lignes = charger_lignes()
    resultats = [
        ligne
        for ligne in lignes
        if (not filtre_outil or ligne.get("outil") == filtre_outil)
        and (not filtre_tag or filtre_tag in ligne.get("tags", []))
    ]

    if not resultats:
        print("Aucun usage ne correspond aux filtres.")
        return 0

    for ligne in resultats:
        duree = (" " + str(ligne["duree_ms"]) + " ms") if "duree_ms" in ligne else ""
        detail = ("  DETAIL : " + ligne["detail"]) if ligne.get("detail") else ""
        print(
            ligne["date"] + "  " + ligne["outil"] + "/" + ligne["commande"]
            + "  code " + str(ligne["code"]) + duree
            + "  tags : " + ", ".join(ligne["tags"])
            + detail
        )
    print(str(len(resultats)) + " usage(s) affiche(s).")
    return 0
