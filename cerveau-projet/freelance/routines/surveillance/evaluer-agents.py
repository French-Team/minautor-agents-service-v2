# -*- coding: ascii -*-
# routine : evaluer-agents -- depose une demande d'evaluation pour EDITH
import json
import os
import sys
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
JARVIS_INBOX = RACINE / "cerveau-projet" / "freelance" / "tools-commun" / \
    "jarvis" / "inbox" / "stark.jsonl"


def observations_recentes():
    obs_dir = Path(RACINE, "freelance", "tools-commun", "routines-server",
                   "observations")
    if not obs_dir.exists():
        return ["(aucune observation)"]
    fichiers = sorted(obs_dir.glob("*.md"))[-5:]
    return [f.name for f in fichiers] or ["(aucune observation)"]


def main():
    msg = {
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
    with open(JARVIS_INBOX, "a", encoding="utf-8") as f:
        f.write(json.dumps(msg, ensure_ascii=False) + "\n")
    print("[ROUTINE] Demande d'evaluation deposee dans l'inbox de stark.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
