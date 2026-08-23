# -*- coding: ascii -*-
"""fonctions/score.py - UNE tache : le score numerique des agents (v0.2.0).

Score sur 100 : depart 50, chaque penalite -1, chaque felicitation +1.
Le score sert a IDENTIFIER les agents a problemes pour qu'ils soient repares.
"""

import json
import os
import sys
from datetime import datetime

_sys_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "..", "os_path", "fonctions")
sys.path.insert(0, _sys_dir)
from racine import trouver_racine

RACINE = trouver_racine(__file__)
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "..", "notes-agents.jsonl")

SCORE_DEPART = 50
BORNE_BASSE = 0
BORNE_HAUTE = 100
DELTA_PENALITE = -1
DELTA_FELICITATION = +1
SEUIL_PROBLEMES = 40  # sous ce score : agent a reparer

NOTATEURS = ["stark", "jarvis", "fury", "rogers", "utilisateur"]


def evenements(agent=None):
    """Tous les evenements de notation (filtres par agent optionnel)."""
    if not os.path.isfile(DATA_FILE):
        return []
    resultats = []
    with open(DATA_FILE, encoding="utf-8") as f:
        for ligne in f:
            try:
                e = json.loads(ligne)
            except ValueError:
                continue
            # ignorer les anciennes entrees a paliers (format v0.1.0)
            if e.get("type") in ("penalite", "felicitation"):
                if agent is None or e.get("agent") == agent:
                    resultats.append(e)
    return resultats


def score(agent):
    """Score courant d'un agent : depart 50 + somme des deltas."""
    total = SCORE_DEPART
    for e in evenements(agent):
        total += e.get("delta", 0)
    return max(BORNE_BASSE, min(BORNE_HAUTE, total))


def enregistrer(type_event, agent, motif, par):
    """Enregistrer un evenement. Retourne (entree, erreur)."""
    if type_event not in ("penalite", "felicitation"):
        return None, "type invalide (penalite ou felicitation)"
    if not motif or len(motif.strip()) < 5:
        return None, "motif obligatoire (min 5 caracteres)"
    delta = DELTA_PENALITE if type_event == "penalite" else DELTA_FELICITATION
    avant = score(agent)
    entree = {
        "date": datetime_now(),
        "type": type_event,
        "agent": agent,
        "delta": delta,
        "score_avant": avant,
        "score_apres": avant + delta,
        "motif": motif.strip(),
        "par": par,
    }
    with open(DATA_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entree, ensure_ascii=False) + "\n")
    return entree, None


def datetime_now():
    from datetime import datetime
    return datetime.now().isoformat(timespec="seconds")


def problemes(seuil=None):
    """Agents sous le seuil de problemes."""
    seuil = SEUIL_PROBLEMES if seuil is None else seuil
    vus = set(e["agent"] for e in evenements())
    return [(a, score(a)) for a in sorted(vus) if score(a) < seuil]


def generer_suivi(agent):
    """Fichier de suivi par agent : POURQUOI ses points (protocole 17)."""
    from pathlib import Path
    rapports = Path(RACINE) / "cerveau-projet" / "freelance" / "edith" / "rapports"
    rapports.mkdir(parents=True, exist_ok=True)
    date = datetime.now().strftime("%Y%m%d-%H%M")
    chemin = rapports / f"suivi-{agent}-{date}.md"
    lignes = [
        f"# Suivi de score -- {agent}",
        "",
        "| Champ | Valeur |",
        "|---|---|",
        f"| Date | {datetime.now().isoformat(timespec='seconds')} |",
        f"| Score actuel | {score(agent)}/100 |",
        f"| Revision requise | {'OUI' if score(agent) < SEUIL_PROBLEMES else 'NON'} |",
        "",
        "| Date | Type | Delta | Score apres | Motif | Par |",
        "|---|---|---|---|---|---|"]
    events = evenements(agent)
    for e in events:
        lignes.append("| {} | {} | {} | {} | {} | {} |".format(
            e["date"][:10], e["type"], e["delta"], e["score_apres"],
            e["motif"], e["par"]))
    if not events:
        lignes.append("| - | aucun evenement | - | - | - | - |")
    chemin.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    return str(chemin)
