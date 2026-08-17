#!/usr/bin/env python3
# -*- coding: ascii -*-
# analyser-round.py
#
# METRIQUES D UN ROUND : resume l activite d une fenetre de temps (un "round"
# de travail) a partir des traces du cerveau-projet. Un round = la periode
# pendant laquelle Cerberus active des agents, qui utilisent des outils et
# lancent des tests, jusqu au retour au point d entree.
#
# Sources (lecture seule, jamais modifiees) :
#   - registre-usages-outils.jsonl : (date, agent, outil, mode) -> agents
#     actives + outils utilises
#   - registre-tests.jsonl : (date, agent, test, verdict, duree) -> tests
#     lances + duree totale
#   - temps-reference.json : reference de temps de la suite (facultatif)
#
# Le "round" est delimite par --fenetre-minutes (defaut 60 min) avant la date
# la plus recente trouvee dans les registres. Le rapport croise les deux
# sources : qui a travaille, avec quels outils, combien de tests, combien de
# temps. C est la base des futurs indicateurs de productivite d un round.
#
# Usage :
#   python3 analyser-round.py
#   python3 analyser-round.py --fenetre-minutes 30
#   python3 analyser-round.py --rapport rapport-round.md
#   python3 analyser-round.py --verbose
#   python3 analyser-round.py --version
#
# Options :
#   --fenetre-minutes N : fenetre du round (defaut 60)
#   --rapport <fichier> : ecrit le rapport markdown
#   --verbose           : detail (outils par agent, tests par agent)
#   --dry-run           : affiche sans ecrire le rapport
#   --no-chrono         : coupe le chrono de l outil
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
# categorie (analyser-).
# =============================================================================
"""
analyser-round.py
analyser-round

Usage:
  analyser-round.py [--fenetre-minutes N] [--rapport F]
"""

import argparse
import io
import json
import os
import sys
import time
from collections import defaultdict
from datetime import datetime, timedelta

VERSION = "0.1.0"
STATUT = "ebauche"
FMT = "%Y-%m-%d %H:%M:%S"


def _couleur(texte, nom="neutre"):
    codes = {"rouge": 31, "vert": 32, "jaune": 33, "bleu": 34, "neutre": 0}
    if not sys.stdout.isatty():
        return texte
    return "\033[%dm%s\033[0m" % (codes.get(nom, 0), texte)


def racine_projet():
    d = os.path.dirname(os.path.abspath(__file__))
    while not os.path.isfile(os.path.join(d, "AGENTS.md")):
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return d


def traces_dir(racine):
    return os.path.join(racine, "cerveau-projet", "agents", "traces")


def charger_jsonl(chemin):
    if not os.path.isfile(chemin):
        return []
    entrees = []
    for ligne in io.open(chemin, encoding="utf-8", errors="replace"):
        ligne = ligne.strip()
        if not ligne:
            continue
        try:
            e = json.loads(ligne)
        except ValueError:
            continue
        if e.get("date"):
            entrees.append(e)
    return entrees


def dans_fenetre(entrees, fenetre_minutes):
    """Filtre les entrees dans la fenetre avant la date la plus recente.
    Retourne (entrees_filtrees, date_max)."""
    if not entrees:
        return [], None
    parsees = []
    for e in entrees:
        try:
            parsees.append((datetime.strptime(e["date"], FMT), e))
        except ValueError:
            continue
    if not parsees:
        return [], None
    dmax = max(d for d, _ in parsees)
    seuil = dmax - timedelta(minutes=fenetre_minutes)
    return [e for d, e in parsees if d >= seuil], dmax


def agreger(usages, tests):
    agents = set()
    outils_par_agent = defaultdict(set)
    tous_outils = set()
    for e in usages:
        agent = e.get("agent", "?")
        outil = e.get("outil", "?")
        agents.add(agent)
        outils_par_agent[agent].add(outil)
        tous_outils.add(outil)
    nb_outils = len(tous_outils)
    tests_par_agent = defaultdict(lambda: [0, 0.0])
    for e in tests:
        agent = e.get("agent", "?")
        tests_par_agent[agent][0] += 1
        tests_par_agent[agent][1] += float(e.get("duree", 0))
    return agents, outils_par_agent, nb_outils, tests_par_agent


