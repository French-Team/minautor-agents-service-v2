#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
valider-spec.py

Verifie l'integrite d'une spec : structure, header, sections,
nommage, placeholders, conformite ASCII.

Utilisation:
  valider-spec.py <fichier> [--verbose] [--help]

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

CHAMPS_HEADER = ["Statut", "ID", "Class", "Cree", "Theme", "Pense-bete source"]

SECTIONS = [
    "## 1. Objectif",
    "## 2. Contexte",
    "## 3. Exigences Fonctionnelles",
    "## 4. Exigences Non-Fonctionnelles",
    "## 5. Architecture / Structure Technique",
    "## 6. Contraintes et Risques",
    "## 7. Livrables attendus",
    "## 8. Plan de validation",
    "## 9. Liens et References",
    "## 10. RVAV de la spec",
]

PATTERN_NOMMAGE = re.compile(r"^spec-[a-z0-9-]+\.[0-9]+\.[0-9]+\.[a-z]+\.md$")
PATTERN_PLACEHOLDER = re.compile(r"\[[A-Za-z][A-Za-z ]+\]")


def afficher_aide():
    print("=== valider-spec v%s ===" % VERSION)
    print("")
    print("Usage: valider-spec.py <fichier>")
    print("")
    print("Arguments :")
    print("  <fichier>   Chemin de la spec a valider")
    print("")
    print("Options :")
    print("  --verbose   Afficher les details de chaque verification")
    print("  --help      Afficher cette aide")
    print("")
    print("Verifications effectuees :")
    print("  1. Le fichier existe et n'est pas vide")
    print("  2. Le header est present (Statut, ID, Class, Cree, Theme, Pense-bete source)")
    print("  3. Les 10 sections sont presentes (1. Objectif ... 10. RVAV)")
    print("  4. Le nommage du fichier est conforme (spec-[theme].[id].[class].[statut].md)")
    print("  5. Aucun placeholder non remplace ([...] restants)")
    print("  6. Conformite ASCII (pas d'accents, pas d'emojis)")


def verifier_header(contenu, verbose):
    erreurs = 0
    for champ in CHAMPS_HEADER:
        if ("**%s :" % champ) in contenu:
            if verbose:
                print("  [OK] Header : %s" % champ)
        else:
            print("  [ERREUR] Header manquant : %s" % champ)
            erreurs += 1
    return erreurs


def verifier_sections(contenu, verbose):
    erreurs = 0
    for section in SECTIONS:
        if section in contenu:
            if verbose:
                print("  [OK] Section : %s" % section)
        else:
            print("  [ERREUR] Section manquante : %s" % section)
            erreurs += 1
    return erreurs


def verifier_nommage(fichier, verbose):
    nom = os.path.basename(fichier)
    if PATTERN_NOMMAGE.match(nom):
        if verbose:
            print("  [OK] Nommage conforme : %s" % nom)
        return 0
    print("  [ERREUR] Nommage non conforme : %s" % nom)
    print("  Attendu : spec-[theme].[id].[class].[statut].md")
    return 1


def verifier_placeholders(contenu, verbose):
    lignes = contenu.split("\n")
    trouves = []
    for i, l in enumerate(lignes, 1):
        if PATTERN_PLACEHOLDER.search(l):
            trouves.append((i, l.strip()))
            if len(trouves) >= 10:
                break
    if trouves:
        print("  [ATTENTION] Placeholders non remplis :")
        for i, l in trouves[:5]:
            print("    %d: %s" % (i, l))
        return 1
    if verbose:
        print("  [OK] Aucun placeholder restant")
    return 0


def verifier_ascii(contenu, verbose):
    mauvaises = [(i, l) for i, l in enumerate(contenu.split("\n"), 1)
                 if any(ord(ch) > 127 for ch in l)]
    if mauvaises:
        print("  [ERREUR] Caracteres non-ASCII detectes :")
        for i, l in mauvaises[:5]:
            print("    %d: %s" % (i, l.rstrip()))
        return 1
    if verbose:
        print("  [OK] Conformite ASCII")
    return 0


def main(argv):
    fichier = ""
    verbose = False

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--verbose":
            verbose = True
        elif arg in ("--aide", "--help", "-h"):
            afficher_aide()
            return 0
        elif arg == "--version":
            print("valider-spec v%s (%s)" % (VERSION, STATUT))
            return 0
        elif arg.startswith("-"):
            print("[ERREUR] Option inconnue : %s" % arg)
            afficher_aide()
            return 1
        else:
            fichier = arg
        i += 1

    if not fichier:
        print("[ERREUR] Le fichier est obligatoire")
        afficher_aide()
        return 1

    if not os.path.isfile(fichier):
        print("[ERREUR] Fichier non trouve : %s" % fichier)
        return 1

    if os.path.getsize(fichier) == 0:
        print("[ERREUR] Fichier vide : %s" % fichier)
        return 1

    try:
        with io.open(fichier, encoding="utf-8") as fh:
            contenu = fh.read()
    except Exception:
        print("[ERREUR] Impossible de lire le fichier : %s" % fichier)
        return 1

    print("=== Validation de la spec ===")
    print("Fichier : %s" % fichier)
    print("")

    total_erreurs = 0

    if verbose:
        print("--- Header ---")
    total_erreurs += verifier_header(contenu, verbose)

    if verbose:
        print("--- Sections ---")
    total_erreurs += verifier_sections(contenu, verbose)

    if verbose:
        print("--- Nommage ---")
    total_erreurs += verifier_nommage(fichier, verbose)

    if verbose:
        print("--- Placeholders ---")
    verifier_placeholders(contenu, verbose)

    if verbose:
        print("--- ASCII ---")
    total_erreurs += verifier_ascii(contenu, verbose)

    print("")
    print("=== Resume ===")
    if total_erreurs == 0:
        print("[OK] La spec est valide")
        return 0
    print("[ERREUR] %d probleme(s) detecte(s)" % total_erreurs)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
