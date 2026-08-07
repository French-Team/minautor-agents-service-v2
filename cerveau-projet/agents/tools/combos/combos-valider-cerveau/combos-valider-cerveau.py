#!/usr/bin/env python3
# combos-valider-cerveau.py
# Combo de validation : etat de sante du cerveau-projet en une commande
VERSION = "0.2.0-py"
STATUT = "beta"

import subprocess
import sys
from pathlib import Path

# Couleurs ANSI (desactivees si la sortie n'est pas un terminal)
if sys.stdout.isatty():
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    NC = "\033[0m"
else:
    RED = GREEN = YELLOW = BLUE = NC = ""

VALIDATEURS = [
    ("valider-relecture", "valider-relecture/valider-relecture.sh"),
    ("valider-cartes-decision", "valider-cartes-decision/valider-cartes-decision.sh"),
    ("valider-conformite-ascii", "valider-conformite-ascii/valider-conformite-ascii.sh"),
]


def verifier_nommage():
    """Regle immuable : le nom du fichier doit commencer par le prefixe du dossier de categorie."""
    nom = Path(__file__).name
    dossier = Path(__file__).resolve().parent.name
    if not nom.startswith(dossier):
        print(RED + "[ERREUR] Nommage invalide : le fichier doit commencer par '" + dossier + "'" + NC)
        print("  Nom actuel : " + nom)
        sys.exit(2)


def trouver_racine():
    """Racine du projet: combos-valider-cerveau/ (script) -> combos/ -> tools/ -> agents/ -> cerveau-projet/ -> racine du projet"""
    return Path(__file__).resolve().parent.parent.parent.parent.parent.parent


def executer_outil(nom, chemin, detail):
    """Executer un validateur et retourner son code de retour."""
    print(BLUE + "--- " + nom + " ---" + NC)

    if not chemin.is_file():
        print("  " + RED + "[ERREUR] outil absent" + NC)
        return 2

    try:
        proc = subprocess.run(
            ["bash", str(chemin)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )
        code = proc.returncode
        sortie = proc.stdout + proc.stderr
    except subprocess.TimeoutExpired:
        print("  " + RED + "[ERREUR]" + NC + " " + nom + " (timeout)")
        return 1
    except OSError as e:
        print("  " + RED + "[ERREUR]" + NC + " " + nom + " (" + str(e) + ")")
        return 1

    if detail:
        for ligne in sortie.splitlines()[:30]:
            print(ligne)
        print("")

    if code == 0:
        print("  " + GREEN + "[OK]" + NC + " " + nom)
        return 0
    else:
        print("  " + RED + "[ERREUR]" + NC + " " + nom + " (code " + str(code) + ")")
        return 1


def main():
    verifier_nommage()

    import argparse

    parser = argparse.ArgumentParser(
        prog="combos-valider-cerveau",
        description="Etat de sante du cerveau-projet en une commande (3 validateurs + verdict combine).",
    )
    parser.add_argument("--detail", action="store_true", help="Afficher la sortie complete des 3 outils")
    parser.add_argument("--stop", action="store_true", help="Arreter au premier echec")
    parser.add_argument("--version", action="version", version="combos-valider-cerveau " + VERSION + " (" + STATUT + ")")
    args = parser.parse_args()

    racine = trouver_racine()
    outils_dir = racine / "cerveau-projet" / "agents" / "tools" / "valider"

    print(BLUE + "=== combos-valider-cerveau v" + VERSION + " ===" + NC)
    print("Etat de sante du cerveau-projet")
    print("")

    codes = {}

    for nom, rel in VALIDATEURS:
        code = executer_outil(nom, outils_dir / rel, args.detail)
        codes[nom] = code
        if args.stop and code != 0:
            print("")
            print(RED + "=== VERDICT GLOBAL : NON CONFORME (arrete sur " + nom + ") ===" + NC)
            return 1

    # Rapport combine
    print("")
    print(BLUE + "=== VERDICT GLOBAL ===" + NC)
    for nom, _ in VALIDATEURS:
        ok = codes.get(nom, 1) == 0
        ligne = "  " + nom + " : "
        if ok:
            print(ligne + GREEN + "OK" + NC)
        else:
            print(ligne + RED + "ERREUR" + NC)

    total_ok = sum(1 for nom, _ in VALIDATEURS if codes.get(nom, 1) == 0)

    if total_ok == len(VALIDATEURS):
        print("  RESULTAT      : " + GREEN + "CONFORME" + NC)
        print("  Code retour   : 0")
        return 0
    else:
        print("  RESULTAT      : " + RED + "NON CONFORME (" + str(total_ok) + "/" + str(len(VALIDATEURS)) + ")" + NC)
        print("  Code retour   : 1")
        return 1


if __name__ == "__main__":
    sys.exit(main())
