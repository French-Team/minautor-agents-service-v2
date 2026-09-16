#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
garde-ascii.py -- Garde ASCII strict matrice (M-099)

Verifie qu un fichier (ou dossier) ne contient que de l ASCII strict
(convention ASCII matrice). code 0 = sain, code 1 = non-ASCII detecte.
Usage: python garde-ascii.py <fichier|dossier> [--ext .py,.md,.json]
"""

import sys
import argparse
from pathlib import Path


# docs/ exclu (decision createur) : sources historiques en lecture seule, accents legitimes.
EXCLUS_DIRS = {".git", "__pycache__", "docs"}


def fichiers_a_controler(cible: Path, exts):
    if cible.is_file():
        yield cible
        return
    for p in cible.rglob("*"):
        if not p.is_file():
            continue
        if any(part in EXCLUS_DIRS for part in p.parts):
            continue
        if exts and p.suffix not in exts:
            continue
        yield p


def main():
    parser = argparse.ArgumentParser(description="Garde ASCII strict")
    parser.add_argument("cible", help="Fichier ou dossier a controler")
    parser.add_argument("--ext", default=".py,.md,.json,.jsonl",
                        help="Extensions (dossier seulement, defaut: .py,.md,.json,.jsonl)")
    args = parser.parse_args()

    cible = Path(args.cible)
    if not cible.exists():
        print(f"Cible introuvable: {cible}")
        return 2

    exts = {e.strip() for e in args.ext.split(",") if e.strip()}
    violations = []
    total = 0
    for p in fichiers_a_controler(cible, exts if cible.is_dir() else None):
        total += 1
        try:
            raw = p.read_bytes()
        except OSError as e:
            violations.append((str(p), f"illisible: {e}"))
            continue
        lignes_fautives = set()
        try:
            texte = raw.decode("ascii")
        except UnicodeDecodeError:
            for i, ligne in enumerate(raw.split(b"\n"), 1):
                try:
                    ligne.decode("ascii")
                except UnicodeDecodeError:
                    lignes_fautives.add(i)
            violations.append((str(p), f"lignes non-ASCII: {sorted(lignes_fautives)[:10]}"))

    if violations:
        print(f"ASCII VIOLE : {len(violations)}/{total} fichier(s) non-ASCII :")
        for f, detail in violations:
            print(f"  - {f} ({detail})")
        return 1

    print(f"ASCII sain : {total} fichier(s) controles, 0 violation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
