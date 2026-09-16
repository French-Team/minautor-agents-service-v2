#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cartographe-matrice.py -- Carte themes/protocoles/outils/BDD d Optimus (M-103)

Inventaire + liens + anomalies (cibles manquantes, orphelins jamais
references). code 0 = sain, code 1 = anomalies.
Usage: python cartographe-matrice.py [--racine <optimus-prime/>]
"""

import sys
import json
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Cartographe matrice (zone Optimus)")
    parser.add_argument("--racine", default=".", help="Dossier _operateur/optimus-prime (defaut: detection auto)")
    args = parser.parse_args()

    racine = Path(args.racine).resolve()
    if racine.name != "optimus-prime":
        cand = racine / "cerveau-projet" / "matrix" / "_operateur" / "optimus-prime"
        if cand.is_dir():
            racine = cand
    if not (racine / "parcours" / "themes").is_dir():
        print(f"Arbre operateur introuvable depuis {args.racine} (parcours/themes manquant)")
        return 2

    themes = sorted((racine / "parcours" / "themes").glob("theme-*.json"))
    protocoles = sorted((racine / "protocoles").glob("proto-*.md"))
    outils_dir = racine / "super-combos" / "combos" / "outils"
    outils = sorted([p for p in outils_dir.iterdir()]) if outils_dir.is_dir() else []
    conventions = sorted((racine / "conventions").glob("convention-*.md"))

    print(f"=== Carte Optimus ({racine.name}) ===")
    print(f"Themes: {len(themes)} | Protocoles: {len(protocoles)} | Outils/combos: {len(outils)} | Conventions: {len(conventions)}")

    # Liens : toutes les cibles citees par les themes
    cites = set()
    for t in themes:
        try:
            d = json.loads(t.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        for r in d.get("theme", {}).get("redirects", []):
            vers = r.get("vers", {}) if isinstance(r.get("vers"), dict) else {}
            for cle in ("fichier", "dossier"):
                if vers.get(cle):
                    cites.add(vers[cle])

    # Anomalie 1 : cibles citees introuvables (multi-racines)
    manquantes = []
    for c in sorted(cites):
        p = Path(c)
        if p.is_absolute():
            existe = p.exists()
        else:
            existe = any((base / c).exists() for base in (racine, racine / "parcours" / "themes", Path.cwd()))
        if not existe:
            manquantes.append(c)

    # Anomalie 2 : protocoles jamais cites par aucun theme
    protocoles_cites = {c for c in cites if c.startswith("protocoles/") or c.startswith("proto-")}
    orphelins_proto = [p.name for p in protocoles
                       if p.name not in cites and f"protocoles/{p.name}" not in cites
                       and not any(p.name in c for c in cites)]

    # Anomalie 3 : outils jamais cites par aucun theme
    noms_outils = [o.name for o in outils]
    orphelins_outils = [n for n in noms_outils
                        if not any(n in c for c in cites) and n not in ("outils-readme.md", "__pycache__")]

    # Cibles manquantes = ERREURS (redirects casses). Orphelins = INFOS
    # (les themes citent souvent des dossiers, pas des noms : pas de verdict).
    if manquantes:
        print(f"\nCIBLES MANQUANTES ({len(manquantes)}):")
        for c in manquantes:
            print(f"  - {c}")
        print(f"\nCarte : {len(manquantes)} anomalie(s).")
        return 1
    print("\nCibles : 0 manquante.")
    if orphelins_proto:
        print(f"\n[info] protocoles jamais cites par nom ({len(orphelins_proto)}):")
        for c in orphelins_proto:
            print(f"  - {c}")
    if orphelins_outils:
        print(f"\n[info] outils jamais cites par nom ({len(orphelins_outils)}):")
        for c in orphelins_outils:
            print(f"  - {c}")
    print("\nCarte saine : 0 anomalie.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
