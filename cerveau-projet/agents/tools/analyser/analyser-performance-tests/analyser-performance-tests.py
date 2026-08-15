#!/usr/bin/env python3
# -*- coding: ascii -*-
# analyser-performance-tests.py
#
# Analyse la performance de la suite anti-regression : lit le registre des
# lancements de tests (registre-tests.jsonl) et classe les tests du DERNIER
# RUN COMPLET par duree consommee, du plus gros consommateur au moins.
#
# Le registre-tests est alimente par tester-lancer-non-regression : chaque
# test execute est journalise avec (date, agent, serie, test, verdict, duree).
# Cet outil sert a analyser la suite quand on veut OPTIMISER les performances
# des tests (reperer les goulots, comme test-028/032 qui dominent le temps
# total).
#
# Dernier run complet : toutes les entrees dont la date est dans la meme
# fenetre temporelle que la date la plus recente (defaut : 10 minutes, option
# --fenetre-minutes N). Un run complet de non-regression dure ~100 s, une
# fenetre de 10 minutes isole donc proprement le dernier lancement.
#
# Usage :
#   python3 analyser-performance-tests.py
#   python3 analyser-performance-tests.py --fenetre-minutes 5
#   python3 analyser-performance-tests.py --top 15
#   python3 analyser-performance-tests.py --rapport rapport-perf.md
#   python3 analyser-performance-tests.py --verbose
#   python3 analyser-performance-tests.py --version
#
# Options :
#   --fenetre-minutes N : fenetre temporelle du dernier run (defaut 10)
#   --top <N>           : n afficher que les N premiers consommateurs
#   --rapport <fichier> : ecrit le rapport markdown
#   --verbose           : detail (agent, serie, verdict par test)
#   --dry-run           : affiche sans ecrire le rapport
#   --no-chrono         : coupe le chrono de l outil lui-meme
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
import argparse
import io
import json
import os
import sys
import time
from datetime import datetime, timedelta


VERSION = "0.1.0"
STATUT = "ebauche"
RATIO_PAR_SECONDE = "s"


def _couleur(texte, nom="neutre"):
    """Coloration simple (desactivee si la sortie n est pas un terminal)."""
    codes = {"rouge": 31, "vert": 32, "jaune": 33, "bleu": 34, "neutre": 0}
    if not sys.stdout.isatty():
        return texte
    return "\033[%dm%s\033[0m" % (codes.get(nom, 0), texte)


def racine_projet():
    """Remonte jusqu'au dossier racine (contenant AGENTS.md)."""
    d = os.path.dirname(os.path.abspath(__file__))
    while not os.path.isfile(os.path.join(d, "AGENTS.md")):
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return d


def registre_tests(racine):
    return os.path.join(racine, "cerveau-projet", "agents", "traces",
                        "registre-tests.jsonl")


def charger_entrees(registre):
    """Charge toutes les entrees JSON du registre (lignes invalides ignorees)."""
    if not os.path.isfile(registre):
        return []
    entrees = []
    for ligne in io.open(registre, encoding="utf-8", errors="replace"):
        ligne = ligne.strip()
        if not ligne:
            continue
        try:
            e = json.loads(ligne)
        except ValueError:
            continue
        if not e.get("date") or not e.get("duree"):
            continue
        entrees.append(e)
    return entrees


def dernier_run(entrees, fenetre_minutes):
    """Isole les entrees du dernier run : fenetre temporelle autour de la
    date la plus recente. Retourne (entrees_run, date_max, ecart_minutes)."""
    if not entrees:
        return [], None, 0
    fmt = "%Y-%m-%d %H:%M:%S"
    parsees = []
    for e in entrees:
        try:
            d = datetime.strptime(e["date"], fmt)
            parsees.append((d, e))
        except ValueError:
            continue
    if not parsees:
        return [], None, 0
    dmax = max(d for d, _ in parsees)
    seuil = dmax - timedelta(minutes=fenetre_minutes)
    run = [e for d, e in parsees if d >= seuil]
    ecart_min = (dmax - min(d for d, _ in parsees if d >= seuil)).total_seconds() / 60.0
    return run, dmax, ecart_min


def classer_par_duree(run):
    """Classe les tests du plus gros consommateur au moins.
    Retourne liste de dicts (test, duree_totale, nb_runs, verdicts)."""
    agg = {}
    for e in run:
        nom = e.get("test", "?")
        a = agg.setdefault(nom, {"test": nom, "duree_totale": 0.0, "nb": 0,
                                 "verdicts": [], "series": []})
        a["duree_totale"] += float(e.get("duree", 0))
        a["nb"] += 1
        a["verdicts"].append(e.get("verdict", "?"))
        if e.get("serie") and e["serie"] not in a["series"]:
            a["series"].append(e["serie"])
    classe = sorted(agg.values(), key=lambda a: a["duree_totale"], reverse=True)
    return classe


