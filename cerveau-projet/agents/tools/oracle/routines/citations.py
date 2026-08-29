#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
routine citations -- Repere visuel v1 (session-admin).

Toutes les 5 minutes (intervalle defini dans manifest.json), une citation
d un dieu grec est historisee dans le tableau Activites recentes v1
(AGENTS-activite-recente.md) : preuve visuelle que le serveur de routines
tourne en arriere-plan.

Univers v1 = dieux grecs (la v2 utilise les heros Marvel - 2 univers
distincts, decision utilisateur 2026-08-27 : on s inspire de la v2 mais
on ne recupere pas son code).

TEMPORAIRE (marqueur manifest.json) : desactivee en production
(actif=false) - la routine sera retiree en fin de dev (Hygie pourra
purger script + entree manifest).

Usage:
    python3 citations.py

Retour: 0 si succes, 1 si erreur.
"""

import json
import os
import random
import sys
from pathlib import Path

VERSION = "0.2.0"

_DOSSIER = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = Path(_DOSSIER) / "data" / "citations-grecques.json"


def _charger_citations():
    """Charger la liste des citations (dieu, phrase) depuis le JSON."""
    if not DATA_FILE.is_file():
        return []
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        return data.get("citations", [])
    except (ValueError, OSError):
        return []


def _racine_projet():
    """Racine du projet (la ou vivent AGENTS-historique.md et
    AGENTS-activite-recente.md). Remonte depuis routines/ jusqu a trouver
    le fichier historique. Independant du cwd (le daemon lance ce script
    avec cwd=routines/)."""
    racine = Path(_DOSSIER)
    while not (racine / "AGENTS-historique.md").is_file():
        if racine.parent == racine:
            return Path.cwd()
        racine = racine.parent
    return racine


def _historiser_agent(agent, raison, type_action="R"):
    """Historiser via activer-agent-principal (meme canal que l activite
    des agents : corps historique + encart activites recentes v1 + BDD).
    La session est session-admin (l encart v1 est celui de la session-admin,
    decision utilisateur 2026-08-26 : chaque session a SES fichiers).
    Les chemins AGENTS_* sont forces en ABSOLU (le daemon lance ce script
    avec cwd=routines/, un chemin relatif ecrirait au mauvais endroit)."""
    import importlib.util
    import os as _os

    aap_path = Path(_DOSSIER).parent.parent / "activer" / \
        "activer-agent-principal" / "activer-agent-principal.py"
    if not aap_path.exists():
        return False
    racine = _racine_projet()
    _os.environ["AGENTS_HISTORIQUE"] = str(racine / "AGENTS-historique.md")
    _os.environ["AGENTS_ACTIVITE_RECENTE"] = str(
        racine / "AGENTS-activite-recente.md")
    _os.environ["AGENTS_FILE"] = str(racine / "AGENTS.md")
    _os.environ["CLASSEUR_STOCKAGE"] = str(
        racine / "cerveau-projet" / "agents" / "classeur-variables" /
        "stockage" / "variables-actuelles.md")
    _os.environ["GRADES_V1"] = str(
        racine / "cerveau-projet" / "agents" / "tools" / "oracle" /
        "grades-v1.json")
    # BDD v1 ecrite dans le module partage historique_bdd (v2) - chemin
    # relatif dans aap (sys.path.insert de 'cerveau-projet/...') -> on
    # l ajoute en ABSOLU pour que l import marche depuis cwd=routines/.
    _bdd_dir = (racine / "cerveau-projet" / "freelance" / "tools-commun" /
                "jarvis" / "fonctions")
    if str(_bdd_dir) not in sys.path:
        sys.path.insert(0, str(_bdd_dir))
    spec = importlib.util.spec_from_file_location("aap_v1", str(aap_path))
    aap = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(aap)
    from datetime import datetime

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    rc = aap.ajouter_historique(ts, "session-admin", agent, raison, type_action)
    return rc == 0


def main():
    citations = _charger_citations()
    if not citations:
        print("[ROUTINE] ERREUR citations : aucune citation chargee depuis "
              "%s" % DATA_FILE)
        return 1
    choix = random.choice(citations)
    dieu = choix.get("dieu", "Olympe")
    phrase = choix.get("phrase", "")
    raison = "%s -- %s" % (dieu, phrase)
    try:
        if not _historiser_agent("citations", raison, "R"):
            print("[ROUTINE] ERREUR citations : ecriture impossible "
                  "(activer-agent-principal introuvable)")
            return 1
    except Exception as exc:
        print("[ROUTINE] ERREUR citations : %s" % exc)
        return 1
    print("%s" % raison)
    return 0


if __name__ == "__main__":
    sys.exit(main())
