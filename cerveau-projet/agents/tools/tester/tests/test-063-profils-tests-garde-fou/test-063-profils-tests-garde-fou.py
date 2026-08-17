#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-063-profils-tests-garde-fou.py
GARDE-FOU : le mode PROFIL du lanceur de non-regression (demande
utilisateur 2026-08-16) est en place et fiable :
  - profils-tests.json existe, est un JSON valide avec les 6 profils
    (cartes, outils, tests, fiches-agents, docs, registre),
  - chaque profil a des fichiers_detectes et une liste de tests non vide,
  - TOUS les tests reels de la suite (test-0XX) sont couverts par au
    moins un profil (aucun test orphelin : Janus ne doit jamais lancer
    une suite incomplete par oubli de mapping),
  - aucun test reference dans profils-tests.json n est inexistant
    (pas de reference morte),
  - le lanceur v0.5.0 expose les options --profil et --fichiers et
    contient les fonctions charger_profils_tests / deduire_profils /
    tests_du_profil / filtrer_tests_par_profils,
  - la deduction automatique par fichiers modifies fonctionne (un
    parcours JSON -> cartes, un test .py -> tests, README.md -> docs,
    un fichier tools/ -> outils, un fichier traces/ -> registre).

Contexte :
  - Outil : tester-lancer-non-regression v0.5.0 + profils-tests.json
    (crees par Vulcain, demande utilisateur).
  - Ce garde-fou est l anti-recurrence du bug des questions orphelines
    transpose aux tests : un test non mappe dans un profil serait
    silencieusement oublie lors d un controle cible de Janus.

Invariants verifies :
  1. profils-tests.json existe et est un JSON valide
  2. La cle version + description + profils (6) sont presentes
  3. Les 6 noms de profils sont exacts (cartes, outils, tests,
     fiches-agents, docs, registre)
  4. Chaque profil a fichiers_detectes et tests non vides
  5. Couverture : tous les tests reels test-0XX sont dans au moins un
     profil (61 attendus)
  6. Aucun test reference n est inexistant (reference morte)
  7. Le lanceur v0.5.0 expose --profil et --fichiers dans --aide
  8. Le lanceur contient les 4 fonctions du mode profil
  9. Preuve reelle de deduction : parcours JSON -> cartes ; test .py ->
     tests ; README.md -> docs ; fichier tools/ -> outils ; registre ->
     registre ; inconnu -> aucun (KO propre)
  10. Normes : ASCII strict + LF pur (profils-tests.json + lanceur +
      test)
