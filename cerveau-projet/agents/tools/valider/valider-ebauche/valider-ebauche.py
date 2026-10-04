#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
valider-ebauche.py

Verifie si un fichier ebauche respecte les exigences minimales :
statut ebauche, nommage, sections minimales, contenu minimal,
et qu'il n'est pas trop complet pour un ebauche.

Utilisation:
  valider-ebauche.py <fichier> [--verbose] [--aide]

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

VERBOSE = False


def afficher_aide():
    print("Usage: valider-ebauche.py <fichier> [options]")
    print("")
    print("Verifie si un fichier ebauche respecte les exigences minimales.")
    print("")
    print("Options:")
    print("  --verbose     Afficher les details")
    print("  --aide        Afficher cette aide")
    print("")
    print("Exemples:")
    print("  valider-ebauche.py protocole-xxx.001.01.ebauche.md")
    print("  valider-ebauche.py --verbose protocole-xxx.001.01.ebauche.md")


def verifier_statut(fichier):
    basename = os.path.basename(fichier)
    if basename.endswith(".ebauche.md"):
        return 0
    print("[ERREUR] Le fichier n'est pas un ebauche : %s" % basename)
    return 1


def verifier_nommage(fichier):
    basename = os.path.basename(fichier)
    pattern = r"^([a-zA-Z0-9_-]+-)?[a-zA-Z0-9_-]+\.[0-9]{3}\.[0-9]{2}\.ebauche\.md$"
    if re.match(pattern, basename):
        return 0
    print("[ATTENTION]  Le nom ne respecte pas la convention : %s" % basename)
    print("  Format attendu: [type]-[theme].[id].[class].ebauche.md")
    return 1


def verifier_sections(fichier):
    erreurs = 0
    try:
        with io.open(fichier, encoding="utf-8") as fh:
            contenu = fh.read()
    except Exception:
        print("[ERREUR] Impossible de lire le fichier")
        return 1

    if not re.search(r"^#", contenu, re.MULTILINE):
        print("[ERREUR] Pas de titre principal (h1)")
        erreurs += 1

    return erreurs


def verifier_contenu(fichier):
    erreurs = 0
    try:
        with io.open(fichier, encoding="utf-8") as fh:
            lignes = fh.read().split("\n")
    except Exception:
        print("[ERREUR] Impossible de lire le fichier")
        return 1

    nb_lignes = len([l for l in lignes if l.strip() != ""])
    if nb_lignes < 5:
        print("[ERREUR] Trop peu de contenu : %d lignes (minimum 5)" % nb_lignes)
        erreurs += 1

    return erreurs


def verifier_pas_trop_complet(fichier):
    warnings = 0
    try:
        with io.open(fichier, encoding="utf-8") as fh:
            lignes = fh.read().split("\n")
    except Exception:
        return 0

    if lignes and lignes[0].strip() == "---":
        print("[ATTENTION]  Frontmatter present (inutile pour un ebauche)")
        warnings += 1

    if any(l.strip().startswith("|") for l in lignes):
        print("[ATTENTION]  Tableaux presents (peut-etre trop structure pour un ebauche)")
        warnings += 1

    nb_sections = sum(1 for l in lignes if l.startswith("## "))
    if nb_sections > 3:
        print("[ATTENTION]  %d sections (peut-etre trop structure pour un ebauche)" % nb_sections)
        warnings += 1

    return warnings


def valider_ebauche(fichier):
    global VERBOSE
    erreurs_totales = 0
    avertissements = 0

    print("=== Validation du fichier ebauche ===")
    print("Fichier : %s" % fichier)
    print("")

    if not os.path.isfile(fichier):
        print("[ERREUR] Fichier non trouve : %s" % fichier)
        return 1

    if verifier_statut(fichier) != 0:
        return 1

    print("--- Verification du nommage ---")
    if verifier_nommage(fichier) != 0:
        avertissements += 1

    print("")
    print("--- Verification de la structure minimale ---")
    erreurs_totales += verifier_sections(fichier)

    print("")
    print("--- Verification du contenu minimal ---")
    erreurs_totales += verifier_contenu(fichier)

    print("")
    print("--- Verification : pas trop complet pour un ebauche ---")
    avertissements += verifier_pas_trop_complet(fichier)

    print("")
    print("=== Resume ===")
    print("Erreurs : %d" % erreurs_totales)
    print("Avertissements : %d" % avertissements)

    if erreurs_totales == 0:
        print("")
        print("[OK] Le fichier ebauche respecte les exigences minimales")
        if avertissements > 0:
            print("[ATTENTION]  Cependant, il semble trop structure pour un ebauche")
            print("[ATTENTION]    Considerez passer au statut 'prepare'")
        return 0
    else:
        print("")
        print("[ERREUR] Le fichier ebauche ne respecte pas les exigences minimales")
        return 1


def main(argv):
    global VERBOSE
    fichier = ""

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in ("--aide", "--help", "-h"):
            afficher_aide()
            return 0
        if arg == "--version":
            print("valider-ebauche v%s (%s)" % (VERSION, STATUT))
            return 0
        if arg == "--verbose":
            VERBOSE = True
        elif arg.startswith("-"):
            print("[ERREUR] Option inconnue : %s" % arg)
            afficher_aide()
            return 1
        else:
            fichier = arg
        i += 1

    if not fichier:
        print("[ERREUR] Aucun fichier specifie")
        afficher_aide()
        return 1

    return valider_ebauche(fichier)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
