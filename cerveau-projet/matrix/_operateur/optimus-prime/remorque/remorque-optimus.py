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


CHEMIN_DOMICILE_MOTIF = RACINE_MATRIX / "matrice" / "data" / "outils" / "ecrire" / "constants.py"


def charger_motif_point_restauration():
    """Le motif du point de restauration, LU depuis son DOMICILE (porte ecrire).

    Rend (motif, raison) : motif compile (raison None), ou None AVEC la raison
    NOMMEE qui empeche de juger -- domicile absent, import casse, nom disparu,
    motif invalide. Une remorque qui ne peut pas lire ce motif ne fait pas
    semblant : un .bak non reconnu serait compte comme equipement et enverrait
    reparer un fichier innocent (L-121 : n a pas pu lire son domicile, le DIRE).
    """
    if not CHEMIN_DOMICILE_MOTIF.is_file():
        return None, ("domicile du motif absent : " + str(CHEMIN_DOMICILE_MOTIF))
    try:
        spec = importlib.util.spec_from_file_location("domicile_forme_bak", str(CHEMIN_DOMICILE_MOTIF))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return re.compile(module.MOTIF_BAK_HORODATE), None
    except AttributeError:
        return None, ("MOTIF_BAK_HORODATE introuvable dans " + str(CHEMIN_DOMICILE_MOTIF))
    except (ImportError, OSError, SyntaxError) as erreur:
        return None, ("import du domicile du motif impossible : " + type(erreur).__name__ + " : " + str(erreur))
    except re.error as erreur:
        return None, ("MOTIF_BAK_HORODATE invalide : " + str(erreur))


MOTIF_POINT_RESTAURATION, RAISON_MOTIF_INDISPONIBLE = charger_motif_point_restauration()


def refuser_motif_indisponible():
    """Une remorque qui ne peut pas juger les .bak le DIT et ne rend AUCUN verdict."""
    if RAISON_MOTIF_INDISPONIBLE is None:
        return False
    print("REFUS : motif des points de restauration ILLISIBLE -- la remorque ne peut pas")
    print("distinguer un .bak (exempte) d un equipement, et ne rend donc AUCUN verdict,")
    print("pour ne pas accuser un fichier innocent (L-121).")
    print("- cause  : " + RAISON_MOTIF_INDISPONIBLE)
    print("- remede : reparer le domicile du motif (porte ecrire : constants.py,")
    print("           MOTIF_BAK_HORODATE) PUIS relancer la remorque")
    return True


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
    if refuser_motif_indisponible():
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
