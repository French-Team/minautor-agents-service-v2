#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bilan-matrice.py -- Tableau de bord zone Optimus + Matrice (M-105)

Agrege : file missions (journal), stats auto-evolution (bdd-frictions),
suivi-optimus, lecons, verdict non-regression. Lecture seule.
Usage: python bilan-matrice.py [--racine <path>]
       section [remorque] : joue `remorque etat` -- un equipement de la zone cree
       pendant la mission et NON declare se DIT ici, et le PRE-VOL de la
       non-regression refuse alors la suite.

"""

import sys
import json
import argparse
import subprocess
import sys
from pathlib import Path

# --- DOMICILE DU LANCEMENT (EO-430 / MO-414, vague 3 du lot) -----------------
RACINE_MATRICE_LANCEMENT = Path(__file__).resolve().parent.parent.parent.parent.parent.parent
if RACINE_MATRICE_LANCEMENT.name != "matrix":
    raise RuntimeError("Structure inattendue : " + str(RACINE_MATRICE_LANCEMENT)
                       + " n est pas la racine `matrix` (garde-foi L-006)")
REPERTOIRE_COMMUN_LANCEMENT = RACINE_MATRICE_LANCEMENT / "matrice" / "data" / "commun"
if not (REPERTOIRE_COMMUN_LANCEMENT / "lancement.py").is_file():
    raise RuntimeError("Structure inattendue : " + str(REPERTOIRE_COMMUN_LANCEMENT)
                       + " ne porte pas le domicile du lancement")
if str(REPERTOIRE_COMMUN_LANCEMENT) not in sys.path:
    sys.path.insert(0, str(REPERTOIRE_COMMUN_LANCEMENT))
from lancement import drapeaux_popen  # noqa: E402


def lancer_enfant(*arguments, **options):
    """Le SEUL lancement de processus de cet outil : jamais de fenetre."""
    return subprocess.run(*arguments, **options, **drapeaux_popen())
import sqlite3
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Tableau de bord Matrice/Optimus")
    parser.add_argument("--racine", default=".", help="Racine projet (defaut: cwd)")
    parser.add_argument("--rapide", action="store_true", help="Saute la non-regression (bilan rapide)")
    args = parser.parse_args()

    racine = Path(args.racine).resolve()
    matrix = None
    for cand in (racine, racine / "matrix", racine / "cerveau-projet" / "matrix"):
        if (cand / "matrice" / "data").is_dir():
            matrix = cand if cand.name == "matrix" else cand / ("matrix" if (cand / "matrix").is_dir() else "cerveau-projet/matrix")
            break
    if matrix is None or not (matrix / "matrice" / "data").is_dir():
        print(f"Dossier matrix/ introuvable depuis {args.racine}")
        return 2
    data = matrix / "matrice" / "data"
    outils = matrix / "_operateur" / "optimus-prime" / "super-combos" / "combos" / "outils"

    print("=== BILAN MATRICE / OPTIMUS ===")

    # 1. File missions (journal)
    crees, terminees = [], set()
    try:
        for ligne in (data / "historiques-missions.jsonl").read_text(encoding="utf-8").splitlines():
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                e = json.loads(ligne)
            except ValueError:
                continue
            if e.get("type") == "mission-creee" and e.get("id"):
                crees.append(e["id"])
            elif e.get("type") == "mission-terminee" and e.get("id"):
                terminees.add(e["id"])
    except OSError:
        pass
    attente = [i for i in crees if i not in terminees]
    print(f"\n[missions] terminees={len(terminees)} en-attente={len(attente)}")
    if attente:
        print(f"  file: {', '.join(attente)}")

    # 2. Stats auto-evolution (bdd frictions)
    print("\n[frictions]")
    r = lancer_enfant([sys.executable, str(outils / "bdd-frictions" / "main.py"), "stats"],
                       capture_output=True, text=True)
    print("  " + (r.stdout.strip().replace("\n", "\n  ") if r.returncode == 0 else f"outil KO: {r.stderr.strip()[:200]}"))

    # 3. Suivi-optimus + lecons
    try:
        n_suivi = sum(1 for _ in open(data / "suivi-optimus.jsonl", encoding="utf-8"))
    except OSError:
        n_suivi = -1
    try:
        lecons = json.loads((data / "lecons.json").read_text(encoding="utf-8"))
        n_lecons = len(lecons.get("lecons", []))
    except (OSError, ValueError):
        n_lecons = -1
    print(f"\n[traces] suivi-optimus={n_suivi} evenements, lecons={n_lecons}")

    # 4. Remorque (attelage) : un equipement NEUF s'est-il declare ?
    # La promesse du README de la remorque ("bilan-matrice le rappelle") etait
    # FAUSSE : mesure du 2026-09-21 -- ce fichier ne prononcait pas le mot.
    # Le bilan JOUE la remorque et DIT son verdict ; il ne decide rien, la suite
    # le fait. Un equipement cree pendant la mission et non declare est l'ecart
    # que le PRE-VOL refuse.
    print("\n[remorque]")
    remorque = matrix / "_operateur" / "optimus-prime" / "remorque" / "remorque-optimus.py"
    if remorque.is_file():
        resultat = lancer_enfant([sys.executable, str(remorque), "etat"],
                                  capture_output=True, text=True)
        verdicts = [l.strip() for l in resultat.stdout.splitlines()
                    if l.strip().startswith(("Remorque", "REFUS", "ECART"))]
        print("  " + (verdicts[-1] if verdicts else
                      "verdict INTROUVABLE (la remorque n'a rendu aucune ligne de verdict)"))
    else:
        print("  remorque INTROUVABLE : " + str(remorque))

    # 5. Verdict non-regression (sauf --rapide)

    if args.rapide:
        print("\n[non-regression] sautee (--rapide)")
    else:
        print("\n[non-regression]")
        r = lancer_enfant([sys.executable, str(outils / "lanceur-non-regression.py"),
                            "--racine", str(racine)], capture_output=True, text=True)
        for ligne in r.stdout.strip().splitlines():
            if ligne.startswith(("==", "  ", "VERDICT")):
                print(f"  {ligne}")

    print("\n=== FIN BILAN ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
