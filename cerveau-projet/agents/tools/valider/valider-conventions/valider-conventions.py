#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
valider-conventions.py

Verifie que les conventions sont respectees dans un fichier :
frontmatter YAML, titre principal, sections ##, espaces en fin de
ligne, longueur des lignes, liens Markdown.

Utilisation:
  valider-conventions.py [OPTIONS] FICHIER

Options:
  --aide, -h          Afficher l'aide
  --verbose, -v       Afficher les details
  --version           Afficher la version

Proprietaire : Vulcain (outil partage)
Version : 0.2.0-py
Statut : prepare
"""

import io
import os
import re
import sys

VERSION = "0.2.0-py"
STATUT = "prepare"


def afficher_aide():
    print("==========================================")
    print("  valider-conventions v%s" % VERSION)
    print("  Verifier les conventions dans un fichier")
    print("==========================================")
    print("")
    print("Usage: valider-conventions.py [OPTIONS] FICHIER")
    print("")
    print("Options:")
    print("  --aide, -h          Afficher cette aide")
    print("  --verbose, -v       Afficher les details")
    print("  --version           Afficher la version")
    print("")
    print("Conventions verifiees:")
    print("  - Frontmatter YAML present")
    print("  - Titre principal present")
    print("  - Sections avec ##")
    print("  - Pas d'espaces en fin de ligne")
    print("  - Fichier non vide")
    print("")
    print("Exemples:")
    print("  valider-conventions.py fichier.md")
    print("  valider-conventions.py --verbose autre-fichier.md")


def valider_conventions(fichier, verbose):
    erreurs = 0
    warnings = 0

    print("[CHECKLIST] Validation des conventions : %s" % os.path.basename(fichier))
    print("")

    if os.path.getsize(fichier) == 0:
        print("  [ERREUR] Fichier vide")
        return 1

    try:
        with io.open(fichier, encoding="utf-8") as fh:
            lignes = fh.read().split("\n")
    except Exception:
        print("  [ERREUR] Impossible de lire le fichier")
        return 1

    # 1. Frontmatter YAML
    print("1. Frontmatter YAML")
    if lignes and lignes[0].strip() == "---":
        print("  [OK] Frontmatter present")
    else:
        print("  [ATTENTION]  Frontmatter absent")
        warnings += 1

    # 2. Titre principal
    print("2. Titre principal")
    if any(l.startswith("# ") for l in lignes):
        print("  [OK] Titre principal present")
    else:
        print("  [ATTENTION]  Titre principal absent")
        warnings += 1

    # 3. Sections
    print("3. Sections")
    nb_sections = sum(1 for l in lignes if l.startswith("## "))
    if nb_sections > 0:
        print("  [OK] %d section(s) trouvee(s)" % nb_sections)
    else:
        print("  [ATTENTION]  Aucune section ## trouvee")
        warnings += 1

    # 4. Espaces en fin de ligne
    print("4. Espaces en fin de ligne")
    nb_espaces = sum(1 for l in lignes if l.rstrip("\r") != l.rstrip("\r").rstrip())
    if nb_espaces > 0:
        print("  [ATTENTION]  %d ligne(s) avec espaces en fin" % nb_espaces)
        warnings += 1
    else:
        print("  [OK] Pas d'espaces en fin de ligne")

    # 5. Longueur des lignes
    print("5. Longueur des lignes")
    nb_longues = sum(1 for l in lignes if len(l) > 120)
    if nb_longues > 0:
        print("  [ATTENTION]  %d ligne(s) > 120 caracteres" % nb_longues)
        warnings += 1
    else:
        print("  [OK] Toutes les lignes < 120 caracteres")

    # 6. Liens Markdown
    print("6. Liens Markdown")
    nb_liens = len(re.findall(r"\[[^\]]*\]\([^)]*\)", "\n".join(lignes)))
    if nb_liens > 0:
        print("  [OK] %d lien(s) Markdown trouve(s)" % nb_liens)
    else:
        print("  [ATTENTION]  Aucun lien Markdown trouve")

    # Resume
    print("")
    print("Resume :")
    print("  [OK] Conventions respectees : Oui")
    if warnings > 0:
        print("  [ATTENTION]  Avertissements : %d" % warnings)
    if erreurs > 0:
        print("  [ERREUR] Erreurs : %d" % erreurs)

    return erreurs


def main(argv):
    fichier = ""
    verbose = False

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in ("--aide", "-h"):
            afficher_aide()
            return 0
        if arg in ("--verbose", "-v"):
            verbose = True
        elif arg == "--version":
            print("valider-conventions v%s" % VERSION)
            return 0
        elif arg.startswith("-"):
            print("Option inconnue: %s" % arg)
            print("Utilisez --aide pour l'aide")
            return 1
        else:
            fichier = arg
        i += 1

    if not fichier:
        print("Erreur: Aucun fichier specifie")
        print("Utilisez --aide pour l'aide")
        return 1

    if not os.path.isfile(fichier):
        print("Erreur: Le fichier '%s' n'existe pas" % fichier)
        return 1

    return valider_conventions(fichier, verbose)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
