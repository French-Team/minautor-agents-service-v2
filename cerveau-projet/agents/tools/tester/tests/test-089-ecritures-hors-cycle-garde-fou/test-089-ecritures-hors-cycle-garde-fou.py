#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-089-ecritures-hors-cycle-garde-fou.py
GARDE-FOU : l outil detecter-ecritures-hors-cycle detecte les ecritures de
fichiers de travail qui echappent au cycle d activation (Cerberus -> agent
-> Cerberus), avec git en primaire et mtime en secours.

Contexte :
  - Derive signalee : l IA a travaille en solo (sans activer d agent) et a
    ecrit des fichiers directement. AGENTS.md / AGENTS-historique.md se
    figeaient alors que le travail continuait.
  - Vulcain a cree detecter-ecritures-hors-cycle v0.1.0 : git status en
    primaire + mtime en secours, verdict KO si Cerberus actif + fichiers de
    travail modifies, ATTENTION (code 0) si un agent de travail est actif.
  - Anti-recurrence : ce garde-fou verifie que l outil detecte une ecriture
    injectee (preuve negative) et distingue bien Cerberus (KO) d un agent de
    travail (ATTENTION).

Invariants verifies :
  1. L outil existe et compile.
  2. --version = v0.1.2.
  3. --aide fonctionne (code 0, sans traceback).
  4. Preuve negative : une ecriture injectee + --agent cerberus -> KO (code 1)
     et le fichier injecte est liste.
  5. Agent de travail : --agent vulcain -> code 0 (ATTENTION, pas KO).
  6. --rapport ecrit un fichier markdown contenant le verdict.
  7. Nettoyage : la preuve injectee est supprimee (0 trace).
  8. Normes : ASCII strict + LF pur (outil + doc + test).
Tags: securite, anti-contournement, anti-recurrence, garde-fou
"""
import importlib.util
import io
import os
import py_compile
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

OUTIL_DIR = os.path.join(TOOLS_DIR, "detecter", "detecter-ecritures-hors-cycle")
OUTIL_PY = os.path.join(OUTIL_DIR, "detecter-ecritures-hors-cycle.py")
OUTIL_MD = os.path.join(OUTIL_DIR, "detecter-ecritures-hors-cycle.md")

# Preuve injectee : fichier de travail dans le dossier du test (jamais exclu).
SENTINELLE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "preuve-ecriture-hors-cycle.txt")
RAPPORT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "rapport-test089.md")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0

# ------------------------------------------------------------------
# OPTIONS ON/OFF + CHRONO (regle immuable v0.3.0) :
#   --no-chrono            desactive le chrono (defaut : actif)
#   --isoler N             n execute que le point N
#   --desactiver 1,3,5     saute les points listes
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
    print("=== CHRONO test-089 (total %.1fs) ===" % total)
    for nom, duree in ETAPES:
        print("  %-38s %6.2fs" % (nom, duree))


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


def lancer(cmd, timeout=90, **kwargs):
    return PROTECTIONS.lancer_protege(cmd, timeout=timeout, **kwargs)


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with io.open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== Garde-fou : detecter-ecritures-hors-cycle ===")
    try:
        # 1. L outil existe et compile.
        if point_actif(1):
            t = time.monotonic()
            existe = os.path.isfile(OUTIL_PY)
            compile_ok = True
            if existe:
                try:
                    py_compile.compile(OUTIL_PY, doraise=True)
                except Exception:
                    compile_ok = False
            verifier("1. outil present + compile",
                     existe and compile_ok, "existe=%s" % existe)
            chrono_etape("1. outil + compile", t)

        # 2. Version.
        if point_actif(2):
            t = time.monotonic()
            r = lancer([PYTHON, OUTIL_PY, "--version"])
            verifier("2. --version v0.1.2",
                     r.returncode == 0 and "v0.1.2" in r.stdout,
                     r.stdout.strip())
            chrono_etape("2. version", t)

        # 3. Aide.
        if point_actif(3):
            t = time.monotonic()
            r = lancer([PYTHON, OUTIL_PY, "--aide"])
            verifier("3. --aide code 0 sans traceback",
                     r.returncode == 0
                     and "Traceback" not in (r.stdout + r.stderr),
                     "rc=%s" % r.returncode)
            chrono_etape("3. aide", t)

        # 4. Preuve negative : ecriture injectee + Cerberus -> KO code 1.
        if point_actif(4):
            t = time.monotonic()
            with io.open(SENTINELLE, "w", encoding="utf-8", newline="\n") as fh:
                fh.write("preuve ecriture hors cycle\n")
            r = lancer([PYTHON, OUTIL_PY, "--agent", "cerberus"])
            detecte = (r.returncode == 1
                       and "preuve-ecriture-hors-cycle.txt" in r.stdout)
            verifier("4. preuve negative : ecriture DETECTEE (KO code 1)",
                     detecte, "rc=%s" % r.returncode)
            chrono_etape("4. preuve negative", t)

        # 5. Agent de travail : code 0 (ATTENTION, pas KO).
        if point_actif(5):
            t = time.monotonic()
            r = lancer([PYTHON, OUTIL_PY, "--agent", "vulcain"])
            verifier("5. agent de travail : code 0 (ATTENTION, pas KO)",
                     r.returncode == 0, "rc=%s" % r.returncode)
            chrono_etape("5. agent travail", t)

        # 6. --rapport ecrit un markdown avec le verdict.
        if point_actif(6):
            t = time.monotonic()
            r = lancer([PYTHON, OUTIL_PY, "--agent", "vulcain",
                        "--rapport", RAPPORT])
            contenu = ""
            try:
                contenu = io.open(RAPPORT, encoding="utf-8",
                                  errors="replace").read()
            except (IOError, OSError):
                contenu = ""
            verifier("6. --rapport markdown avec verdict",
                     os.path.isfile(RAPPORT) and "Verdict" in contenu,
                     "existe=%s" % os.path.isfile(RAPPORT))
            if os.path.isfile(RAPPORT):
                try:
                    os.remove(RAPPORT)
                except OSError:
                    pass
            chrono_etape("6. rapport", t)

        # 7. Nettoyage : preuve injectee supprimee (0 trace).
        if point_actif(7):
            t = time.monotonic()
            if os.path.isfile(SENTINELLE):
                try:
                    os.remove(SENTINELLE)
                except OSError:
                    pass
            verifier("7. nettoyage : preuve supprimee (0 trace)",
                     not os.path.exists(SENTINELLE))
            chrono_etape("7. nettoyage", t)
    finally:
        # Filet de securite : aucune preuve ne doit survivre au test.
        for chemin in (SENTINELLE, RAPPORT):
            if os.path.isfile(chemin):
                try:
                    os.remove(chemin)
                except OSError:
                    pass

    # 8. Normes : ASCII strict + LF pur (outil + doc + test).
    if point_actif(8):
        t = time.monotonic()
        fichiers = [OUTIL_PY, os.path.abspath(__file__)]
        if os.path.isfile(OUTIL_MD):
            fichiers.append(OUTIL_MD)
        na_total = sum(ascii_count(f) for f in fichiers)
        crlf_total = sum(crlf_count(f) for f in fichiers)
        verifier("8. ASCII strict : 0 non-ASCII (outil + doc + test)",
                 na_total == 0, "total=%d" % na_total)
        verifier("8b. LF pur : 0 CRLF (outil + doc + test)",
                 crlf_total == 0, "total=%d" % crlf_total)
        chrono_etape("8. normes", t)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
