#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
revert-fichier.py -- Revert un fichier depuis sa sauvegarde .bak la plus recente

Usage: python revert-fichier.py --fichier <path> [--depuis-bak]
"""

import sys
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Revert fichier depuis .bak")
    parser.add_argument("--fichier", required=True, help="Fichier a revert")
    parser.add_argument("--depuis-bak", action="store_true", help="Utiliser le .bak le plus recent")
    args = parser.parse_args()

    filepath = Path(args.fichier)
    if not filepath.exists():
        print(f"Fichier introuvable: {filepath}")
        return 1

    # Trouver le .bak le plus recent
    bak_files = list(filepath.parent.glob(f"{filepath.name}.bak.*"))
    if not bak_files:
        print(f"Aucune sauvegarde .bak trouvee pour {filepath}")
        return 1

    latest_bak = max(bak_files, key=lambda p: p.stat().st_mtime)
    print(f"Revert depuis: {latest_bak}")

    # Lire la sauvegarde
    content = latest_bak.read_text(encoding="utf-8")

    # Ecrire dans le fichier original
    filepath.write_text(content, encoding="utf-8")
    print(f"Revert effectue: {filepath}")
    return 0


if __name__ == "__main__":
    sys.exit(main())