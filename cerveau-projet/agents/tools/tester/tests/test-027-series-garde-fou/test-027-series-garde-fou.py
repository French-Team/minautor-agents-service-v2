#!/usr/bin/env python3
# -*- coding: ascii -*-
# test-027-series-garde-fou.py
#
# Garde-fou du decoupage en series du lanceur de non-regression (round 10).
#
# Le lanceur tester-lancer-non-regression v0.1.2 decoupe la suite en 4 series
# thematiques (--series a|b|c|d|tous) executables en parallele (--parallele).
# Ce garde-fou verifie :
#   1. Chaque test-0XX du disque appartient a UNE serie du lanceur (couverture
#      100% : un nouveau test sans serie serait signale hors-serie a
#      l execution et ici en KO - anti-recurrence de l oubli d affectation).
#   2. Aucun test n appartient a deux series (pas de chevauchement).
#   3. test-027 lui-meme est affecte a la serie D (registre et garde-fous).
#   4. --version affiche v0.1.6.
#   5. --series z (inconnue) : code 2 + message usage, jamais de traceback.
#   6. Isolation : --series a --tests test-001 ne lance que test-001 ;
#      --series c --tests test-001 ne trouve aucun test (filtre de serie actif).
#   7. Defaut = parallele (round 10b) : sans option, --tests test-001 lance le
#      test via la structure Serie A (1 OK / 0 KO sur 1 tests) - preuve du
#      defaut parallele ET de l heritage du filtre par les sous-processus.
#   8. --serial force l ancien mode serie : --serial --tests test-001 donne la
#      structure RESULTAT : (serie) et 1 OK / 0 KO sur 1 tests.
#   9. ASCII strict : 0 non-ASCII (lanceur + doc + test).
#  10. LF pur : 0 CRLF (lanceur + doc + test).
#
# ATTENTION RECURSION : ce test ne lance JAMAIS le lanceur sans filtre
# --tests qui l inclurait lui-meme (il appartient a la serie D). Toute
# invocation du lanceur combine --series <X> et --tests <test hors serie D>.
#
# Usage:
#   python3 test-027-series-garde-fou.py
import glob
import importlib.util
import io
import os
import subprocess
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isfile(os.path.join(PROJECT_ROOT, "AGENTS.md")):
    parent = os.path.dirname(PROJECT_ROOT)
    if parent == PROJECT_ROOT:
        break
    PROJECT_ROOT = parent

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
TESTS_DIR = os.path.join(TOOLS_DIR, "tester", "tests")
LANCER = os.path.join(TOOLS_DIR, "tester", "tester-lancer-non-regression",
                      "tester-lancer-non-regression.py")
LANCER_DOC = os.path.join(TOOLS_DIR, "tester", "tester-lancer-non-regression",
                          "tester-lancer-non-regression.md")

PYTHON = sys.executable

def charger_protections():
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

PROTECTIONS = charger_protections()

MOI = os.path.basename(__file__)

NB_POINTS = 0
NB_OK = 0
NB_KO = 0