def afficher(racine, classe, run, dmax, ecart_min, top=0, verbose=False,
             no_chrono=False):
    t0 = time.monotonic()
    nb = len(run)
    nb_tests = len(classe)
    duree_totale = sum(a["duree_totale"] for a in classe)
    print("")
    print(_couleur("=== ANALYSE PERFORMANCE DES TESTS (dernier run) ===", "bleu"))
    if dmax:
        print("Dernier run : %s (%d entrees, %d tests distincts, fenetre %.0f min)"
              % (dmax, nb, nb_tests, ecart_min))
    print("Duree totale consommee : %.1f s" % duree_totale)
    print("")
    affiche = classe if top <= 0 else classe[:top]
    print(_couleur("%-4s %-8s %-52s %s" % ("#", "Duree(s)", "Test", "Serie(s)"),
                   "neutre"))
    for i, a in enumerate(affiche, 1):
        verdicts = ",".join(sorted(set(a["verdicts"])))
        series = ",".join(a["series"]) or "-"
        ligne = "%-4d %-8.1f %-52s %s" % (i, a["duree_totale"], a["test"], series)
        if verbose:
            ligne += "  [%s]" % verdicts
        print(ligne)
    if len(classe) > len(affiche):
        print("... (%d test(s) non affiches, --top pour en voir plus)"
              % (len(classe) - len(affiche)))
    print("")
    if not no_chrono:
        print(_couleur("[chrono] analyser-performance-tests %.2fs"
                       % (time.monotonic() - t0), "neutre"))
    return classe


def ecrire_rapport(chemin, classe, run, dmax, ecart_min, racine):
    """Ecrit le rapport markdown du dernier run (classement + details)."""
    with io.open(chemin, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Rapport performance des tests (dernier run)\n\n")
        if dmax:
            fh.write("- Dernier run : %s\n" % dmax)
            fh.write("- Entrees : %d (fenetre %.0f min)\n" % (len(run), ecart_min))
        fh.write("- Tests distincts : %d\n" % len(classe))
        duree_totale = sum(a["duree_totale"] for a in classe)
        fh.write("- Duree totale consommee : %.1f s\n\n" % duree_totale)
        fh.write("## Classement (du plus gros consommateur au moins)\n\n")
        fh.write("| # | Duree (s) | Test | Serie(s) | Verdicts |\n")
        fh.write("|---|---|---|---|---|\n")
        for i, a in enumerate(classe, 1):
            fh.write("| %d | %.1f | `%s` | %s | %s |\n"
                     % (i, a["duree_totale"], a["test"],
                        ",".join(a["series"]) or "-",
                        ",".join(sorted(set(a["verdicts"])))))
        fh.write("\n## Duree cumulee (pour identifier le seuil a optimiser)\n\n")
        cumul = 0.0
        fh.write("| # | Test | Duree (s) | Cumulee (s) | %% cumule |\n")
        fh.write("|---|---|---|---|---|\n")
        for i, a in enumerate(classe, 1):
            cumul += a["duree_totale"]
            pct = 100.0 * cumul / duree_totale if duree_totale else 0.0
            fh.write("| %d | `%s` | %.1f | %.1f | %.1f%% |\n"
                     % (i, a["test"], a["duree_totale"], cumul, pct))


def main():
    parser = argparse.ArgumentParser(
        description="Analyse la performance des tests du dernier run de "
                    "non-regression (registre-tests.jsonl)")
    parser.add_argument("--fenetre-minutes", type=int, default=10,
                        help="Fenetre temporelle du dernier run (defaut 10)")
    parser.add_argument("--top", type=int, default=0,
                        help="N afficher que les N premiers consommateurs")
    parser.add_argument("--rapport", type=str, default="",
                        help="Chemin du rapport markdown (optionnel)")
    parser.add_argument("--verbose", action="store_true",
                        help="Detail : agent, serie, verdict par test")
    parser.add_argument("--dry-run", action="store_true",
                        help="Afficher sans ecrire le rapport")
    parser.add_argument("--no-chrono", action="store_true",
                        help="Couper le chrono de l outil")
    parser.add_argument("--version", action="version",
                        version="analyser-performance-tests v%s" % VERSION)
    args = parser.parse_args()

    racine = racine_projet()
    registre = registre_tests(racine)
    if not os.path.isfile(registre):
        print(_couleur("[ERREUR] Registre introuvable : %s" % registre, "rouge"))
        return 2
    entrees = charger_entrees(registre)
    if not entrees:
        print(_couleur("[ERREUR] Registre-tests vide : %s" % registre, "rouge"))
        return 2
    run, dmax, ecart_min = dernier_run(entrees, args.fenetre_minutes)
    if not run:
        print(_couleur("[ERREUR] Aucune entree dans la fenetre du dernier run "
                       "(--fenetre-minutes %d)" % args.fenetre_minutes, "rouge"))
        return 2
    classe = classer_par_duree(run)
    afficher(racine, classe, run, dmax, ecart_min, top=args.top,
             verbose=args.verbose, no_chrono=args.no_chrono)
    if args.rapport and not args.dry_run:
        ecrire_rapport(args.rapport, classe, run, dmax, ecart_min, racine)
        print(_couleur("[OK] Rapport ecrit : %s" % args.rapport, "vert"))
    elif args.rapport and args.dry_run:
        print(_couleur("[DRY-RUN] Rapport NON ecrit (--dry-run) : %s"
                       % args.rapport, "jaune"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
