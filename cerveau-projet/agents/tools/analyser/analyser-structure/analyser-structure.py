#!/usr/bin/env python3
# -*- coding: ascii -*-
# analyser-structure.py
# Analyser la structure du projet
# Version : 0.2.0
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true

# ============================================================
# OUTIL PYTHON - VERSION DE analyser-structure.sh
# ============================================================
# Meme logique que la version bash, traduite en Python.
# 100% stdlib, ASCII strict, compatible Windows/Git Bash.
# ============================================================

"""
analyser-structure.py
analyser-structure

Usage:
  analyser-structure.py [OPTIONS]
"""

import argparse
import os
import sys
from collections import Counter
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
    print("  analyser-structure v%s" % VERSION)
    print("  Analyser la structure du projet")
    print("==========================================")
    print("")
    parser.print_help()


def construire_parser():
    """Construit le parseur d'arguments."""
    parser = argparse.ArgumentParser(
        prog="analyser-structure",
        description="Analyser la structure du projet",
        epilog="Version %s (Statut : %s)" % (VERSION, STATUT),
    )
    parser.add_argument("chemin", nargs="?", type=str, default=".", help="Chemin a analyser (defaut: .)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Afficher les details")
    parser.add_argument("--profondeur", "-p", type=int, default=2, help="Profondeur d'analyse (defaut: 2)")
    parser.add_argument("--version", action="version", version="analyser-structure v%s" % VERSION)
    return parser


def analyser_structure(chemin, verbose, profondeur):
    """Analyse la structure du projet."""
    if not chemin:
        chemin = "."
    print(_couleur("[ANALYSE] Structure de : %s" % chemin, "bleu"))
    print("")

    if not os.path.exists(chemin):
        print(_couleur("Erreur: Le chemin '%s' n'existe pas" % chemin, "rouge"))
        return 1

    # 1. Statistiques generales
    print(_couleur("----------------------------------------", "cyan"))
    print(_couleur("[STATS] Statistiques generales", "vert"))
    print(_couleur("----------------------------------------", "cyan"))

    nb_dossiers = 0
    nb_fichiers = 0
    nb_md = 0
    nb_sh = 0
    nb_py = 0
    nb_js = 0
    extensions = Counter()

    for racine, dossiers, fichiers in os.walk(chemin):
        # Calculer la profondeur relative
        rel = os.path.relpath(racine, chemin)
        prof_rel = 0 if rel == "." else rel.count(os.sep) + 1
        if prof_rel > profondeur:
            # Ne pas descendre plus profond (prune)
            dossiers[:] = []
            continue

        nb_dossiers += len(dossiers)
        for nom in fichiers:
            nb_fichiers += 1
            ext = os.path.splitext(nom)[1].lstrip(".").lower()
            if ext:
                extensions[ext] += 1
            if nom.endswith(".md"):
                nb_md += 1
            elif nom.endswith(".sh"):
                nb_sh += 1
            elif nom.endswith(".py"):
                nb_py += 1
            elif nom.endswith(".js"):
                nb_js += 1

    print("  [DOSSIERS] %d" % nb_dossiers)
    print("  [FICHIERS] %d" % nb_fichiers)
    print("  [MD] %d" % nb_md)
    print("  [SH] %d" % nb_sh)
    print("  [PY] %d" % nb_py)
    print("  [JS] %d" % nb_js)
    print("")

    # 2. Taille totale
    print(_couleur("----------------------------------------", "cyan"))
    print(_couleur("[TAILLE]", "vert"))
    print(_couleur("----------------------------------------", "cyan"))

    taille_total = 0
    for racine, dossiers, fichiers in os.walk(chemin):
        for nom in fichiers:
            try:
                taille_total += os.path.getsize(os.path.join(racine, nom))
            except OSError:
                continue

    def taille_humaine(octets):
        for unite in ("o", "Ko", "Mo", "Go"):
            if octets < 1024:
                return "%.1f %s" % (octets, unite)
            octets /= 1024
        return "%.1f To" % octets

    print("  [TAILLE] Taille totale : %s" % taille_humaine(taille_total))
    print("")

    # 3. Extensions
    print(_couleur("----------------------------------------", "cyan"))
    print(_couleur("[EXTENSIONS]", "vert"))
    print(_couleur("----------------------------------------", "cyan"))

    for ext, count in extensions.most_common(10):
        print("  .%s : %d fichier(s)" % (ext, count))
    print("")

    # 4. Structure arborescente (limitee)
    print(_couleur("----------------------------------------", "cyan"))
    print(_couleur("[STRUCTURE]", "vert"))
    print(_couleur("----------------------------------------", "cyan"))

    dossiers_affiches = []
    for racine, dossiers, fichiers in os.walk(chemin):
        rel = os.path.relpath(racine, chemin)
        prof_rel = 0 if rel == "." else rel.count(os.sep) + 1
        if prof_rel > profondeur:
            dossiers[:] = []
            continue
        dossiers_affiches.append(racine)
        if verbose and len(dossiers_affiches) >= 30:
            break
        if not verbose and len(dossiers_affiches) >= 20:
            break

    for d in dossiers_affiches[:30]:
        print("  %s" % d)
    print("")

    # 5. Fichiers recents (7 jours)
    print(_couleur("----------------------------------------", "cyan"))
    print(_couleur("[RECENTS] Fichiers recents (7 jours)", "vert"))
    print(_couleur("----------------------------------------", "cyan"))

    import time

    limite = time.time() - 7 * 24 * 3600
    nb_recents = 0
    for racine, dossiers, fichiers in os.walk(chemin):
        for nom in fichiers:
            try:
                if os.path.getmtime(os.path.join(racine, nom)) >= limite:
                    nb_recents += 1
            except OSError:
                continue
    print("  [RECENTS] %d fichier(s) recent(s)" % nb_recents)
    print("")

    print(_couleur("Analyse terminee.", "bleu"))
    return 0


def main():
    """Point d'entree principal de l'outil."""
    verifier_nommage(sys.argv[0])

    parser = construire_parser()
    parser.add_argument("--aide", action="help",
                  help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    return analyser_structure(args.chemin, args.verbose, args.profondeur)


if __name__ == "__main__":
    sys.exit(main())
