# -*- coding: ascii -*-
# routine : evaluer-agents -- depose une demande d'evaluation pour EDITH
import json
import os
import sys
import uuid
from datetime import datetime, timezone

from pathlib import Path

# P10 : racine DETECTEE en remontant jusqu'a AGENTS.md (jamais compte)
_d = os.path.dirname(os.path.abspath(__file__))
while not os.path.isfile(os.path.join(_d, "AGENTS.md")):
    _p = os.path.dirname(_d)
    if _p == _d:
        break
    _d = _p
RACINE = Path(_d)
JARVIS_DIR = RACINE / "cerveau-projet" / "freelance" / "tools-commun" / "jarvis"


def observations_recentes():
    obs_dir = Path(RACINE, "cerveau-projet", "freelance", "tools-commun",
                   "routines-server", "observations")
    if not obs_dir.exists():
        return ["(aucune observation)"]
    fichiers = sorted(obs_dir.glob("*.md"))[-5:]
    return [f.name for f in fichiers] or ["(aucune observation)"]


def demande_deja_en_attente():
    """True si une demande d'evaluation NON-LUE attend deja dans l'inbox
    de stark (anti-inondation : la routine tourne toutes les 10 min)."""
    inbox = JARVIS_DIR / "inbox" / "stark.jsonl"
    if not inbox.exists():
        return False
    with open(inbox, encoding="utf-8") as f:
        for ligne in f:
            if not ligne.strip():
                continue
            try:
                m = json.loads(ligne)
            except ValueError:
                continue
            if not m.get("lu") and \
                    "[EDITH-EVALUATION]" in str(m.get("objet", "")):
                return True
    return False


def main():
    if demande_deja_en_attente():
        print("[ROUTINE] Demande d'evaluation deja en attente - rien depose.")
        return 0
    msg = {
        "id": str(uuid.uuid4())[:8],
        "de": "edith", "vers": "stark", "priorite": 2,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "objet": "[EDITH-EVALUATION] cycle periodique d'evaluation des agents",
        "corps": (
            "Routine 10 min (protocole 17). EDITH est demandee en "
            "evaluation : appliquer le QUESTIONNAIRE STANDARD aux agents "
            "actifs depuis la derniere passe et transmettre le rapport "
            "des changements proposes a JARVIS pour application via "
            "rating-agents.\nObservations recentes du serveur : "
            + ", ".join(observations_recentes())
        ),
        "lu": False, "accuse": False,
    }
    jarvis_inbox = JARVIS_DIR / "inbox" / "stark.jsonl"
    jarvis_outbox = JARVIS_DIR / "outbox" / "edith.jsonl"
    for cible in (jarvis_inbox, jarvis_outbox):
        cible.parent.mkdir(parents=True, exist_ok=True)
        with open(cible, "a", encoding="utf-8") as f:
            f.write(json.dumps(msg, ensure_ascii=False) + "\n")
    # Tracabilite : le depot apparait dans les activites recentes
    try:
        _fo = Path(RACINE, "cerveau-projet", "freelance", "tools-commun",
                   "os_path", "fonctions")
        _fj = JARVIS_DIR / "fonctions"
        for p in (_fo, _fj):
            if str(p) not in sys.path:
                sys.path.insert(0, str(p))
        from historique import historiser
        historiser("edith",
                   "Depose demande d'evaluation periodique des agents",
                   "R", session="session-freelance")
    except Exception:
        pass
    print("[ROUTINE] Demande d'evaluation deposee dans l'inbox de stark.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
