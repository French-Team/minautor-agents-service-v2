"""Fonctions simples des echelons 1-2 : classer, proposer la categorie.

Une seule tache chacune (convention-architecture-outils).
"""
from listes import CATEGORIES, CATEGORIES_DEFAUT, MOTS_CLES_CATEGORIES, TYPES
from mots import mot_parcourt, mots_de
from stockage import horodater


def proposer_categorie(theme, objectif):
    """PROPOSE une categorie par MOTS ENTIERS (deterministe, reclassable a la main).

    Retourne (categorie_proposee, mot_cle_trouve) ; "" si aucun mot-cle ne parle.
    """
    mots = mots_de(theme + " " + objectif)
    for mot_cle, categorie_associee in MOTS_CLES_CATEGORIES:
        if mot_parcourt(mots, mot_cle):
            return categorie_associee, mot_cle
    return "", ""


def mission_du_vrac(etat, identifiant):
    """Retourne la mission E-XXX du vrac, ou None (une seule tache : chercher)."""
    for mission in etat.get("vrac", []):
        if mission.get("id") == identifiant:
            return mission
    return None


def classer_mission(etat, identifiant, type_cible, categorie_explicite):
    """Classe la mission E-XXX du vrac vers SA file-type (echelons 1-2).

    Type FERME (code 2) ; categorie : explicite (souveraine, verifiee contre
    la liste fermee) ou PROPOSEE par mots entiers (M-027) quand le createur
    ne la precise pas -- la proposition n'est gardee que si elle appartient
    aux categories du type, sinon categorie par defaut du type.
    Mission inconnue : code 1 (les listes sont toujours validees AVANT la
    recherche, lecon M-018). Retourne (code, message).
    """
    if type_cible not in TYPES:
        return 2, "Type inconnu : " + repr(type_cible) + " (types fermes : " + ", ".join(TYPES) + ")"
    categories_du_type = CATEGORIES.get(type_cible, ())
    if categorie_explicite:
        categorie_cible = categorie_explicite
    else:
        mission_trouvee = mission_du_vrac(etat, identifiant)
        if mission_trouvee is None:
            categorie_cible = categorie_par_defaut(type_cible)
        else:
            proposee, _ = proposer_categorie(mission_trouvee.get("theme", ""), mission_trouvee.get("objectif", ""))
            categorie_cible = proposee if proposee in categories_du_type else categorie_par_defaut(type_cible)
    if categorie_cible not in categories_du_type:
        return 2, (
            "Categorie inconnue pour " + type_cible + " : " + repr(categorie_cible)
            + " (categories fermees : " + ", ".join(categories_du_type) + ")"
        )
    vrac = etat.get("vrac", [])
    for position, mission in enumerate(vrac):
        if mission.get("id") == identifiant:
            mission_classee = dict(mission)
            mission_classee["type"] = type_cible
            mission_classee["categorie"] = categorie_cible
            mission_classee["classee_le"] = horodater()
            etat.setdefault("files", {}).setdefault(type_cible, []).append(mission_classee)
            del vrac[position]
            return 0, (
                "Mission " + identifiant + " classee : type " + type_cible
                + ", categorie " + categorie_cible + "."
            )
    return 1, "Mission inconnue au vrac : " + identifiant


def categorie_par_defaut(type_cible):
    """Retourne la categorie par defaut de ce type (toujours dans la liste fermee)."""
    return CATEGORIES_DEFAUT.get(type_cible, "autre")
