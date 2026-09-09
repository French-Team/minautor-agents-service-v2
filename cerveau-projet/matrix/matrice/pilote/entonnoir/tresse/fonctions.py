"""Echelon 4 : la TRESSE -- file principale deterministe (le brin d'ADN).

Regle (decision createur, M-019) : URGENCES D'ABORD, puis round-robin equitable.
Lecture articulee : par PALIERS d'urgence (toutes les bloquantes, puis les hautes,
les normales, les basses) et, A L'INTERIEUR de chaque palier, round-robin entre
les files-types (aucune file ne s'etouffe). Deterministe : meme contenu = meme brin.
"""
from listes import TYPES, URGENCES
from stockage import horodater


def trier_par_urgence(missions):
    """Retourne les missions triees par urgence (bloquante -> basse), ordre stable."""
    ordre = {urgence: rang for rang, urgence in enumerate(URGENCES)}
    return sorted(missions, key=lambda m: ordre.get(m.get("urgence", "normale"), 99))


def urgence_rang(mission):
    """Retourne le rang d'urgence d'une mission (99 si inconnue : jamais en tete)."""
    return URGENCES.index(mission["urgence"]) if mission.get("urgence") in URGENCES else 99


def tresser(files_par_type):
    """TRESSE les files-types en une sequence plate et deterministe (le brin).

    Par paliers d'urgence (dans l'ordre URGENCES), round-robin entre files
    a l'interieur de chaque palier (ordre fixe : TYPES). Les files vides
    n'y laissent aucune trace.
    """
    files = {
        type_file: trier_par_urgence([dict(m) for m in missions])
        for type_file, missions in files_par_type.items()
        if missions
    }
    brin = []
    while any(files.values()):
        tetes = [missions[0] for missions in files.values() if missions]
        urgence_palier = min(tetes, key=urgence_rang)["urgence"]
        progres = True
        while progres:
            progres = False
            for type_file in TYPES:
                missions = files.get(type_file)
                if missions and missions[0].get("urgence") == urgence_palier:
                    brin.append(missions.pop(0))
                    progres = True
    return brin


def marquer_brin(brin):
    """Retourne le brin enrichi de sa position (la sequence est verifiable)."""
    return [
        dict(mission, position_brin=rang + 1, tresse_le=horodater())
        for rang, mission in enumerate(brin)
    ]
