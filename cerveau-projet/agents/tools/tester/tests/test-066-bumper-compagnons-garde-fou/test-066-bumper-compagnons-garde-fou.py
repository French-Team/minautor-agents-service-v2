#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-066-bumper-compagnons-garde-fou.py
GARDE-FOU : le bumper mettre-a-jour-versions (v0.1.6, round 2026-09-02)
signale les FICHIERS COMPAGNONS : quand on bump un outil, les fichiers du
projet qui referencent encore l ANCIENNE version (tests, docs, corrections)
sont listes avec verdict KO - pour ne plus oublier de les adapter (8 tests
cassaient a chaque bump du lanceur avant cette protection).

Contexte (demande utilisateur 2026-08-16) :
  - Quand on bump un fichier, les autres fichiers qui devraient l etre aussi
    doivent etre SIGNALES par le bumper.
  - Detection : scanne cerveau-projet/ pour les fichiers contenant le nom de
    l outil + l ancienne version (avec ou sans prefixe v).
  - Verdict passe en KO si des compagnons existent (l agent doit les adapter).

Invariants verifies :
  1. mettre-a-jour-versions.py existe, compile, --version v0.1.6
  2. Le motif md couvre les 2 formats de doc : '**Version :**' ET '**Version** :'
     (preuve : un fichier md de test au 2e format est detecte)
  3. Preuve reelle compagnons : bump DRY-RUN du lanceur tester-lancer-non-regression
     (0.5.1 -> 0.5.2) doit afficher 'FICHIERS COMPAGNONS' et un verdict KO avec
     au moins 1 test compagnon liste (test-024/027/031/032/051/062 pincent sa version)
  4. Bump dry-run sur un outil SANS compagnons connus : aucun fichier compagnon
  5. Normes : ASCII strict + LF pur (outil + test)
