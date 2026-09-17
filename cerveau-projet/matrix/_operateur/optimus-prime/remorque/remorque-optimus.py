#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
remorque-optimus.py -- Inventaire des equipements d Optimus (M-112)

Usage:
  python remorque-optimus.py inventorier  (regenere inventaire.json)
  python remorque-optimus.py etat         (compare, code 0 = conforme, 1 = ecarts)
"""

import sys
import re
import json
import importlib.util
from datetime import datetime
from pathlib import Path


BASE = Path(__file__).resolve().parent
# La remorque vit DANS la zone : ZONE = ancetre nomme optimus-prime.
ZONE = next(p for p in [BASE, *BASE.parents] if p.name == "optimus-prime")
INVENTAIRE = BASE / "inventaire.json"
# Le domicile de la forme des points de restauration (porte qui la PRODUIT).
RACINE_MATRIX = next(p for p in [BASE, *BASE.parents] if p.name == "matrix")

# Un EQUIPEMENT est permanent ; l'ETAT d'un processus ne l'est pas.
# Avant ce filtre (2026-09-13), `watchdog-flux2.pid` etait ramasse comme un
# equipement : la remorque criait INATTENDU tant que le chien de garde VIVAIT,
# puis MANQUANT une fois arrete. Un inventaire qui crie dans les deux sens ne
# dit plus rien (meme famille que la porte qui ne dit rien).
SUFFIXES_ETAT = (".pid", ".flag", ".arret", ".log", ".jsonl", ".tmp", ".pyc")
NOMS_ETAT = ("__pycache__",)

# POINT DE RESTAURATION (friction 42 / MO-133) : un `.bak` horodate est
# l'artefact d'une transaction d'ecriture -- il apparait et disparait avec les
# ecritures, exactement comme un `.pid` ou un `.log`. Il n'est donc PAS un
# equipement, et la remorque ne doit ni crier INATTENDU quand il nait, ni
# MANQUANT quand il disparait. Le motif n'est PAS redevine ici : il vient de la
# porte `ecrire`, qui produit la forme (MO-133, lecons L-100/L-102). Les
# fichiers epargnes sont COMPTES et NOMMES -- une exemption muette serait un
# angle mort.


def charger_motif_point_restauration():
    """Le motif du point de restauration, LU depuis son DOMICILE (porte ecrire)."""
    chemin = RACINE_MATRIX / "matrice" / "data" / "outils" / "ecrire" / "constants.py"
    if not chemin.is_file():
        return None
    try:
        spec = importlib.util.spec_from_file_location("domicile_forme_bak", str(chemin))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return re.compile(module.MOTIF_BAK_HORODATE)
    except (ImportError, OSError, SyntaxError, AttributeError, re.error):
        return None


MOTIF_POINT_RESTAURATION = charger_motif_point_restauration()


def est_point_restauration(nom):
    """Vrai pour un point de restauration horodate (forme declaree par la porte)."""
    return bool(MOTIF_POINT_RESTAURATION and MOTIF_POINT_RESTAURATION.search(nom))


def collecter():
    """Retourne (equipements, points de restauration vus).

    Les points de restauration sont rendus A PART pour etre DITS : ils ne
    comptent pas comme equipements, mais leur presence ne se cache pas.
    """
    equipements = []
    restaurations = []
    if not ZONE.is_dir():
        return equipements, restaurations
    for t in sorted((ZONE / "parcours" / "themes").glob("theme-*.json")):
        equipements.append({"nom": t.stem, "type": "theme", "chemin": str(t.relative_to(ZONE))})
    for p in sorted((ZONE / "protocoles").glob("proto-*.md")):
        equipements.append({"nom": p.stem, "type": "protocole", "chemin": str(p.relative_to(ZONE))})
    for c in sorted((ZONE / "conventions").glob("convention-*.md")):
        equipements.append({"nom": c.stem, "type": "convention", "chemin": str(c.relative_to(ZONE))})
    outils = ZONE / "super-combos" / "combos" / "outils"
    if outils.is_dir():
        for o in sorted(outils.iterdir()):
            if est_point_restauration(o.name):
                restaurations.append(str(o.relative_to(ZONE)))
                continue
            if o.name in NOMS_ETAT or o.suffix in SUFFIXES_ETAT:
                continue
            typ = "outil-dossier" if o.is_dir() else "outil"
            equipements.append({"nom": o.name, "type": typ, "chemin": str(o.relative_to(ZONE))})
    combos = ZONE / "super-combos" / "combos"
    if combos.is_dir():
        for c in sorted(combos.iterdir()):
            if c.is_dir() and c.name != "outils" and c.name != "__pycache__":
                equipements.append({"nom": c.name, "type": "combo", "chemin": str(c.relative_to(ZONE))})
    # SUPER-combos : leurs objets vivent dans super-combos/ (hors du dossier
    # combos/), sous le prefixe sc-. Avant le 2026-09-13 (MO-067) ils etaient
    # ranges avec les combos : l'inventaire les etiquetait "combo" et le prefixe
    # sc- ne distinguait donc RIEN dans la remorque (cecite mesuree : la
    # remorque etait le seul instrument qui niait le contrat CV-008).
    super_combos = ZONE / "super-combos"
    if super_combos.is_dir():
        for s in sorted(super_combos.iterdir()):
            if s.is_dir() and s.name.startswith("sc-") and s.name != "__pycache__":
                equipements.append({"nom": s.name, "type": "super-combo", "chemin": str(s.relative_to(ZONE))})
    return equipements, restaurations


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("inventorier", "etat"):
        print(__doc__)
        return 2
    if sys.argv[1] == "inventorier":
        equipements, restaurations = collecter()
        INVENTAIRE.write_text(json.dumps({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total": len(equipements),
            "equipements": equipements,
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Inventaire : {len(equipements)} equipements.")
        if restaurations:
            print(f"  ~ {len(restaurations)} point(s) de restauration vu(s) : "
                  "etat de transaction, pas un equipement.")
        return 0
    # etat
    if not INVENTAIRE.is_file():
        print("Inventaire absent : lancer inventorier d abord.")
        return 2
    ref = {e["chemin"] for e in json.loads(INVENTAIRE.read_text(encoding="utf-8"))["equipements"]}
    reel = set()
    equipements, restaurations = collecter()
    for e in equipements:
        reel.add(e["chemin"])
    manquants = sorted(ref - reel)
    inattendus = sorted(reel - ref)
    for m in manquants:
        print(f"  - MANQUANT : {m}")
    for m in inattendus:
        print(f"  + INATTENDU : {m}")
    if restaurations:
        print(f"  ~ POINT DE RESTAURATION (etat de transaction, non equipement) : "
              f"{len(restaurations)} vu(s)")
        for r in sorted(restaurations):
            print(f"      {r}")
    if manquants or inattendus:
        return 1
    print(f"Remorque conforme : {len(reel)} equipements.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
