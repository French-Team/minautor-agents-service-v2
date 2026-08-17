#!/usr/bin/env python3
# -*- coding: ascii -*-
# analyser-workers.py
#
# ETUDE D ECHELLE : mesure le temps d execution de la suite de non-regression
# (ou d un sous-ensemble de tests) a DIFFERENTS nombres de workers paralleles,
# pour trouver l optimum qui minimisera le temps total. C est le complement
# dynamique de configurer-environnement : la config donne un point de depart
# theorique, cet outil mesure le point d equilibre REEL (parallele utile vs
# contention).
#
# Principe : pour chaque nombre de workers (1, 2, 4, 8, 16 par defaut), on
# lance le lanceur en mode --parallele avec ce nombre de workers sur le meme
# sous-ensemble de tests, on mesure le temps mural, puis on classe et on
# recommande le plus rapide.
#
# Le lanceur est appele via subprocess avec --no-reference (ne touche pas la
# reference de temps globale) et --journal (ne touche pas au registre d usage) :
# une etude d echelle ne doit pas polluer les metriques de production.
#
# Usage :
#   python3 analyser-workers.py --tests test-028,test-032
#   python3 analyser-workers.py --tests test-028,test-032 --workers-list 1,2,4,8
#   python3 analyser-workers.py --tests test-032 --agent vulcain --rapport w.md
#   python3 analyser-workers.py --verbose
#   python3 analyser-workers.py --version
#
# Options :
#   --tests <liste>      Tests a mesurer (virgule, ex: test-028,test-032)
#   --workers-list <l>   Nombres de workers a tester (defaut 1,2,4,8,16)
#   --agent <nom>        Agent transmis au verrou du lanceur (defaut vulcain)
#   --rapport <fichier>  Ecrit le rapport markdown
#   --verbose            Detail des commandes lancees
#   --dry-run            Affiche les commandes sans lancer
#   --no-chrono          Coupe le chrono de l outil lui-meme
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
analyser-workers.py
analyser-workers

Usage:
  analyser-workers.py --tests test-028,test-032 [OPTIONS]
