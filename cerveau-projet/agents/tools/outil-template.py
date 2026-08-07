#!/usr/bin/env python3
# -*- coding: ascii -*-
# [nom-outil].py
# [Description courte de ce que fait l'outil]
# Version : 0.1.0-beta
# Statut : ebauche

# ============================================================
# OUTIL-TEMPLATE PYTHON - MODELE DE SCRIPT
# ============================================================
# Instructions d'utilisation de ce template :
#   1. Copier ce fichier vers agents/tools/[categorie]/[nom-outil]/[nom-outil].py
#      (categorie = dossier d'ACTION : ajouter, analyser, corriger, lister, ...)
#   2. Remplacer [nom-outil] par le nom reel de l'outil
#   3. Remplacer [Description courte] par la vraie description
#   4. Completer les fonctions selon le besoin
#   5. Remplir le modele de documentation [nom-outil].md (outil-template-python.md)
#   6. Ajouter l'outil dans index-tools.md
#   7. Assigner l'outil a l'agent concerne (protocole-outils Regle 6)
#   8. Tester en --dry-run avant toute utilisation
#   9. Valider la conformite ASCII avec valider-conformite-ascii
# ============================================================
# REGLE IMMUABLE DE NOMMAGE :
#   Le nom de l'outil DOIT commencer par le prefixe du dossier de categorie.
#   Exemples : dossier 'rechercher/' -> outil 'rechercher-xxx'
#             dossier 'lire/'       -> outil 'lire-xxx'
#   La fonction verifier_nommage ci-dessous controle cela au demarrage.
#   (Ne pas supprimer ce bloc lors de la creation de l'outil)
# ============================================================
# REGLE IMMUABLE : 100% stdlib Python
#   Aucune dependance externe (pip install) n'est autorisee.
#   Utiliser uniquement la bibliotheque standard : sys, os, pathlib,
#   argparse, re, io, json, subprocess, ...
# ============================================================
# REGLE IMMUABLE : ASCII strict
#   Aucun accent, emoji ou caractere Unicode dans le code ni les
#   commentaires. Utiliser uniquement des caracteres ASCII (0-127).
# ============================================================

import argparse
import os
import sys
from pathlib import Path

VERSION = "0.1.0-beta"
STATUT = "ebauche"

# Couleurs ANSI (optionnel, activees uniquement si le terminal les supporte)
_COULEURS = {
    "rouge": "\033[0;31m",
    "vert": "\033[0;32m",
    "jaune": "\033[1;33m",
    "bleu": "\033[0;34m",
    "neutre": "\033[0m",
}


def _couleur(texte, nom="neutre"):
    """Retourne le texte colore si le terminal le supporte, sinon le texte brut."""
    if not sys.stdout.isatty():
        return texte
    return _COULEURS.get(nom, "") + texte + _COULEURS["neutre"]


def verifier_nommage(script_path):
    """VERIFIE que le nom du fichier commence par le prefixe du dossier de categorie.

    Exemple : agents/tools/rechercher/rechercher-texte/rechercher-texte.py
    -> dossier parent = 'rechercher-texte', prefixe attendu = 'rechercher-'

    Exception : le template lui-meme (outil-template) vit a la racine de tools/
    et n'a pas de prefixe de categorie -- la verification est sautee.
    """
    chemin = Path(script_path)
    nom_fichier = chemin.stem
    if nom_fichier == "outil-template":
        return
    dossier = chemin.parent.name
    prefixe = dossier.split("-")[0] + "-"
    if not nom_fichier.startswith(prefixe):
        print(
            _couleur(
                "ERREUR: Le nom '%s' ne commence pas par le prefixe du dossier '%s'"
                % (nom_fichier, prefixe),
                "rouge",
            ),
            file=sys.stderr,
        )
        sys.exit(1)


def afficher_aide(parser):
    """Affiche l'aide de l'outil."""
    print("=== [nom-outil] v%s ===" % VERSION)
    print("")
    parser.print_help()


def construire_parser():
    """Construit le parseur d'arguments avec les options standard de l'outil."""
    parser = argparse.ArgumentParser(
        prog="[nom-outil]",
        description="[Description courte de ce que fait l'outil]",
        epilog="Version %s (Statut : %s)" % (VERSION, STATUT),
    )
    parser.add_argument("--dry-run", action="store_true", help="Simuler sans rien modifier")
    parser.add_argument("--verbose", action="store_true", help="Afficher les details")
    parser.add_argument("--version", action="version", version="[nom-outil] v%s" % VERSION)
    # --- Options specifiques de l'outil : ajouter ici ---
    # parser.add_argument("--option", type=str, help="Description de l'option")
    # --- Arguments positionnels de l'outil : ajouter ici ---
    # parser.add_argument("cible", type=str, help="Description de l'argument")
    return parser


def main():
    """Point d'entree principal de l'outil."""
    # Verifier la regle immuable de nommage
    verifier_nommage(sys.argv[0])

    parser = construire_parser()
    args = parser.parse_args()

    # --- LOGIQUE DE L'OUTIL : implementer ici ---
    # if args.dry_run:
    #     print("[DRY-RUN] Aucune modification reelle")
    #     return 0
    #
    # resultat = faire_quelque_chose(args)
    # if resultat:
    #     print(_couleur("OK", "vert"))
    #     return 0
    # else:
    #     print(_couleur("ERREUR", "rouge"), file=sys.stderr)
    #     return 1

    # Placeholder : afficher l'aide si rien n'est implemente
    afficher_aide(parser)
    return 0


if __name__ == "__main__":
    sys.exit(main())
