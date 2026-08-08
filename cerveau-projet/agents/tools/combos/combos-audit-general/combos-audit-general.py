#!/usr/bin/env python3
# combos-audit-general.py
# Combo audit-general : chainage des 4 evaluateurs + synthese
# Proprietaire : Themis (outil partage)
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION = "0.2.0-py"
STATUT = "beta"

import datetime
import os
import re
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

EVALUATEURS = [
    ("evaluer-structure", "evaluer-structure/evaluer-structure.sh"),
    ("evaluer-conventions", "evaluer-conventions/evaluer-conventions.sh"),
    ("evaluer-coherence", "evaluer-coherence/evaluer-coherence.sh"),
    ("evaluer-agents", "evaluer-agents/evaluer-agents.sh"),
]


def verifier_nommage():
    """Regle immuable : le nom du fichier doit commencer par le prefixe du dossier de categorie."""
    nom = Path(__file__).name
    dossier = Path(__file__).resolve().parent.name
    if not nom.startswith(dossier):
        print(RED + "[ERREUR] Nommage invalide : le fichier doit commencer par '" + dossier + "'" + NC)
        print("  Nom actuel : " + nom)
        sys.exit(2)


def trouver_script_dir():
    return Path(__file__).resolve().parent


def executer_evaluateur(nom, script, dossier, resultats, scores, compteurs):
    """Executer un evaluateur, capturer son score et ses compteurs."""
    print(BLUE + "--- Etape : " + nom + " ---" + NC)

    if not script.is_file():
        print(RED + "[ERREUR] Script introuvable : " + str(script) + NC)
        resultats.append("## " + nom + "\n\nERREUR : script introuvable\n")
        return

    try:
        proc = subprocess.run(
            ["bash", str(script), str(dossier)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=300,
        )
        resultat = proc.stdout + proc.stderr
    except subprocess.TimeoutExpired:
        print(RED + "[ERREUR] Timeout sur " + nom + NC)
        resultats.append("## " + nom + "\n\nERREUR : timeout\n")
        return
    except OSError as e:
        print(RED + "[ERREUR] Echec d'execution de " + nom + " : " + str(e) + NC)
        resultats.append("## " + nom + "\n\nERREUR : " + str(e) + "\n")
        return

    # Extraire le score (ex: "Score coherence : 75/100")
    m = re.search(r"Score [a-z]+ : (\d+)", resultat)
    score = m.group(1) if m else None

    erreurs = resultat.count("| ERREUR |")
    avertissements = resultat.count("| AVERTISSEMENT |")

    resultats.append("## " + nom + "\n\nScore : " + (score or "?") + "/100\n\n" + resultat + "\n")
    if score is not None:
        scores[nom] = int(score)
    compteurs["erreurs"] += erreurs
    compteurs["avertissements"] += avertissements

    for ligne in resultat.splitlines():
        if ligne.startswith(("| ", "## ", "Score")):
            print(ligne)
    print("")


def main():
    verifier_nommage()

    import argparse

    parser = argparse.ArgumentParser(
        prog="combos-audit-general",
        description="Combo audit-general : chainage des 4 evaluateurs + synthese.",
    )
    parser.add_argument("dossier", nargs="?", default=".", help="Dossier a auditer (defaut: .)")
    parser.add_argument("--rapport", action="store_true", help="Sauvegarder le rapport dans themis/rapports/")
    parser.add_argument("--version", action="version", version="combos-audit-general " + VERSION + " (" + STATUT + ")")
    args = parser.parse_args()

    dossier = args.dossier
    print(BLUE + "=== combos-audit-general v" + VERSION + " ===" + NC)
    print("Cible : " + dossier)
    print("Date : " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("")

    if not Path(dossier).is_dir():
        print(RED + "[ERREUR] Le dossier n'existe pas : " + dossier + NC)
        return 1

    evaluer_dir = trouver_script_dir().parent.parent / "evaluer"
    resultats = []
    scores = {}
    compteurs = {"erreurs": 0, "avertissements": 0}

    for nom, rel in EVALUATEURS:
        executer_evaluateur(nom, evaluer_dir / rel, dossier, resultats, scores, compteurs)

    # Score global (moyenne des scores collectes)
    score_global = sum(scores.values()) // len(scores) if scores else 0

    # Severite
    if compteurs["erreurs"] > 0:
        severite = "CRITIQUE"
    elif compteurs["avertissements"] > 2:
        severite = "MAJEUR"
    elif compteurs["avertissements"] > 0:
        severite = "MINEUR"
    else:
        severite = "INFORMATION"

    # Synthese
    print(BLUE + "=== SYNTHESE ===" + NC)
    print("")
    print("Score global : " + str(score_global) + "/100")
    print("Severite : " + severite)
    print("Erreurs : " + str(compteurs["erreurs"]))
    print("Avertissements : " + str(compteurs["avertissements"]))
    print("")
    print("Tableau des scores :")
    print("| Evaluateur | Score |")
    print("|---|---|")
    for nom, score in scores.items():
        print("| " + nom + " | " + str(score) + "/100 |")

    # Rapport
    if args.rapport:
        rapport_dir = Path(dossier) / "cerveau-projet" / "agents" / "themis" / "rapports"
        date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
        rapport_file = rapport_dir / ("audit-general-" + date + ".md")
        rapport_dir.mkdir(parents=True, exist_ok=True)

        contenu = [
            "# Rapport d'evaluation -- " + date,
            "",
            "## Contexte",
            "- Active par : Cerberus",
            "- Combo utilise : audit-general",
            "- Cible : " + dossier,
            "",
            "## Score global : " + str(score_global) + "/100",
            "- Severite : " + severite,
            "- Erreurs : " + str(compteurs["erreurs"]),
            "- Avertissements : " + str(compteurs["avertissements"]),
            "",
        ]
        contenu.extend(resultats)

        try:
            rapport_file.write_text("\n".join(contenu) + "\n", encoding="utf-8")
            print("")
            print(GREEN + "Rapport sauvegarde : " + str(rapport_file) + NC)
        except OSError as e:
            print(RED + "[ERREUR] Impossible de sauvegarder le rapport : " + str(e) + NC)

    return 0


if __name__ == "__main__":
    sys.exit(main())