"""

import argparse
import io
import os
import subprocess
import sys
import time

VERSION = "0.1.0"
STATUT = "ebauche"


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


def lanceur_chemin(racine):
    return os.path.join(racine, "cerveau-projet", "agents", "tools",
                        "tester", "tester-lancer-non-regression",
                        "tester-lancer-non-regression.py")


def parse_workers_list(chaine):
    try:
        vals = [int(x.strip()) for x in chaine.split(",") if x.strip()]
    except ValueError:
        return []
    return [v for v in vals if v > 0]


def lancer_une_mesure(lanceur, tests, workers, agent, verbose, dry_run):
    """Lance le lanceur avec N workers sur le sous-ensemble et mesure le temps
    mural. Retourne (workers, duree, returncode, stdout_tail)."""
    cmd = [sys.executable, lanceur, "--parallele", "--workers", str(workers),
           "--tests", tests, "--agent", agent, "--no-reference", "--journal"]
    if verbose or dry_run:
        print(_couleur("[CMD %d workers] %s" % (workers, " ".join(cmd)), "jaune"))
    if dry_run:
        return workers, 0.0, 0, "(dry-run)"
    t0 = time.monotonic()
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
        duree = time.monotonic() - t0
    except subprocess.TimeoutExpired:
        return workers, 1800.0, 124, "(timeout 1800s)"
    except OSError as exc:
        return workers, 0.0, 1, str(exc)
    tail = (r.stdout or "").strip().splitlines()
    tail = tail[-1] if tail else "(sortie vide)"
    return workers, duree, r.returncode, tail


def afficher_resultats(resultats, no_chrono, dry_run=False):
    t0 = time.monotonic()
    print("")
    print(_couleur("=== ETUDE D ECHELLE DES WORKERS (temps mural par N workers) ===", "bleu"))
    print("%-10s %-12s %-8s" % ("Workers", "Duree(s)", "Verdict"))
    for workers, duree, rc, _ in resultats:
        verdict = "OK" if rc == 0 else ("KO rc=%d" % rc)
        print("%-10d %-12.2f %-8s" % (workers, duree, verdict))
    if dry_run:
        print(_couleur("[DRY-RUN] Commandes affichees, aucune mesure reelle (relancer sans --dry-run).", "jaune"))
        if not no_chrono:
            print(_couleur("[chrono] analyser-workers %.2fs" % (time.monotonic() - t0), "neutre"))
        return
    valides = [(w, d) for w, d, rc, _ in resultats if rc == 0 and d > 0]
    if valides:
        meilleur = min(valides, key=lambda x: x[1])
        pire = max(valides, key=lambda x: x[1])
        gain = 0.0
        if pire[1] > 0:
            gain = 100.0 * (pire[1] - meilleur[1]) / pire[1]
        print("")
        print(_couleur("RECOMMANDATION : %d workers (%.2fs) - gain %.0f%% vs le pire (%d workers, %.2fs)"
                       % (meilleur[0], meilleur[1], gain, pire[0], pire[1]), "vert"))
    else:
        print(_couleur("Aucune mesure valide (tous les runs en KO) - verifier --tests et --agent.", "rouge"))
    if not no_chrono:
        print(_couleur("[chrono] analyser-workers %.2fs" % (time.monotonic() - t0), "neutre"))


def ecrire_rapport(chemin, tests, resultats):
    with io.open(chemin, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Etude d echelle des workers\n\n")
        fh.write("- Tests mesures : `%s`\n" % tests)
        fh.write("\n| Workers | Duree (s) | Verdict |\n")
        fh.write("|---|---|---|\n")
        for workers, duree, rc, _ in resultats:
            fh.write("| %d | %.2f | %s |\n" % (workers, duree, "OK" if rc == 0 else "KO"))
        valides = [(w, d) for w, d, rc, _ in resultats if rc == 0 and d > 0]
        if valides:
            meilleur = min(valides, key=lambda x: x[1])
            fh.write("\n## Recommandation\n\n")
            fh.write("%d workers est le plus rapide (%.2fs).\n" % meilleur)


def main():
    parser = argparse.ArgumentParser(
        description="Etude d echelle : temps de la suite a differents nombres "
                    "de workers paralleles (optimum reel)")
    parser.add_argument("--tests", type=str, default="test-007,test-081",
                        help="Tests a mesurer, separes par des virgules (defaut test-007,test-081)")
    parser.add_argument("--workers-list", type=str, default="1,2,4,8,16",
                        help="Nombres de workers a tester (defaut 1,2,4,8,16)")
    parser.add_argument("--agent", type=str, default="vulcain",
                        help="Agent transmis au verrou du lanceur (defaut vulcain)")
    parser.add_argument("--rapport", type=str, default="",
                        help="Chemin du rapport markdown (optionnel)")
    parser.add_argument("--verbose", action="store_true",
                        help="Detail des commandes lancees")
    parser.add_argument("--dry-run", action="store_true",
                        help="Affiche les commandes sans les lancer")
    parser.add_argument("--no-chrono", action="store_true",
                        help="Coupe le chrono de l outil")
    parser.add_argument("--version", action="version",
                        version="analyser-workers v%s" % VERSION)
    parser.add_argument("--aide", action="help",
                        help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    racine = racine_projet()
    lanceur = lanceur_chemin(racine)
    if not os.path.isfile(lanceur):
        print(_couleur("[ERREUR] Lanceur introuvable : %s" % lanceur, "rouge"))
        return 2
    workers_list = parse_workers_list(args.workers_list)
    if not workers_list:
        print(_couleur("[ERREUR] --workers-list invalide : %s" % args.workers_list, "rouge"))
        return 2

    t0 = time.monotonic()
    resultats = []
    for workers in workers_list:
        resultats.append(lancer_une_mesure(lanceur, args.tests, workers,
                                           args.agent, args.verbose, args.dry_run))
    afficher_resultats(resultats, args.no_chrono, args.dry_run)
    if args.rapport and not args.dry_run:
        ecrire_rapport(args.rapport, args.tests, resultats)
        print(_couleur("[OK] Rapport ecrit : %s" % args.rapport, "vert"))
    print(_couleur("[chrono] etude complete %.2fs (hors chrono par run)"
                   % (time.monotonic() - t0), "neutre"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
