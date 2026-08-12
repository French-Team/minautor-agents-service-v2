#!/usr/bin/env python3
# -*- coding: ascii -*-
# detecter-usage-scripts-temporaires.py
#
# Mesure l'usage des scripts temporaires (.zz-*.py / .tmp-*.py) par les agents :
# scripts presents a la racine, scripts qui ont existe (git log), scripts
# mentionnes dans les lecons/corrections et rapports. Puis croise avec le
# registre d'usage : un script detecte SANS declaration (mode
# script-temporaire dans le registre) est un contournement a signaler.
#
# Sources scannees :
#   1. Racine du projet : fichiers .zz-* / .tmp-* presents
#   2. Git : git log --all --diff-filter=A --name-only (scripts crees un jour)
#   3. Corrections/lecons : grep '\.zz-|\\.tmp-' dans cerveau-projet/agents/*/corrections.md
#   4. Rapports : grep dans cerveau-projet/agents/*/controles/ + rapports/
#   5. Registre : cerveau-projet/agents/traces/registre-usages-outils.jsonl (mode script-temporaire)
#
# Options :
#   --rapport <fichier> : ecrit le rapport markdown
#   --verbose           : detail par source
#   --version
#
# Usage:
#   python3 detecter-usage-scripts-temporaires.py
#   python3 detecter-usage-scripts-temporaires.py --rapport rapport-scripts-temp.md
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
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime

VERSION = "0.1.1"
STATUT = "ebauche"

_COULEURS = {
    "rouge": "\033[0;31m",
    "vert": "\033[0;32m",
    "jaune": "\033[0;33m",
    "bleu": "\033[0;34m",
    "neutre": "\033[0m",
}


def _couleur(texte, nom="neutre"):
    return "%s%s%s" % (_COULEURS.get(nom, _COULEURS["neutre"]), texte, _COULEURS["neutre"])


def racine_projet():
    d = os.path.dirname(os.path.abspath(__file__))
    while not os.path.isfile(os.path.join(d, "AGENTS.md")):
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return d


def registre_defaut(racine):
    return os.path.join(racine, "cerveau-projet", "agents", "traces", "registre-usages-outils.jsonl")


def registre_historique(racine):
    """Historique du registre (round 8 : les declarations archivees lors des
    non-regressions restent verifiables, sinon le detecteur devient aveugle
    au passe et signale de faux ecarts permanents)."""
    return os.path.join(racine, "cerveau-projet", "agents", "traces",
                        "registre-usages-outils.historique.jsonl")


def est_script_temporaire(nom):
    """Un script temporaire est un FICHIER .py/.sh dont le basename commence
    par .zz- ou .tmp- (round 8 : les dossiers de tests .tmp-*/ et les
    fichiers .md/.json n en sont pas)."""
    base = os.path.basename(nom)
    if not (base.startswith(".zz-") or base.startswith(".tmp-")):
        return False
    return base.endswith(".py") or base.endswith(".sh")


def scanner_racine(racine):
    """Scripts temporaires .zz-* / .tmp-* (.py/.sh) presents a la racine
    (niveau 1 seulement)."""
    trouves = []
    for nom in os.listdir(racine):
        if est_script_temporaire(nom):
            trouves.append(nom)
    return sorted(trouves)


def scanner_git(racine):
    """Scripts qui ont existe dans git (creations de fichiers). Filtre :
    uniquement les fichiers .py/.sh dont le basename est .zz-*/.tmp-*
    (round 8 : les dossiers de tests et les .md/.json ne sont pas des
    scripts)."""
    try:
        r = subprocess.run(
            ["git", "log", "--all", "--diff-filter=A", "--name-only", "--pretty=format:"],
            cwd=racine, capture_output=True, text=True, timeout=60)
        lignes = r.stdout.split("\n")
    except Exception:
        return []
    trouves = set()
    for l in lignes:
        nom = l.strip()
        if nom and est_script_temporaire(nom):
            trouves.add(os.path.basename(nom))
    return sorted(trouves)


def scanner_dossiers(racine, dossiers, pattern):
    """Grep le pattern dans une liste de dossiers (corrections, controles, rapports)."""
    trouves = []
    for dossier in dossiers:
        if not os.path.isdir(dossier):
            continue
        for racine_dir, _, fichiers in os.walk(dossier):
            for f in fichiers:
                if not f.endswith(".md"):
                    continue
                chemin = os.path.join(racine_dir, f)
                try:
                    txt = io.open(chemin, encoding="utf-8", errors="replace").read()
                except Exception:
                    continue
                for m in re.finditer(pattern, txt):
                    script = m.group(0)
                    # contexte approximatif : l'agent du dossier parent
                    rel = os.path.relpath(chemin, racine)
                    trouves.append((script, rel))
    return trouves


