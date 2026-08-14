#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-044-triplet-template.py
GARDE-FOU : le template-test.md v0.3.0 doit imposer le TRIPLET
(protections + options on/off + chrono) aux futurs tests.

Contexte (demande utilisateur 2026-08-13) :
  - Le template-test.md est passe en v0.3.0 (regle immuable triplet,
    mission Buffy) : canevas avec point_actif/chrono_etape/bilan_chrono,
    options --no-chrono/--isoler/--desactiver, DEBUT_TEST/ETAPES.
  - Le test-029 verifie les invariants vitaux de CHAQUE test existant ;
    ce test protege la REFERENCE AMONT : si un futur template perdait un
    element du triplet, il serait signale ici.
  - Ce test est le PREMIER conforme au template v0.3.0 : il embarque le
    triplet (import time, options on/off, chrono par etape).

Invariants verifies (sur le TEMPLATE, pas sur les tests existants) :
  1. Version 0.3.0 (header + frontmatter)
  2. Canevas : fonctions point_actif / chrono_etape / bilan_chrono
  3. Constantes : CHRONO_ACTIF, ISOLE, DESACTIVES, DEBUT_TEST, ETAPES
  4. Options documentees : --no-chrono, --isoler, --desactiver
  5. Usage reel dans le canevas (appels dans main)
  6. Structure OBLIGATOIRE + checklist mentionnent le triplet
  7. Coherence aval : protocole-tests v0.3.2 (avec PREUVE NEGATIVE) + protocole-outils Regle 9
  8. Normes : ASCII strict + LF pur (template + test)
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

TEMPLATE = os.path.join(TOOLS_DIR, "tester", "template-test.md")
PROTO_TESTS = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                           "regles-immuables", "general", "protocole-tests",
                           "protocole-tests.001.01.ebauche.md")
PROTO_OUTILS = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                            "regles-immuables", "general", "protocole-outils",
                            "protocole-outils.001.01.ebauche.md")

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
            ISOLE = None
    if arg == "--desactiver" and i + 1 < len(sys.argv):
        DESACTIVES = [int(x) for x in sys.argv[i + 1].split(",")
                      if x.strip().isdigit()]

DEBUT_TEST = time.monotonic()
ETAPES = []  # (nom, duree_secondes) alimente le bilan chrono


def charger_protections():
    """Importe le point d entree unique des protections (test-030 le verifie)."""
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def point_actif(numero):
    """True si le point N doit s executer (options on/off du test)."""
    if ISOLE is not None:
        return numero == ISOLE
    return numero not in DESACTIVES


