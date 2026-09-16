#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ajouter-case-theme.py -- Ajouter une case securisee dans un theme JSON

Usage: python ajouter-case-theme.py <fichier-theme.json> --besoin "<texte>" --action procedure --etapes "etape1" "etape2" --regle "<regle>"
       python ajouter-case-theme.py <fichier-theme.json> --besoin "<texte>" --action redirect --vers-type theme --vers-fichier <fichier> [--vers-case <case>]
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description="Ajouter une case dans un theme")
    parser.add_argument("fichier", help="Fichier theme JSON")
    parser.add_argument("--besoin", required=True, help="Description du besoin")
    parser.add_argument("--action", required=True, choices=["procedure", "redirect"])
    parser.add_argument("--etapes", nargs="+", help="Etapes (pour action=procedure)")
    parser.add_argument("--regle", help="Regle associee (pour action=procedure)")
    parser.add_argument("--vers-type", choices=["theme", "protocole", "combo", "outil", "bdd", "procedure"], help="Type de redirect")
    parser.add_argument("--vers-fichier", help="Fichier cible (pour redirect)")
    parser.add_argument("--vers-case", help="Case cible (pour redirect)")
    parser.add_argument("--condition", help="Condition de declenchement (pour redirect)")
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

    # Construire la nouvelle case
    if args.action == "procedure":
        if not args.etapes:
            print("Erreur: --etapes requis pour action=procedure")
            return 1
        nouvelle_case = {
            "besoin": args.besoin,
            "action": "procedure",
            "etapes": args.etapes,
        }
        if args.regle:
            nouvelle_case["regle"] = args.regle
    else:  # redirect
        if not args.vers_type or not args.vers_fichier:
            print("Erreur: --vers-type et --vers-fichier requis pour action=redirect")
            return 1
        nouvelle_case = {
            "besoin": args.besoin,
            "action": "redirect",
            "vers": {
                "type": args.vers_type,
                "fichier": args.vers_fichier,
            },
        }
        if args.vers_case:
            nouvelle_case["vers"]["case"] = args.vers_case
        if args.condition:
            nouvelle_case["condition"] = args.condition

    # Ajouter au theme
    if "theme" not in theme:
        theme["theme"] = {}
    if "redirects" not in theme["theme"]:
        theme["theme"]["redirects"] = []

    theme["theme"]["redirects"].append(nouvelle_case)

    # Ecrire
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(theme, f, ensure_ascii=False, indent=2)

    print(f"Case ajoutee dans {filepath}")
    return 0


if __name__ == "__main__":
    sys.exit(main())