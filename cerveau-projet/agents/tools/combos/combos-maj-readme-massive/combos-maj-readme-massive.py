#!/usr/bin/env python3
# combos-maj-readme-massive.py
# Combo maj-readme-massive : GROSSE mise a jour conservative du README
# (analyse complete -> verifier -> maj -> correctifs de fond -> ASCII -> rapport)
# Proprietaire : Clio (outil partage)
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION = "0.1.0"
STATUT = "prepare"

import datetime
import os
import re
import subprocess
import sys
from pathlib import Path

if sys.stdout.isatty():
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    NC = "\033[0m"
else:
    RED = GREEN = YELLOW = BLUE = NC = ""

OUTILS = {
    "mettre-a-jour-readme": "cerveau-projet/agents/tools/mettre-a-jour/mettre-a-jour-readme/mettre-a-jour-readme.py",
    "combos-analyse-projet": "cerveau-projet/agents/tools/combos/combos-analyse-projet/combos-analyse-projet.py",
    "valider-conformite-ascii": "cerveau-projet/agents/tools/valider/valider-conformite-ascii/valider-conformite-ascii.py",
    "editer-fichier": "cerveau-projet/agents/tools/editer/editer-fichier/editer-fichier.py",
    "lire-fichier": "cerveau-projet/agents/tools/lire/lire-fichier/lire-fichier.py",
}


def verifier_nommage():
    nom = Path(__file__).name
    dossier = Path(__file__).resolve().parent.name
    if not nom.startswith(dossier):
        print(RED + "[ERREUR] Nommage invalide : le fichier doit commencer par '" + dossier + "'" + NC)
        sys.exit(2)


def executer(racine, rel, args):
    p = Path(racine) / rel
    if not p.is_file():
        print(RED + "[ERREUR] Outil introuvable : " + str(p) + NC)
        return None
    try:
        proc = subprocess.run(
            [sys.executable, str(p)] + args,
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600,
        )
        return (proc.stdout or "") + (proc.stderr or "")
    except Exception as e:
        print(RED + "[ERREUR] Echec d'execution de " + str(p) + " : " + str(e) + NC)
        return None


def main():
    verifier_nommage()
    import argparse

    parser = argparse.ArgumentParser(
        prog="combos-maj-readme-massive",
        description="Combo maj-readme-massive : grosse mise a jour conservative du README.",
    )
    parser.add_argument("racine", nargs="?", default=".", help="Racine du projet (defaut: .)")
    parser.add_argument("--rapport", action="store_true",
                        help="Sauvegarder le rapport dans clio/rapports/")
    parser.add_argument("--version", action="version",
                        version="combos-maj-readme-massive " + VERSION + " (" + STATUT + ")")
    args = parser.parse_args()

    racine = Path(args.racine)
    print(BLUE + "=== combos-maj-readme-massive v" + VERSION + " ===" + NC)
    print("Racine : " + str(racine.resolve()))
    print("Date : " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("")
    print(YELLOW + "MODE CONSERVATIF : la structure du README est conservee - on corrige "
                   "les compteurs, tables et badges, on ne refond pas les sections." + NC)
    print("")

    etapes = []
    rapport = []

    # Etape 1 : analyse complete
    print(BLUE + "--- Etape 1/5 : analyse complete (combos-analyse-projet) ---" + NC)
    r = executer(racine, OUTILS["combos-analyse-projet"], [])
    if r is None:
        return 1
    print(r)
    etapes.append("analyse")
    rapport.append("## Etape 1 - Analyse\n\n" + r + "\n")

    # Etape 2 : verifier
    print(BLUE + "--- Etape 2/5 : verifier (mettre-a-jour-readme --verifier) ---" + NC)
    r = executer(racine, OUTILS["mettre-a-jour-readme"], ["--verifier"])
    if r is None:
        return 1
    print(r)
    etapes.append("verifier")
    rapport.append("## Etape 2 - Verifier\n\n" + r + "\n")

    # Etape 3 : maj des compteurs
    print(BLUE + "--- Etape 3/5 : maj des compteurs (--maj) ---" + NC)
    r = executer(racine, OUTILS["mettre-a-jour-readme"], ["--maj"])
    if r is None:
        return 1
    print(r)
    etapes.append("maj")
    rapport.append("## Etape 3 - Maj compteurs\n\n" + r + "\n")

    # Etape 4 : correctifs de fond (tables, categories manquantes)
    print(BLUE + "--- Etape 4/5 : correctifs de fond (tables et categories) ---" + NC)
    print(YELLOW + "  Indice : verifier le resultat du --maj - si une NOUVELLE categorie est "
                   "absente de la table, inserer manuellement la ligne avec editer-fichier "
                   "(lecon Clio : --maj ne cree pas les nouvelles lignes de categories)." + NC)
    print(YELLOW + "  Indice : verifier aussi les badges du header (Outils-N) et la table des "
                   "agents - aligner sur les compteurs reels." + NC)
    etapes.append("correctifs")
    rapport.append("## Etape 4 - Correctifs de fond\n\n"
                   "Correctifs appliques manuellement (nouvelles categories, badges, tables).\n")

    # Etape 5 : ASCII
    print(BLUE + "--- Etape 5/5 : verification ASCII ---" + NC)
    r = executer(racine, OUTILS["valider-conformite-ascii"], ["README.md"])
    if r is None:
        return 1
    print(r)
    etapes.append("ascii")
    rapport.append("## Etape 5 - ASCII\n\n" + r + "\n")

    # Synthese
    print("")
    print(BLUE + "=== SYNTHESE ===" + NC)
    print("Etapes executees : " + ", ".join(etapes))
    print(GREEN + "Grosse MAJ conservative terminee. Verifier ensuite avec combos-analyse-projet "
                  "que le verdict passe a A JOUR." + NC)

    if args.rapport:
        rapport_dir = racine / "cerveau-projet" / "agents" / "clio" / "rapports"
        rapport_dir.mkdir(parents=True, exist_ok=True)
        date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
        rapport_file = rapport_dir / ("maj-readme-massive-" + date + ".md")
        contenu = [
            "# Rapport de grosse MAJ du README -- " + date,
            "",
            "## Contexte",
            "- Combo utilise : combos-maj-readme-massive v" + VERSION,
            "- Mode : conservatif (structure conservee)",
            "- Racine : " + str(racine.resolve()),
            "",
        ] + rapport
        rapport_file.write_text("\n".join(contenu) + "\n", encoding="utf-8")
        print("")
        print(GREEN + "Rapport sauvegarde : " + str(rapport_file) + NC)

    return 0


if __name__ == "__main__":
    sys.exit(main())
