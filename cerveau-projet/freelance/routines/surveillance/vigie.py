# -*- coding: ascii -*-
# routine : vigie -- guetteuse des modifications du perimetre EDITH
# (ex-surveiller-modifications, renommee 2026-08-26 : nom simple qui
# exprime ce qu'elle est).
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
    etat_path = Path(RACINE, "cerveau-projet", "freelance", "tools-commun",
                     "routines-server", "observations",
                     "etat-empreintes.json")
    import json
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    # Etat PERSISTANT (comme l'ancien serveur) : sans lui, chaque passe
    # repart de {} et aucune modification n'est jamais detectee.
    etat = {}
    if etat_path.exists():
        try:
            etat = json.loads(etat_path.read_text(encoding="utf-8"))
        except ValueError:
            etat = {}
    # Hygiene : purger les empreintes de fichiers qui n'existent plus
    # (ex: routines-server.py parti au .bak lors du refactoring).
    etat = {k: v for k, v in etat.items() if os.path.exists(k)}
    detection.surveiller_modifications(manifest, etat)
    etat_path.parent.mkdir(parents=True, exist_ok=True)
    etat_path.write_text(json.dumps(etat, ensure_ascii=False),
                         encoding="utf-8")
    print("Passe de detection terminee.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