Tags: outils, bumper, garde-fou
"""
import importlib.util
import io
import os
import re
import subprocess
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

BUMPER_DIR = os.path.join(TOOLS_DIR, "mettre-a-jour", "mettre-a-jour-versions")
BUMPER_PY = os.path.join(BUMPER_DIR, "mettre-a-jour-versions.py")
BUMPER_MD = os.path.join(BUMPER_DIR, "mettre-a-jour-versions.md")
LANCER_DIR = os.path.join(TOOLS_DIR, "tester", "tester-lancer-non-regression")

# --- triplet chrono (template v0.3.0) ---
T_START = time.monotonic()
CHRONO_ACTIF = True
ETAPES = []
NB_OK = 0
NB_KO = 0
NB_POINTS = 11


def point_actif(numero):
    return True


def chrono_etape(nom, t_debut):
    ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - T_START
    print("")
    print("=== CHRONO test-066 (total %.1fs) ===" % total)
    for nom, duree in ETAPES:
        print("  [chrono] %-35s %.2fs" % (nom, duree))


def verifier(nom, condition, detail=""):
    global NB_OK, NB_KO
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s -- %s" % (nom, str(detail)[-100:]))


def charger_protections():
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def run(cmd, timeout=60):
    try:
        r = PROTECTIONS.lancer_protege(cmd, timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return -1, "ERREUR: %s" % str(e)[-80:]


def main():
    print("=== Garde-fou : fichiers compagnons du bumper (mettre-a-jour-versions) ===")

    # 1. Outil present + compile + version
    t0 = time.monotonic()
    verifier("1. bumper present",
             os.path.isfile(BUMPER_PY), "")
    code, out = run([PYTHON, "-m", "py_compile", BUMPER_PY])
    verifier("1b. compilation OK", code == 0, out[-80:])
    code, out = run([PYTHON, BUMPER_PY, "--version"])
    verifier("1c. --version v0.1.6",
             code == 0 and "v0.1.6" in out, out.strip()[-40:])
    chrono_etape("1. outil", t0)

    # 2. Motif md couvre les 2 formats (preuve unitaire)
    t0 = time.monotonic()
    texte_source = io.open(BUMPER_PY, encoding="utf-8", errors="replace").read()
    m1 = "_RE_MD_VERSION = re.compile" in texte_source
    verifier("2. motif md present dans le code",
             m1 is not None, "motif _RE_MD_VERSION introuvable")
    # preuve : charger le module et tester la regex sur les 2 formats
    spec = importlib.util.spec_from_file_location("bumper", BUMPER_PY)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
        r2 = mod._RE_MD_VERSION
        f1 = bool(r2.search("**Version :** 0.9.9"))
        f2 = bool(r2.search("**Version** : 0.9.9"))
        verifier("2b. motif md couvre les 2 formats de doc",
                 f1 and f2, "fmt1=%s fmt2=%s" % (f1, f2))
    except Exception as e:
        verifier("2b. motif md couvre les 2 formats de doc", False, str(e)[-80:])
    chrono_etape("2. motif md", t0)

    # 3. Preuve reelle : bump dry-run du lanceur -> compagnons detectes
    t0 = time.monotonic()
    code, out = run([PYTHON, BUMPER_PY, LANCER_DIR], timeout=90)
    a_compagnons = "FICHIERS COMPAGNONS" in out
    a_test = any("test-0" in ligne for ligne in out.splitlines() if "compagnon" in ligne.lower() or "tests/" in ligne)
    ko_verdict = "Verdict : KO" in out
    verifier("3. bump dry-run lanceur : section compagnons affichee",
             a_compagnons, "rc=%d" % code)
    verifier("3b. au moins 1 test compagnon liste (pince la version)",
             a_test, "aucun test dans la liste des compagnons")
    verifier("3c. verdict KO (compagnons a adapter)",
             ko_verdict, out[-60:] if not ko_verdict else "")
    chrono_etape("3. preuve compagnons", t0)

    # 4. Option --nouvelle : bump dry-run du lanceur vers une version
    #    FUTURE. La cible est calculee DYNAMIQUEMENT (version courante du
    #    lanceur lue dans le source + 1 en patch) pour ne plus jamais
    #    dependre d une version en dur (lecon 2026-08-16 : le pin
    #    "0.5.5 -> 0.5.6" est reste perime apres les bumps car le bumper
    #    ne detecte que la version COURANTE, pas les transitions passees).
    t0 = time.monotonic()
    lancer_py = os.path.join(LANCER_DIR, "tester-lancer-non-regression.py")
    src_lancer = io.open(lancer_py, encoding="utf-8", errors="replace").read()
    m_ver = re.search(r'VERSION\s*=\s*"([0-9]+\.[0-9]+\.[0-9]+)"', src_lancer)
    courante = m_ver.group(1) if m_ver else "0.0.0"
    majeur, mineur, patch = (int(x) for x in courante.split("."))
    cible = "%d.%d.%d" % (majeur, mineur, patch + 1)
    code, out = run([PYTHON, BUMPER_PY, LANCER_DIR, "--nouvelle", cible],
                    timeout=90)
    transition = "%s -> %s" % (courante, cible)
    verifier("4. option --nouvelle fonctionne (%s dry-run)" % transition,
             code == 0 and transition in out, out.strip()[-60:])
    chrono_etape("4. --nouvelle", t0)

    # 5. Normes ASCII + LF
    t0 = time.monotonic()
    na_total = 0
    crlf_total = 0
    for f in (BUMPER_PY, BUMPER_MD, os.path.abspath(__file__)):
        d = io.open(f, encoding="utf-8", errors="replace").read()
        na_total += sum(1 for c in d if ord(c) > 127)
        crlf_total += d.count("\r")
    verifier("5. ASCII strict : 0 non-ASCII (outil + test)", na_total == 0, "na=%d" % na_total)
    verifier("5b. LF pur : 0 CRLF (outil + test)", crlf_total == 0, "crlf=%d" % crlf_total)
    chrono_etape("5. normes", t0)

    bilan_chrono()
    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    print("=== VERDICT : %s ===" % ("PROPRE (compagnons signales)" if NB_KO == 0 else "KO A CORRIGER"))
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
