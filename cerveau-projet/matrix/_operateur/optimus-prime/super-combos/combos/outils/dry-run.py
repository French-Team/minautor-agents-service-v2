#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dry-run.py -- Simule une evolution sans ecrire (M-107)

Simule l ajout d une case ou d un redirect dans un theme : charge en
memoire, applique, valide (JSON + tester-theme sur copie tmp-optimus),
affiche diff resume. Le fichier cible N EST JAMAIS modifie.
Usage:
  python dry-run.py ajouter-case --fichier <theme> --besoin "..." --etapes "a" "b" [--regle "..."]
  python dry-run.py ajouter-redirect --fichier <theme> --besoin "..." --vers-type <t> --vers-fichier <f> [--vers-case C] [--condition "..."]
"""

import sys
import json
import argparse
import subprocess
import shutil
from datetime import datetime
from pathlib import Path


def _tmp_copy(fichier: Path, contenu: dict) -> Path:
    tmpdir = Path("cerveau-projet/matrix/tmp-optimus")
    if not tmpdir.is_dir():
        alt = Path(__file__).parent / "tmp-dry-run"
        alt.mkdir(exist_ok=True)
        tmpdir = alt
    else:
        tmpdir.mkdir(exist_ok=True)
    dest = tmpdir / f"_dryrun-{datetime.now().strftime('%H%M%S')}-{fichier.name}"
    dest.write_text(json.dumps(contenu, ensure_ascii=False, indent=2), encoding="utf-8")
    return dest


def main():
    parser = argparse.ArgumentParser(description="Simule une evolution sans ecrire")
    parser.add_argument("operation", choices=["ajouter-case", "ajouter-redirect"])
    parser.add_argument("--fichier", required=True)
    parser.add_argument("--besoin", required=True)
    parser.add_argument("--etapes", nargs="*", default=[])
    parser.add_argument("--regle", default="")
    parser.add_argument("--vers-type", default="")
    parser.add_argument("--vers-fichier", default="")
    parser.add_argument("--vers-case", default="")
    parser.add_argument("--condition", default="")
    args = parser.parse_args()

    fichier = Path(args.fichier)
    if not fichier.is_file():
        print(f"Fichier introuvable: {fichier}")
        return 2
    avant = fichier.read_text(encoding="utf-8")
    try:
        theme = json.loads(avant)
    except ValueError as e:
        print(f"Theme JSON invalide: {e}")
        return 2

    if args.operation == "ajouter-case":
        if not args.etapes:
            print("ajouter-case exige --etapes")
            return 2
        case = {"besoin": args.besoin, "action": "procedure", "etapes": args.etapes}
        if args.regle:
            case["regle"] = args.regle
    else:
        if not args.vers_type or not args.vers_fichier:
            print("ajouter-redirect exige --vers-type et --vers-fichier")
            return 2
        case = {"besoin": args.besoin, "action": "redirect",
                "vers": {"type": args.vers_type, "fichier": args.vers_fichier}}
        if args.vers_case:
            case["vers"]["case"] = args.vers_case
        if args.condition:
            case["condition"] = args.condition

    theme.setdefault("theme", {}).setdefault("redirects", []).append(case)
    apres = json.dumps(theme, ensure_ascii=False, indent=2)

    print(f"=== DRY-RUN {args.operation} sur {fichier.name} ===")
    print(f"Taille : {len(avant)} -> {len(apres)} chars (+{len(apres) - len(avant)})")
    print(f"Cases : avant/apres = redirect ajoute en position {len(theme['theme']['redirects']) - 1}")
    print(f"Nouvelle case : {json.dumps(case, ensure_ascii=False)[:300]}")

    # Validation sur copie tmp (tester-theme si dispo)
    dest = _tmp_copy(fichier, theme)
    try:
        tester = Path(__file__).parent / "tester-theme.py"
        if tester.is_file():
            r = subprocess.run([sys.executable, str(tester), str(dest)],
                               capture_output=True, text=True)
            print(f"Validation simulee (tester-theme) : {'OK' if r.returncode == 0 else 'KO'}")
            if r.returncode != 0:
                print(r.stdout.strip())
        else:
            print("Validation simulee : JSON OK (tester-theme absent)")
    finally:
        try:
            dest.unlink()
        except OSError:
            pass

    # Preuve de non-ecriture
    intact = fichier.read_text(encoding="utf-8") == avant
    print(f"Fichier cible inchange : {'OUI' if intact else 'NON (ANOMALIE)'}.")
    return 0 if intact else 1


if __name__ == "__main__":
    sys.exit(main())
