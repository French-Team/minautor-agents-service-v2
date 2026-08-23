# -*- coding: ascii -*-
"""fonctions/missions.py - UNE tache : lancer des missions en SERIE ou
PARALLEL (protocole 13 v2 / demande utilisateur).

SERIE    : chaque activation attend la fin de la precedente (controle).
PARALLEL : les activations partent simultanement (aucune collision).

LIMITATION HONNETE : l'ANALYSE de collision reste un jugement LLM
(JARVIS choisit le mode) ; l'outil n'execute que le lancement et
collecte les resultats.
"""

import json
import subprocess
import sys
import time
from pathlib import Path

from racine import trouver_racine

RACINE = Path(trouver_racine(__file__))
JARVIS_CLI = RACINE / "cerveau-projet" / "freelance" / "tools-commun" / \
    "jarvis" / "jarvis.py"


def _lancer_activation(agent, mission, session, de):
    """Activer un agent via le CLI jarvis (sous-processus)."""
    return subprocess.run(
        [sys.executable, str(JARVIS_CLI), "activer",
         "--agent", agent, "--session", session,
         "--mission", mission, "--de", de],
        capture_output=True, text=True, cwd=str(RACINE), timeout=60)


def lancer(fichier_scenario):
    """Executer un scenario {session, mode, missions:[{agent, mission}]}.
    Retourne le rapport machine-lisible."""
    try:
        scenario = json.loads(Path(fichier_scenario).read_text(
            encoding="utf-8"))
    except (OSError, ValueError) as e:
        return {"statut": "ERREUR", "reponse": f"scenario invalide: {e}"}

    session = scenario.get("session", "")
    mode = scenario.get("mode", "serie")
    missions = scenario.get("missions", [])
    if not session or not missions:
        return {"statut": "ERREUR",
                "reponse": "session et missions obligatoires"}

    resultats = []
    if mode == "serie":
        # SERIE : strictement sequentiel - chaque activation est terminee
        # avant la suivante (cas : l'agent suivant controle le precedent)
        for i, m in enumerate(missions, 1):
            p = _lancer_activation(m["agent"], m["mission"], session,
                                   scenario.get("de", "stark"))
            resultats.append({"ordre": i, "agent": m["agent"], "rc": p.returncode})
    else:
        # PARALLEL : tous les lancements partent ensemble (aucune collision)
        processus = []
        for i, m in enumerate(missions, 1):
            processus.append((i, m["agent"],
                              _lancer_activation(m["agent"], m["mission"],
                                                 session,
                                                 scenario.get("de", "stark"))))
        for i, agent, p in processus:
            resultats.append({"ordre": i, "agent": agent, "rc": p.returncode})

    echecs = [r["agent"] for r in resultats if r["rc"] != 0]
    return {
        "statut": "PASSE" if not echecs else "PARTIEL/ECHOUE",
        "mode": mode,
        "session": session,
        "resultats": resultats,
        "limite": ("mecanique uniquement : le CHOIX du mode (collision "
                   "ou non) reste une decision JARVIS/LLM. En PARALLEL, "
                   "les activations concurrentes ecrivent le bloc "
                   "session AGENTS.md : dernier ecrivain gagne"),
    }
