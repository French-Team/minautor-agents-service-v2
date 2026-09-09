"""Fonctions simples de l'echelon 0-1 : deposer au vrac, proposer le type.

Une seule tache chacune (convention-architecture-outils).
"""
try:
    from listes import MOTS_CLES_TYPES, URGENCE_DEFAUT
    from mots import mot_parcourt, mots_de
    from stockage import horodater
except ImportError:  # importe comme paquet (depuis le pilote) : chemins complets
    from entonnoir.listes import MOTS_CLES_TYPES, URGENCE_DEFAUT
    from entonnoir.mots import mot_parcourt, mots_de
    from entonnoir.stockage import horodater


def deposer_vrac(etat, theme, objectif, urgence, source):
    """Depose UNE mission brute au vrac (echelon 0) et retourne son identifiant E-XXX."""
    etat["compteur"] = etat.get("compteur", 0) + 1
    identifiant = "E-" + str(etat["compteur"]).zfill(3)
    etat.setdefault("vrac", []).append(
        {
            "id": identifiant,
            "theme": theme,
            "objectif": objectif,
            "urgence": urgence,
            "source": source,
            "deposee_le": horodater(),
        }
    )
    return identifiant


def proposer_type(theme, objectif):
    """PROPOSE un type par regles de MOTS ENTIERS (deterministe, reclassable a la main).

    Un mot-cle ne parle que s'il est un mot entier du texte (casse ignoree,
    pluriel simple tolere) : 'preparer' ne propose plus 'reparation'.
    Retourne (type_propose, mot_cle_trouve) ; le mot-cle est "" si aucun ne parle.
    """
    mots = mots_de(theme + " " + objectif)
    for mot_cle, type_associe in MOTS_CLES_TYPES:
        if mot_parcourt(mots, mot_cle):
            return type_associe, mot_cle
    return "dev", ""


def proposer_urgence(urgence):
    """Retourne l'urgence validee (par defaut : normale)."""
    return urgence or URGENCE_DEFAUT
