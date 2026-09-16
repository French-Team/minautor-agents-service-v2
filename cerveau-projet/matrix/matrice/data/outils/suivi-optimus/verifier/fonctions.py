"""Fonctions simples de la categorie verifier : une seule tache chacune.

Coherence debut/fin (marbre suivi-optimus) : chaque mission a 1 debut + 1 fin.
"""
from collections import defaultdict

MARBRE_DATE = "2026-09-11 19:00:00"  # decree marbre, avant = legacy
# Missions de reprise : doublon volontaire documente (meme M-XX traitee sur 2 sessions, 2 debut + 2 fin legitimes).
REPRISES_DOUBLON_OK = {"M-115"}


def verifier_coherence(evenements):
    """Verifie la coherence debut/fin du journal (marbre, Flux 2).

    Retourne (ok, messages, stats) avec stats = {orphelines, doublons, ouvertes}.
    - orpheline : fin sans debut
    - doublon   : >1 debut ou >1 fin pour la meme mission
    - ouverte   : debut sans fin (mission en cours, normal si recente)
    Les missions avant MARBRE_DATE sont comptees comme legacy (signalees mais
    n'entrainent pas d'ECART bloqueur - elles ont ete ecrites avant le garde
    anti-fin-orpheline). Seules les missions >= MARBRE_DATE bloquent.
    """
    par_mission = defaultdict(list)
    for ev in evenements:
        mid = ev.get("mission", "")
        if not mid:
            continue
        par_mission[mid].append(ev)
    orphelines = []
    orphelines_legacy = []
    doublons = []
    ouvertes = []
    for mission, lst in par_mission.items():
        deb = sum(1 for e in lst if e.get("action") == "debut")
        fin = sum(1 for e in lst if e.get("action") == "fin")
        if fin > 0 and deb == 0:
            # date de la fin pour filtrer legacy
            dates_fin = [e.get("date", "") for e in lst if e.get("action") == "fin"]
            plus_ancienne = min(dates_fin) if dates_fin else ""
            if plus_ancienne and plus_ancienne < MARBRE_DATE:
                orphelines_legacy.append(mission)
            else:
                orphelines.append(mission)
        elif deb > 1 or fin > 1:
            if mission in REPRISES_DOUBLON_OK and deb == 2 and fin == 2:
                # Reprise documentee : 2 sessions, pas un ECART.
                continue
            doublons.append((mission, deb, fin))
        elif deb == 1 and fin == 0:
            ouvertes.append(mission)
    messages = []
    ok = True
    if orphelines:
        ok = False
        messages.append("ECART : " + str(len(orphelines)) + " fin(s) sans debut (>= marbre) : " + ", ".join(sorted(orphelines)[:10]) + (" ..." if len(orphelines) > 10 else ""))
    if orphelines_legacy:
        messages.append("LEGACY : " + str(len(orphelines_legacy)) + " fin(s) sans debut (avant marbre " + MARBRE_DATE + ") : " + ", ".join(sorted(orphelines_legacy)[:10]) + (" ..." if len(orphelines_legacy) > 10 else ""))
    if doublons:
        ok = False
        details = ", ".join(m + "(" + str(d) + "/" + str(f) + ")" for m, d, f in doublons[:10])
        messages.append("ECART : " + str(len(doublons)) + " doublon(s) debut/fin : " + details)
    if ouvertes:
        messages.append("INFO : " + str(len(ouvertes)) + " mission(s) ouverte(s) (debut sans fin) : " + ", ".join(sorted(ouvertes)[:10]) + (" ..." if len(ouvertes) > 10 else ""))
    if ok and not orphelines_legacy:
        messages.append("Coherence debut/fin : OK (0 orpheline, 0 doublon, " + str(len(ouvertes)) + " ouverte(s))")
    elif ok:
        messages.append("Coherence debut/fin : OK pour le marbre (>= " + MARBRE_DATE + ")")
    stats = {"orphelines": orphelines, "orphelines_legacy": orphelines_legacy, "doublons": doublons, "ouvertes": ouvertes}
    return ok, messages, stats


def verifier_integrite(empreinte_reelle, empreinte_enregistree):
    """Compare l'empreinte recalculee a l'empreinte enregistree (etalon-or).

    Retourne (succes, message) : le message dit ce qui casse, ou pourquoi.
    """
    if empreinte_reelle is None:
        return (False, "ECART : la BDD est absente ou illisible a l'emplacement attendu.")
    if empreinte_enregistree is None:
        return (False, "ECART : aucune empreinte enregistree (la BDD n'a jamais ete ecrite par l'outil).")
    if empreinte_reelle == empreinte_enregistree:
        return (True, "Integrite verifiee : empreinte " + empreinte_reelle[:16] + "...")
    return (
        False,
        "ECART : empreinte reelle "
        + empreinte_reelle[:16]
        + "... != enregistree "
        + empreinte_enregistree[:16]
        + "... (la BDD a ete modifiee hors de l'outil).",
    )
