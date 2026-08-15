#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-036-detecter-evaluations-incompletes.py
GARDE-FOU : detecter-evaluations-incompletes scan les 4 sources
(validateur, spec, generateurs, tests) et classe les mentions residuelles.

Contexte (2026-08-13, mission Themis axe A, Vulcain) :
  - Lecon Themis du 2026-08-11 : un re-audit qui ne scanne que les fichiers
    modifies RATE les mentions residuelles dans les sources voisines
    (validateur, spec, generateurs .md/spec/code, tests) - 8 mentions
    avaient ete ratees sur la convention cT*.
  - Vulcain a cree detecter-evaluations-incompletes v0.1.0 qui automatise
    la methode Themis : motif + filtre + contexte, rapport markdown.

Invariants verifies :
  1. L outil existe et compile
  2. Motif inexistant : 0 mention + rc=0 (correction complete)
  3. Motif reel (0.2.9) : >0 mentions + rc=1 (mentions restantes detectees)
  4. --version affiche la version
  5. --rapport ecrit un rapport markdown
  6. Normes : ASCII strict + LF pur (outil + test)
"""
import importlib.util
import io
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

OUTIL = os.path.join(TOOLS_DIR, "detecter",
                     "detecter-evaluations-incompletes",
                     "detecter-evaluations-incompletes.py")

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


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def lancer(extra_args):
    """Lance l outil SOUS PROTECTION et retourne (code, stdout)."""
    proc = PROTECTIONS.lancer_protege(
        [PYTHON, OUTIL] + extra_args,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=PROJECT_ROOT, timeout=120,
    )
    return proc.returncode, proc.stdout + proc.stderr


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== test-036 : detecter-evaluations-incompletes (scan anti-recurrence) ===")
    try:
        # 1. L outil existe et compile
        verifier("1. Outil present", os.path.isfile(OUTIL), OUTIL)
        rc = PROTECTIONS.lancer_protege(
            [PYTHON, "-m", "py_compile", OUTIL], cwd=PROJECT_ROOT).returncode
        verifier("1b. Compilation OK", rc == 0, "rc=%d" % rc)

        # 2. Motif inexistant : 0 mention + rc=0
        # NOTE : le motif est construit en CONCATENANT deux morceaux pour
        # qu il n apparaisse jamais litteralement dans ce fichier de test
        # (sinon le scan des tests le trouverait dans le test lui-meme :
        # auto-reference).
        motif_vide = "zzz-inexistant-" + "9f4a2c7e"
        code, out = lancer(["--motif", motif_vide])
        propre = out.strip()
        verifier("2. Motif inexistant : 0 mention (rc=0)",
                 "0 mention" in propre and code == 0,
                 "rc=%d out=%s" % (code, propre[-60:]))

        # 3. Motif reel : >0 mention + rc=1 (les mentions sont detectees)
        code, out = lancer(["--motif", "0.2.9"])
        verifier("3. Motif reel (0.2.9) : >0 mention (rc=1)",
                 code == 1 and "mentions" in out,
                 "rc=%d out=%s" % (code, out.strip()[-60:]))

        # 4. --version
        code, out = lancer(["--version"])
        verifier("4. --version affiche la version",
                 "detecter-evaluations-incompletes v" in out and code == 0,
                 "out=%s" % out.strip()[-40:])

        # 5. --rapport ecrit un rapport markdown
        rapport = os.path.join(PROJECT_ROOT, ".tmp-test-036-rapport.md")
        if os.path.isfile(rapport):
            os.remove(rapport)
        code, out = lancer(["--motif", "0.2.9", "--rapport", rapport])
        ecrit = os.path.isfile(rapport)
        contenu_ok = False
        if ecrit:
            with io.open(rapport, encoding="utf-8", errors="replace") as fh:
                contenu_ok = "Rapport" in fh.read()
            os.remove(rapport)
        verifier("5. --rapport ecrit un rapport markdown",
                 ecrit and contenu_ok, "rc=%d ecrit=%s" % (code, ecrit))
    except PROTECTIONS.ArretProtection as e:
        print("  [KO] ARRET PROTECTION : %s" % e.message)
        NB_KO += 1

    # 6. Normes ASCII strict + LF pur (outil + test)
    fichiers = [OUTIL, os.path.abspath(__file__)]
    total_non_ascii = sum(ascii_count(f) for f in fichiers)
    verifier("6. ASCII strict : 0 non-ASCII (outil + test)",
             total_non_ascii == 0, "total=%d" % total_non_ascii)
    total_crlf = sum(crlf_count(f) for f in fichiers)
    verifier("7. LF pur : 0 CRLF (outil + test)",
             total_crlf == 0, "total=%d" % total_crlf)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
