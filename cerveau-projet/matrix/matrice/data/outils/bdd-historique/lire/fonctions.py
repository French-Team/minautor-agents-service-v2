"""Fonctions simples de la categorie lire : une seule tache chacune."""
from constants import TYPE_MARQUEUR


def ids_obsoletes(lignes):
    """Retourne l'ensemble des ids vises par un marquage obsolete."""
    return {
        ligne.get("cible")
        for ligne in lignes
        if ligne.get("type") == TYPE_MARQUEUR and ligne.get("cible")
    }


def filtrer(lignes, type_evenement=None, tag=None, depuis=None, tout=False):
    """Retourne les evenements filtres (ACTIFS par defaut ; --tout les inclut tous).

    Les lignes de marquage obsolete (type obsolete) ne sont JAMAIS affichees :
    ce sont des marqueurs, pas des evenements.
    """
    obsoletes = ids_obsoletes(lignes)
    resultats = []
    for ligne in lignes:
        if ligne.get("type") == TYPE_MARQUEUR:
            continue
        if not tout and ligne.get("id") in obsoletes:
            continue
        if type_evenement and ligne.get("type") != type_evenement:
            continue
        if tag and tag not in ligne.get("tags", ()):
            continue
        if depuis and ligne.get("date", "") < depuis:
            continue
        resultats.append(ligne)
    return resultats


def afficher(evenements):
    """Affiche les evenements en format lisible (ASCII strict)."""
    if not evenements:
        print("Aucun evenement.")
        return
    for evenement in evenements:
        print(
            evenement["id"] + "  " + evenement["date"] + "  " + evenement["type"]
            + "  " + evenement["detail"]
            + "  [" + ", ".join(evenement.get("tags", ())) + "]"
        )
    print(str(len(evenements)) + " evenement(s) affiche(s).")
