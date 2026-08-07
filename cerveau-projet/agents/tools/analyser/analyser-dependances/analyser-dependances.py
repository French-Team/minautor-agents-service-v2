#!/usr/bin/env python3
# -*- coding: ascii -*-
# analyser-dependances.py
# Analyser les dependances entre fichiers
# Version : 0.2.0
# Statut : ebauche

# ============================================================
# OUTIL PYTHON - VERSION DE analyser-dependances.sh
# ============================================================
# Meme logique que la version bash, traduite en Python.
# 100% stdlib, ASCII strict, compatible Windows/Git Bash.
# ============================================================

import argparse
import os
import re
import sys
from pathlib import Path

VERSION = "0.2.0"
STATUT = "ebauche"

_COULEURS = {
    "rouge": "\033[0;31m",
    "vert": "\033[0;32m",
    "jaune": "\033[1;33m",
    "bleu": "\033[0;34m",
    "cyan": "\033[0;36m",
    "neutre": "\033[0m",
}


def _couleur(texte, nom="neutre"):
    """Retourne le texte colore si le terminal le supporte, sinon le texte brut."""
    if not sys.stdout.isatty():
        return texte
    return _COULEURS.get(nom, "") + texte + _COULEURS["neutre"]


def verifier_nommage(script_path):
    """VERIFIE que le nom du fichier commence par le prefixe du dossier de categorie."""
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
    print("==========================================")
    print("  analyser-dependances v%s" % VERSION)
    print("  Analyser les dependances entre fichiers")
    print("==========================================")
    print("")
    parser.print_help()


def construire_parser():
    """Construit le parseur d'arguments."""
    parser = argparse.ArgumentParser(
        prog="analyser-dependances",
        description="Analyser les dependances entre fichiers",
        epilog="Version %s (Statut : %s)" % (VERSION, STATUT),
    )
    parser.add_argument("fichier", nargs="?", type=str, help="Fichier a analyser")
    parser.add_argument("--verbose", "-v", action="store_true", help="Afficher les details")
    parser.add_argument("--inverse", "-i", action="store_true", help="Afficher les fichiers qui dependent de celui-ci")
    parser.add_argument("--version", action="version", version="analyser-dependances v%s" % VERSION)
    return parser


def analyser_dependances(fichier, verbose, inverse):
    """Analyse les dependances du fichier (ou les dependants en mode inverse)."""
    print(_couleur("[ANALYSE] Dependances de : %s" % os.path.basename(fichier), "bleu"))
    print("")

    if not Path(fichier).is_file():
        print(_couleur("Erreur: Le fichier '%s' n'existe pas" % fichier, "rouge"))
        return 1

    dossier_fichier = os.path.dirname(fichier)

    if inverse:
        # Mode inverse : trouver les fichiers qui dependent de celui-ci
        print(_couleur("----------------------------------------", "cyan"))
        print(_couleur("[DEPENDANTS] Fichiers qui dependent de %s" % os.path.basename(fichier), "vert"))
        print(_couleur("----------------------------------------", "cyan"))

        dependants = 0
        nom_base = os.path.basename(fichier)
        for racine, dossiers, fichiers in os.walk("."):
            for nom in fichiers:
                if not nom.endswith(".md"):
                    continue
                autrefichier = os.path.join(racine, nom)
                if os.path.abspath(autrefichier) == os.path.abspath(fichier):
                    continue
                try:
                    with open(autrefichier, "r", encoding="utf-8", errors="replace") as f:
                        if nom_base in f.read():
                            print("  [FICHIER] %s" % autrefichier)
                            dependants += 1
                except OSError:
                    continue

        print("")
        print(_couleur("Termine.", "bleu"))
        return 0

    # Mode normal : analyser les dependances de ce fichier
    print(_couleur("----------------------------------------", "cyan"))
    print(_couleur("[DEPENDANCES] Dependances de %s" % os.path.basename(fichier), "vert"))
    print(_couleur("----------------------------------------", "cyan"))

    # 1. Liens Markdown
    print(_couleur("1. Liens Markdown", "bleu"))
    try:
        with open(fichier, "r", encoding="utf-8", errors="replace") as f:
            contenu = f.read()
    except OSError:
        print(_couleur("Erreur: Impossible de lire le fichier '%s'" % fichier, "rouge"))
        return 1

    liens = re.findall(r"\[([^\]]*)\]\(([^)]*)\)", contenu)

    if liens:
        nb_valides = 0
        nb_invalides = 0
        for texte, chemin in liens:
            # Verifier si c'est un lien interne
            if not re.match(r"^https?://", chemin):
                chemin_complet = os.path.normpath(os.path.join(dossier_fichier, chemin))
                if os.path.isfile(chemin_complet) or os.path.isdir(chemin_complet):
                    nb_valides += 1
                    if verbose:
                        print(_couleur("  [OK] %s -> %s" % (texte, chemin), "vert"))
                else:
                    nb_invalides += 1
                    print(_couleur("  [ERREUR] %s -> %s" % (texte, chemin), "rouge"))

        print(_couleur("  Valides : %d" % nb_valides, "vert"))
        print(_couleur("  Invalides : %d" % nb_invalides, "rouge"))
    else:
        print(_couleur("  Aucun lien Markdown trouve", "jaune"))
    print("")

    # 2. Imports/Inclusions (pour les fichiers de code)
    print(_couleur("2. Imports/Inclusions", "bleu"))
    extension = os.path.splitext(fichier)[1].lstrip(".")

    if extension in ("sh", "bash"):
        sources = sum(1 for ligne in contenu.split("\n")
                      if re.match(r"^\s*(source\s+|\.\s+)", ligne))
        print("  [SOURCES] Sources Bash : %d" % sources)
    elif extension == "py":
        imports = sum(1 for ligne in contenu.split("\n")
                      if re.match(r"^\s*(import\s+|from\s+)", ligne))
        print("  [IMPORTS] Imports Python : %d" % imports)
    elif extension in ("js", "ts"):
        imports = sum(1 for ligne in contenu.split("\n")
                      if re.match(r"^\s*(import\s+|require\s*\()", ligne))
        print("  [IMPORTS] Imports JavaScript : %d" % imports)
    else:
        print(_couleur("  Type de fichier non analyse pour les imports", "jaune"))
    print("")

    # 3. Fichiers references
    print(_couleur("3. Fichiers references", "bleu"))
    refs = re.findall(r"[a-zA-Z0-9_./-]+\.(md|sh|py|js|ts|json)", contenu)
    nb_refs = len(sorted(set(refs)))
    print("  [REFERENCES] %d fichier(s) reference(s)" % nb_refs)
    print("")

    print(_couleur("Termine.", "bleu"))
    return 0


def main():
    """Point d'entree principal de l'outil."""
    verifier_nommage(sys.argv[0])

    parser = construire_parser()
    args = parser.parse_args()

    if not args.fichier:
        print("Erreur: Aucun fichier specifie")
        print("Utilisez --aide pour l'aide")
        return 1

    return analyser_dependances(args.fichier, args.verbose, args.inverse)


if __name__ == "__main__":
    sys.exit(main())
