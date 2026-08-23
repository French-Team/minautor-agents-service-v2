# -*- coding: ascii -*-
# routine : surveiller-flux-jarvis -- alerter sur les P1 non-acquittes
import json
import os
from pathlib import Path

# P10 : racine DETECTEE en remontant jusqu'a AGENTS.md (jamais compte)
_d = os.path.dirname(os.path.abspath(__file__))
while not os.path.isfile(os.path.join(_d, "AGENTS.md")):
    _p = os.path.dirname(_d)
    if _p == _d:
        break
    _d = _p
RACINE = Path(_d)
INBOX_DIR = RACINE / "cerveau-projet" / "freelance" / "tools-commun" / \
    "jarvis" / "inbox"


def main():
    alertes = 0
    for f in INBOX_DIR.glob("*.jsonl"):
        for ligne in f.read_text(encoding="utf-8").splitlines():
            if not ligne.strip():
                continue
            try:
                m = json.loads(ligne)
            except ValueError:
                continue
            if not m.get("lu") and m.get("priorite") == 1:
                alertes += 1
                print(f"ALERTE : P1 non-acquitte chez {f.stem} - "
                      f"{m.get('objet', '')[:50]}")
    if not alertes:
        print("Aucun P1 non-acquitte.")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
