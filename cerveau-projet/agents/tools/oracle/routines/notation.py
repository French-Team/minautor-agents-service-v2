#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
routine notation -- Demande periodique d evaluation des agents (v1).

Transposee de la routine v2 notation (surveillance/notation.py) pour
l univers v1 (decision utilisateur 2026-08-29 : creer les routines v1
inspirees des v2, sans recuperer leur code - 2 univers distincts).

Toutes les 5 minutes (manifest 300s), depose une DEMANDE D EVALUATION
CROISEE dans l inbox d Oracle (le coordinateur - decision utilisateur
2026-08-30 : les routines previennent Oracle, pas Cerberus) : les agents
de la v1 (Themis evalue en croise, Janus controle les statuts) sont
candidats a une evaluation periodique.

Anti-inondation (meme principe que la v2) : ne depose PAS si une demande
d evaluation est DEJA en attente (non-lue dans l inbox d Oracle) OU
si une a ete deposee il y a moins de 10 minutes (fichier .notation_derniere).

Historise UNIQUEMENT quand une demande est deposee (pas quand une demande
est deja en attente), comme la v2.

Usage:
    python3 notation.py [--dry-run]

Retour: 0 si succes, 1 si erreur.
"""

import json
import os
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path

VERSION = "0.1.0"

_DOSSIER = os.path.dirname(os.path.abspath(__file__))
ORACLE_DIR = Path(_DOSSIER).parent
INBOX_DIR = ORACLE_DIR / "inbox"
def _rotation_ajouter(agent, message):
    """Rotation inbox : garder les 5 messages les plus recents (decision
    utilisateur 2026-08-29 : les inbox s accumulaient, personne ne les
    lisait). Reutilise le module central oracle/fonctions/rotation.py."""
    try:
        import importlib.util
        _f = Path(_DOSSIER).parent / "fonctions" / "rotation.py"
        _spec = importlib.util.spec_from_file_location("rotation", str(_f))
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        return _mod.ajouter_message(INBOX_DIR, agent, message)
    except Exception:
        return False

_DERNIERE = Path(_DOSSIER) / ".notation_derniere.txt"
DELAI_DEPOT_SECONDES = 600
OBJET_PREFIX = "[NOTATION]"


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


def demande_deja_en_attente():
    """True si une demande d evaluation attend deja :
    - NON-LUE dans l inbox d Oracle (anti-inondation d origine), OU
    - DEPOSEE il y a moins de <DELAI> secondes (.notation_derniere)."""
    oracle_inbox = INBOX_DIR / "oracle.jsonl"
    if oracle_inbox.is_file():
        try:
            for ligne in oracle_inbox.read_text(encoding="utf-8").splitlines():
                if not ligne.strip():
                    continue
                m = json.loads(ligne)
                if not isinstance(m, dict):
                    continue
                if not m.get("lu") and OBJET_PREFIX in str(m.get("objet", "")):
                    return True
        except (ValueError, OSError):
            pass
    # Depot recent
    if _DERNIERE.exists():
        try:
            ancien = float(_DERNIERE.read_text().strip())
            if time.time() - ancien < DELAI_DEPOT_SECONDES:
                return True
        except (ValueError, OSError):
            pass
    return False


def main():
    dry_run = "--dry-run" in sys.argv
    if demande_deja_en_attente():
        print("[NOTATION] Demande d evaluation deja en attente - rien depose.")
        return 0

    msg = {
        "id": "notation-%s" % uuid.uuid4().hex[:8],
        "de": "notation",
        "vers": "oracle",
        "priorite": 2,
        "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "objet": OBJET_PREFIX + " demande activation de l evaluation "
                 "periodique des agents",
        "corps": (
            "DEMANDE D EVALUATION CROISEE (routine 5 min, manifest 300s). "
            "Themis doit etre activee pour poser le questionnaire "
            "d evaluation croisee aux agents actifs, attribuer les +/- et "
            "transmettre son rapport (protocole evaluation croisee v1). "
            "Janus peut controler les statuts en parallele. Oracle coordonne."
        ),
        "lu": False,
        "accuse": False,
        "type": "notation",
    }
    try:
        INBOX_DIR.mkdir(parents=True, exist_ok=True)
        if dry_run:
            print("[NOTATION] --dry-run : demande simulee, "
                  "non deposee/historisee")
            return 0
        _rotation_ajouter("oracle", msg)
        _DERNIERE.write_text(str(time.time()))
    except OSError as exc:
        print("[NOTATION] ERREUR depot : %s" % exc)
        return 1

    _historiser_agent("notation",
                      "Depose demande evaluation periodique des agents", "R")
    print("[NOTATION] Demande d evaluation deposee dans l inbox d Oracle.")
    return 0


if __name__ == "__main__":
    sys.exit(main())