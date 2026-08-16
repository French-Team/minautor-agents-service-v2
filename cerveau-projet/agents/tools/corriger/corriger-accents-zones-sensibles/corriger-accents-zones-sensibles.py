#!/usr/bin/env python3
# -*- coding: ascii -*-
# corriger-accents-zones-sensibles.py
# Outil pour corriger les accents dans les zones sensibles
# Mode standard --all : purge totale (texte francais et titres inclus)
# Conforme a la regle regles-emojis-ascii.md
# Version : 0.2.3-py
# Statut : beta

# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
corriger-accents-zones-sensibles.py
corriger-accents-zones-sensibles

Usage:
  corriger-accents-zones-sensibles.py [OPTIONS]
"""

VERSION = "0.2.3-py"
STATUT = "beta"

import re
import sys
from pathlib import Path

# Couleurs ANSI (desactivees si la sortie n'est pas un terminal)
if sys.stdout.isatty():
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    NC = "\033[0m"
else:
    RED = GREEN = YELLOW = NC = ""


def verifier_nommage():
    """Regle immuable : le nom du fichier doit commencer par le prefixe du dossier de categorie."""
    nom = Path(__file__).name
    dossier = Path(__file__).resolve().parent.name
    if not nom.startswith(dossier):
        print(RED + "[ERREUR] Nommage invalide : le fichier doit commencer par '" + dossier + "'" + NC)
        print("  Nom actuel : " + nom)
        sys.exit(2)


def lire_dictionnaire(dict_file):
    """Lire le dictionnaire (lignes 'accent|remplacement', ignorer # et vides)."""
    replacements = []
    try:
        with Path(dict_file).open(encoding="utf-8") as df:
            for line in df:
                line = line.rstrip("\n").rstrip("\r")
                if not line or line.startswith("#"):
                    continue
                if "|" in line:
                    accent, repl = line.split("|", 1)
                    if accent:
                        replacements.append((accent, repl))
    except OSError:
        pass
    return replacements


def est_fichier_code(fichier):
    """Detecter si le fichier est un fichier de code (fichier entier = zone technique)."""
    ext_code = (".sh", ".py", ".js", ".json", ".yaml", ".yml", ".txt")
    return str(fichier).lower().endswith(ext_code)


def corriger_fichier(fichier, replacements, dry_run, verbose, zones, all_mode):
    """Corriger les accents dans les zones sensibles d'un fichier. Retourne (changes, conserve)."""
    fichier_path = Path(fichier)
    est_code = est_fichier_code(fichier_path)

    try:
        with fichier_path.open(encoding="utf-8") as f:
            lines = f.readlines()
    except OSError:
        return 0, 0

    original = "".join(lines)
    zones_liste = zones.split(",")

    # Frontmatter end
    frontmatter_end = -1
    if "frontmatter" in zones_liste and lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                frontmatter_end = i
                break

    # Detecter les lignes dans les blocs de code
    dans_bloc = False
    lignes_blocs = set()
    if "blocs" in zones_liste:
        for i, line in enumerate(lines):
            if line.strip().startswith("```"):
                dans_bloc = not dans_bloc
                lignes_blocs.add(i)
            elif dans_bloc:
                lignes_blocs.add(i)

    def est_zone_technique(line, line_num):
        """Determiner si une ligne est dans une zone technique."""
        if all_mode:
            return True
        if "frontmatter" in zones_liste and 0 <= line_num <= frontmatter_end:
            return True
        if "blocs" in zones_liste and line_num in lignes_blocs:
            return True
        if "liens" in zones_liste and re.search(r"\[([^\]]*)\]\(([^)]*)\)", line):
            return True
        if "noms" in zones_liste and re.search(r"[/\\][a-zA-Z0-9_-]+\.[a-zA-Z]{1,4}", line):
            return True
        if "code" in zones_liste and est_code:
            return True
        return False

    total_changes = 0
    total_conserve = 0
    changes_par_zone = {z: 0 for z in zones_liste}

    for i, line in enumerate(lines):
        if est_zone_technique(line, i):
            new_line = line
            for accent, repl in replacements:
                count = new_line.count(accent)
                if count > 0:
                    new_line = new_line.replace(accent, repl)
                    total_changes += count
                    if 0 <= i <= frontmatter_end:
                        changes_par_zone["frontmatter"] = changes_par_zone.get("frontmatter", 0) + count
                    elif i in lignes_blocs:
                        changes_par_zone["blocs"] = changes_par_zone.get("blocs", 0) + count
                    elif re.search(r"\[([^\]]*)\]\(([^)]*)\)", line):
                        changes_par_zone["liens"] = changes_par_zone.get("liens", 0) + count
                    elif re.search(r"[/\\][a-zA-Z0-9_-]+\.[a-zA-Z]{1,4}", line):
                        changes_par_zone["noms"] = changes_par_zone.get("noms", 0) + count
                    else:
                        changes_par_zone["code"] = changes_par_zone.get("code", 0) + count
            if new_line != line:
                lines[i] = new_line
        else:
            for accent, _ in replacements:
                total_conserve += line.count(accent)

    content = "".join(lines)

    # Sauvegarder si necessaire
    if not dry_run and total_changes > 0:
        try:
            backup = str(fichier_path) + ".bak"
            Path(backup).write_text(original, encoding="utf-8", newline="")
            fichier_path.write_text(content, encoding="utf-8", newline="")
        except OSError:
            pass

    if verbose and total_changes > 0:
        for accent, repl in replacements:
            count_original = original.count(accent)
            count_final = content.count(accent)
            if count_original > 0:
                print("  '" + accent + "' -> '" + repl + "' : " + str(count_original) + " -> " + str(count_final))

    return total_changes, total_conserve


def main():
    verifier_nommage()

    import argparse

    parser = argparse.ArgumentParser(
        prog="corriger-accents-zones-sensibles",
        description="Corriger les accents dans les zones sensibles (frontmatter, blocs, code, liens, noms).",
    )
    parser.add_argument("cible", help="Fichier ou dossier a corriger")
    parser.add_argument("--dry-run", action="store_true", help="Afficher les changements sans les appliquer")
    parser.add_argument("--all", action="store_true",
                        help="(compat) Corriger TOUS les accents - desormais le MODE PAR DEFAUT (regle immuable : aucun caractere non-ASCII tolere)")
    parser.add_argument("--zones-seules", action="store_true",
                        help="Mode ponctuel : ne corriger QUE les zones sensibles (frontmatter, blocs, code, liens, noms) - les accents du corps du texte sont CONSERVES (usage exceptionnel uniquement)")
    parser.add_argument("--zones", default="frontmatter,noms,blocs,code,liens", help="Zones a corriger")
    parser.add_argument("--recursive", action="store_true", help="Traiter recursivement les sous-dossiers")
    parser.add_argument("--verbose", action="store_true", help="Afficher les details")
    parser.add_argument("--extensions", default="sh,py,js,json,yaml,yml,txt", help="Extensions des fichiers de code")
    parser.add_argument("--exclure", default="node_modules,.git,.agents,.backup,.tmp,test-,dictionnaire-,exemples",
                        help="Motifs de chemins a exclure")
    parser.add_argument("--dictionnaire", default=None, help="Chemin vers le dictionnaire")
    parser.add_argument("--version", action="version",
                        version="corriger-accents-zones-sensibles " + VERSION + " (" + STATUT + ")")
    parser.add_argument("--aide", action="help",
                  help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    if args.dictionnaire:
        dict_file = Path(args.dictionnaire)
    else:
        dict_file = Path(__file__).resolve().parent.parent / "corriger-dictionnaire-accents" / "corriger-dictionnaire-accents.txt"

    cible = Path(args.cible)
    if not cible.exists():
        print(RED + "[ERREUR] Cible non trouvee: " + args.cible + NC)
        return 1

    if not dict_file.is_file():
        print(RED + "[ERREUR] Dictionnaire non trouve: " + str(dict_file) + NC)
        return 1

    # MODE PAR DEFAUT = --all (purge totale, regle immuable) - l option
    # --zones-seules force l ancien comportement ponctuel (zones sensibles
    # uniquement). --all reste accepte (compat, explicite).
    all_mode = not args.zones_seules
    if all_mode:
        print("[INFO] Correction de TOUS les accents (mode par defaut --all)")
    else:
        print("[INFO] Correction intelligente des accents dans les zones sensibles (--zones-seules)")
    print("Cible: " + args.cible)
    print("Zones: " + args.zones)
    print("Dictionnaire: " + str(dict_file))
    print("")

    replacements = lire_dictionnaire(dict_file)
    exclusions = args.exclure.split(",")

    # Construire la liste des fichiers
    fichiers = []
    if cible.is_file():
        fichiers = [cible]
    elif cible.is_dir():
        if args.recursive:
            extensions = args.extensions.split(",")
            for p in cible.rglob("*"):
                if not p.is_file():
                    continue
                if p.suffix.lstrip(".") not in extensions and p.suffix != ".md":
                    continue
                chemin = str(p)
                if any(excl in chemin for excl in exclusions):
                    continue
                fichiers.append(p)
        else:
            for p in cible.iterdir():
                if p.is_file() and p.suffix in (".md", ".sh", ".py", ".js"):
                    fichiers.append(p)

    if not fichiers:
        print(YELLOW + "[AVERTISSEMENT] Aucun fichier trouve" + NC)
        return 0

    total_fichiers = 0
    total_corrections = 0
    total_conserve = 0

    for fichier in fichiers:
        if not fichier.is_file():
            continue
        chemin = str(fichier)
        if any(excl in chemin for excl in exclusions):
            continue
        # Exclusion speciale pour le dossier exemples
        if "exemples" in fichier.parts:
            continue

        total_fichiers += 1
        if args.verbose:
            print(GREEN + "[INFO] Traitement: " + chemin + NC)

        changes, conserve = corriger_fichier(fichier, replacements, args.dry_run, args.verbose, args.zones, all_mode)
        total_corrections += changes
        total_conserve += conserve

        if args.verbose and changes > 0:
            print(GREEN + "  [OK] " + str(changes) + " corrections, " + str(conserve) + " accents conserves" + NC)
        elif args.verbose:
            print(YELLOW + "  [OK] Aucune correction necessaire" + NC)

    print("")
    print("=== Resume ===")
    print("Fichiers analyses: " + str(total_fichiers))
    print("Corrections appliquees: " + str(total_corrections))
    print("Accents francais conserves: " + str(total_conserve))

    if args.dry_run:
        print(YELLOW + "[INFO] Dry-run : aucun fichier n'a ete modifie" + NC)
    elif total_corrections > 0:
        print(GREEN + "[OK] Corrections appliquees avec succes" + NC)
    else:
        print(GREEN + "[OK] Aucune correction necessaire" + NC)

    return 0


if __name__ == "__main__":
    sys.exit(main())