def verifier(nom, condition, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s %s" % (nom, ("-- " + detail) if detail else ""))


def run(cmd, timeout=120):
    proc = PROTECTIONS.lancer_protege(cmd, capture_output=True, text=True, timeout=timeout)
    return proc


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with io.open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def charger_series():
    """Charge les constantes SERIES du lanceur par import (aucun effet de bord)."""
    spec = importlib.util.spec_from_file_location("lanceur_nonreg", LANCER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.SERIES, mod.SERIES_ORDRE


def lister_tests():
    """Tous les tests test-0XX du disque (fichiers .py)."""
    return sorted(glob.glob(os.path.join(TESTS_DIR, "test-0*", "test-0*.py")))


def main():
    series, ordre = charger_series()

    # 1. Couverture : chaque test du disque appartient a une serie.
    tests = [os.path.basename(t) for t in lister_tests()]
    absents = []
    for nom in tests:
        if not any(any(nom.startswith(p) for p in series[s]) for s in ordre):
            absents.append(nom)
    verifier("1. Couverture : chaque test-0XX appartient a une serie",
             len(absents) == 0, "hors-serie : %s" % ", ".join(absents[:5]))

    # 2. Pas de chevauchement entre series.
    vu = {}
    doublons = []
    for s in ordre:
        for p in series[s]:
            if p in vu:
                doublons.append("%s (serie %s et %s)" % (p, vu[p], s))
            vu[p] = s
    verifier("2. Aucun test dans deux series",
             len(doublons) == 0, ", ".join(doublons[:5]))

    # 3. test-027 affecte a la serie D.
    verifier("3. test-027 affecte a la serie D",
             any(MOI.startswith(p) for p in series["d"]),
             "serie D = %s" % series["d"])

    # 4. Version du lanceur.
    r = run([PYTHON, LANCER, "--version"])
    verifier("4. --version v0.3.1",
             r.returncode == 0 and "v0.3.1" in r.stdout, r.stdout.strip()[-60:])

    # 5. Serie inconnue : code 2 + message usage, sans traceback.
    # (argparse ecrit le message usage sur stderr, pas sur stdout)
    r = run([PYTHON, LANCER, "--series", "z"])
    sortie = r.stdout + r.stderr
    sans_traceback = "Traceback" not in sortie
    verifier("5. --series z : code 2 + usage sans traceback",
             r.returncode == 2 and "usage:" in sortie and sans_traceback,
             "rc=%d" % r.returncode)

    # 6a. Isolation : --series a --tests test-001 ne lance que test-001.
    r = run([PYTHON, LANCER, "--series", "a", "--journal",
             "--tests", "test-001-evaluer-agents-coherence"])
    ok6a = (r.returncode == 0 and "RESULTAT Serie A" in r.stdout
            and "1 OK / 0 KO (sur 1 tests, 0 non lances)" in r.stdout)
    verifier("6a. --series a --tests test-001 : 1 seul test lance",
             ok6a, r.stdout.strip()[-80:])

    # 6b. Isolation : --series c filtre test-001 (aucun test trouve).
    r = run([PYTHON, LANCER, "--series", "c", "--journal",
             "--tests", "test-001-evaluer-agents-coherence"])
    ok6b = (r.returncode == 2 and "Aucun test trouve" in r.stdout)
    verifier("6b. --series c exclut test-001 (aucun test trouve)",
             ok6b, "rc=%d %s" % (r.returncode, r.stdout.strip()[-60:]))

    # 7. Defaut = pool de workers (round 12) : sans option, le filtre --tests
    #    est herite et le test passe par la structure Pool.
    r = run([PYTHON, LANCER, "--journal", "--tests", "test-001-evaluer-agents-coherence"])
    ok7 = (r.returncode == 0 and "Pool de workers" in r.stdout
           and "RESULTAT Pool" in r.stdout
           and "1 OK / 0 KO (sur 1 tests, 0 non lances)" in r.stdout)
    verifier("7. Defaut = pool de workers (structure Pool + filtre herite)",
             ok7, r.stdout.strip()[-80:])

    # 8. --serial force l ancien mode serie.
    r = run([PYTHON, LANCER, "--serial", "--journal", "--tests", "test-001-evaluer-agents-coherence"])
    ok8 = (r.returncode == 0 and "RESULTAT : 1 OK / 0 KO (sur 1 tests, 0 non lances)" in r.stdout
           and "RESULTAT Serie" not in r.stdout
           and "Pool de workers" not in r.stdout)
    verifier("8. --serial force le mode serie",
             ok8, r.stdout.strip()[-80:])

    # 9. ASCII strict.
    ko_ascii = 0
    for f in [LANCER, LANCER_DOC, os.path.abspath(__file__)]:
        ko_ascii += ascii_count(f)
    verifier("9. ASCII strict : 0 non-ASCII (lanceur + doc + test)",
             ko_ascii == 0, "nb=%d" % ko_ascii)

    # 10. LF pur.
    ko_crlf = 0
    for f in [LANCER, LANCER_DOC, os.path.abspath(__file__)]:
        ko_crlf += crlf_count(f)
    verifier("10. LF pur : 0 CRLF (lanceur + doc + test)",
             ko_crlf == 0, "nb=%d" % ko_crlf)

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
