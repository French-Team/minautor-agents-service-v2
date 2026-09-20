#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scan-valeurs-en-dur.py -- Scan convention zero-valeurs-en-dur (M-102)

Detecte secrets, chemins absolus, IPs en dur dans les fichiers matrice.
code 0 = sain, code 1 = valeurs detectees.
Usage: python scan-valeurs-en-dur.py <fichier|dossier> [--ext .py,.md,.json]
"""

import sys
import re
import argparse
from pathlib import Path


MOTIFS = {
    "secret": re.compile(r"(?i)\b(password|passwd|secret|api[_-]?key|token)\b\s*[:=]\s*\S+"),
    "chemin-win": re.compile(r"[A-Za-z]:[\\/][^\s\"']*"),
    "chemin-home": re.compile(r"(/(home|Users)/[^\s\"']*|C:\\Users\\[^\s\"']*)"),
    "ip": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
}
EXCLUS_DIRS = {".git", "__pycache__"}
# Faux positifs connus : documentation et empreintes.
EXCLUS_FICHIERS = {"scan-valeurs-en-dur.py"}


def main():
    parser = argparse.ArgumentParser(description="Scan zero-valeurs-en-dur")
    parser.add_argument("cible", help="Fichier ou dossier a scanner")
    parser.add_argument("--ext", default=".py,.md,.json,.jsonl",
                        help="Extensions (dossier seulement)")
    args = parser.parse_args()

    cible = Path(args.cible)
    if not cible.exists():
        print(f"Cible introuvable: {cible}")
        return 2

    exts = {e.strip() for e in args.ext.split(",") if e.strip()}
    fichiers = [cible] if cible.is_file() else [
        p for p in cible.rglob("*")
        if p.is_file()
        and not any(part in EXCLUS_DIRS for part in p.parts)
        and p.suffix in exts
        and p.name not in EXCLUS_FICHIERS
    ]

    trouvailles = []
    for p in fichiers:
        try:
            lignes = p.read_text(encoding="utf-8", errors="strict").split("\n")
        except (OSError, UnicodeError):
            continue
        for i, ligne in enumerate(lignes, 1):
            for nom, motif in MOTIFS.items():
                m = motif.search(ligne)
                if m:
                    extrait = m.group(0)[:60]
                    trouvailles.append((str(p), i, nom, extrait))
                    break

    if trouvailles:
        print(f"VALEURS EN DUR : {len(trouvailles)} occurrence(s) :")
        for f, ligne, nom, extrait in trouvailles[:30]:
            print(f"  - {f}:{ligne} [{nom}] {extrait}")
        if len(trouvailles) > 30:
            print(f"  ... +{len(trouvailles) - 30} autres")
        return 1

    print(f"Zero-valeurs-en-dur sain : {len(fichiers)} fichier(s) controles, 0 valeur.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
