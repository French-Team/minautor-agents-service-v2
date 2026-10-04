"""Stockage des checklists : fabrique une checklist et la lit depuis la file.

NOMMAGE : stockage.py (PAS commun.py) -- pas de collision avec les modules du pilote.
Chaque fonction fait UNE chose (convention-architecture-outils).
"""
try:
    from listes import ETAPES_COMMUNES, ETAPES_PAR_TYPE, TYPES, VERIFICATIONS_COMMUNES, VERIFICATIONS_PAR_TYPE
except ImportError:  # importe comme paquet (depuis le pilote) : chemin complet
    from checklist.listes import ETAPES_COMMUNES, ETAPES_PAR_TYPE, TYPES, VERIFICATIONS_COMMUNES, VERIFICATIONS_PAR_TYPE


def fabrique_checklist(type_mission):
    """Fabrique LA checklist d'un type (commun + specifique), dans l'ordre ferme.

    Retourne une liste de chaines "E: ..." (etapes) et "V: ..." (verifications).

    Type hors liste -> les garde-fous COMMUNS seulement : la checklist n'est
    JAMAIS vide. Avant (jusqu'au 2026-09-13), un type inconnu rendait une liste
    VIDE -- six missions (MO-043 a MO-048) ont donc tourne sans AUCUN garde-fou
    (ni tests reels, ni py_compile, ni ASCII, ni fin par le pilote) sans que rien
    ne le signale. Les garde-fous communs sont communs : ils ne dependent pas du
    type. Le specifique, lui, exige toujours un type (liste fermee de l'entonnoir).
    """
    connu = type_mission in TYPES
    entrees = []
    if connu:
        for etape in ETAPES_PAR_TYPE.get(type_mission, ()):
            entrees.append("E: " + etape)
    for etape in ETAPES_COMMUNES:
        entrees.append("E: " + etape)
    if connu:
        for verification in VERIFICATIONS_PAR_TYPE.get(type_mission, ()):
            entrees.append("V: " + verification)
    for verification in VERIFICATIONS_COMMUNES:
        entrees.append("V: " + verification)
    return entrees


def checklist_de_mission(missions, identifiant):
    """Retourne la checklist enregistree de la mission, ou None si absente."""
    for mission in missions:
        if mission.get("id") == identifiant:
            return mission.get("checklist")
    return None
