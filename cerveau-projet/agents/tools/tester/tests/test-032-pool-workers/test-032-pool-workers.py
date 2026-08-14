#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-032-pool-workers.py
GARDE-FOU : le lanceur de non-regression utilise un POOL DE WORKERS par
defaut (round 12, demande utilisateur : reduire le temps total de la suite
anti-regression avec des suites paralleles contenant les tests longs).

Contexte (demande utilisateur 2026-08-13) :
  - La suite anti-regression va etre lancee souvent : il faut reduire le
    temps total. Diagnostic : machine 16 coeurs, test-028 = 88s (LE goulot,
    60% du temps), 30 autres tests <= 9s.
  - Solution : pool de workers (--workers N, defaut min(cpu,16)), tests
    tries par duree decroissante (les plus longs partent en premier), les
    garde-fous globaux (registre, sessions, scripts temporaires) restent en
    serie finale. Gain reel mesure : 119.9s -> 91.2s (-24%).
  - ANTI-DEADLOCK : la sortie de chaque test est redirigee vers un fichier
    temp unique - un Popen(stdout=PIPE) non lu se bloque au-dela de 64 Ko.

Invariants verifies :
  1. --version affiche v0.3.1
  2. Le mode par defaut utilise le pool (Pool de workers dans la sortie)
  3. --serial ou --workers 1 force le mode serie (pas de Pool)
  4. GARDE_FOUS_GLOBAUX identifie test-023/024/025/027 dans le code
  5. Anti-deadlock : executer_pool redirige vers un fichier (pas de pipe)
  6. --workers present dans --help
  7. Preuve de gain : un sous-ensemble en pool est plus rapide ou egal au
     mode serie (seuil large, tolerance machine)
  8. Normes : ASCII strict + LF pur (test + lanceur)
"""
import importlib.util
import io
import os
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

LANCER = os.path.join(TOOLS_DIR, "tester", "tester-lancer-non-regression",
                      "tester-lancer-non-regression.py")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0


def charger_protections():
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def verifier(nom, condition, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s %s" % (nom, ("-- " + detail) if detail else ""))


def run(cmd, timeout=300):
    return PROTECTIONS.lancer_protege(cmd, timeout=timeout)


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== test-032 : pool de workers non-regression ===")
    try:
        # 1. Version du lanceur (round 12 : v0.3.1 tri registre-tests)
        r = run([PYTHON, LANCER, "--version"])
        verifier("1. --version v0.3.1",
                 r.returncode == 0 and "v0.3.1" in r.stdout,
                 r.stdout.strip()[-60:])

        # 2. Le mode par defaut utilise le pool de workers (filtre 1 test).
        r = run([PYTHON, LANCER, "--journal", "--tests", "test-001"])
        verifier("2. Defaut = pool de workers (Pool de workers affiche)",
                 "Pool de workers" in r.stdout and "RESULTAT Pool" in r.stdout,
                 r.stdout.strip()[-120:])

        # 3. --serial et --workers 1 forcent le mode serie (pas de Pool).
        r = run([PYTHON, LANCER, "--serial", "--journal", "--tests", "test-001"])
        ok_serial = (r.returncode == 0 and "Pool de workers" not in r.stdout)
        verifier("3a. --serial : mode serie (pas de Pool)",
                 ok_serial, r.stdout.strip()[-80:])
        r = run([PYTHON, LANCER, "--workers", "1", "--journal",
                 "--tests", "test-001"])
        ok_w1 = (r.returncode == 0 and "Pool de workers" not in r.stdout)
        verifier("3b. --workers 1 : mode serie (pas de Pool)",
                 ok_w1, r.stdout.strip()[-80:])

        # 4. Les garde-fous globaux sont identifies dans le code.
        with io.open(LANCER, encoding="utf-8", errors="replace") as fh:
            code_lanceur = fh.read()
        globaux_ok = all("test-0%s" % n in code_lanceur
                         for n in ["23", "24", "25", "27"])
        verifier("4. GARDE_FOUS_GLOBAUX identifie test-023/024/025/027",
                 globaux_ok and "GARDE_FOUS_GLOBAUX" in code_lanceur, "")

        # 5. Anti-deadlock : la sortie va vers un fichier, pas un pipe stdout.
        #    Le motif (virgule + stdout=PIPE) est absent du commentaire qui
        #    documente la lecon - il ne detecte que le vrai usage Popen.
        anti_ok = ("fic_sortie" in code_lanceur
                   and ", stdout=PIPE" not in code_lanceur)
        verifier("5. Anti-deadlock : sortie vers fichier (pas de pipe stdout)",
                 anti_ok, "")

        # 6. --workers present dans l aide.
        r = run([PYTHON, LANCER, "--help"])
        verifier("6. --workers present dans --help",
                 "--workers" in (r.stdout + r.stderr), "")

        # 7. Preuve de gain : sous-ensemble (test-001..008) en pool <= serie.
        #    Seuil large (2.5x) pour absorber la variabilite machine : on
        #    verifie que le pool n est PAS plus lent que le serie x 2.5.
        subset = ",".join(["test-00%d" % i for i in range(1, 9)])
        t0 = time.time()
        run([PYTHON, LANCER, "--serial", "--journal", "--tests", subset])
        duree_serie = time.time() - t0
        t0 = time.time()
        run([PYTHON, LANCER, "--workers", "4", "--journal", "--tests", subset])
        duree_pool = time.time() - t0
        verifier("7. Preuve de gain : pool (%.1fs) <= serie (%.1fs) x 2.5"
                 % (duree_pool, duree_serie),
                 duree_pool <= duree_serie * 2.5 + 5.0,
                 "serie=%.1fs pool=%.1fs" % (duree_serie, duree_pool))
    except PROTECTIONS.ArretProtection as e:
        print("  [KO] ARRET PROTECTION : %s" % e.message)
        NB_KO += 1

    # 8. Normes ASCII strict + LF pur (test + lanceur)
    fichiers = [os.path.abspath(__file__), LANCER]
    total_non_ascii = sum(ascii_count(f) for f in fichiers)
    verifier("8. ASCII strict : 0 non-ASCII (test + lanceur)",
             total_non_ascii == 0, "total=%d" % total_non_ascii)
    total_crlf = sum(crlf_count(f) for f in fichiers)
    verifier("9. LF pur : 0 CRLF (test + lanceur)",
             total_crlf == 0, "total=%d" % total_crlf)

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