def afficher(agents, outils_par_agent, nb_outils, tests_par_agent,
             nb_usages, nb_tests, duree_tests, dmax, fenetre, no_chrono):
    t0 = time.monotonic()
    print("")
    print(_couleur("=== ANALYSE DU ROUND (fenetre %d min) ===" % fenetre, "bleu"))
    if dmax:
        print("Derniere activite : %s" % dmax)
    print("Agents actives : %d" % len(agents))
    print("Usages d outils : %d (%d outils distincts)" % (nb_usages, nb_outils))
    print("Tests lances : %d (duree totale %.1f s)" % (nb_tests, duree_tests))
    print("")
    print(_couleur("=== OUTILS PAR AGENT ===", "neutre"))
    for agent in sorted(agents):
        outils = sorted(outils_par_agent.get(agent, []))
        print("  %-14s : %d outil(s) %s" % (agent, len(outils),
                                             "(" + ", ".join(outils[:6]) + ")"
                                             if outils else ""))
    if tests_par_agent:
        print("")
        print(_couleur("=== TESTS PAR AGENT ===", "neutre"))
        for agent in sorted(tests_par_agent):
            nb, dur = tests_par_agent[agent]
            print("  %-14s : %d test(s), %.1f s" % (agent, nb, dur))
    if not no_chrono:
        print(_couleur("[chrono] analyser-round %.2fs" % (time.monotonic() - t0), "neutre"))


def ecrire_rapport(chemin, agents, outils_par_agent, nb_outils,
                   tests_par_agent, nb_usages, nb_tests, duree_tests, dmax, fenetre):
    with io.open(chemin, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Rapport d analyse du round\n\n")
        if dmax:
            fh.write("- Derniere activite : %s\n" % dmax)
        fh.write("- Fenetre : %d min\n" % fenetre)
        fh.write("- Agents actives : %d\n" % len(agents))
        fh.write("- Usages d outils : %d (%d distincts)\n" % (nb_usages, nb_outils))
        fh.write("- Tests lances : %d (%.1f s)\n\n" % (nb_tests, duree_tests))
        fh.write("## Outils par agent\n\n")
        fh.write("| Agent | Outils |\n|---|---|\n")
        for agent in sorted(agents):
            fh.write("| %s | %s |\n" % (agent, ", ".join(sorted(outils_par_agent.get(agent, []))) or "-"))
        if tests_par_agent:
            fh.write("\n## Tests par agent\n\n")
            fh.write("| Agent | Tests | Duree (s) |\n|---|---|---|\n")
            for agent in sorted(tests_par_agent):
                nb, dur = tests_par_agent[agent]
                fh.write("| %s | %d | %.1f |\n" % (agent, nb, dur))


def main():
    parser = argparse.ArgumentParser(
        description="Resume l activite d un round (fenetre de temps) : agents "
                    "actives, outils utilises, tests lances")
    parser.add_argument("--fenetre-minutes", type=int, default=60,
                        help="Fenetre du round (defaut 60 min)")
    parser.add_argument("--rapport", type=str, default="",
                        help="Chemin du rapport markdown (optionnel)")
    parser.add_argument("--verbose", action="store_true",
                        help="Detail : outils par agent, tests par agent")
    parser.add_argument("--dry-run", action="store_true",
                        help="Affiche sans ecrire le rapport")
    parser.add_argument("--no-chrono", action="store_true",
                        help="Coupe le chrono de l outil")
    parser.add_argument("--version", action="version",
                        version="analyser-round v%s" % VERSION)
    parser.add_argument("--aide", action="help",
                        help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    racine = racine_projet()
    traces = traces_dir(racine)
    usages = charger_jsonl(os.path.join(traces, "registre-usages-outils.jsonl"))
    tests = charger_jsonl(os.path.join(traces, "registre-tests.jsonl"))
    if not usages and not tests:
        print(_couleur("[ERREUR] Registres vides : aucun usage ni test a analyser.", "rouge"))
        return 2

    usages_f, dmax_u = dans_fenetre(usages, args.fenetre_minutes)
    tests_f, dmax_t = dans_fenetre(tests, args.fenetre_minutes)
    dmax = None
    for d in (dmax_u, dmax_t):
        if d and (dmax is None or d > dmax):
            dmax = d

    agents, outils_par_agent, nb_outils, tests_par_agent = agreger(usages_f, tests_f)
    nb_usages = len(usages_f)
    nb_tests = len(tests_f)
    duree_tests = sum(v[1] for v in tests_par_agent.values())

    afficher(agents, outils_par_agent, nb_outils, tests_par_agent,
             nb_usages, nb_tests, duree_tests, dmax, args.fenetre_minutes,
             args.no_chrono)
    if args.rapport and not args.dry_run:
        ecrire_rapport(args.rapport, agents, outils_par_agent, nb_outils,
                       tests_par_agent, nb_usages, nb_tests, duree_tests,
                       dmax, args.fenetre_minutes)
        print(_couleur("[OK] Rapport ecrit : %s" % args.rapport, "vert"))
    elif args.rapport and args.dry_run:
        print(_couleur("[DRY-RUN] Rapport NON ecrit : %s" % args.rapport, "jaune"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
