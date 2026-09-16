#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lire-fichier-complet.py -- Lire un fichier en entier (controle encodage, taille)

Usage: python lire-fichier-complet.py <fichier>
"""

import sys
from pathlib import Path


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 1

    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"Fichier introuvable: {filepath}")
        return 1

    try:
        content = filepath.read_text(encoding="utf-8")
        print(f"=== {filepath} ({len(content)} chars, {content.count(chr(10)) + 1} lignes) ===")
        print(content)
        return 0
    except UnicodeDecodeError as e:
        print(f"Erreur encodage (non UTF-8): {e}")
        return 1
    except Exception as e:
        print(f"Erreur lecture: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())