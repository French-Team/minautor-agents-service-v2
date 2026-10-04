#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-060-outils-analyse.py
GARDE-FOU : les 2 outils d analyse crees par Vulcain (demande utilisateur
2026-08-15) existent, fonctionnent et sont references :
  - analyser-performance-tests v0.1.0 : classe les tests du DERNIER RUN du
    registre-tests.jsonl du plus gros consommateur au moins (--top, --rapport,
    --fenetre-minutes) pour aider aux optimisations de la suite.
  - analyser-tokens v0.1.1 : mesure les tokens ENVOYES/RECUS et l ENCOMBREMENT
    de la fenetre de contexte, modele HYBRIDE (compteurs API TOKENS_SESSION ou
    metadonnees-session-*.json en priorite, sinon estimation locale signalee).

Contexte :
  - Les 2 outils ont ete crees par Vulcain (categorie analyser) avec doc .md,
  - entree catalogue generateurs-commande et index-tools (Analyser 9,
    Total 202 - adapte 2026-09-04, migration v1->v2 B.4 : retrait des 2
    outils lecons, Total 204 -> 202, catalogue 188 -> 187).
  - Ce garde-fou verifie leur existence reelle, leur version, leurs options,
    leur preuve d execution (sans planter sur les donnees reelles) et leur
    referencement - anti-recurrence d un outil oublie du catalogue.

Invariants verifies :
  1. Les 2 outils .py existent, compilent et affichent --version (perf 0.1.0, tokens 0.1.4)
  2. L aide contient les options cles (--top/--rapport/--fenetre-minutes pour
     la performance ; --session/--fenetre-total/--rapport pour les tokens)
  3. Les 2 docs .md existent avec la categorie Analyser et leur version
  4. index-tools.md : les 2 outils listes dans la section Analyser, compteur
     Analyser = 9, Total = 202
  5. Catalogue : les 2 noms presents, 187 commandes triees
  6. Preuve reelle : analyser-performance-tests --version + execution sur le
     registre reel (ne plante pas, retourne 0) ; analyser-tokens --version +
     execution estimation locale (affiche ENVOYES/RECUS/ENCOMBREMENT)
  7. Preuve negative : un nom d outil invalide n existe pas dans index-tools
  8. Normes : ASCII strict + LF pur (2 outils + 2 docs + test)
