#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit-invisibilite.py -- Audit coherence d invisibilite L-016/CV-006 (M-101)

Verifie qu aucun contenu lisible par le cameleon ne nomme l invisible
(Optimus) ni ses zones internes. code 0 = sain, code 1 = fuites.
Usage: python audit-invisibilite.py <fichier|dossier> [--mots a,b] [--ext .py,.md,.json]
"""

import sys
import argparse
from pathlib import Path


DEFAUT_INTERDITS = (
    "optimus-prime",
    "optimus",
    "_operateur",
    "tmp-optimus",
    "suivi-optimus",
)
EXCLUS_DIRS = {".git", "__pycache__"}


def main():
    parser = argparse.ArgumentParser(description="Audit invisibilite L-016/CV-006")
    parser.add_argument("cible", help="Fichier ou dossier lu par le cameleon")
    parser.add_argument("--mots", default=",".join(DEFAUT_INTERDITS),
                        help="Mots interdits separes par virgules")
    parser.add_argument("--ext", default=".py,.md,.json,.jsonl",
                        help="Extensions (dossier seulement)")
    args = parser.parse_args()

    cible = Path(args.cible)
    if not cible.exists():
        print(f"Cible introuvable: {cible}")
        return 2

    interdits = [m.strip().lower() for m in args.mots.split(",") if m.strip()]
    exts = {e.strip() for e in args.ext.split(",") if e.strip()}

    fichiers = [cible] if cible.is_file() else [
        p for p in cible.rglob("*")
        if p.is_file()
        and not any(part in EXCLUS_DIRS for part in p.parts)
        and p.suffix in exts
    ]

    fuites = []
    for p in fichiers:
        try:
            texte = p.read_text(encoding="utf-8", errors="strict").lower()
        except (OSError, UnicodeError):
            continue
        lignes = texte.split("\n")
        for i, ligne in enumerate(lignes, 1):
            for mot in interdits:
                if mot in ligne:
                    fuites.append((str(p), i, mot))
                    break

    if fuites:
        print(f"FUITES : {len(fuites)} mention(s) de l invisible :")
        for f, ligne, mot in fuites[:20]:
            print(f"  - {f}:{ligne} (mot: {mot})")
        if len(fuites) > 20:
            print(f"  ... +{len(fuites) - 20} autres")
        return 1

    print(f"Invisibilite saine : {len(fichiers)} fichier(s) controles, 0 fuite.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
