#!/usr/bin/env python3
# -*- coding: ascii -*-
# corriger-nommage.py
# Corriger le nommage des fichiers selon les conventions
# Version : 0.3.1-py
# Statut : beta

# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
corriger-nommage.py
corriger-nommage

Usage:
  corriger-nommage.py [OPTIONS]
"""

VERSION = "0.3.1-py"
STATUT = "beta"

import re
import shutil
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


def renommer(fichier, nouveau_nom, dry_run):
    """Renommer le fichier si le nouveau nom differe, avec verification."""
    basename = fichier.name
    if basename == nouveau_nom:
        print("  " + GREEN + "[OK] Aucune correction necessaire" + NC)
        return 0

    print("  " + YELLOW + "[ATTENTION] Correction necessaire :" + NC)
    print("    Actuel : " + basename)
    print("    Nouveau : " + nouveau_nom)

    if dry_run:
        print("  " + YELLOW + "Mode dry-run : aucun fichier modifie" + NC)
        return 0

    chemin_complet = fichier.parent / nouveau_nom
    if chemin_complet.exists():
        print("  " + RED + "[ERREUR] Le fichier destination existe deja" + NC)
        return 1

    try:
        shutil.move(str(fichier), str(chemin_complet))
        print("  " + GREEN + "[OK] Fichier renomme" + NC)
        return 0
    except OSError as e:
        print("  " + RED + "[ERREUR] Echec du renommage : " + str(e) + NC)
        return 1


def detecter_type_chemin(fichier):
    """Detecte le type de fichier depuis son chemin quand --type est absent.
    Retourne None si aucun type n'est detectable avec certitude (le fichier
    n'est alors pas renomme : il sort du perimetre des 4 conventions)."""
    chemin = str(fichier).replace("\\", "/")
    basename = fichier.name

    # Outil : sous agents/tools/ ou outils-llm/ (les outils vivent dans ces dossiers)
    if "/agents/tools/" in chemin:
        return "outil"
    # Convention : dossier agents/conventions/ ou nom convention-*.md
    if "/agents/conventions/" in chemin or basename.startswith("convention-"):
        return "convention"
    # Protocole : chemin contenant un dossier protocole-* (regles-immuables)
    if "/protocole-" in chemin:
        return "protocole"
    # Agent : sous agents/<agent>/ (dossier direct d'un agent, hors outils/conventions)
    m = re.match(r"^.*/agents/([a-z0-9-]+)/.*$", chemin)
    if m and m.group(1) not in ("regles-immuables", "classeur-variables", "traces", "lecons", "habilitation", "corrections-db.md"):
        return "agent"
    return None


def extension_compatible(type_fichier, fichier):
    """Garde anti-renommage : ne corriger que les fichiers dont l extension
    correspond au type (protocole/agent/convention = .md ; outil = .sh/.py/.md).
    Les autres fichiers (ex: .json de parcours v2) sortent du perimetre : ils
    ne doivent JAMAIS etre renommes par corriger-nommage."""
    ext = fichier.suffix.lower()
    if type_fichier in ("protocole", "agent", "convention"):
        return ext == ".md"
    return ext in (".sh", ".py", ".md")


def corriger_protocole(fichier, dry_run):
    basename = fichier.name
    print(BLUE + "[OUTIL] Correction du nommage : " + basename + NC)
    print("")

    if fichier.suffix.lower() != ".md":
        print("  " + GREEN + "[OK] Aucune correction necessaire (fichier non .md)" + NC)
        return 0

    # Format : [nom].[major].[minor].[statut].md
    parties = basename.split(".")
    if len(parties) < 5:
        print("  " + GREEN + "[OK] Aucune correction necessaire (format hors protocole)" + NC)
        return 0

    nouveau_nom = ".".join(parties) if basename.endswith(".md") else basename + ".md"
    # Le format attendu est deja nom.majeur.mineur.statut.md
    return renommer(fichier, basename, dry_run)


