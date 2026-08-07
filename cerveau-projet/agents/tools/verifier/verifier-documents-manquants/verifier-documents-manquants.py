#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
verifier-documents-manquants.py

Verifie que chaque script .sh a sa documentation .md et inversement.
Ignore les faux positifs (spec/, test-*, index-*, *template*) sauf si
--inclure-speciaux est demande.

Utilisation:
  verifier-documents-manquants.py [OPTIONS] [DOSSIER]

Options :
  --sh-sans-md       Verifier les .sh sans .md correspondant (defaut: on)
  --md-sans-sh       Verifier les .md sans .sh correspondant (defaut: on)
  --inclure-speciaux Inclure les fichiers speciaux (spec/, test-*, index-*, *template*)
  --dry-run          Simuler sans rien modifier
  --verbose          Afficher les details
  --help             Afficher cette aide

Proprietaire : Vulcain (outil partage)
Version : 0.2.0-py
Statut : prepare
"""

import io
import os
import sys

VERSION = "0.2.0-py"
STATUT = "prepare"


def afficher_aide():
    print("=== verifier-documents-manquants v%s ===" % VERSION)
    print("")
    print("Usage: verifier-documents-manquants.py [OPTIONS] [DOSSIER]")
    print("")
    print("Options :")
    print("  --sh-sans-md       Verifier les .sh sans .md correspondant (defaut: on)")
    print("  --md-sans-sh       Verifier les .md sans .sh correspondant (defaut: on)")
    print("  --inclure-speciaux Inclure les fichiers speciaux (spec/, test-*, index-*, *template*)")
    print("  --dry-run          Simuler sans rien modifier")
    print("  --verbose          Afficher les details")
    print("  --help             Afficher cette aide")
    print("")
    print("Exemples :")
    print("  verifier-documents-manquants.py                                    # Dossier courant")
    print("  verifier-documents-manquants.py cerveau-projet/agents/tools/      # Les outils")
    print("  verifier-documents-manquants.py --sh-sans-md outils/              # .sh sans .md")
    print("  verifier-documents-manquants.py --inclure-speciaux outils/        # Tout inclure")


def est_faux_positif(fichier):
    """Un fichier de support (spec, test, index, template) n'a pas besoin de jumeau."""
    nom_base = os.path.basename(fichier)
    dossier_fichier = os.path.dirname(fichier)

    if "spec" in dossier_fichier.split(os.sep):
        return True
    if nom_base.startswith("test-") or nom_base.startswith("test_"):
        return True
    if nom_base.startswith("index-") or nom_base.startswith("index_"):
        return True
    if "template" in nom_base:
        return True
    return False


def lister_fichiers(dossier, ext):
    resultat = []
    for r, dossiers, fs in os.walk(dossier):
        for f in fs:
            if f.endswith(ext):
                resultat.append(os.path.join(r, f))
    return sorted(resultat)


def main(argv):
    dossier = "."
    check_sh = True
    check_md = True
    dry_run = False
    verbose = False
    help_demande = False
    inclure_speciaux = False

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--sh-sans-md":
            check_sh = True
            check_md = False
        elif arg == "--md-sans-sh":
            check_md = True
            check_sh = False
        elif arg == "--inclure-speciaux":
            inclure_speciaux = True
        elif arg == "--dry-run":
            dry_run = True
        elif arg == "--verbose":
            verbose = True
        elif arg in ("--help", "-h"):
            help_demande = True
        elif arg == "--version":
            print("verifier-documents-manquants v%s (%s)" % (VERSION, STATUT))
            return 0
        elif arg.startswith("-"):
            print("[ERREUR] Option inconnue : %s" % arg)
            afficher_aide()
            return 1
        else:
            dossier = arg
        i += 1

    if help_demande:
        afficher_aide()
        return 0

    if not os.path.isdir(dossier):
        print("[ERREUR] Le dossier n'existe pas : %s" % dossier)
        return 1

    print("=== Verification des documents manquants ===")
    print("Dossier : %s" % dossier)
    print("")

    total_sh = len(lister_fichiers(dossier, ".sh"))
    total_md = len(lister_fichiers(dossier, ".md"))
    total_manquants = 0

    if check_sh:
        print("--- Scripts .sh sans documentation .md ---")
        count = 0
        for sh_file in lister_fichiers(dossier, ".sh"):
            if not inclure_speciaux and est_faux_positif(sh_file):
                continue
            base = sh_file[:-3]
            md_file = base + ".md"
            if not os.path.isfile(md_file):
                count += 1
                print("  [MANQUANT] %s" % sh_file)
                if verbose:
                    print("        -> Documentation manquante : %s" % md_file)
        total_manquants += count
        print("  -> %d script(s) sans documentation" % count)
        print("")

    if check_md:
        print("--- Documentation .md sans script .sh ---")
        count = 0
        for md_file in lister_fichiers(dossier, ".md"):
            if not inclure_speciaux and est_faux_positif(md_file):
                continue
            base = md_file[:-3]
            sh_file = base + ".sh"
            if not os.path.isfile(sh_file):
                count += 1
                print("  [SANS-SCRIPT] %s" % md_file)
                if verbose:
                    print("        -> Script correspondant manquant : %s" % sh_file)
        total_manquants += count
        print("  -> %d documentation(s) sans script" % count)
        print("")

    print("=== Resume ===")
    print("Scripts .sh : %d" % total_sh)
    print("Documentations .md : %d" % total_md)
    print("Documents manquants : %d" % total_manquants)

    if total_manquants > 0:
        print("")
        print("[ATTENTION] Des documents manquants ont ete detectes")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
