#!/usr/bin/env python3
# -*- coding: ascii -*-
# detecter-evaluations-incompletes.py
#
# Scan ANTI-RECURRENCE apres correction d'une convention ou d'un pattern :
# trouve les mentions residuelles d'un MOTIF dans les 4 sources documentaires
# du cerveau-projet, pour garantir qu'une correction declaree est COMPLETE.
#
# Contexte (lecon Themis 2026-08-11) : un re-audit qui ne scanne que les
# fichiers modifies RATE les mentions residuelles dans les sources voisines
# (validateur, spec, generateurs .md/spec/code, tests). Cet outil croise les
# 4 sources avec une fenetre de contexte, comme Themis le fait a la main.
#
# Sources scannees :
#   1. VALIDATEUR  : cerveau-projet/agents/tools/valider/
#   2. SPEC        : cerveau-projet/agents/tools/*/spec/ + docs-dev-cerveau-projet/
#   3. GENERATEURS : cerveau-projet/agents/tools/generateurs/ (.py .sh .md)
#   4. TESTS       : cerveau-projet/agents/tools/tester/tests/ (.py)
#
# Chaque source peut recevoir un FILTRE (ex: --motif cT\\* --filtre 'convention')
# pour ne chercher le motif que dans les lignes contenant le filtre (methode
# Themis : fenetre de contexte).
#
# Usage:
#   python3 detecter-evaluations-incompletes.py --motif <motif>
#   python3 detecter-evaluations-incompletes.py --motif cT1 --filtre cT\\* --contexte 2
#   python3 detecter-evaluations-incompletes.py --motif <motif> --rapport rapport.md
#
# Options :
#   --motif <regex>    : motif a rechercher (obligatoire)
#   --filtre <regex>   : ne garder que les lignes contenant aussi ce filtre
#   --contexte <n>     : fenetre de lignes avant/apres (defaut 0)
#   --rapport <fichier>: ecrit le rapport markdown
#   --verbose          : detail des fichiers scans
#   --version
#
# Version : 0.1.0
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
# =============================================================================
# REGLE IMMUABLE DE NOMMAGE : le nom commence par le prefixe du dossier de
# categorie (detecter-).
# =============================================================================
import argparse
import io
import os
import re
import sys
from datetime import datetime

VERSION = "0.1.0"

# Les 4 sources documentaires, avec leurs extensions scannees.
SOURCES = [
    ("VALIDATEUR", "cerveau-projet/agents/tools/valider/", (".py", ".md")),
    ("SPEC", "cerveau-projet/agents/tools/", (".md",), "spec"),
    ("SPEC_DOCS", "cerveau-projet/docs-dev-cerveau-projet/", (".md",)),
    ("GENERATEURS", "cerveau-projet/agents/tools/generateurs/", (".py", ".sh", ".md")),
    ("TESTS", "cerveau-projet/agents/tools/tester/tests/", (".py",)),
]


def racine_projet():
    """Remonte jusqu'au dossier racine (contenant AGENTS.md)."""
    d = os.path.dirname(os.path.abspath(__file__))
    while not os.path.isfile(os.path.join(d, "AGENTS.md")):
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return d


def _marcher(racine, rel, extensions, sous_dossier=None):
    """Parcourt un dossier recursivement et retourne les fichiers d extension
    donnee. Si sous_dossier est fourni, ne garder que les chemins contenant
    ce sous-dossier (ex: 'spec')."""
    base = os.path.join(racine, rel)
    resultats = []
    if not os.path.isdir(base):
        return resultats
    for dossier, _, fichiers in os.walk(base):
        if "__pycache__" in dossier or ".git" in dossier:
            continue
        if sous_dossier and sous_dossier not in dossier:
            continue
        for nom in sorted(fichiers):
            if nom.endswith(extensions):
                resultats.append(os.path.join(dossier, nom))
    return resultats