def scanner_registre(racine):
    """Entrees mode script-temporaire du registre COURANT et de l HISTORIQUE
    (round 8 : les declarations archivees restent verifiables)."""
    entrees = []
    for chemin in (registre_defaut(racine), registre_historique(racine)):
        if not os.path.isfile(chemin):
            continue
        try:
            fh = io.open(chemin, encoding="utf-8")
        except Exception:
            continue
        with fh:
            for l in fh:
                if not l.strip():
                    continue
                try:
                    e = json.loads(l)
                except ValueError:
                    continue
                if e.get("mode") == "script-temporaire":
                    entrees.append(e)
    return entrees


def main():
    parser = argparse.ArgumentParser(
        description="Detecte et mesure l'usage des scripts temporaires par les agents")
    parser.add_argument("--rapport", type=str, default="", help="Chemin du rapport markdown (optionnel)")
    parser.add_argument("--verbose", action="store_true", help="Detail par source")
    parser.add_argument("--version", action="version",
                        version="detecter-usage-scripts-temporaires v%s" % VERSION)
    args = parser.parse_args()

    racine = racine_projet()
    pattern_script = re.compile(r"\.zz-[a-zA-Z0-9_-]+\.py|\.tmp-[a-zA-Z0-9_-]+\.py|\.zz-[a-zA-Z0-9_-]+\.sh|\.tmp-[a-zA-Z0-9_-]+\.sh")

    # --- 1. racine
    racine_scripts = scanner_racine(racine)

    # --- 2. git
    git_scripts = scanner_git(racine)

    # --- 3. corrections/lecons
    corrections = os.path.join(racine, "cerveau-projet", "agents")
    dossiers_lecons = [os.path.join(corrections, a) for a in os.listdir(corrections)
                       if os.path.isdir(os.path.join(corrections, a))]
    lecons = scanner_dossiers(racine, dossiers_lecons, pattern_script)

    # --- 4. registre (declarations)
    declarations = scanner_registre(racine)
    noms_declares = set(e.get("outil", "") for e in declarations)

    # --- consolidation
    tous = set(racine_scripts) | set(git_scripts)
    tous_lecons = set(s for s, _ in lecons)
    tous |= tous_lecons

    # scripts trouves mais non declares
    non_declares = sorted(tous - noms_declares)

    # par agent (meilleure estimation : contexte des lecons + agent des declarations)
    agents_lecons = Counter(agent for agent in dossiers_lecons
                            for s, rel in lecons if rel.startswith(os.path.relpath(agent, racine) + os.sep))
    agents_declarations = Counter(e.get("agent", "?") for e in declarations)

    print(_couleur("=== Detecter l'usage des scripts temporaires ===", "bleu"))
    print("  1. A la racine (present)     : %d script(s)  %s" % (
        len(racine_scripts), ", ".join(racine_scripts[:5]) if racine_scripts else "(aucun)"))
    print("  2. Dans git (cree un jour)   : %d script(s)" % len(git_scripts))
    print("  3. Dans les lecons/rapports  : %d mention(s) dans %d fichier(s)" % (
        len(lecons), len(set(rel for _, rel in lecons))))
    print("  4. Declares au registre (mode script-temporaire) : %d" % len(declarations))
    print("")
    print("  Scripts detectes non declares : %d" % len(non_declares))
    for s in sorted(non_declares)[:10]:
        print("     - %s" % s)
    if len(non_declares) > 10:
        print("     ... (%d autres)" % (len(non_declares) - 10))

    if agents_lecons or agents_declarations:
        print("")
        print("  Par agent (lecons)      : %s" % dict(agents_lecons))
        print("  Par agent (declarations) : %s" % dict(agents_declarations))

    ecart = len(non_declares)
    verdict = "PROPRE" if ecart == 0 else "ECART DETECTE"
    print("")
    print(_couleur("  Verdict : %s (%d script(s) non declare(s))" % (verdict, ecart),
                   "vert" if ecart == 0 else "rouge"))

    if args.rapport:
        with io.open(args.rapport, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# Rapport : usage des scripts temporaires\n\n")
            fh.write("Date : %s\n\n" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            fh.write("- A la racine : %d\n" % len(racine_scripts))
            fh.write("- Git : %d\n" % len(git_scripts))
            fh.write("- Lecons/rapports : %d mentions\n" % len(lecons))
            fh.write("- Declarations registre : %d\n" % len(declarations))
            fh.write("- Verdict : %s\n\n" % verdict)
            if non_declares:
                fh.write("## Scripts non declares\n\n")
                for s in sorted(non_declares):
                    fh.write("- %s\n" % s)
            if lecons:
                fh.write("\n## Mentions dans les lecons\n\n")
                for s, rel in sorted(set(lecons)):
                    fh.write("- %s (in %s)\n" % (s, rel))
        print(_couleur("[OK] Rapport ecrit : %s" % args.rapport, "vert"))

    return 1 if ecart else 0


if __name__ == "__main__":
    sys.exit(main())
