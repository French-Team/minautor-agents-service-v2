#!/usr/bin/env python3
# -*- coding: ascii -*-
# analyser-fonctions.py
#
# PROFILEUR DE FONCTIONS : lance un script cible sous cProfile et affiche les
# fonctions les plus couteuses (temps cumule, temps propre, nombre d appels),
# pour cibler les goulots INTERNES d un outil ou d un test (au-dela du simple
# temps mural que donne analyser-performance-tests).
#
# Le script cible est execute tel quel via 'python -m cProfile -o <tmp>.prof',
# puis le resultat est relu avec pstats et classe par la cle demandee. Le
# fichier de profil temporaire est ecrit dans un dossier temporaire du
# workspace et supprime a la fin (aucun residu).
#
# Usage :
#   python3 analyser-fonctions.py <script> [args du script...]
#   python3 analyser-fonctions.py <script> --agent janus --tests test-041
#   python3 analyser-fonctions.py --top 10 --sort tottime <script>
#   python3 analyser-fonctions.py --sort ncalls <script>
#   python3 analyser-fonctions.py --version
#
# Options :
#   --top <N>      N fonctions a afficher (defaut 20)
#   --sort <cle>   cle de tri : cumtime | tottime | ncalls (defaut cumtime)
#   --no-chrono    coupe le chrono de l outil
#   --version
#
# Version : 0.1.1
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
analyser-fonctions.py
analyser-fonctions

Usage:
  analyser-fonctions.py <script> [args...] [--top N] [--sort cumtime|tottime|ncalls]
"""

import argparse
import os
import pstats
import subprocess
import sys
import tempfile
import time

VERSION = "0.1.1"
STATUT = "ebauche"
CLES_TRI = ("cumtime", "tottime", "ncalls")


def _couleur(texte, nom="neutre"):
    codes = {"rouge": 31, "vert": 32, "jaune": 33, "bleu": 34, "neutre": 0}
    if not sys.stdout.isatty():
        return texte
    return "\033[%dm%s\033[0m" % (codes.get(nom, 0), texte)


def executer_profil(script, args_cible):
    """Lance le script cible sous cProfile, retourne le chemin du .prof
    (fichier temporaire du workspace) et le code retour."""
    racine = os.getcwd()
    dossier_temp = os.path.join(racine, "workspace", "tmp-analyser-fonctions")
    os.makedirs(dossier_temp, exist_ok=True)
    fd, chemin = tempfile.mkstemp(suffix=".prof", dir=dossier_temp)
    os.close(fd)
    cmd = [sys.executable, "-m", "cProfile", "-o", chemin, script] + args_cible
    print(_couleur("[PROFIL] %s" % " ".join(cmd), "jaune"))
    t0 = time.monotonic()
    r = subprocess.run(cmd, capture_output=True, text=True)
    duree = time.monotonic() - t0
    print(_couleur("[PROFIL] fin : %.2fs (rc=%d)" % (duree, r.returncode), "neutre"))
    if r.stderr.strip():
        print(_couleur("--- stderr du script cible ---", "jaune"))
        for ligne in r.stderr.strip().splitlines()[-10:]:
            print("  " + ligne)
    return chemin, r.returncode


def afficher_profil(chemin, top, cle_tri, no_chrono):
    t0 = time.monotonic()
    stats = pstats.Stats(chemin)
    stats.sort_stats(cle_tri)
    print("")
    print(_couleur("=== TOP %d FONCTIONS (tri : %s) ===" % (top, cle_tri), "bleu"))
    print("%-6s %-10s %-10s %s" % ("Appels", "Cumule(s)", "Propre(s)", "Fonction"))
    for i, (func, data) in enumerate(stats.stats.items(), 1):
        if i > top:
            break
        cc, nc, tt, ct, _ = data
        nom = "%s:%d(%s)" % (func[0], func[1], func[2])
        if len(nom) > 60:
            nom = "..." + nom[-57:]
        print("%-6s %-10.3f %-10.3f %s" % (nc, ct, tt, nom))
    if not no_chrono:
        print(_couleur("[chrono] analyser-fonctions %.2fs" % (time.monotonic() - t0), "neutre"))


def main():
    parser = argparse.ArgumentParser(
        description="Profile un script cible (cProfile) et affiche les fonctions "
                    "les plus couteuses (goulots internes)")
    parser.add_argument("cible", nargs="?", help="Script a profiler")
    parser.add_argument("args_cible", nargs=argparse.REMAINDER,
                        help="Arguments passes au script cible - les options a tiret (--agent, --tests, ...) sont acceptees ; placez les options de CE outil (--top/--sort/--no-chrono) AVANT le script")
    parser.add_argument("--top", type=int, default=20,
                        help="N fonctions a afficher (defaut 20)")
    parser.add_argument("--sort", type=str, default="cumtime", choices=list(CLES_TRI),
                        help="Cle de tri : cumtime | tottime | ncalls (defaut cumtime)")
    parser.add_argument("--no-chrono", action="store_true",
                        help="Coupe le chrono de l outil")
    parser.add_argument("--version", action="version",
                        version="analyser-fonctions v%s" % VERSION)
    parser.add_argument("--aide", action="help",
                        help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    if not args.cible:
        print(_couleur("[ERREUR] Script cible manquant : "
                       "analyser-fonctions.py <script> [args...]", "rouge"))
        return 2
    if not os.path.isfile(args.cible):
        print(_couleur("[ERREUR] Script introuvable : %s" % args.cible, "rouge"))
        return 2

    chemin_prof, rc = executer_profil(args.cible, args.args_cible)
    try:
        afficher_profil(chemin_prof, args.top, args.sort, args.no_chrono)
    finally:
        try:
            os.remove(chemin_prof)
        except OSError:
            pass
    return 0 if rc == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