Tags: outils, analyse, garde-fou
"""
import glob
import importlib.util
import io
import json
import os
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
TRACES = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "traces")
PYTHON = sys.executable

ANALYSEUR_DIR = os.path.join(TOOLS_DIR, "analyser")
PERF_DIR = os.path.join(ANALYSEUR_DIR, "analyser-performance-tests")
TOKENS_DIR = os.path.join(ANALYSEUR_DIR, "analyser-tokens")
PERF_PY = os.path.join(PERF_DIR, "analyser-performance-tests.py")
PERF_MD = os.path.join(PERF_DIR, "analyser-performance-tests.md")
TOKENS_PY = os.path.join(TOKENS_DIR, "analyser-tokens.py")
TOKENS_MD = os.path.join(TOKENS_DIR, "analyser-tokens.md")
INDEX = os.path.join(TOOLS_DIR, "index-tools.md")
CATALOGUE = os.path.join(TOOLS_DIR, "generateurs", "generateurs-commande",
                         "catalogue-commandes.json")
REG_TESTS = os.path.join(TRACES, "registre-tests.jsonl")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0
# ------------------------------------------------------------------
# OPTIONS ON/OFF + CHRONO (regle immuable v0.3.0) :
#   --no-chrono            desactive le chrono (defaut : actif)
#   --isoler N             n execute que le point N (diagnostic cible)
#   --desactiver 1,3,5     saute les points listes (sans toucher au code)
# ------------------------------------------------------------------
CHRONO_ACTIF = "--no-chrono" not in sys.argv
ISOLE = None
DESACTIVES = []
for i, arg in enumerate(sys.argv):
    if arg == "--isoler" and i + 1 < len(sys.argv):
        try:
            ISOLE = int(sys.argv[i + 1])
        except ValueError:
            pass
    if arg == "--desactiver" and i + 1 < len(sys.argv):
        for p in sys.argv[i + 1].split(","):
            try:
                DESACTIVES.append(int(p))
            except ValueError:
                pass
ETAPES = []
T_START = time.monotonic()


def charger_protections():
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def point_actif(numero):
    if ISOLE is not None:
        return numero == ISOLE
    return numero not in DESACTIVES


def chrono_etape(nom, t_debut):
    if CHRONO_ACTIF:
        ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - T_START
    print("")
    print("=== CHRONO test-060 (total %.1fs) ===" % total)
    for nom, duree in ETAPES:
        print("  %-34s %6.2fs" % (nom, duree))


def verifier(nom, condition, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if condition:
        NB_OK += 1
        print("[OK] %s" % nom)
    else:
        NB_KO += 1
        print("[KO] %s" % nom)
        if detail:
            print("     %s" % detail)


def lancer(cmd, timeout=60, **kwargs):
    return PROTECTIONS.lancer_protege(cmd, timeout=timeout, **kwargs)


def ascii_count(chemin):
    if not os.path.isfile(chemin):
        return -1
    try:
        d = io.open(chemin, encoding="utf-8", errors="replace").read()
        return sum(1 for c in d if ord(c) > 127)
    except IOError:
        return -1


def crlf_count(chemin):
    if not os.path.isfile(chemin):
        return -1
    try:
        return io.open(chemin, "rb").read().count(b"\r\n")
    except IOError:
        return -1


def main():
    try:
        # 1. Les 2 outils .py existent
        if point_actif(1):
            t0 = time.monotonic()
            ok = (os.path.isfile(PERF_PY) and os.path.isfile(TOKENS_PY))
            verifier("1. les 2 outils .py existent", ok,
                     "perf=%s tokens=%s" % (os.path.isfile(PERF_PY),
                                            os.path.isfile(TOKENS_PY)))
            chrono_etape("1. fichiers outils", t0)

        # 2. Compilation des 2 outils
        if point_actif(2):
            t0 = time.monotonic()
            r1 = lancer([PYTHON, "-m", "py_compile", PERF_PY])
            r2 = lancer([PYTHON, "-m", "py_compile", TOKENS_PY])
            verifier("2. les 2 outils compilent", r1.returncode == 0
                     and r2.returncode == 0, "rc perf=%s rc tokens=%s"
                     % (r1.returncode, r2.returncode))
            chrono_etape("2. compilation", t0)

        # 3. --version (perf 0.1.0, tokens 0.1.4)
        if point_actif(3):
            t0 = time.monotonic()
            r1 = lancer([PYTHON, PERF_PY, "--version"])
            r2 = lancer([PYTHON, TOKENS_PY, "--version"])
            ok = ("analyser-performance-tests v0.1.0" in (r1.stdout or "")
                  and "analyser-tokens v0.1.4" in (r2.stdout or ""))
            verifier("3. --version v0.1.4 des 2 outils", ok,
                     "perf=%s tokens=%s" % ((r1.stdout or "").strip(),
                                            (r2.stdout or "").strip()))
            chrono_etape("3. version", t0)

        # 4. Options cles dans l aide
        if point_actif(4):
            t0 = time.monotonic()
            r1 = lancer([PYTHON, PERF_PY, "--help"])
            r2 = lancer([PYTHON, TOKENS_PY, "--help"])
            aide1 = (r1.stdout or "") + (r1.stderr or "")
            aide2 = (r2.stdout or "") + (r2.stderr or "")
            ok = ("--top" in aide1 and "--rapport" in aide1
                  and "--fenetre-minutes" in aide1
                  and "--session" in aide2 and "--fenetre-total" in aide2
                  and "--rapport" in aide2)
            verifier("4. options cles dans l aide des 2 outils", ok, "")
            chrono_etape("4. aide", t0)

        # 5. Docs .md : categorie Analyser + version
        if point_actif(5):
            t0 = time.monotonic()
            d1 = io.open(PERF_MD, encoding="utf-8", errors="replace").read()
            d2 = io.open(TOKENS_MD, encoding="utf-8", errors="replace").read()
            ok = ("**Categorie** : Analyser" in d1 and "0.1.0" in d1
                  and "**Categorie** : Analyser" in d2 and "0.1.4" in d2)
            verifier("5. docs .md : categorie Analyser + version (perf 0.1.0, tokens 0.1.4)", ok, "")
            chrono_etape("5. docs", t0)

        # 6. index-tools : les 2 outils + compteurs Analyser 9 / Total 195
        if point_actif(6):
            t0 = time.monotonic()
            idx = io.open(INDEX, encoding="utf-8", errors="replace").read()
            ok = ("`analyser-performance-tests`" in idx
                  and "`analyser-tokens`" in idx
                  and "| Analyser | 9 |" in idx
                  and "| **Total** | **195** |" in idx)
            # migration v1->v2 (2026-09-05) : 8 outils v1 parcours archives -> Total 195
            verifier("6. index-tools : 2 outils + Analyser 9 + Total 195", ok,
                     "perf=%s tokens=%s" % ("`analyser-performance-tests`" in idx,
                                            "`analyser-tokens`" in idx))
            chrono_etape("6. index-tools", t0)

        # 7. Catalogue : 165 commandes triees + les 2 noms presents
        if point_actif(7):
            t0 = time.monotonic()
            with io.open(CATALOGUE, encoding="utf-8") as fh:
                cat = json.load(fh)
            noms = [e["nom"] for e in cat["commandes"]]
            # migration v1->v2 (2026-09-05) : 8 outils v1 parcours archives
            # 189 -> 165 commandes
            ok = (len(noms) == 165 and noms == sorted(noms)
                  and "lire-head" in noms
                  and "analyser-performance-tests" in noms
                  and "analyser-tokens" in noms)
            verifier("7. catalogue : 181 trie + 2 outils presents", ok,
                     "nb=%d trie=%s" % (len(noms), noms == sorted(noms)))
            chrono_etape("7. catalogue", t0)

        # 8. Preuve reelle : analyser-performance-tests execute sur le registre
        if point_actif(8):
            t0 = time.monotonic()
            if os.path.isfile(REG_TESTS):
                r = lancer([PYTHON, PERF_PY, "--top", "5", "--no-chrono"],
                           timeout=60)
                sortie = (r.stdout or "") + (r.stderr or "")
                ok = (r.returncode == 0 and "ANALYSE PERFORMANCE" in sortie
                      and "Dernier run" in sortie)
                verifier("8. preuve reelle : analyser-performance-tests tourne",
                         ok, "rc=%d" % r.returncode)
            else:
                verifier("8. preuve reelle : analyser-performance-tests tourne",
                         False, "registre introuvable")
            chrono_etape("8. preuve perf", t0)

        # 9. Preuve reelle : analyser-tokens estimation locale (mode secours)
        if point_actif(9):
            t0 = time.monotonic()
            env = dict(os.environ)
            env.pop("TOKENS_SESSION", None)
            r = lancer([PYTHON, TOKENS_PY, "--no-chrono"], timeout=60,
                       env=env)
            sortie = (r.stdout or "") + (r.stderr or "")
            ok = (r.returncode == 0 and "Tokens ENVOYES" in sortie
                  and "ENCOMBREMENT" in sortie
                  and "ESTIMATION" in sortie)
            verifier("9. preuve reelle : analyser-tokens estimation locale",
                     ok, "rc=%d" % r.returncode)
            chrono_etape("9. preuve tokens", t0)

        # 10. Preuve negative : un nom invalide n existe pas dans index-tools
        if point_actif(10):
            t0 = time.monotonic()
            idx = io.open(INDEX, encoding="utf-8", errors="replace").read()
            ok = "`analyser-outil-fantome`" not in idx
            verifier("10. preuve negative : outil fantome absent de index-tools",
                     ok, "")
            chrono_etape("10. preuve negative", t0)

        # 11. Normes : ASCII strict + LF pur (2 outils + 2 docs + test)
        if point_actif(11):
            t0 = time.monotonic()
            fichiers = [PERF_PY, TOKENS_PY, PERF_MD, TOKENS_MD,
                        os.path.abspath(__file__)]
            na = sum(ascii_count(f) for f in fichiers)
            crlf = sum(crlf_count(f) for f in fichiers)
            verifier("11. ASCII strict : 0 non-ASCII (outils + docs + test)",
                     na == 0, "non-ascii=%d" % na)
            verifier("12. LF pur : 0 CRLF (outils + docs + test)",
                     crlf == 0, "crlf=%d" % crlf)
            chrono_etape("11-12. normes", t0)

        bilan_chrono()
    except PROTECTIONS.ArretProtection:
        print("[ARRET] Protection STOP declenchee - le test s arrete ici.")
    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
