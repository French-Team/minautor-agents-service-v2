#!/usr/bin/env python3
# combos-corriger-non-ascii.py
# Combo corriger-non-ascii : detecte et corrige les accents et emojis
# Ressource partagee : utilise par Themis, Buffy, ou tout autre agent
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION = "0.2.0-py"
STATUT = "beta"

import datetime
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


def verifier_nommage():
    """Regle immuable : le nom du fichier doit commencer par le prefixe du dossier de categorie."""
    nom = Path(__file__).name
    dossier = Path(__file__).resolve().parent.name
    if not nom.startswith(dossier):
        print(RED + "[ERREUR] Nommage invalide : le fichier doit commencer par '" + dossier + "'" + NC)
        print("  Nom actuel : " + nom)
        sys.exit(2)


def trouver_tools_dir():
    """Combos/combos-corriger-non-ascii/ -> tools/"""
    return Path(__file__).resolve().parent.parent.parent


def executer_bash(script, *args):
    """Executer un script bash avec des arguments et retourner sa sortie."""
    try:
        proc = subprocess.run(
            ["bash", str(script)] + list(args),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=300,
        )
        return proc.stdout + proc.stderr
    except subprocess.TimeoutExpired:
        return "[ERREUR] Timeout sur " + script.name + "\n"
    except OSError as e:
        return "[ERREUR] Echec d'execution de " + script.name + " : " + str(e) + "\n"


def compter_problemes(sortie):
    """Compter les lignes de detection au format: deux espaces + [motif]."""
    n = 0
    for ligne in sortie.splitlines():
        if re.match(r"^  \[[a-z]+\]", ligne):
            n += 1
    return n


def extraire_nombre(sortie, motif):
    """Extraire le premier nombre d'une ligne contenant le motif."""
    for ligne in sortie.splitlines():
        if motif in ligne:
            m = re.findall(r"\d+", ligne)
            if m:
                return m[0]
    return "0"


def main():
    verifier_nommage()

    import argparse

    parser = argparse.ArgumentParser(
        prog="combos-corriger-non-ascii",
        description="Combo : detecte et corrige les accents et emojis.",
    )
    parser.add_argument("dossier", nargs="?", default=".", help="Dossier cible (defaut: .)")
    parser.add_argument("--dry-run", action="store_true", help="Afficher les changements sans les appliquer")
    parser.add_argument("--all", action="store_true", help="Corriger TOUS les accents (texte francais et titres)")
    parser.add_argument("--rapport", action="store_true", help="Sauvegarder un rapport dans themis/rapports/")
    parser.add_argument("--version", action="version", version="combos-corriger-non-ascii " + VERSION + " (" + STATUT + ")")
    args = parser.parse_args()

    dossier = args.dossier.rstrip("/")
    if "cerveau-projet" in dossier:
        cible = dossier
    else:
        cible = os_join(dossier, "cerveau-projet")

    mode = "DRY-RUN" if args.dry_run else "APPLICATION"

    print(BLUE + "=== combos-corriger-non-ascii v" + VERSION + " ===" + NC)
    print("Cible : " + dossier)
    print("Mode : " + mode)
    print("Date : " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("")

    if not Path(dossier).is_dir():
        print(RED + "[ERREUR] Le dossier n'existe pas : " + dossier + NC)
        return 1

    tools_dir = trouver_tools_dir()
    rechercher = tools_dir / "rechercher" / "rechercher-accents-sensibles" / "rechercher-accents-sensibles.sh"
    corriger_emojis = tools_dir / "corriger" / "corriger-emojis" / "corriger-emojis.sh"
    corriger_accents = tools_dir / "corriger" / "corriger-accents-zones-sensibles" / "corriger-accents-zones-sensibles.sh"

    # Etape 1 : Detection
    print(BLUE + "--- Etape 1/4 : Detection des problemes ---" + NC)
    avant = compter_problemes(executer_bash(rechercher, dossier))
    print("Lignes detectees avant correction : " + str(avant))
    print("")

    # Etape 2 : Correction des emojis
    print(BLUE + "--- Etape 2/4 : Correction des emojis ---" + NC)
    if args.dry_run:
        sortie_emojis = executer_bash(corriger_emojis, "--dry-run", dossier)
    else:
        sortie_emojis = executer_bash(corriger_emojis, dossier)
    for ligne in sortie_emojis.splitlines()[-5:]:
        if ligne.strip():
            print(ligne)
    print("")

    # Etape 3 : Correction des accents (mode dossier recursif, un seul appel)
    print(BLUE + "--- Etape 3/4 : Correction des accents ---" + NC)
    accents_args = ["--recursive"]
    if args.all:
        accents_args.append("--all")
    if args.dry_run:
        accents_args.append("--dry-run")
    accents_args.append(cible)
    resultat_accents = executer_bash(corriger_accents, *accents_args)

    nb_accents = extraire_nombre(resultat_accents, "Fichiers analys")
    total_corr = extraire_nombre(resultat_accents, "Corrections appliqu")
    total_cons = extraire_nombre(resultat_accents, "Accents fran")
    print("Fichiers analyses : " + nb_accents)
    print("Corrections zones sensibles : " + total_corr)
    print("Accents francais conserves : " + total_cons)
    print("")

    # Etape 4 : Verification
    print(BLUE + "--- Etape 4/4 : Verification ---" + NC)
    apres = compter_problemes(executer_bash(rechercher, dossier))
    print("Lignes detectees apres correction : " + str(apres))

    if apres < avant:
        print(GREEN + "[OK] Reduction : " + str(avant) + " -> " + str(apres) + " (" + str(avant - apres) + " lignes corrigees)" + NC)
    elif avant == 0 and apres == 0:
        print(GREEN + "[OK] Aucun probleme detecte" + NC)
    else:
        print(YELLOW + "[ATTENTION] " + str(apres) + " lignes restantes : relancez avec --all (regle immuable : aucun accent tolere)" + NC)
        print(YELLOW + "Les seules exceptions admises : exemples/ et dictionnaires fonctionnels." + NC)

    # Rapport
    if args.rapport:
        rapport_dir = Path(cible) / "agents" / "themis" / "rapports"
        date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
        rapport_file = rapport_dir / ("corriger-non-ascii-" + date + ".md")
        rapport_dir.mkdir(parents=True, exist_ok=True)

        contenu = [
            "# Rapport corriger-non-ascii -- " + date,
            "",
            "## Contexte",
            "- Cible : " + dossier,
            "- Mode : " + mode,
            "",
            "## Resultats",
            "- Lignes avant : " + str(avant),
            "- Lignes apres : " + str(apres),
            "- Reduction : " + str(avant - apres) + " lignes",
            "- Fichiers accents corriges : " + nb_accents,
        ]
        try:
            rapport_file.write_text("\n".join(contenu) + "\n", encoding="utf-8")
            print("")
            print(GREEN + "Rapport sauvegarde : " + str(rapport_file) + NC)
        except OSError as e:
            print(RED + "[ERREUR] Impossible de sauvegarder le rapport : " + str(e) + NC)

    return 0


def os_join(a, b):
    """Joindre 2 chemins en gardant le separateur du systeme."""
    return str(Path(a) / b)


if __name__ == "__main__":
    sys.exit(main())
