"""Fonctions simples de l'echelon 0-1 : deposer au vrac, proposer le type.

Une seule tache chacune (convention-architecture-outils).
"""
try:
    from listes import (CHAMP_AUTO_AXES, CHAMP_AUTO_VALIDATION, MOTS_CLES_TYPES,
                       PREFIXE_ITEM, URGENCE_DEFAUT, VERDICT_NON, CHAMP_TYPE_PROPOSE,
                       MOT_CLE_DECLARE)
    from mots import mot_parcourt, mots_de
    from roles import CHAMP_ROLE, CHAMP_TITRE
    from stockage import horodater
except ImportError:  # importe comme paquet (depuis le pilote) : chemins complets
    from entonnoir.listes import (CHAMP_AUTO_AXES, CHAMP_AUTO_VALIDATION,
                                  MOTS_CLES_TYPES, PREFIXE_ITEM, URGENCE_DEFAUT,
                                  VERDICT_NON, CHAMP_TYPE_PROPOSE, MOT_CLE_DECLARE)
    from entonnoir.mots import mot_parcourt, mots_de
    from entonnoir.roles import CHAMP_ROLE, CHAMP_TITRE
    from entonnoir.stockage import horodater


def deposer_vrac(etat, theme, objectif, urgence, source, role="", verdict="",
                 axes=None, type_propose=""):
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
        # Le verdict d AUTO-VALIDATION est pose A LA CREATION (MO-175). Un verdict
        # NON RENDU se DIT (`non`) : jamais un repli muet -- la file auto-validee
        # ne doit recevoir que ce qui a ete declare, pas ce qui a ete oublie.
        CHAMP_AUTO_VALIDATION: verdict or VERDICT_NON,
        CHAMP_AUTO_AXES: axes or [],
        # Le type est PORTE (R5) : le classement le consomme au lieu de le
        # re-deviner, et la trace dit qui a parle (le crochet ou la table).
        CHAMP_TYPE_PROPOSE: type_propose,
    }
    if role:
        mission[CHAMP_ROLE] = role
    etat.setdefault("vrac", []).append(mission)
    return identifiant


def proposer_type(theme, objectif, type_declare=""):
    """PROPOSE un type : DECLARE (crochet du createur) ou par MOTS ENTIERS.

    Un type DECLARE est SOUVERAIN : il n est pas re-devine. C est ce qui
    rend le crochet utile -- `[outil]` porte `reparation`, `[audit]` porte
    `audit` : sans cela le type annonce etait seulement IMPRIME (mesure
    MO-174) et une demande sans mot-cle partait en `dev`.
    Sinon un mot-cle ne parle que s il est un mot ENTIER du texte (casse
    ignoree, pluriel simple tolere) : 'preparer' ne propose plus 'reparation'.
    Retourne (type_propose, mot_cle_trouve) ; le mot-cle vaut MOT_CLE_DECLARE
    quand le type vient d une declaration, "" si aucun mot-cle ne parle.
    """
    if type_declare:
        return type_declare, MOT_CLE_DECLARE
    mots = mots_de(theme + " " + objectif)
    for mot_cle, type_associe in MOTS_CLES_TYPES:
        if mot_parcourt(mots, mot_cle):
            return type_associe, mot_cle
    return "dev", ""


def proposer_urgence(urgence):
    """Retourne l'urgence validee (par defaut : normale)."""
    return urgence or URGENCE_DEFAUT
