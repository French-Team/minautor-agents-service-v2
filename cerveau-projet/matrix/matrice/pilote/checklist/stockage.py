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
    Type hors liste -> liste vide (le type doit d'abord passer par l'entonnoir).
    """
    if type_mission not in TYPES:
        return []
    entrees = []
    for etape in ETAPES_PAR_TYPE.get(type_mission, ()):
        entrees.append("E: " + etape)
    for etape in ETAPES_COMMUNES:
        entrees.append("E: " + etape)
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
