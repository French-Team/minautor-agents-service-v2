#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
valider-todo.py

Verifie l'integrite d'un todo : phases (0 a 9), nommage,
placeholders, conformite ASCII.

Utilisation:
  valider-todo.py <fichier> [--verbose] [--help]

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

PHASES = [
    ("## Phase 0 -- Activation de l'agent", "Phase 0 -- Activation de l'agent", True),
    ("## Phase 1 -- Analyse de la demande", "Phase 1 -- Analyse de la demande", False),
    ("## Phase 2 -- Verification du cerveau", "Phase 2 -- Verification du cerveau", False),
    ("## Phase 3 -- Recherches", "Phase 3 -- Recherches", False),
    ("## Phase 4 -- Preparation des outils", "Phase 4 -- Preparation des outils", False),
    ("## Phase 5 -- Developpement", "Phase 5 -- Developpement", False),
    ("## Phase 6 -- Tests et validation", "Phase 6 -- Tests et validation", False),
    ("## Phase 7 -- Controle secondaire", "Phase 7 -- Controle secondaire", False),
    ("## Phase 8 -- Finalisation", "Phase 8 -- Finalisation", False),
    ("## Phase 9 -- Reactivation de Cerberus", "Phase 9 -- Reactivation de Cerberus", True),
]

PATTERN_NOMMAGE = re.compile(r"^todo-[a-z0-9-]+\.[0-9]+\.[0-9]+\.[a-z]+\.md$")
PATTERN_PLACEHOLDER = re.compile(r"\[[A-Za-z][A-Za-z ]+\]")


def afficher_aide():
    print("=== valider-todo v%s ===" % VERSION)
    print("")
    print("Usage: valider-todo.py <fichier>")
    print("")
    print("Arguments :")
    print("  <fichier>   Chemin du todo a valider")
    print("")
    print("Options :")
    print("  --verbose   Afficher les details de chaque verification")
    print("  --help      Afficher cette aide")
    print("")
    print("Verifications effectuees :")
    print("  1. Le fichier existe et n'est pas vide")
    print("  2. La Phase 0 (activation de l'agent) est presente -- OBLIGATOIRE")
    print("  3. Les 10 phases (0 a 9) sont presentes")
    print("  4. La Phase 9 (reactivation de Cerberus) est presente -- OBLIGATOIRE")
    print("  5. Le nommage du fichier est conforme (todo-[theme].[id].[class].[statut].md)")
    print("  6. Aucun placeholder non remplace ([...] restants)")
    print("  7. Conformite ASCII (pas d'accents, pas d'emojis)")


def verifier_phases(contenu, verbose):
    erreurs = 0
    for motif, libelle, obligatoire in PHASES:
        if motif in contenu:
            if verbose:
                print("  [OK] Phase : %s" % libelle)
        else:
            if obligatoire:
                print("  [ERREUR] Phase obligatoire manquante : %s" % libelle)
                erreurs += 1
            else:
                print("  [ATTENTION] Phase manquante : %s" % libelle)
    return erreurs


def verifier_nommage(fichier, verbose):
    nom = os.path.basename(fichier)
    if PATTERN_NOMMAGE.match(nom):
        if verbose:
            print("  [OK] Nommage conforme : %s" % nom)
        return 0
    print("  [ERREUR] Nommage non conforme : %s" % nom)
    print("  Attendu : todo-[theme].[id].[class].[statut].md")
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
        elif arg in ("--help", "-h"):
            afficher_aide()
            return 0
        elif arg == "--version":
            print("valider-todo v%s (%s)" % (VERSION, STATUT))
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

    print("=== Validation du todo ===")
    print("Fichier : %s" % fichier)
    print("")

    total_erreurs = 0

    if verbose:
        print("--- Phases ---")
    total_erreurs += verifier_phases(contenu, verbose)

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
        print("[OK] Le todo est valide")
        return 0
    print("[ERREUR] %d probleme(s) detecte(s)" % total_erreurs)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
