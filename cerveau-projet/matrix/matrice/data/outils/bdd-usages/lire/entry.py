"""Categorie lire : lecture filtree de la BDD des usages.

Interface entre main.py et les fonctions simples (pas de fonctions.py ici :
2 filtres, 1 affichage -- convention action minimale).
"""
from commun import charger_lignes, extraire_options
from constants import EVENEMENTS_GARDES_JOURNAL, SEUIL_OCTETS_JOURNAL

NOMS_OPTIONS = ("outil", "tag")


def publier_capacite():
    """PUBLIE la capacite declaree du journal (MO-101 / P3 de la revue MO-098).

    La valeur appartient a l'outil (constants.py) ; l'observateur (cockpit) la
    LIT ici au lieu de comparer a un nombre ecrit chez lui. Format STABLE :
    "Capacite declaree du journal usages : <octets> octets (<n> gardes apres
    rotation)". Publiee MEME quand aucun usage ne correspond aux filtres : une
    publication qui disparait avec les donnees rendrait le controle aveugle.
    """
    print(
        "Capacite declaree du journal usages : " + str(SEUIL_OCTETS_JOURNAL)
        + " octets (" + str(EVENEMENTS_GARDES_JOURNAL) + " evenements gardes apres rotation)"
    )


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    filtre_outil = options.get("outil", "")
    filtre_tag = options.get("tag", "")

    publier_capacite()
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
        # Espion tokens (E-097) : affiche seulement quand la ligne en porte.
        tokens = ""
        if "tokens_avant" in ligne or "tokens_apres" in ligne:
            avant = ligne.get("tokens_avant", 0)
            apres = ligne.get("tokens_apres", 0)
            tokens = "  tokens " + str(avant) + " -> " + str(apres)
        print(
            ligne["date"] + "  " + ligne["outil"] + "/" + ligne["commande"]
            + "  code " + str(ligne["code"]) + duree + tokens
            + "  tags : " + ", ".join(ligne["tags"])
            + detail
        )
    print(str(len(resultats)) + " usage(s) affiche(s).")
    return 0
