#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tester-theme.py -- Test un theme case par case (accessibilite, boucles, fins)

Usage: python tester-theme.py <fichier-theme.json>
"""

import sys
import json
from pathlib import Path
from typing import Set, Dict, Any, List

# Racine matrix/ DETECTEE par le marqueur partage (M-076 : matrice/data/commun/racine.py),
# jamais comptee a la main (L-013).
BORNES_REMONTEE = 30
_courant = Path(__file__).resolve().parent
for _ in range(BORNES_REMONTEE):
    if (_courant / "matrice" / "data" / "commun" / "racine.py").is_file():
        break
    _courant = _courant.parent
else:
    raise RuntimeError("Racine matrix/ introuvable en remontant.")
RACINE_MATRICE = _courant


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 1

    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"Fichier introuvable: {filepath}")
        return 1

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            theme = json.load(f)
    except json.JSONDecodeError as e:
        print(f"JSON invalide: {e}")
        return 1

    errors = []
    warnings = []

    # 1. Verifier structure de base
    if "theme" not in theme:
        errors.append("Champ 'theme' manquant")
    else:
        t = theme["theme"]
        if "redirects" not in t:
            errors.append("Champ 'theme.redirects' manquant")
        else:
            redirects = t["redirects"]
            # 2. Verifier chaque redirect
            cases_connues = set()
            for i, r in enumerate(redirects):
                case_id = f"case_{i}"
                if "besoin" in r:
                    cases_connues.add(r["besoin"])

                # Verifier action
                if "action" not in r:
                    errors.append(f"{case_id}: champ 'action' manquant")
                elif r["action"] == "redirect":
                    if "vers" not in r:
                        errors.append(f"{case_id} (redirect): champ 'vers' manquant")
                    else:
                        vers = r["vers"]
                        # Un 'vers' qui n'est pas un OBJET est une ERREUR DITE, jamais un
                        # plantage : la version precedente faisait tomber le testeur
                        # (AttributeError sur une chaine) au lieu d'accuser le theme --
                        # un controle qui crashe ne dit rien (lecon L-026).
                        if not isinstance(vers, dict):
                            errors.append(f"{case_id} (redirect): 'vers' doit etre un OBJET"
                                          f" (type + fichier), recu {type(vers).__name__}")
                        elif "type" not in vers:
                            errors.append(f"{case_id}: redirect sans type")
                        elif vers["type"] in ("theme", "protocole", "combo", "outil", "fiche", "convention", "regle"):
                            if "fichier" not in vers and "dossier" not in vers:
                                errors.append(f"{case_id}: redirect {vers['type']} sans fichier ni dossier")

            # 3. Verifier fin
            if "fin" not in theme:
                warnings.append("Champ 'fin' manquant (theme sans fin explicite)")
            else:
                fin = theme["fin"]
                if fin.get("type") == "lien" and "vers" not in fin:
                    errors.append("Fin de type lien sans champ 'vers'")

    # 4. Detecter boucles potentielles (redirects vers le meme fichier)
    if "theme" in theme and "redirects" in theme["theme"]:
        for i, r in enumerate(theme["theme"]["redirects"]):
            if r.get("action") == "redirect" and isinstance(r.get("vers"), dict):
                vers = r["vers"]
                if vers.get("type") == "theme" and vers.get("fichier") == filepath.name and "case" not in vers:
                    warnings.append(f"case_{i}: redirect vers soi-meme sans case (risque boucle)")

    # 5. Verifier existence des cibles (redirects + fin)
    # Convention : cibles exprimees en relatif depuis optimus-prime/ ; repli theme-dir puis cwd
    def _existe(cible):
        p = Path(cible)
        if p.is_absolute():
            return p.exists()
        for base in (OPTIMUS_ROOT, filepath.parent, Path.cwd()):
            if (base / cible).exists():
                return True
        return False

    OPTIMUS_ROOT = RACINE_MATRICE / "_operateur" / "optimus-prime"
    if "theme" in theme and "redirects" in theme["theme"]:
        for i, r in enumerate(theme["theme"]["redirects"]):
            if r.get("action") == "redirect" and isinstance(r.get("vers"), dict):
                vers = r["vers"]
                if vers.get("type") in ("theme", "protocole", "combo", "outil", "fiche", "convention", "regle"):
                    cible = vers.get("fichier") or vers.get("dossier")
                    if cible and not _existe(cible):
                        warnings.append(f"case_{i}: cible introuvable ({cible})")
        fin = theme.get("fin", {})
        if fin.get("type") == "lien" and "vers" in fin:
            if not _existe(fin["vers"]):
                warnings.append(f"fin: cible introuvable ({fin['vers']})")

    # Affichage resultats
    print(f"=== Test theme: {filepath.name} ===")
    if errors:
        print(f"\nERREURS ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")
    else:
        print("\nAucune erreur structurelle.")

    if warnings:
        print(f"\nAVERTISSEMENTS ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")

    print(f"\nCases detectees: {len(cases_connues) if 'cases_connues' in locals() else 0}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())