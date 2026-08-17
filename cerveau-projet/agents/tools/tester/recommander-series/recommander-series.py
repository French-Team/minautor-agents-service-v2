#!/usr/bin/env python3
# -*- coding: ascii -*-
# recommander-series.py
#
# Croise les TAGS des tests (bloc 'Tags:' des docstrings), les DUREES
# d execution (registre-tests.jsonl) et le rating (profils-rating.json) pour
# proposer une REORGANISATION des series de la non-regression (demande
# utilisateur 2026-08-16) : les tests lents ensembles, les rapides ensembles,
# groupes par categorie, pour equilibrer les series et reduire le temps total.
#
# Sortie : par categorie, liste des tests tries par duree decroissante +
# suggestion de decoupage en series (max tests / max duree par serie).
#
# Options :
#   --tous             Analyser tous les tests (defaut si aucun chemin)
#   --test <nom>       Analyser UN test (nom test-0XX)
#   --max-par-serie N  Nombre max de tests par serie suggeree (defaut 10)
#   --max-duree N      Duree max (secondes) par serie suggeree (defaut 60)
#   --rapport <fichier> Ecrire un rapport markdown
#   --verbose
#   --version
#
# Usage:
#   python3 recommander-series.py
#   python3 recommander-series.py --max-par-serie 6 --rapport rapport-series.md
#
# Version : 0.1.0
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
# =============================================================================
# REGLE IMMUABLE DE NOMMAGE : le nom commence par le prefixe du dossier de
# categorie (tester-).
# =============================================================================

import argparse
import glob
import io
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime

VERSION = "0.1.0"
STATUT = "ebauche"