Tags: performance, profils, garde-fou
"""
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
PYTHON = sys.executable

LANCEUR_DIR = os.path.join(TOOLS_DIR, "tester", "tester-lancer-non-regression")
LANCEUR_PY = os.path.join(LANCEUR_DIR, "tester-lancer-non-regression.py")
PROFILS_JSON = os.path.join(LANCEUR_DIR, "profils-tests.json")
TESTS_DIR = os.path.join(TOOLS_DIR, "tester", "tests")

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
    print("=== CHRONO test-063 (total %.1fs) ===" % total)
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


def lire(chemin):
    if not os.path.exists(chemin):
        return ""
    return io.open(chemin, encoding="utf-8", errors="replace").read()


def ascii_count(chemin):
    if not os.path.exists(chemin):
        return 999
    return sum(1 for c in lire(chemin) if ord(c) > 127)


def crlf_count(chemin):
    if not os.path.exists(chemin):
        return 999
    return io.open(chemin, "rb").read().count(b"\r\n")


def lister_tests_reels():
    """Liste les tests test-0XX reels (prefixe 8 car) du repertoire tests.

    Le JSON profils-tests.json stocke les PREFIXES test-0XX (meme format
    que filtrer_tests_par_profils du lanceur : basename[:8]).
    """
    resultats = []
    if not os.path.isdir(TESTS_DIR):
        return resultats
    for nom in sorted(os.listdir(TESTS_DIR)):
        if nom.startswith("test-0") and os.path.isdir(os.path.join(TESTS_DIR, nom)):
            resultats.append(nom[:8])
    return resultats


def charger_lanceur():
    """Importe le lanceur en module (sans lancer la suite)."""
    spec = importlib.util.spec_from_file_location("lanceur_nr", LANCEUR_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== GARDE-FOU test-063 : PROFILS DE TESTS ===")
    try:
        # 1. profils-tests.json existe et est un JSON valide
        if point_actif(1):
            t0 = time.monotonic()
            try:
                data = json.load(io.open(PROFILS_JSON, encoding="utf-8"))
                valide = True
            except Exception as exc:
                data = None
                valide = False
            verifier("1. profils-tests.json existe et JSON valide",
                     os.path.isfile(PROFILS_JSON) and valide,
                     "exception=%s" % ("OK" if valide else "fichier manquant"))
            chrono_etape("1. json", t0)

        # 2. Cles version + description + profils (6)
        if point_actif(2):
            t0 = time.monotonic()
            if data is not None:
                ok_version = "version" in data and data.get("version")
                ok_desc = "description" in data and data.get("description")
                profils = data.get("profils", [])
                ok_profils = isinstance(profils, list) and len(profils) == 6
                verifier("2. version + description + 6 profils presents",
                         ok_version and ok_desc and ok_profils,
                         "version=%s profils=%d" %
                         (data.get("version", "?"), len(profils)))
            else:
                verifier("2. version + description + 6 profils presents",
                         False, "json non charge")
            chrono_etape("2. cles", t0)

        # 3. Les 6 noms de profils exacts
        if point_actif(3):
            t0 = time.monotonic()
            attendus = ["cartes", "outils", "tests", "fiches-agents",
                        "docs", "registre"]
            noms = [p.get("nom") for p in data.get("profils", [])]
            verifier("3. 6 noms de profils exacts",
                     noms == attendus, "noms=%s" % noms)
            chrono_etape("3. noms", t0)

        # 4. Chaque profil a fichiers_detectes et tests non vides
        if point_actif(4):
            t0 = time.monotonic()
            defauts = []
            for p in data.get("profils", []):
                if not p.get("fichiers_detectes"):
                    defauts.append("%s:sans fichiers_detectes" % p.get("nom"))
                if not p.get("tests"):
                    defauts.append("%s:sans tests" % p.get("nom"))
            verifier("4. chaque profil a fichiers_detectes + tests",
                     not defauts, "; ".join(defauts))
            chrono_etape("4. completude", t0)

        # 5. Couverture : tous les tests reels dans au moins un profil
        if point_actif(5):
            t0 = time.monotonic()
            reels = lister_tests_reels()
            couverts = set()
            for p in data.get("profils", []):
                couverts.update(p.get("tests", []))
            manquants = [t for t in reels if t not in couverts]
            verifier("5. tous les %d tests reels couverts par un profil"
                     % len(reels), not manquants,
                     "orphelins=%s" % ", ".join(manquants))
            chrono_etape("5. couverture", t0)

        # 6. Aucun test reference inexistant
        if point_actif(6):
            t0 = time.monotonic()
            reels = set(lister_tests_reels())
            fantomes = []
            for p in data.get("profils", []):
                for t in p.get("tests", []):
                    if t not in reels:
                        fantomes.append("%s:%s" % (p.get("nom"), t))
            verifier("6. aucun test reference inexistant", not fantomes,
                     "; ".join(fantomes))
            chrono_etape("6. refs mortes", t0)

        # 7. Le lanceur expose --profil et --fichiers dans --aide
        if point_actif(7):
            t0 = time.monotonic()
            res = lancer([PYTHON, LANCEUR_PY, "--aide"], timeout=30)
            ok = "--profil" in res.stdout and "--fichiers" in res.stdout
            verifier("7. lanceur --aide expose --profil et --fichiers",
                     ok, "rc=%d" % res.returncode)
            chrono_etape("7. aide", t0)

        # 8. Les 4 fonctions du mode profil sont dans le lanceur
        if point_actif(8):
            t0 = time.monotonic()
            try:
                mod = charger_lanceur()
                fonctions = ["charger_profils_tests", "deduire_profils",
                             "tests_du_profil", "filtrer_tests_par_profils"]
                manquantes = [f for f in fonctions
                              if not hasattr(mod, f)]
                verifier("8. 4 fonctions du mode profil presentes",
                         not manquantes, "manquantes=%s" % manquantes)
            except Exception as exc:
                verifier("8. 4 fonctions du mode profil presentes",
                         False, "exception=%s" % exc)
            chrono_etape("8. fonctions", t0)

        # 9. Preuve reelle de deduction automatique par fichiers
        if point_actif(9):
            t0 = time.monotonic()
            try:
                mod = charger_lanceur()
                profils = data.get("profils", [])
                cas = [
                    ("cerveau-projet/agents/cerberus/parcours/"
                     "parcours-cerberus.json", ["cartes"]),
                    ("cerveau-projet/agents/tools/tester/tests/"
                     "test-001-evaluer-agents-coherence/"
                     "test-001-evaluer-agents-coherence.py", ["tests"]),
                    ("README.md", ["docs"]),
                    ("cerveau-projet/agents/tools/creer/creer-fichier/"
                     "creer-fichier.py", ["outils"]),
                    ("cerveau-projet/agents/traces/"
                     "registre-usages-outils.jsonl", ["registre"]),
                ]
                echecs = []
                for fichier, attendu in cas:
                    deduit = mod.deduire_profils([fichier], profils,
                                                 PROJECT_ROOT)
                    if sorted(deduit) != sorted(attendu):
                        echecs.append("%s -> %s (attendu %s)" %
                                      (fichier.split("/")[-1], deduit, attendu))
                # cas inconnu : aucun profil -> liste vide (sans erreur)
                inconnu = mod.deduire_profils(
                    ["docs/nouveau-dossier-inconnu/x.txt"], profils,
                    PROJECT_ROOT)
                verifier("9. deduction auto : 5 cas reels OK + inconnu vide",
                         not echecs and inconnu == [],
                         "; ".join(echecs) + (" inconnu=%s" % inconnu
                                              if echecs or inconnu else ""))
            except Exception as exc:
                verifier("9. deduction auto : 5 cas reels OK + inconnu vide",
                         False, "exception=%s" % exc)
            chrono_etape("9. deduction", t0)

        # 10. Normes ASCII + LF pur (json + lanceur + test)
        if point_actif(10):
            t0 = time.monotonic()
            fichiers = [PROFILS_JSON, LANCEUR_PY,
                        os.path.abspath(__file__)]
            total_na = sum(ascii_count(f) for f in fichiers)
            total_crlf = sum(crlf_count(f) for f in fichiers)
            verifier("10. ASCII strict : 0 non-ASCII (json + lanceur + test)",
                     total_na == 0, "total=%d" % total_na)
            verifier("11. LF pur : 0 CRLF (json + lanceur + test)",
                     total_crlf == 0, "total=%d" % total_crlf)
            chrono_etape("10. normes", t0)

    except PROTECTIONS.ArretProtection as e:
        print("  [KO] ARRET PROTECTION : %s" % e.message)
        NB_KO += 1

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO,
                                                               NB_POINTS))
    PROTECTIONS.afficher_rating("test-063-profils-tests-garde-fou")
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
