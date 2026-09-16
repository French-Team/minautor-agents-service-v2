#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ajouter-redirect-theme.py -- Ajouter un redirect securise dans un theme JSON

Usage: python ajouter-redirect-theme.py <fichier-theme.json> --besoin "<texte>" --vers-type <type> --vers-fichier <fichier> [--vers-case <case>] [--condition "<txt>"]
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description="Ajouter un redirect dans un theme")
    parser.add_argument("fichier", help="Fichier theme JSON")
    parser.add_argument("--besoin", required=True, help="Description du besoin")
    parser.add_argument("--vers-type", required=True, choices=["theme", "protocole", "combo", "outil", "bdd", "procedure"])
    parser.add_argument("--vers-fichier", required=True, help="Fichier cible")
    parser.add_argument("--vers-case", help="Case cible (optionnel)")
    parser.add_argument("--condition", help="Condition de declenchement (optionnel)")
    args = parser.parse_args()

    filepath = Path(args.fichier)
    if not filepath.exists():
        print(f"Fichier introuvable: {filepath}")
        return 1

    # Sauvegarde
    bak_path = filepath.with_suffix(f".bak.{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    filepath.rename(bak_path)
    print(f"Sauvegarde: {bak_path}")

    try:
        with open(bak_path, "r", encoding="utf-8") as f:
            theme = json.load(f)
    except json.JSONDecodeError as e:
        print(f"JSON invalide: {e}")
        return 1

    # Construire le redirect
    redirect = {
        "besoin": args.besoin,
        "action": "redirect",
        "vers": {
            "type": args.vers_type,
            "fichier": args.vers_fichier,
        },
    }
    if args.vers_case:
        redirect["vers"]["case"] = args.vers_case
    if args.condition:
        redirect["condition"] = args.condition

    # Ajouter au theme
    if "theme" not in theme:
        theme["theme"] = {}
    if "redirects" not in theme["theme"]:
        theme["theme"]["redirects"] = []

    theme["theme"]["redirects"].append(redirect)

    # Ecrire
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(theme, f, ensure_ascii=False, indent=2)

    print(f"Redirect ajoute dans {filepath}")
    return 0


if __name__ == "__main__":
    sys.exit(main())