def scanner(racine, motif, filtre, contexte, verbose=False):
    """Scan les 4 sources et retourne [(source, relpath, numero, ligne, extrait)]."""
    trouvailles = []
    try:
        rx = re.compile(motif)
    except re.error as e:
        print("Erreur : motif regex invalide (%s)" % e)
        sys.exit(2)
    rxF = re.compile(filtre) if filtre else None
    total_fic = 0
    for source, rel, ext, *suite in SOURCES:
        sous = suite[0] if suite else None
        fichiers = _marcher(racine, rel, ext, sous)
        total_fic += len(fichiers)
        for chemin in fichiers:
            try:
                with io.open(chemin, encoding="utf-8", errors="replace") as fh:
                    lignes = fh.readlines()
            except (IOError, OSError):
                continue
            for i, ligne in enumerate(lignes):
                if not rx.search(ligne):
                    continue
                if rxF and not rxF.search(ligne):
                    continue
                # Fenetre de contexte (contexte lignes avant, plus la ligne)
                debut = max(0, i - contexte)
                extrait = "".join(lignes[debut:i + 1]).strip()
                trouvailles.append((source, os.path.relpath(chemin, racine),
                                    i + 1, ligne.strip(), extrait))
                if verbose:
                    print("  [%s] %s:%d : %s" % (
                        source, os.path.relpath(chemin, racine), i + 1,
                        ligne.strip()[:90]))
    return trouvailles, total_fic


def afficher(trouvailles, total_fic, motif):
    if not trouvailles:
        print("SYNTHESE : 0 mention residuelle de '%s' (%d fichiers scannes)"
              % (motif, total_fic))
        return
    par_source = {}
    for t in trouvailles:
        par_source.setdefault(t[0], []).append(t)
    for source, liste in sorted(par_source.items()):
        print("== %s : %d ==" % (source, len(liste)))
        for _, chemin, num, ligne, _ in liste[:8]:
            print("  %s:%d : %s" % (chemin, num, ligne[:90]))
        if len(liste) > 8:
            print("  ... (%d autres)" % (len(liste) - 8))
    print("")
    print("SYNTHESE : %d mentions residuelles de '%s' (%d fichiers scannes)"
          % (len(trouvailles), motif, total_fic))


def ecrire_rapport(chemin, trouvailles, total_fic, motif):
    with io.open(chemin, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Rapport detecter-evaluations-incompletes\n\n")
        fh.write("**Date** : %s | **Motif** : `%s` | **Mentions** : %d "
                 "(%d fichiers scannes)\n\n" % (
                     datetime.now().strftime("%Y-%m-%d %H:%M"), motif,
                     len(trouvailles), total_fic))
        if not trouvailles:
            fh.write("Aucune mention residuelle. Correction COMPLETE.\n")
            return
        par_source = {}
        for t in trouvailles:
            par_source.setdefault(t[0], []).append(t)
        for source, liste in sorted(par_source.items()):
            fh.write("## %s (%d)\n\n" % (source, len(liste)))
            for _, chemin, num, ligne, extrait in liste:
                fh.write("- `%s:%d` : %s\n" % (chemin, num, ligne[:120]))
                if extrait and len(extrait) > len(ligne):
                    fh.write("  ```\n%s\n  ```\n" % extrait[:400])
            fh.write("\n")
    print("Rapport ecrit : %s" % os.path.abspath(chemin))


def main():
    parser = argparse.ArgumentParser(
        prog="detecter-evaluations-incompletes",
        description="Scan anti-recurrence : mentions residuelles d un motif "
                    "dans les 4 sources (validateur, spec, generateurs, tests)")
    parser.add_argument("--motif", default="", help="Motif regex a rechercher (obligatoire)")
    parser.add_argument("--filtre", default="", help="Ne garder que les lignes contenant aussi ce filtre")
    parser.add_argument("--contexte", type=int, default=0, help="Fenetre de lignes avant/apres (defaut 0)")
    parser.add_argument("--rapport", default="", help="Chemin du rapport markdown")
    parser.add_argument("--verbose", action="store_true", help="Detail des fichiers scannes")
    parser.add_argument("--version", action="version", version="detecter-evaluations-incompletes v%s" % VERSION)
    args = parser.parse_args()

    if not args.motif:
        parser.error("--motif est obligatoire")
    if args.contexte < 0:
        parser.error("--contexte doit etre >= 0")

    racine = racine_projet()
    trouvailles, total_fic = scanner(racine, args.motif, args.filtre,
                                     args.contexte, args.verbose)
    afficher(trouvailles, total_fic, args.motif)
    if args.rapport:
        ecrire_rapport(args.rapport, trouvailles, total_fic, args.motif)
    return 1 if trouvailles else 0


if __name__ == "__main__":
    sys.exit(main())
