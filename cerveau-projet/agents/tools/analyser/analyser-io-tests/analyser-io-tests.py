#!/usr/bin/env python3
# -*- coding: ascii -*-
# analyser-io-tests.py
#
# Mesure la LECTURE/ECRITURE DISQUE PENDANT l execution d un ou plusieurs
# tests de la suite anti-regression : pour chaque test, execute le test et
# capture (via psutil.io_counters du processus + enfants recursifs) :
#   - duree (secondes)
#   - octets lus (read_bytes)
#   - octets ecrits (write_bytes)
#   - operations de lecture / ecriture (read_count / write_count)
# Objectif : identifier les tests gourmands en I/O disque (goulots de la
# suite) pour comprendre pourquoi la suite est longue et l optimiser.
#
# psutil est une DEPENDANCE DOUCE : s il est absent, l outil mesure la duree
# seule et affiche un avertissement (jamais bloquant).
#
# Usage :
#   python3 analyser-io-tests.py test-032 test-028
#   python3 analyser-io-tests.py --serie e
#   python3 analyser-io-tests.py --tous
#   python3 analyser-io-tests.py <chemin/vers/test.py> ...
#   python3 analyser-io-tests.py --serie c,d --rapport rapport-io.md
#   python3 analyser-io-tests.py --verbose
#   python3 analyser-io-tests.py --version
#
# Options :
#   --serie <a,b..>    tests des series indiquees (definition lue dans le
#                      lanceur tester-lancer-non-regression - synchro auto)
#   --tous             tous les tests du dossier tester/tests/
#   --rapport <fichier> ecrit le rapport markdown
#   --verbose          detail des compteurs par test (rc, erreurs)
#   --no-chrono        coupe le chrono de l outil lui-meme
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
analyser-io-tests.py
analyser-io-tests

Usage:
  analyser-io-tests.py test-032 test-028
  analyser-io-tests.py --serie e
  analyser-io-tests.py --tous
