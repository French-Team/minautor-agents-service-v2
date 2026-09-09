"""Fonctions simples de la categorie bilan : une seule tache chacune."""
from datetime import datetime, timedelta

from constants import LIMITE_LIGNES, TOP_USAGES
from commun import dans_periode, horodatage, lire_json, lire_jsonl


def collecter_missions(chemin, borne):
    """Retourne les missions terminees dans la periode (les plus recentes d'abord)."""
    missions = [m for m in lire_jsonl(chemin) if dans_periode(m.get("date"), borne)]
    missions.reverse()
    return missions


def collecter_usages(chemin, borne):
    """Retourne (total, top) : top des appels avec codes et durees (moy, max)."""
    usages = [u for u in lire_jsonl(chemin) if dans_periode(u.get("date"), borne)]
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
    transitions = [
        t for t in lire_jsonl(chemin) if dans_periode(t.get("quand"), borne)
    ]
    transitions.reverse()
    return transitions


def afficher_bilan(nom_periode, heures, missions, usages, activites, transitions):
    """Affiche le bilan complet de la periode (presentation uniquement)."""
    borne = datetime.now() - timedelta(hours=heures)
    print("=== BILAN -- periode : " + nom_periode + " (depuis " + borne.strftime("%Y-%m-%d %H:%M:%S") + ") ===")

    print("Missions terminees : " + str(len(missions)))
    for m in missions[:LIMITE_LIGNES]:
        print("  " + str(m.get("id")) + " (" + str(m.get("theme")) + ") -- " + str(m.get("date")))

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
