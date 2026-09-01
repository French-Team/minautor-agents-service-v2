#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
routine flux -- Surveillance des P1 non-acquittes (v1, session-admin).

Transposee de la routine v2 flux (surveillance/flux.py) pour l univers v1
(decision utilisateur 2026-08-29 : creer les routines v1 inspirees des v2).

Surveille le flux de messages dans l inbox Oracle (inbox/*.jsonl) et
alerte Cerberus quand des P1 restent non-lus/non-acquittes.

Historise UNIQUEMENT quand le nombre de P1 non-acquittes change (fichier
de persistance .flux_derniere.txt), pour eviter de noyer l encart avec
des entrees identiques - meme principe que la v2.

Usage:
    python3 flux.py [--dry-run]

Retour: 0 si succes, 1 si erreur.
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
_DERNIERE_VALEUR = Path(_DOSSIER) / ".flux_derniere.txt"


def _racine_projet():
    """Racine du projet (remonte depuis routines/ jusqu a
    AGENTS-historique.md). Independant du cwd."""
    racine = Path(_DOSSIER)
    while not (racine / "AGENTS-historique.md").is_file():
        if racine.parent == racine:
            return Path.cwd()
        racine = racine.parent
    return racine


def _historiser_agent(agent, raison, type_action="R"):
    """Historiser via activer-agent-principal (meme canal que l activite
    des agents). Copie du helper de citations.py, chemins en ABSOLU."""
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


def _compter_p1_non_acquittes():
    """Nombre de messages P1 non-lus dans l inbox Oracle.

    On ne compte QUE les P1 d action REELS (missions/instructions pour les
    agents) : champ `type` NON renseigne (None). Les P1 dont le champ
    `type` est renseigne sont des AUTO-ALERTES des routines (statuts,
    vigie-perimetre, vigie-round, sante, notation...), qui se re-nourrissent
    : la routine depose une alerte P1 non-lue, flux la re-compte -> le
    compteur change -> verifier-statuts historise un URGENT -> nouvelle
    mission asap. Decision utilisateur 2026-08-30 : le compteur de flux
    doit refleter les P1 a traiter par les agents, pas le telephone interne
    des routines."""
    total = 0
    if not INBOX_DIR.is_dir():
        return 0
    for f in sorted(INBOX_DIR.glob("*.jsonl")):
        try:
            for ligne in f.read_text(encoding="utf-8").splitlines():
                if not ligne.strip():
                    continue
                m = json.loads(ligne)
                if not isinstance(m, dict):
                    continue
                if not m.get("lu") and m.get("priorite") == 1 \
                        and not m.get("type"):
                    total += 1
        except (ValueError, OSError):
            continue
    return total


def main():
    dry_run = "--dry-run" in sys.argv
    alertes = _compter_p1_non_acquittes()

    # Persistance : historique UNIQUEMENT si le nombre change.
    derniere_valeur = 0
    if _DERNIERE_VALEUR.exists():
        try:
            derniere_valeur = int(_DERNIERE_VALEUR.read_text().strip())
        except (ValueError, OSError):
            pass

    if alertes == derniere_valeur:
        print("[FLUX] Inchange : %d P1 (pas d'historisation)" % alertes)
        return 0

    # Changement detecte : historiser (probleme apparu ou regle).
    if alertes:
        raison = "%d P1 non-acquitte(s) detecte(s)" % alertes
    else:
        raison = "Aucun P1 non-acquitte (probleme regle)"
    if dry_run:
        # Convention v1 : un --dry-run ne modifie RIEN (ni etat, ni
        # historique). L etat .flux_derniere.txt n est ecrit qu en reel,
        # reel, apres ce point.
        print("[FLUX] --dry-run : changement %d -> %d (%s) non historique" %
              (derniere_valeur, alertes, raison))
        return 0
    _DERNIERE_VALEUR.write_text(str(alertes))
    ok = _historiser_agent("flux", raison, "R")
    print("[FLUX] Changement : %d -> %d P1 (%s) historique=%s" %
          (derniere_valeur, alertes, raison, ok))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())