def chrono_etape(nom, t_debut):
    """Enregistre la duree d une etape (no-op si --no-chrono)."""
    if CHRONO_ACTIF:
        ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    """Affiche le bilan des durees : total + detail par etape."""
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - DEBUT_TEST
    detail = " | ".join("%s=%.2fs" % e for e in ETAPES)
    print("=== CHRONO : total %.2fs (%s) ===" % (total, detail))


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
    return PROTECTIONS.lancer_protege(cmd, timeout=timeout)


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== test-044 : triplet impose par le template-test v0.3.0 ===")
    try:
        if not os.path.isfile(TEMPLATE):
            PROTECTIONS.verifier_critique(
                "1. Le template-test.md existe (STOP si absent)",
                False, TEMPLATE)

        with io.open(TEMPLATE, encoding="utf-8", errors="replace") as fh:
            contenu = fh.read()

        # 1. Version du template
        if point_actif(1):
            t = time.monotonic()
            verifier("1. template-test.md en v0.3.0 (header + frontmatter)",
                     "Version : 0.3.0" in contenu and '"0.3.0"' in contenu)
            chrono_etape("1. version", t)

        # 2. Les 3 fonctions du triplet dans le canevas
        if point_actif(2):
            t = time.monotonic()
            verifier("2. Canevas : point_actif + chrono_etape + bilan_chrono",
                     "def point_actif(" in contenu
                     and "def chrono_etape(" in contenu
                     and "def bilan_chrono(" in contenu)
            chrono_etape("2. triplet", t)

        # 3. Constantes du chrono et des options
        if point_actif(3):
            t = time.monotonic()
            verifier("3. Constantes CHRONO_ACTIF + ISOLE + DESACTIVES",
                     "CHRONO_ACTIF" in contenu and "ISOLE" in contenu
                     and "DESACTIVES" in contenu)
            verifier("4. Constantes DEBUT_TEST + ETAPES",
                     "DEBUT_TEST = time.monotonic()" in contenu
                     and "ETAPES = []" in contenu)
            chrono_etape("3. constantes", t)

        # 4. Options documentees
        if point_actif(5):
            t = time.monotonic()
            verifier("5. Options documentees : --no-chrono/--isoler/--desactiver",
                     "--no-chrono" in contenu and "--isoler" in contenu
                     and "--desactiver" in contenu)
            chrono_etape("4. options", t)

        # 5. Usage reel dans le canevas (appels dans main)
        if point_actif(6):
            t = time.monotonic()
            verifier("6. Canevas : chaque point demarre par if point_actif(",
                     "if point_actif(" in contenu)
            verifier("7. Canevas : appels chrono_etape(\"...\", t)",
                     'chrono_etape("' in contenu)
            idx_bilan = contenu.find("bilan_chrono()")
            idx_resultat = contenu.find("RESULTAT")
            verifier("8. Canevas : bilan_chrono() appele avant RESULTAT",
                     idx_bilan != -1 and idx_resultat != -1
                     and idx_bilan < idx_resultat,
                     "bilan=%d resultat=%d" % (idx_bilan, idx_resultat))
            chrono_etape("5. usage", t)

        # 6. Structure OBLIGATOIRE + checklist
        if point_actif(9):
            t = time.monotonic()
            verifier("9. Structure OBLIGATOIRE : section Options on/off du test",
                     "## Options on/off du test" in contenu)
            verifier("10. Checklist : triplet (options on/off + chrono v0.3.0)",
                     "Options on/off + chrono (v0.3.0)" in contenu
                     and "point_actif" in contenu)
            chrono_etape("6. structure", t)

        # 7. Coherence aval (protocoles)
        with io.open(PROTO_TESTS, encoding="utf-8", errors="replace") as fh:
            proto_tests = fh.read()
        with io.open(PROTO_OUTILS, encoding="utf-8", errors="replace") as fh:
            proto_outils = fh.read()
        if point_actif(11):
            t = time.monotonic()
            verifier("11. protocole-tests v0.3.2 + REGLE triplet + preuve negative",
                     'version: "0.3.2"' in proto_tests
                     and "PROTECTIONS + OPTIONS ON/OFF + CHRONO" in proto_tests
                     and "PREUVE NEGATIVE" in proto_tests)
            verifier("12. protocole-outils : Regle 9 (IMMUABLE)",
                     "### Regle 9 -- Protections + Options on/off + Chrono (IMMUABLE)"
                     in proto_outils)
            verifier("12b. protocole-outils : Regle 10 string.Template (IMMUABLE)",
                     "### Regle 10 -- Choix de primitive de template" in proto_outils
                     and "string.Template" in proto_outils)
            chrono_etape("7. protocoles", t)

        # 8. Normes (ASCII strict + LF pur) sur le template et ce test
        if point_actif(13):
            t = time.monotonic()
            fichiers = [TEMPLATE, os.path.abspath(__file__)]
            total_non_ascii = sum(ascii_count(f) for f in fichiers)
            verifier("13. ASCII strict : 0 non-ASCII (template + test)",
                     total_non_ascii == 0, "total=%d" % total_non_ascii)
            total_crlf = sum(crlf_count(f) for f in fichiers)
            verifier("14. LF pur : 0 CRLF (template + test)",
                     total_crlf == 0, "total=%d" % total_crlf)
            chrono_etape("8. normes", t)
    except PROTECTIONS.ArretProtection as e:
        print("  [KO] ARRET PROTECTION : %s" % e.message)
        NB_KO += 1

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
