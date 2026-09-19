#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
revert-periode.py -- Revert toutes les modifs BDD-tracees d une periode (M-106)

Liste les fichiers TRACES au domicile unique des modifications
(modifications-par-fichier.json, EO-154) entre --depuis et --jusquau, revert
chacun depuis son .bak le plus recent. Fichiers sans .bak = signales, non
revertis. Le domicile ne porte PAS de statut : seule la fenetre filtre.
Usage: python revert-periode.py --depuis "2026-09-11 00:00:00" [--jusquau "..."] [--executer]
  sans --executer : dry-run (liste seulement). code 0 = rien a revert ou tout reverti.
"""

import sys
import json
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

# EO-154 (2026-09-19) : le vocabulaire des statuts n'a plus de domicile ici --
# l'appui sqlite bdd-modifs est RETIRE, et le domicile unique des modifications
# (modifications-par-fichier.json) ne porte PAS de statut. Ce script lit donc la
# FENETRE de dates, sans filtre de statut, et ne devine rien.
BORNES_REMONTEE = 30


def fichiers_traces(db_json, depuis, jusquau):
    """Fichiers du domicile unique ayant une entree dans la fenetre (liste)."""
    try:
        donnees = json.loads(Path(db_json).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    trouves = []
    for chemin, fiche in (donnees.get("fichiers") or {}).items():
        for entree in (fiche or {}).get("modifications") or []:
            date = entree.get("date") or ""
            if depuis <= date <= jusquau and chemin not in trouves:
                trouves.append(chemin)
    return trouves


def main():
    parser = argparse.ArgumentParser(description="Revert les modifs d une periode")
    parser.add_argument("--depuis", required=True, help="Debut periode (YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--jusquau", default="9999-12-31 23:59:59")
    parser.add_argument("--executer", action="store_true", help="Revert reel (defaut: liste seulement)")
    parser.add_argument("--racine", default=".", help="Racine projet")
    args = parser.parse_args()

    try:
        datetime.strptime(args.depuis, "%Y-%m-%d %H:%M:%S")
        datetime.strptime(args.jusquau, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        print("Format date exige : YYYY-MM-DD HH:MM:SS")
        return 2

    racine = Path(args.racine).resolve()
    db = None
    for cand in (racine, racine / "matrix", racine / "cerveau-projet" / "matrix"):
        if (cand / "matrice" / "data" / "modifications-par-fichier.json").is_file():
            db = cand / "matrice" / "data" / "modifications-par-fichier.json"
            base_matrix = cand if cand.name == "matrix" else None
            break
    if db is None:
        print("Domicile des modifications (modifications-par-fichier.json) introuvable")
        return 2
    if base_matrix is None:
        # Racine matrix/ DETECTEE par le marqueur partage (M-076), jamais comptee (L-013).
        for candidat in db.parents:
            if (candidat / "matrice" / "data" / "commun" / "racine.py").is_file():
                base_matrix = candidat
                break
        else:
            print("Racine matrix/ introuvable depuis " + str(db))
            return 2
    outils = base_matrix / "_operateur" / "optimus-prime" / "super-combos" / "combos" / "outils"

    fichiers = fichiers_traces(db, args.depuis, args.jusquau)
    if fichiers is None:
        print("Domicile des modifications illisible : " + str(db))
        return 2

    if not fichiers:
        print(f"Periode {args.depuis} -> {args.jusquau} : aucune modification validee, rien a revertir.")
        return 0

    print(f"Periode {args.depuis} -> {args.jusquau} : {len(fichiers)} fichier(s) :")
    for f in fichiers:
        print(f"  - {f}")
    if not args.executer:
        print("\nMode liste (ajouter --executer pour revertir).")
        return 0

    revertis, sans_bak = [], []
    for f in fichiers:
        cible = Path(f)
        if not cible.is_absolute():
            cible = racine / f
        baks = sorted(cible.parent.glob(cible.name + ".bak.*"),
                      key=lambda p: p.stat().st_mtime, reverse=True) if cible.parent.is_dir() else []
        if not baks:
            sans_bak.append(f)
            continue
        r = subprocess.run([sys.executable, str(outils / "revert-fichier.py"),
                            "--fichier", str(cible), "--depuis-bak"],
                           capture_output=True, text=True)
        if r.returncode == 0:
            # EO-154 : plus d'appel a bdd-modifs (appui retire). Le revert
            # lui-meme est trace par la porte de revert, pas ici.
            revertis.append(f)
        else:
            sans_bak.append(f"{f} (revert KO: {r.stdout.strip()[:100]})")

    print(f"\nRevertis: {len(revertis)} | Sans .bak / echec: {len(sans_bak)}")
    for f in revertis:
        print(f"  OK: {f}")
    for f in sans_bak:
        print(f"  KO: {f}")
    return 0 if not sans_bak else 1


if __name__ == "__main__":
    sys.exit(main())
