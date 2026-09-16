#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
calculer-hash.py -- Calculer SHA256 d'un fichier

Usage: python calculer-hash.py <fichier>
"""

import sys
import hashlib
from pathlib import Path


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 1

    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"Fichier introuvable: {filepath}")
        return 1

    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)

    hash_hex = sha256.hexdigest()
    print(f"{hash_hex}  {filepath}")
    return 0


if __name__ == "__main__":
    sys.exit(main())