def trouver_racine():
    d = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isfile(os.path.join(d, "AGENTS.md")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


RACINE = trouver_racine()
if RACINE is None:
    sys.stderr.write("ERREUR : racine du projet introuvable (AGENTS.md absent).\n")
    sys.exit(2)


def lire_tags_test(chemin):
    """Extrait le bloc 'Tags:' de la docstring d un test."""
    tags = []
    try:
        with io.open(chemin, encoding="utf-8", errors="replace") as fh:
            tete = fh.read(4096)
    except (IOError, OSError):
        return tags
    m = re.search(r"^Tags:\s*(.+)$", tete, re.M)
    if m:
        for t in m.group(1).split(","):
            t = t.strip().lower()
            if t and t not in tags:
                tags.append(t)
    return tags


def lire_durees(registre):
    """Lit registre-tests.jsonl : retourne {test: [durees]} (derniere duree
    de chaque run pris en compte, la plus recente par test)."""
    durees = {}
    if not os.path.isfile(registre):
        return durees
    try:
        with io.open(registre, encoding="utf-8") as fh:
            lignes = [l.strip() for l in fh if l.strip()]
    except (IOError, OSError):
        return durees
    # le registre est trie par date DECROISSANT : la premiere duree vue est
    # la plus recente pour chaque test
    vus = set()
    for l in lignes:
        try:
            e = json.loads(l)
        except ValueError:
            continue
        nom = e.get("test", "")
        if nom in vus:
            continue
        vus.add(nom)
        durees[nom] = e.get("duree", 0.0)
    return durees


def lister_tests(racine):
    pattern = os.path.join(racine, "cerveau-projet", "agents", "tools",
                           "tester", "tests", "test-0*", "test-0*.py")
    return sorted(glob.glob(pattern))


def analyser(racine, filtres=None, verbose=False):
    """Analyse les tests : tags + duree. Retourne (par_tag, lignes, total)."""
    registre = os.path.join(racine, "cerveau-projet", "agents", "traces",
                            "registre-tests.jsonl")
    durees = lire_durees(registre)
    tests = lister_tests(racine)
    if filtres:
        tests = [t for t in tests if any(f in os.path.basename(t) for f in filtres)]

    par_tag = defaultdict(list)   # tag -> [(duree, nom_test, tags)]
    lignes = []
    total_duree = 0.0
    for t in tests:
        nom = os.path.basename(t)
        tags = lire_tags_test(t)
        duree = durees.get(nom, 0.0)
        total_duree += duree
        lignes.append((duree, nom, tags))
        for tag in tags:
            par_tag[tag].append((duree, nom, tags))
    # tri par duree decroissante
    lignes.sort(reverse=True)
    for tag in par_tag:
        par_tag[tag].sort(reverse=True)
    return par_tag, lignes, total_duree, durees


def main():
    ap = argparse.ArgumentParser(description="Recommander une organisation des "
                                             "series par tags + durees")
    ap.add_argument("--test", nargs="*", default=None, help="Test(s) a analyser")
    ap.add_argument("--max-par-serie", type=int, default=10,
                    help="Nombre max de tests par serie suggeree")
    ap.add_argument("--max-duree", type=float, default=60.0,
                    help="Duree max (s) par serie suggeree")
    ap.add_argument("--rapport", metavar="FICHIER", default=None,
                    help="Ecrire un rapport markdown")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--version", action="version", version=VERSION)
    args = ap.parse_args()

    par_tag, lignes, total_duree, durees = analyser(RACINE, args.test, args.verbose)

    print("=== RECOMMANDER-SERIES v%s ===" % VERSION)
    if args.test:
        print("Tests analyses : %d" % len(lignes))
    else:
        print("Tests analyses : %d (total duree connue : %.1fs)" %
              (len(lignes), total_duree))
    print("Tags couverts : %d" % len(par_tag))
    print("")

    sections = []
    # 1. Par tag : liste des tests tries par duree decroissante
    for tag in sorted(par_tag):
        items = par_tag[tag]
        print("--- Tag: %s (%d tests) ---" % (tag, len(items)))
        somme = 0.0
        for duree, nom, _tags in items[:20]:
            ligne = "  %-45s %6.1fs" % (nom, duree)
            print(ligne)
            somme += duree
        sections.append("## Tag: %s (%d tests, %.1fs cumulees)\n\n"
                        "| Test | Duree (s) |\n|---|---|\n%s\n" %
                        (tag, len(items), somme,
                         "\n".join("| %s | %.1f |" % (nom, d) for d, nom, _ in items)))
        print("  (cumul: %.1fs)" % somme)
        print("")

    # 2. Suggestion de decoupage en series (equilibrage duree)
    print("=== SUGGESTION DE DECOUPAGE (max %d tests / %.0fs par serie) ===" %
          (args.max_par_serie, args.max_duree))
    suggestions = []
    serie = []
    duree_serie = 0.0
    num = 0
    for duree, nom, _tags in lignes:  # deja tries par duree decroissante
        if len(serie) >= args.max_par_serie or duree_serie + duree > args.max_duree:
            if serie:
                num += 1
                suggestions.append((num, list(serie), duree_serie))
            serie = []
            duree_serie = 0.0
        serie.append(nom)
        duree_serie += duree
    if serie:
        num += 1
        suggestions.append((num, serie, duree_serie))
    print("Series suggerees : %d" % len(suggestions))
    for num, noms, duree in suggestions:
        print("  Serie %d : %d tests, %.1fs -> %s" %
              (num, len(noms), duree, ", ".join(n.replace('.py','') for n in noms[:6])))
    sections.append("## Suggestion de decoupage (%d series)\n\n"
                    "| Serie | Tests | Duree (s) |\n|---|---|---|\n%s\n" %
                    (len(suggestions),
                     "\n".join("| %d | %d | %.1f |" % (n, len(ns), d) for n, ns, d in suggestions)))

    if args.rapport:
        with io.open(args.rapport, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# Recommandation de series\n\n")
            fh.write("**Version outil** : %s\n\n" % VERSION)
            fh.write("**Date** : %s\n\n" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            fh.write("\n\n".join(sections))
        print("")
        print("=== RAPPORT : %s ===" % args.rapport)
    return 0


if __name__ == "__main__":
    sys.exit(main())
