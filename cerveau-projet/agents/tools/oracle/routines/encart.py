#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
routine encart -- Verification de l integrite de l encart v1
(session-admin, AGENTS-activite-recente.md).

Transposee de la routine v2 encart (surveillance/encart.py). Le format v1
est un tableau markdown simple (sans emoji grade) :
  | Grade | Agent | Executeur | Etat | Secteur | Raison | Heure | id | Type |

La colonne Etat porte l etat de l activite (decision utilisateur
2026-08-29) : DEBUT, FIN, ATTENTE, URGENT, BUG, ACTIF.

Verifie la presence de l en-tete de colonnes, l integrite structurelle et
que les valeurs de la colonne Etat sont parmi les valeurs connues,
historise UNIQUEMENT en cas d anomalie (evenementiel).

Usage:
    python3 encart.py [--dry-run]

Retour: 0 si OK, 1 si anomalie(s).
"""

import io
import json
import os
import sys
from datetime import datetime
from pathlib import Path

VERSION = "0.2.0"

_DOSSIER = os.path.dirname(os.path.abspath(__file__))
ORACLE_DIR = Path(_DOSSIER).parent

ENTETE_V1 = "| Grade | Agent | Executeur | Etat | Secteur | Raison |"

# Etats connus de la colonne Etat (decision utilisateur 2026-08-29) :
# charges DYNAMIQUEMENT depuis etats-actions.json (v0.2.0) pour ne plus
# editer le code quand on ajoute un etat. Repli : ensemble v0.1.0.
ETATS_CONNUS_DEFAUT = {"DEBUT", "FIN", "ATTENTE", "URGENT", "BUG",
                       "ACTIF", "DEV", "AUTO", "ACTION"}


def _charger_etats_connus():
    """Lire la liste des etats depuis etats-actions.json (cles de 'etats')."""
    try:
        with io.open(str(ORACLE_DIR / "etats-actions.json"), "r",
                     encoding="utf-8", errors="replace") as fh:
            data = json.load(fh)
        etats = data.get("etats")
        if isinstance(etats, dict) and etats:
            return set(etats.keys())
    except (OSError, ValueError):
        pass
    return ETATS_CONNUS_DEFAUT


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


def main():
    dry_run = "--dry-run" in sys.argv
    racine = _racine_projet()
    encart = racine / "AGENTS-activite-recente.md"
    anomalies = []

    if not encart.is_file():
        anomalies.append("Fichier AGENTS-activite-recente.md absent")
    else:
        contenu = encart.read_text(encoding="utf-8", errors="replace")
        if ENTETE_V1 not in contenu:
            anomalies.append("En-tete de colonnes v1 absent : %s" % ENTETE_V1)
        # Verifier que les valeurs de la colonne Etat sont connues.
        for ligne in contenu.splitlines():
            if not ligne.strip().startswith("| ") or "| Grade |" in ligne:
                continue
            cols = [c.strip() for c in ligne.split("|")]
            if len(cols) < 6:
                continue
            etat = cols[4]  # Grade|Agent|Executeur|Etat|Secteur|...
            if etat and etat not in _charger_etats_connus():
                anomalies.append("Etat inconnu '%s' (colonne Etat)" % etat)

    if not anomalies:
        print("[ENCART] OK (encart v1 coherent)")
        return 0

    print("[ENCART] %d anomalie(s) :" % len(anomalies))
    for a in anomalies:
        print("  ! %s" % a)
    if dry_run:
        print("[ENCART] --dry-run : anomalie non historisee")
        return 1
    _historiser_agent("encart", "%d anomalie(s): %s" %
                      (len(anomalies), "; ".join(anomalies[:3])), "R")
    return 1


if __name__ == "__main__":
    sys.exit(main())