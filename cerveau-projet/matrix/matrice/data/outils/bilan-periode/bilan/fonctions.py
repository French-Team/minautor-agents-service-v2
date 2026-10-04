"""Fonctions simples de la categorie bilan : une seule tache chacune.

Optimisation M-130 (TH-023) : les 3 journaux JSONL append-only sont lus
EN SENS INVERSE avec break precoce (lire_jsonl_depuis) : 4.4x sur 6h,
17x sur 1h (mesures reelles, journal trie par date croissante).
"""
from datetime import datetime, timedelta

from constants import BUDGET_PASSE_MS, LIMITE_LIGNES, TOP_USAGES
from commun import dans_periode, horodatage, lire_json, lire_jsonl, lire_jsonl_depuis


def collecter_missions(chemin, borne):
    """Retourne les missions terminees dans la periode (les plus recentes d'abord)."""
    missions = lire_jsonl_depuis(chemin, borne, "date")
    missions.reverse()
    return missions


def collecter_missions_par_source(sources, borne):
    """Retourne {etiquette: missions de la periode}, sources vides exclues.

    PLUSIEURS AVAL : chaque flux a le sien (cameleon / optimus), crees expres
    pour ne pas melanger les historiques. `[bilan]` les lit TOUS : n'en lire
    qu'un seul fait annoncer "0 mission" des qu'un autre flux travaille (constat
    MO-061 : 15 missions d'Optimus le 2026-09-13, bilan annoncant 0). On
    ETIQUETTE chaque source, jamais de fusion anonyme : le lecteur doit voir
    d'ou vient chaque mission.
    """
    par_source = {}
    for etiquette, chemin in sources:
        missions = collecter_missions(chemin, borne)
        if missions:
            par_source[etiquette] = missions
    return par_source


def collecter_usages(chemin, borne):
    """Retourne (total, top) : top des appels avec codes et durees (moy, max)."""
    usages = lire_jsonl_depuis(chemin, borne, "date")
    stats = {}
    for u in usages:
        cle = str(u.get("outil", "?")) + " " + str(u.get("commande", "?"))
        s = stats.setdefault(cle, {"n": 0, "codes": {}, "durees": []})
        s["n"] += 1
        code = u.get("code", "?")
        s["codes"][code] = s["codes"].get(code, 0) + 1
        duree = u.get("duree_ms")
        if isinstance(duree, int):
            s["durees"].append(duree)
    top = sorted(stats.items(), key=lambda paire: (-paire[1]["n"], paire[0]))[:TOP_USAGES]
    return len(usages), top


def collecter_activites(chemin, borne):
    """Retourne {section: items de la periode}, sections vides exclues."""
    donnees = lire_json(chemin, {"sections": {}})
    par_section = {}
    for nom, items in donnees.get("sections", {}).items():
        if not isinstance(items, list):
            continue
        retenus = [i for i in items if dans_periode(i.get("date"), borne)]
        if retenus:
            par_section[nom] = retenus
    return par_section


def collecter_defcon(chemin, borne):
    """Retourne les transitions defcon dans la periode (les plus recentes d'abord)."""
    transitions = lire_jsonl_depuis(chemin, borne, "quand")
    transitions.reverse()
    return transitions


def afficher_bilan(nom_periode, heures, missions_par_source, usages, activites, transitions):
    """Affiche le bilan complet de la periode (presentation uniquement)."""
    borne = datetime.now() - timedelta(hours=heures)
    print("=== BILAN -- periode : " + nom_periode + " (depuis " + borne.strftime("%Y-%m-%d %H:%M:%S") + ") ===")
    # La duree de reference est PUBLIEE par l'outil, pas ecrite chez l'observateur
    # (MO-100) : le cockpit lit cette ligne au lieu de comparer a un nombre qu'il
    # possederait lui-meme. Format STABLE : "Budget declare de l'outil : <n> ms".
    print("Budget declare de l'outil : " + str(BUDGET_PASSE_MS) + " ms")

    total = sum(len(ms) for ms in missions_par_source.values())
    detail = ", ".join(e + " " + str(len(ms)) for e, ms in sorted(missions_par_source.items()))
    print("Missions terminees : " + str(total) + ((" (" + detail + ")") if detail else ""))
    for etiquette, ms in sorted(missions_par_source.items()):
        for m in ms[:LIMITE_LIGNES]:
            print("  [" + etiquette + "] " + str(m.get("id")) + " (" + str(m.get("theme")) + ") -- " + str(m.get("date")))

    total_usages, top = usages
    print("Usages d'outils : " + str(total_usages) + " appel(s)")
    for nom, s in top:
        codes = ", ".join(str(c) + " x" + str(n) for c, n in sorted(s["codes"].items()))
        durees = s["durees"]
        if durees:
            codes += ", duree moy " + str(sum(durees) // len(durees)) + " ms, max " + str(max(durees)) + " ms"
        print("  " + nom + " x" + str(s["n"]) + " (" + codes + ")")

    if activites:
        print("Activites recentes :")
        for nom, items in activites.items():
            print("  " + nom + " : " + str(len(items)) + " evenement(s)")
            for i in items[:2]:
                print("    " + str(i.get("date")) + " -- " + str(i.get("detail"))[:100])
    else:
        print("Activites recentes : aucune dans la periode.")

    print("Transitions defcon : " + str(len(transitions)))
    for t in transitions[:LIMITE_LIGNES]:
        print(
            "  " + str(t.get("de")) + " -> " + str(t.get("vers"))
            + " -- " + str(t.get("quand")) + " (" + str(t.get("raison"))[:60] + ")"
        )
    return 0
