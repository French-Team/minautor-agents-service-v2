# -*- coding: ascii -*-
# routine : surveiller-modifications -- passe de detection du perimetre EDITH
import os
import sys
from pathlib import Path

# P10 : racine DETECTEE en remontant jusqu'a AGENTS.md (jamais compte)
_d = os.path.dirname(os.path.abspath(__file__))
while not os.path.isfile(os.path.join(_d, "AGENTS.md")):
    _p = os.path.dirname(_d)
    if _p == _d:
        break
    _d = _p
RACINE = Path(_d)
sys.path.insert(0, str(RACINE / "cerveau-projet" / "freelance" / "routines" /
                       "surveillance"))
import detection  # noqa: E402


def main():
    manifest_path = RACINE / "cerveau-projet" / "freelance" / "routines" / \
        "manifest.json"
    import json
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    etat = {}
    detection.surveiller_modifications(manifest, etat)
    print("Passe de detection terminee.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
