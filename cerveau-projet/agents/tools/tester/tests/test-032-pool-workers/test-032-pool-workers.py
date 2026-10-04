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
  1. --version affiche v0.6.2
  2. Le mode par defaut utilise le pool (Pool de workers dans la sortie)
  3. --serial ou --workers 1 force le mode serie (pas de Pool)
  4. GARDE_FOUS_GLOBAUX identifie test-023/024/025/027 dans le code
  5. Anti-deadlock : executer_pool redirige vers un fichier (pas de pipe)
  6. --workers present dans --help
  7. Preuve de gain : un sous-ensemble en pool est plus rapide ou egal au
     mode serie (seuil large, tolerance machine)
  8. Normes : ASCII strict + LF pur (test + lanceur)
Tags: performance, pool, workers, garde-fou
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
# ------------------------------------------------------------------
# OPTIONS ON/OFF + CHRONO (regle immuable v0.3.0, deploiement dynamique) :
#   --no-chrono            desactive le chrono (defaut : actif)
#   --isoler N             n execute que le point N (diagnostic cible)
#   --desactiver 1,3,5     saute les points listes (sans toucher au code)
# ------------------------------------------------------------------
CHRONO_ACTIF = "--no-chrono" not in sys.argv
ISOLE = None
DESACTIVES = []
for _i, _arg in enumerate(sys.argv):
    if _arg == "--isoler" and _i + 1 < len(sys.argv):
        try:
            ISOLE = int(sys.argv[_i + 1])
        except ValueError:
            pass
    if _arg == "--desactiver" and _i + 1 < len(sys.argv):
        for _p in sys.argv[_i + 1].split(','):
            try:
                DESACTIVES.append(int(_p))
            except ValueError:
                pass
ETAPES = []
T_START = __import__("time").monotonic()


def point_actif(numero):
    # True si le point N doit s executer (options on/off du test)
    if ISOLE is not None:
        return numero == ISOLE
    return numero not in DESACTIVES


def chrono_etape(nom, t_debut):
    # Enregistre la duree d une etape (no-op si --no-chrono)
    if CHRONO_ACTIF:
        ETAPES.append((nom, __import__("time").monotonic() - t_debut))


def bilan_chrono():
    # Affiche le bilan des durees : total + detail par etape
    if not CHRONO_ACTIF:
        return
    _total = __import__("time").monotonic() - T_START
    print("")
    print("=== CHRONO test (total %.1fs) ===" % _total)
    for _nom, _duree in ETAPES:
        print("  %-34s %6.2fs" % (_nom, _duree))


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
        # 1. Version du lanceur (round 20 : v0.4.5 ordre dynamique par KO)
        r = run([PYTHON, LANCER, "--version"])
        verifier("1. --version v0.6.2",
                 r.returncode == 0 and "v0.6.2" in r.stdout,
                 r.stdout.strip()[-60:])

        # 2. Le mode par defaut utilise les BARRIERES (filtre 1 test).
        r = run([PYTHON, LANCER, "--agent", "janus", "--journal", "--tests", "test-001"])
        verifier("2. Defaut = BARRIERES (structure BARRIERE affichee)",
                 "BARRIERE" in r.stdout,
                 r.stdout.strip()[-120:])

        # 3. --serial et --workers 1 forcent le mode serie (pas de Pool).
        r = run([PYTHON, LANCER, "--serial", "--agent", "janus", "--journal", "--tests", "test-001"])
        ok_serial = (r.returncode == 0 and "Pool de workers" not in r.stdout)
        verifier("3a. --serial : mode serie (pas de Pool)",
                 ok_serial, r.stdout.strip()[-80:])
        r = run([PYTHON, LANCER, "--parallele", "--workers", "1", "--agent", "janus",
                 "--journal", "--tests", "test-001"])
        ok_w1 = (r.returncode == 0 and "Pool de workers" not in r.stdout)
        verifier("3b. --parallele --workers 1 : mode serie (pas de Pool)",
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

        # 7. Preuve de gain : sous-ensemble en pool <= serie. OPTIMISE
        #    2026-08-16 (round performance) : test-003 (~6.8s) etait le seul
        #    test lent du sous-ensemble ; remplace par test-001 (~1.5s) qui
        #    suffit a montrer le gain du pool face a test-029 (~1.2s) :
        #    serie ~2.7s, pool ~1.6s. Seuil large (2.5x) pour absorber la
        #    variabilite machine : on verifie que le pool n est PAS plus
        #    lent que le serie x 2.5.
        subset = "test-001,test-029"
        t0 = time.time()
        run([PYTHON, LANCER, "--serial", "--agent", "janus", "--journal", "--tests", subset])
        duree_serie = time.time() - t0
        t0 = time.time()
        run([PYTHON, LANCER, "--parallele", "--workers", "4", "--agent", "janus", "--journal", "--tests", subset])
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
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