def corriger_agent(fichier, dry_run):
    basename = fichier.name
    print(BLUE + "[OUTIL] Correction du nommage : " + basename + NC)
    print("")

    if fichier.suffix.lower() != ".md":
        print("  " + GREEN + "[OK] Aucune correction necessaire (fichier non .md)" + NC)
        return 0

    # Format : nom-agent.md (minuscules)
    if re.match(r"^[a-z]+\.md$", basename):
        print("  " + GREEN + "[OK] Aucune correction necessaire" + NC)
        return 0

    nom = basename[:-3]
    nouveau_nom = nom + ".md"
    return renommer(fichier, nouveau_nom, dry_run)


def corriger_outil(fichier, dry_run):
    basename = fichier.name
    print(BLUE + "[OUTIL] Correction du nommage : " + basename + NC)
    print("")

    # Format : nom-outil.sh ou nom-outil.md (minuscules + tirets)
    if re.match(r"^[a-z-]+\.(sh|md)$", basename):
        print("  " + GREEN + "[OK] Aucune correction necessaire" + NC)
        return 0

    stem = basename.rsplit(".", 1)[0]
    ext = basename.rsplit(".", 1)[1]
    nouveau_nom = stem + "." + ext
    return renommer(fichier, nouveau_nom, dry_run)


def corriger_convention(fichier, dry_run):
    basename = fichier.name
    print(BLUE + "[OUTIL] Correction du nommage : " + basename + NC)
    print("")

    if fichier.suffix.lower() != ".md":
        print("  " + GREEN + "[OK] Aucune correction necessaire (fichier non .md)" + NC)
        return 0

    # Format : convention-nom.md
    if re.match(r"^convention-[a-z-]+\.md$", basename):
        print("  " + GREEN + "[OK] Aucune correction necessaire" + NC)
        return 0

    nom = basename[:-3]
    nom = re.sub(r"^convention-", "", nom)
    nouveau_nom = "convention-" + nom + ".md"
    return renommer(fichier, nouveau_nom, dry_run)


def main():
    verifier_nommage()

    import argparse

    parser = argparse.ArgumentParser(
        prog="corriger-nommage",
        description="Corriger le nommage des fichiers selon les conventions.",
    )
    parser.add_argument("fichier", help="Chemin du fichier a corriger")
    parser.add_argument("--type", default=None, choices=["protocole", "agent", "outil", "convention"],
                        help="Type de fichier (protocole, agent, outil, convention). Absent -> auto-detection par le chemin.")
    parser.add_argument("--dry-run", action="store_true", help="Simuler sans modifier")
    parser.add_argument("--verbose", action="store_true", help="Afficher les details")
    parser.add_argument("--version", action="version", version="corriger-nommage " + VERSION + " (" + STATUT + ")")
    parser.add_argument("--aide", action="help",
                  help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    fichier = Path(args.fichier)
    if not fichier.is_file():
        print("Erreur: Le fichier '" + args.fichier + "' n'existe pas")
        return 1

    type_fichier = args.type
    if type_fichier is None:
        type_fichier = detecter_type_chemin(fichier)
        if type_fichier is None:
            print(BLUE + "[OUTIL] Correction du nommage : " + fichier.name + NC)
            print("")
            print("  " + GREEN + "[OK] Aucune correction necessaire (type non specifie et non detectable depuis le chemin)" + NC)
            return 0
        print(YELLOW + "[AUTO] Type detecte depuis le chemin : " + type_fichier + NC)

    if not extension_compatible(type_fichier, fichier):
        print(BLUE + "[OUTIL] Correction du nommage : " + fichier.name + NC)
        print("")
        print("  " + GREEN + "[OK] Aucune correction necessaire (extension hors perimetre du type " + type_fichier + ")" + NC)
        return 0

    if type_fichier == "protocole":
        return corriger_protocole(fichier, args.dry_run)
    elif type_fichier == "agent":
        return corriger_agent(fichier, args.dry_run)
    elif type_fichier == "outil":
        return corriger_outil(fichier, args.dry_run)
    elif type_fichier == "convention":
        return corriger_convention(fichier, args.dry_run)
    return 1


if __name__ == "__main__":
    sys.exit(main())
