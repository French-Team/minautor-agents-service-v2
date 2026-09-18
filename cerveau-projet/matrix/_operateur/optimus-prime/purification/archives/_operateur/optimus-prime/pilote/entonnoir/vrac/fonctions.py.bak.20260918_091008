"""Fonctions simples de l'echelon 0-1 : deposer au vrac, proposer le type.

Une seule tache chacune (convention-architecture-outils).
"""
try:
    from listes import MOTS_CLES_TYPES, PREFIXE_ITEM, URGENCE_DEFAUT
    from mots import mot_parcourt, mots_de
    from roles import CHAMP_ROLE, CHAMP_TITRE
    from stockage import horodater
except ImportError:  # importe comme paquet (depuis le pilote) : chemins complets
    from entonnoir.listes import MOTS_CLES_TYPES, PREFIXE_ITEM, URGENCE_DEFAUT
    from entonnoir.mots import mot_parcourt, mots_de
    from entonnoir.roles import CHAMP_ROLE, CHAMP_TITRE
    from entonnoir.stockage import horodater


def deposer_vrac(etat, theme, objectif, urgence, source, role=""):
    """Depose UNE mission brute au vrac (echelon 0) et retourne son identifiant EO-XXX.

    Le prefixe vient de listes.py PREFIXE_ITEM (CV-009 : chaque porte attribue
    le prefixe depuis ses constantes, jamais recopie).

    `theme` = le TITRE de la demande (texte libre) ; `role` = le ROLE de la
    mission, optionnel au depot (une source qui sait deja quoi il s'agit le
    donne, sinon c'est le classement qui le pose, L-061/MO-076).
    """
    etat["compteur"] = etat.get("compteur", 0) + 1
    identifiant = PREFIXE_ITEM + str(etat["compteur"]).zfill(3)
    mission = {
        "id": identifiant,
        CHAMP_TITRE: theme,
        "objectif": objectif,
        "urgence": urgence,
        "source": source,
        "deposee_le": horodater(),
    }
    if role:
        mission[CHAMP_ROLE] = role
    etat.setdefault("vrac", []).append(mission)
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
