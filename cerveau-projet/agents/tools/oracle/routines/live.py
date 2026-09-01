#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
routine live -- Surveillance des activations/desactivations d agents v1
(session-admin).

Transposee de la routine v2 live (surveillance/live.py). Verifie :
  1. AGENTS.md : un agent est-il declare actif (session-admin) ?
  2. Inbox oracle : debordement de P1 non-lus ?
  3. Derniere activite : l agent actif a-t-il une activite recente ?

Historise UNIQUEMENT en cas d anomalie (evenementiel).

Usage:
    python3 live.py [--dry-run]

Retour: 0 si sain, 1 si anomalie(s).
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

VERSION = "0.1.0"

_DOSSIER = os.path.dirname(os.path.abspath(__file__))
ORACLE_DIR = Path(_DOSSIER).parent
INBOX_DIR = ORACLE_DIR / "inbox"

SEUIL_P1_INBOX = 20
SEUIL_SANS_ACTIVITE_HEURES = 24


def _racine_projet():
    racine = Path(_DOSSIER)
    while not (racine / "AGENTS-historique.md").is_file():
        if racine.parent == racine:
            return Path.cwd()
        racine = racine.parent
    return racine


def _historiser_agent(agent, raison, type_action="R"):
    """Helper d historisation (meme que flux.py)."""
    import importlib.util
    import os as _os
    aap_path = ORACLE_DIR.parent / "activer" / "activer-agent-principal" / \
        "activer-agent-principal.py"
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
    _bdd_dir = (racine / "cerveau-projet" / "freelance" / "tools-commun" /
                "jarvis" / "fonctions")
    if str(_bdd_dir) not in sys.path:
        sys.path.insert(0, str(_bdd_dir))
    spec = importlib.util.spec_from_file_location("aap_v1", str(aap_path))
    aap = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(aap)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    rc = aap.ajouter_historique(ts, "session-admin", agent, raison,
                                type_action)
    return rc == 0


def _agent_actif():
    """L agent actif de session-admin depuis le classeur (gauche)."""
    racine = _racine_projet()
    classeur = racine / "cerveau-projet" / "agents" / "classeur-variables" / \
        "stockage" / "variables-actuelles.md"
    if not classeur.is_file():
        return None
    for ligne in classeur.read_text(encoding="utf-8",
                                    errors="replace").split("\n"):
        if "profil-session-admin" not in ligne:
            continue
        for partie in ligne.split("/"):
            p = partie.strip()
            if p.startswith("agent:"):
                return p.split(":", 1)[1].strip()
    return None


def _verifier_inbox():
    """Debordement de P1 non-lus dans l inbox Oracle."""
    if not INBOX_DIR.is_dir():
        return True, "inbox: pas de dossier"
    total = 0
    for f in sorted(INBOX_DIR.glob("*.jsonl")):
        try:
            for ligne in f.read_text(encoding="utf-8").splitlines():
                if not ligne.strip():
                    continue
                m = json.loads(ligne)
                if not isinstance(m, dict):
                    continue
                if not m.get("lu") and m.get("priorite") == 1:
                    total += 1
        except (ValueError, OSError):
            continue
    if total > SEUIL_P1_INBOX:
        return False, "inbox: %d P1 non-lus (seuil %d)" % (total, SEUIL_P1_INBOX)
    return True, "inbox: %d P1 non-lus (OK)" % total


def _verifier_derniere_activite(agent):
    """Derniere trace de l agent dans l encart v1."""
    racine = _racine_projet()
    activite = racine / "AGENTS-activite-recente.md"
    if not activite.is_file():
        return True, "activite: encart absent"
    dernier_heure = None
    for ligne in activite.read_text(encoding="utf-8",
                                    errors="replace").split("\n"):
        if not ligne.startswith("| "):
            continue
        cellules = [c.strip() for c in ligne.split("|")]
        # Le prefixe vide du tableau decale les colonnes : Heure=[8], pas [7].
        if len(cellules) < 9:
            continue
        if cellules[2].lower() != agent.lower():
            continue
        heure = cellules[8]
        try:
            h = datetime.strptime(heure[:8], "%H:%M:%S")
        except ValueError:
            continue
        if dernier_heure is None or h > dernier_heure:
            dernier_heure = h
    if dernier_heure is None:
        return True, "activite: aucune trace de %s" % agent
    maintenant = datetime.now().replace(hour=dernier_heure.hour,
                                        minute=dernier_heure.minute,
                                        second=dernier_heure.second,
                                        microsecond=0)
    age_h = (datetime.now() - maintenant).total_seconds() / 3600
    if age_h >= SEUIL_SANS_ACTIVITE_HEURES:
        return False, "activite: %s inactif depuis %.0fh" % (agent, age_h)
    return True, "activite: %s recent (%dh)" % (agent, int(age_h))


def main():
    dry_run = "--dry-run" in sys.argv
    anomalies = []
    stats = []

    agent = _agent_actif()
    stats.append("agent_actif: %s" % (agent or "aucun"))
    if agent and agent.lower() != "cerberus":
        ok, msg = _verifier_derniere_activite(agent)
        stats.append(msg)
        if not ok:
            anomalies.append("ACTIVITE: " + msg)

    ok, msg = _verifier_inbox()
    stats.append(msg)
    if not ok:
        anomalies.append("INBOX: " + msg)

    print("[LIVE] Surveillance des agents v1:")
    for s in stats:
        print("  - %s" % s)

    if not anomalies:
        print("[LIVE] Aucune anomalie - activations normales")
        return 0

    print("[LIVE] %d anomalie(s) :" % len(anomalies))
    for a in anomalies:
        print("  ! %s" % a)
    if dry_run:
        print("[LIVE] --dry-run : anomalies non historisees")
        return 1
    _historiser_agent("live", "%d anomalie(s): %s" %
                      (len(anomalies), "; ".join(anomalies[:3])), "R")
    return 1


if __name__ == "__main__":
    sys.exit(main())