#!/usr/bin/env python3
# -*- coding: ascii -*-
# compter-sortie -- mesure les tokens SORTIE (resultats d'outils executes)
# D15 : entry point, delegue a fonctions/mesurer.py
# Extensible : ajouter des sources dans data/sources.json
"""
compter-sortie

Usage:
  compter-sortie.py
  compter-sortie.py --json
  compter-sortie.py --snapshot
  compter-sortie.py --compare
  compter-sortie.py --version
"""
import argparse
import json
import os
import sys
from pathlib import Path

_d = os.path.dirname(os.path.abspath(__file__))
while not os.path.isfile(os.path.join(_d, "AGENTS.md")):
    _p = os.path.dirname(_d)
    if _p == _d:
        break
    _d = _p
RACINE = Path(_d)

sys.path.insert(0, str(Path(__file__).parent / "fonctions"))
from mesurer import (
    charger_sources, mesurer_toutes_sources, calculer_tokens_sortie,
    comparer_snapshots_sortie
)

DATA_DIR = Path(__file__).parent / "data"
SNAPSHOT_FILE = DATA_DIR / "dernier-snapshot.json"


def main():
    parser = argparse.ArgumentParser(description="Mesure les tokens SORTIE")
    parser.add_argument("--json", action="store_true", help="Sortie JSON")
    parser.add_argument("--snapshot", action="store_true",
                        help="Sauvegarde le snapshot")
    parser.add_argument("--compare", action="store_true",
                        help="Compare au dernier snapshot")
    parser.add_argument("--version", action="store_true")
    args = parser.parse_args()

    if args.version:
        print("compter-sortie v0.1.0")
        return

    sources_config = charger_sources(str(DATA_DIR / "sources.json"))
    resultats = mesurer_toutes_sources(str(RACINE), sources_config)
    tokens = calculer_tokens_sortie(
        resultats, sources_config.get("chars_par_token", 4.0))

    if args.json:
        resultat = {"tokens": tokens, "sources": resultats}
        if args.compare:
            precedent = {}
            if SNAPSHOT_FILE.exists():
                try:
                    precedent = json.loads(SNAPSHOT_FILE.read_text(encoding="utf-8"))
                except (ValueError, OSError):
                    pass
            resultat["comparison"] = comparer_snapshots_sortie(
                precedent.get("tokens", {}), tokens)
        print(json.dumps(resultat, indent=2, ensure_ascii=False))
    else:
        print("=== TOKENS SORTIE (resultats d'outils executes) ===")
        print("Total : %d tokens (%d octets, %d sources)" % (
            tokens["total_tokens"], tokens["total_octets"],
            tokens["nb_sources"]))
        print()
        for cat, info in sorted(tokens["par_categorie"].items()):
            print("  %-15s %6d tokens  (%d sources)" % (
                cat, info["tokens"], info["sources"]))
        if args.compare and SNAPSHOT_FILE.exists():
            try:
                prec = json.loads(SNAPSHOT_FILE.read_text(encoding="utf-8"))
                comp = comparer_snapshots_sortie(prec.get("tokens", {}), tokens)
                print()
                if comp["delta_tokens"] > 0:
                    print("  CROISSANCE : +%d tokens" % comp["delta_tokens"])
                elif comp["delta_tokens"] < 0:
                    print("  DIMINUTION : %d tokens" % comp["delta_tokens"])
                else:
                    print("  STABLE")
            except (ValueError, OSError):
                pass

    if args.snapshot:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        SNAPSHOT_FILE.write_text(
            json.dumps(tokens, indent=2, ensure_ascii=False),
            encoding="utf-8")
        if not args.json:
            print("Snapshot sauvegarde.")


if __name__ == "__main__":
    main()
