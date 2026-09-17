#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
espion-integrite-optimus.py -- Empreintes zone Optimus (M-111)

L espion SIGNALE, il ne repare jamais.
Usage:
  python espion-integrite-optimus.py enregistrer  (pose les empreintes de reference)
  python espion-integrite-optimus.py verifier     (compare, code 0 = sain, 1 = ecarts)
"""

import sys
import json
import hashlib
from datetime import datetime
from pathlib import Path


BASE = Path(__file__).resolve().parent
# L espion vit DANS la zone : ZONE = ancetre nomme optimus-prime.
ZONE = next(p for p in [BASE, *BASE.parents] if p.name == "optimus-prime")
REGISTRE = BASE / "registre" / "registre.json"

DOSSIERS = ["parcours", "protocoles", "conventions", "regles-immuables"]
FICHIERS_RACINE = ["optimus-prime.md"]
EXCLUS = {".bak", "__pycache__"}


def fichiers_zone():
    if not ZONE.is_dir():
        return []
    resultats = []
    for d in DOSSIERS:
        base = ZONE / d
        if base.is_dir():
            resultats += [p for p in base.rglob("*") if p.is_file()]
    for f in FICHIERS_RACINE:
        p = ZONE / f
        if p.is_file():
            resultats.append(p)
    outils = ZONE / "super-combos" / "combos" / "outils"
    if outils.is_dir():
        resultats += [p for p in outils.rglob("*.py") if p.is_file()]
    # Objets numerotes de la zone (sc-*.py + le lanceur) : ajoutes le 2026-09-13
    # (MO-067). Ils vivaient DANS combos/ et n'etaient donc jamais surveilles,
    # alors que les outils de ce meme dossier l'etaient : le rangement corrige,
    # la surveillance suit (un fichier nait EQUIPE ET VU). `glob` non recursif :
    # combos/ a son propre scan, au-dessus.
    objets = ZONE / "super-combos"
    if objets.is_dir():
        resultats += [p for p in objets.glob("*.py") if p.is_file()]
    for propre in ("espions", "remorque"):
        dossier = ZONE / propre
        if dossier.is_dir():
            resultats += [p for p in dossier.rglob("*.py") if p.is_file()]
    return [p for p in resultats
            if not any(part in EXCLUS or part.endswith(".bak") for part in p.parts)]


def empreinte(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for bloc in iter(lambda: f.read(65536), b""):
            h.update(bloc)
    return h.hexdigest()


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("enregistrer", "verifier"):
        print(__doc__)
        return 2
    fichiers = fichiers_zone()
    if sys.argv[1] == "enregistrer":
        REGISTRE.parent.mkdir(parents=True, exist_ok=True)
        registre = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "empreintes": {str(p.relative_to(ZONE)): empreinte(p) for p in fichiers},
        }
        REGISTRE.write_text(json.dumps(registre, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Registre pose : {len(registre['empreintes'])} empreintes.")
        return 0
    # verifier
    if not REGISTRE.is_file():
        print("Registre absent : lancer enregistrer d abord.")
        return 2
    ref = json.loads(REGISTRE.read_text(encoding="utf-8"))["empreintes"]
    actuel = {str(p.relative_to(ZONE)): empreinte(p) for p in fichiers}
    nouveaux = sorted(set(actuel) - set(ref))
    disparus = sorted(set(ref) - set(actuel))
    modifies = sorted(k for k in ref if k in actuel and ref[k] != actuel[k])
    if nouveaux:
        print(f"NOUVEAUX ({len(nouveaux)}):")
        for k in nouveaux:
            print(f"  + {k}")
    if disparus:
        print(f"DISPARUS ({len(disparus)}):")
        for k in disparus:
            print(f"  - {k}")
    if modifies:
        print(f"MODIFIES ({len(modifies)}):")
        for k in modifies:
            print(f"  ~ {k}")
    if nouveaux or disparus or modifies:
        return 1
    print(f"Integrite Optimus saine : {len(actuel)} fichiers conformes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
