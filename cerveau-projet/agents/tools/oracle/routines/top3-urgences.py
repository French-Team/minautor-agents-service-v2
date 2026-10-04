#!/usr/bin/env python3
# -*- coding: ascii -*-
"""Surveille les trois premieres activites v1 et alerte Oracle."""
import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

DOSSIER = Path(__file__).resolve().parent
ORACLE_DIR = DOSSIER.parent
RACINE = ORACLE_DIR.parents[3]
ACTIVITE = RACINE / "AGENTS-activite-recente.md"
ETAT = DOSSIER / "data" / "etat-top3-urgences.json"

MARQUEURS = ("URGENT", "ANOMALIE", "BUG", "ERREUR", "SERVEUR MORT",
             "FANTOME", "VIOLATION", "PIDFILE", "ARRET AUTO")


def _lignes_top3():
    if not ACTIVITE.is_file():
        return []
    lignes = []
    for ligne in ACTIVITE.read_text(encoding="utf-8", errors="replace").splitlines():
        if not ligne.startswith("| ") or "|---" in ligne or "| Grade |" in ligne:
            continue
        cellules = [x.strip() for x in ligne.split("|")]
        if len(cellules) >= 11:
            lignes.append(cellules)
        if len(lignes) == 3:
            break
    return lignes


def _empreinte(lignes):
    brut = "\n".join("|".join(x) for x in lignes)
    return hashlib.sha256(brut.encode("utf-8")).hexdigest()


def _urgent(ligne):
    return any(m in "|".join(ligne).upper() for m in MARQUEURS)


def _alerter(empreinte, lignes):
    corps = "Top 3 activites v1 critique(s):\n" + "\n".join(
        "- " + " | ".join(ligne) for ligne in lignes)
    message = {
        "id": "top3-" + empreinte[:12], "de": "top3-urgences", "vers": "oracle",
        "priorite": 1, "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "objet": "[URGENT] Probleme detecte dans les 3 premieres activites",
        "corps": corps, "lu": False, "accuse": False, "type": "top3-urgences",
    }
    rotation = ORACLE_DIR / "fonctions" / "rotation.py"
    spec = __import__("importlib.util").util.spec_from_file_location("rotation", rotation)
    module = __import__("importlib.util").util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.ajouter_message(ORACLE_DIR / "inbox", "oracle", message)


def main():
    lignes = _lignes_top3()
    critiques = [x for x in lignes if _urgent(x)]
    empreinte = _empreinte(critiques) if critiques else ""
    ancien = ""
    if ETAT.is_file():
        try:
            ancien = json.loads(ETAT.read_text(encoding="utf-8")).get("empreinte", "")
        except (OSError, ValueError):
            pass
    if critiques and empreinte != ancien and "--dry-run" not in sys.argv:
        _alerter(empreinte, critiques)
    if "--dry-run" not in sys.argv:
        ETAT.parent.mkdir(parents=True, exist_ok=True)
        ETAT.write_text(json.dumps({"empreinte": empreinte}, ensure_ascii=True), encoding="utf-8")
    print("[TOP3-URGENCES] %d ligne(s) critique(s), alerte=%s" %
          (len(critiques), bool(critiques and empreinte != ancien)))
    return 1 if critiques else 0


if __name__ == "__main__":
    sys.exit(main())
