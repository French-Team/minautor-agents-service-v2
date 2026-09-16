#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
c-003-historique -- Combo numerote c-003 dedie a la BDD Historiques des missions (historiques-missions.jsonl)

Genere par creer-combo.py (imperatif 46, contrat de nommage CV-008) le 2026-09-13 10:43:41.
Chaine : lire (filtre par tags) -> normaliser -> noter usage.

Usage:
    python main.py executer [--tag <tag>] [--mission <id>]
    python main.py lire [--tag <tag>]
    python main.py status
"""

import sys
import argparse
import subprocess
from pathlib import Path


# --- Constantes (convention-zero-valeurs-en-dur) ---------------------------

COMBO_ID = "c-003-historique"
COMBO_NUMERO = "c-003"
BDD_ID = "historique"
BDD_TITRE = "Historiques des missions (historiques-missions.jsonl)"
OUTIL_BDD_REL = "matrice/data/outils/bdd-historique/main.py"
COMMANDE_LIRE = "lire"
OPTION_FILTRE = "--tag"
OUTIL_USAGES_REL = "matrice/data/outils/bdd-usages/main.py"
TAGS_USAGE = "combo,bdd," + BDD_ID
COMMANDE_USAGE = "executer"

BORNES_REMONTEE = 30
REPERTOIRE_COMBO = Path(__file__).resolve().parent
_courant = REPERTOIRE_COMBO
for _ in range(BORNES_REMONTEE):
    if (_courant / "matrice" / "data" / "commun" / "racine.py").is_file():
        break
    _courant = _courant.parent
else:
    raise RuntimeError("Racine matrix/ introuvable en remontant.")
RACINE_MATRICE = _courant
OUTIL_BDD = RACINE_MATRICE / OUTIL_BDD_REL
OUTIL_USAGES = RACINE_MATRICE / OUTIL_USAGES_REL

CODE_OK = 0
CODE_ECHEC = 1
CODE_INJOIGNABLE = 127


def lancer_outil(chemin, arguments):
    """Executer un outil Python et retourner (code, stdout, stderr)."""
    if not chemin.exists():
        return CODE_INJOIGNABLE, "", "Outil introuvable : " + str(chemin)
    resultat = subprocess.run(
        [sys.executable, str(chemin)] + arguments,
        capture_output=True,
        text=True,
    )
    return resultat.returncode, resultat.stdout, resultat.stderr


def args_lecture(tag):
    """Construire les arguments de lecture (commande + filtre optionnel)."""
    arguments = [COMMANDE_LIRE]
    if tag:
        arguments += [OPTION_FILTRE, tag]
    return arguments


def lire_bdd(tag):
    """Etape 1 : lire la BDD (filtre par tags optionnel)."""
    return lancer_outil(OUTIL_BDD, args_lecture(tag))


def normaliser(sortie):
    """Etape 2 : resumer la sortie (lignes utiles, jamais vides)."""
    lignes = [l for l in sortie.splitlines() if l.strip()]
    return len(lignes), lignes


def noter_usage(code):
    """Etape 3 : noter l'usage du combo dans la BDD usages."""
    return lancer_outil(
        OUTIL_USAGES,
        ["noter", "--outil", COMBO_ID, "--commande", COMMANDE_USAGE,
         "--code", str(code), "--tags", TAGS_USAGE],
    )


def cmd_lire(arguments):
    """Passerelle directe vers la lecture de la BDD."""
    parser = argparse.ArgumentParser(description="Lire la BDD " + BDD_TITRE)
    parser.add_argument("--tag", default=None, help="Filtre par tag")
    parsed = parser.parse_args(arguments)

    code, sortie, erreur = lire_bdd(parsed.tag)
    if sortie:
        print(sortie, end="")
    if erreur:
        print(erreur, end="", file=sys.stderr)
    return code


def cmd_executer(arguments):
    """Chaine complete : lire -> normaliser -> noter usage."""
    parser = argparse.ArgumentParser(description="Executer le combo " + COMBO_ID)
    parser.add_argument("--tag", default=None, help="Filtre par tag")
    parser.add_argument("--mission", default=None, help="ID de mission (trace)")
    parsed = parser.parse_args(arguments)

    print("=" * 60)
    print("COMBO " + COMBO_NUMERO + " (" + COMBO_ID + ") -- BDD " + BDD_TITRE)
    print("=" * 60)

    print("\nETAPE 1/3 -- LIRE")
    code, sortie, erreur = lire_bdd(parsed.tag)
    if sortie:
        print(sortie, end="")
    if erreur:
        print(erreur, end="", file=sys.stderr)

    print("\nETAPE 2/3 -- NORMALISER")
    nombre, lignes = normaliser(sortie)
    print("Lignes utiles : " + str(nombre))

    print("\nETAPE 3/3 -- NOTER USAGE")
    code_usage, _, erreur_usage = noter_usage(code)
    if erreur_usage:
        print(erreur_usage, end="", file=sys.stderr)
    print("Usage note : " + COMBO_ID)

    print("\n" + "=" * 60)
    print("RESULTAT : code " + str(code) + " (" + str(nombre) + " lignes)")
    print("=" * 60)
    return code if code in (CODE_OK, CODE_ECHEC) else CODE_ECHEC


def cmd_status(arguments):
    """Etat du combo : outil BDD joignable, BDD declaree, piste d'usage."""
    print("Combo  : " + COMBO_NUMERO + " (" + COMBO_ID + ")")
    print("BDD    : " + BDD_ID + " (" + BDD_TITRE + ")")
    print("Outil  : " + str(OUTIL_BDD) + (" [OK]" if OUTIL_BDD.exists() else " [ABSENT]"))
    print("Usages : " + str(OUTIL_USAGES) + (" [OK]" if OUTIL_USAGES.exists() else " [ABSENT]"))
    return CODE_OK if OUTIL_BDD.exists() else CODE_ECHEC


VERBES = {
    "executer": cmd_executer,
    "lire": cmd_lire,
    "status": cmd_status,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in VERBES:
        print(__doc__)
        return CODE_ECHEC
    return VERBES[sys.argv[1]](sys.argv[2:])


if __name__ == "__main__":
    sys.exit(main())