"""

import argparse
import ast
import glob
import io
import os
import re
import subprocess
import sys
import time

VERSION = "0.1.0"

try:
    import psutil  # dependance douce (io_counters disque)
    HAS_PSUTIL = True
except ImportError:
    psutil = None
    HAS_PSUTIL = False

RACINE = os.path.dirname(os.path.abspath(__file__))
while not os.path.isfile(os.path.join(RACINE, "AGENTS.md")):
    RACINE = os.path.dirname(RACINE)

TESTS_DIR = os.path.join(RACINE, "cerveau-projet", "agents", "tools",
                         "tester", "tests")
LANCEUR = os.path.join(RACINE, "cerveau-projet", "agents", "tools",
                       "tester", "tester-lancer-non-regression",
                       "tester-lancer-non-regression.py")


def couleur(texte, nom):
    """Colorisation simple (ANSI), desactivee si non-tty."""
    codes = {"rouge": "31", "vert": "32", "jaune": "33", "bleu": "34"}
    if not sys.stdout.isatty() or nom not in codes:
        return texte
    return "\x1b[%sm%s\x1b[0m" % (codes[nom], texte)


def lire_series_lanceur():
    """Extraire la definition SERIES du lanceur (sync automatique)."""
    try:
        src = io.open(LANCEUR, encoding="utf-8", errors="replace").read()
        m = re.search(r"SERIES\s*=\s*(\{.*?\n\})", src, re.S)
        if not m:
            return {}
        series = ast.literal_eval(m.group(1))
        return series if isinstance(series, dict) else {}
    except (IOError, ValueError, SyntaxError):
        return {}


def resoudre_tests(noms, series):
    """Resoudre noms (test-032, chemins, serie a,b, tous) vers des fichiers."""
    fichiers = []
    for nom in noms:
        if nom.startswith("--serie"):
            continue
        if os.path.isfile(nom):
            fichiers.append(os.path.abspath(nom))
            continue
        motif = os.path.join(TESTS_DIR, nom + "-*", nom + "*.py")
        trouves = sorted(glob.glob(motif))
        if not trouves:
            motif2 = os.path.join(TESTS_DIR, nom + "*", "*.py")
            trouves = sorted(glob.glob(motif2))
        if not trouves:
            print(couleur("  [AVERT] Test introuvable : " + nom, "jaune"))
            continue
        fichiers.extend(trouves)
    return fichiers


def tests_serie(lettres, series):
    """Liste des noms de tests (test-NNN) des series demandees."""
    noms = []
    for lettre in lettres.replace(" ", "").split(","):
        if not lettre:
            continue
        if lettre not in series:
            print(couleur("  [AVERT] Serie inconnue : " + lettre, "jaune"))
            continue
        noms.extend(series[lettre])
    return noms


def tous_les_tests():
    """Tous les fichiers .py des dossiers de tests."""
    fichiers = []
    for dossier in sorted(glob.glob(os.path.join(TESTS_DIR, "test-*"))):
        for f in sorted(glob.glob(os.path.join(dossier, "*.py"))):
            if "__pycache__" not in f:
                fichiers.append(f)
    return fichiers


def cumul_io(pid):
    """Somme des io_counters du processus + enfants recursifs (vivants)."""
    if not HAS_PSUTIL:
        return None
    total = [0, 0, 0, 0]  # read_bytes, write_bytes, read_count, write_count
    vus = set()
    try:
        proc = psutil.Process(pid)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None
    try:
        arbre = [proc] + proc.children(recursive=True)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        arbre = [proc]
    for c in arbre:
        if c.pid in vus:
            continue
        vus.add(c.pid)
        try:
            io_cnt = c.io_counters()
            total[0] += io_cnt.read_bytes
            total[1] += io_cnt.write_bytes
            total[2] += io_cnt.read_count
            total[3] += io_cnt.write_count
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return tuple(total)


def mesurer_test(chemin):
    """Executer un test et mesurer duree + I/O disque pendant l execution."""
    nom = os.path.basename(chemin)
    debut = time.monotonic()
    dernier_io = None
    try:
        proc = subprocess.Popen([sys.executable, chemin], cwd=RACINE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    except OSError as e:
        return {"test": nom, "duree": 0.0, "rc": -1,
                "io": None, "erreur": str(e)}
    # Boucle de mesure : cumule l I/O du process + enfants pendant le run
    while proc.poll() is None:
        dernier_io = cumul_io(proc.pid)
        time.sleep(0.02)
    dernier_io = cumul_io(proc.pid) or dernier_io
    try:
        proc.communicate(timeout=30)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.communicate()
    duree = time.monotonic() - debut
    return {"test": nom, "duree": duree, "rc": proc.returncode,
            "io": dernier_io, "erreur": ""}


def fmt_mo(octets):
    if octets is None:
        return "-"
    return "%.1f" % (octets / (1024.0 * 1024.0))


def main():
    global RACINE, TESTS_DIR, LANCEUR
    parser = argparse.ArgumentParser(
        prog="analyser-io-tests",
        description="Mesure la lecture/ecriture disque pendant l execution des tests.")
    parser.add_argument("tests", nargs="*", help="Tests a mesurer (noms ou chemins)")
    parser.add_argument("--serie", default="", help="Series a mesurer (a,b,c,d,e)")
    parser.add_argument("--tous", action="store_true", help="Tous les tests")
    parser.add_argument("--rapport", default="", help="Rapport markdown")
    parser.add_argument("--verbose", action="store_true", help="Detail par test")
    parser.add_argument("--no-chrono", action="store_true", help="Coupe le chrono")
    parser.add_argument("--version", action="store_true", help="Affiche la version")
    args = parser.parse_args()

    if args.version:
        print("analyser-io-tests v" + VERSION)
        return 0

    t_debut = time.monotonic()
    print("=== analyser-io-tests v" + VERSION + " ===")
    print("Racine : " + RACINE)
    if not HAS_PSUTIL:
        print(couleur("  [AVERT] psutil absent : mesure de la duree seule "
                      "(pas d I/O disque).", "jaune"))

    series = lire_series_lanceur()
    fichiers = []
    if args.tous:
        fichiers = tous_les_tests()
    if args.serie:
        noms = tests_serie(args.serie, series)
        fichiers.extend(resoudre_tests(noms, series))
    fichiers.extend(resoudre_tests(args.tests, series))
    # deduplication en conservant l ordre (iteration sur une COPIE : le
    # reassignement de fichiers ne doit pas vider la source avant l iteration)
    vus = set()
    dedup = []
    for f in sorted(set(fichiers)):
        if f not in vus:
            vus.add(f)
            dedup.append(f)
    fichiers = dedup

    if not fichiers:
        print(couleur("  [ERREUR] Aucun test a mesurer (donnez des noms, "
                      "--serie ou --tous).", "rouge"))
        return 2

    print("Tests a mesurer : %d" % len(fichiers))
    print("")

    resultats = []
    for chemin in fichiers:
        r = mesurer_test(chemin)
        resultats.append(r)
        io_txt = ""
        if r["io"]:
            rb, wb, rc, wc = r["io"]
            io_txt = " | lect %.1f Mo | ecrit %.1f Mo" % (rb / 1048576.0,
                                                          wb / 1048576.0)
        ligne = "  [%s] %-45s %6.1f s%s" % (
            "OK " if r["rc"] == 0 else "KO ", r["test"], r["duree"], io_txt)
        print(couleur(ligne, "vert" if r["rc"] == 0 else "rouge"))

    print("")
    duree_totale = sum(r["duree"] for r in resultats)
    print(couleur("=== SYNTHESE I/O ===", "bleu"))
    print("Tests : %d | duree totale : %.1f s | (mesure : %.1f s)" % (
        len(resultats), duree_totale, time.monotonic() - t_debut))
    if HAS_PSUTIL:
        tot_rb = sum((r["io"][0] or 0) for r in resultats if r["io"])
        tot_wb = sum((r["io"][1] or 0) for r in resultats if r["io"])
        print("Lecture totale : %.1f Mo | Ecriture totale : %.1f Mo" % (
            tot_rb / 1048576.0, tot_wb / 1048576.0))
        print("")
        print("=== TOP CONSOMMATEURS ECRITURE DISQUE ===")
        avec_io = [r for r in resultats if r["io"]]
        for r in sorted(avec_io, key=lambda x: -(x["io"][1] or 0))[:10]:
            rb, wb, rc, wc = r["io"]
            print("  %-45s ecrit %7.1f Mo | lu %7.1f Mo | %5.1f s" % (
                r["test"], wb / 1048576.0, rb / 1048576.0, r["duree"]))

    # rapport markdown
    if args.rapport:
        lignes = [
            "# Rapport I/O disque des tests -- " +
            time.strftime("%Y-%m-%d %H:%M"),
            "",
            "- Outil : analyser-io-tests v" + VERSION,
            "- Tests mesures : %d" % len(resultats),
            "- Duree totale : %.1f s" % duree_totale,
            "",
            "| Test | Duree (s) | Lecture (Mo) | Ecriture (Mo) | Lect ops | Ecrit ops |",
            "|---|---|---|---|---|---|",
        ]
        for r in sorted(resultats, key=lambda x: -x["duree"]):
            if r["io"]:
                rb, wb, rc, wc = r["io"]
                lignes.append("| %s | %.1f | %.1f | %.1f | %d | %d |" % (
                    r["test"], r["duree"], rb / 1048576.0, wb / 1048576.0,
                    rc, wc))
            else:
                lignes.append("| %s | %.1f | - | - | - | - |" % (
                    r["test"], r["duree"]))
        io.open(args.rapport, "w", encoding="utf-8", newline="\n").write(
            "\n".join(lignes) + "\n")
        print("")
        print("Rapport ecrit : " + args.rapport)

    if not args.no_chrono:
        print(couleur("=== CHRONO outil (total %.1fs) ===" % (
            time.monotonic() - t_debut), "bleu"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
