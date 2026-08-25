#!/usr/bin/env python3
# -*- coding: ascii -*-
"""test-090-bdd-lecons-garde-fou.py
GARDE-FOU : la BDD portable des lecons (SQLite unique partagee) est la
memoire LONGUE des lecons. Deux outils dedies la touchent :
  - enregistrer-lecon (ecriture : anti-usurpation + verrou + ASCII +
    anti-doublon)
  - consulter-lecons (lecture : verrou + filtres + journalisation d activite)

Contexte (2026-08-17, demande utilisateur) : les corrections.md sont devenus
indigestes (memoire courte saturee). La BDD les decouple : corrections.md =
fenetre glissante (memoire courte), lecons.db = memoire longue partagee.

Invariants verifies :
  1. Les 2 outils existent et compilent.
  2. --version des 2 outils.
  3. enregistrer-lecon : creation OK (id retourne) pour l agent actif.
  4. Anti-usurpation : --agent != agent actif -> code 1.
  5. ASCII strict : lecon non-ASCII -> code 1.
  6. Anti-doublon : meme lecon -> code 1.
  7. consulter-lecons : la lecon est retrouvee (--toutes + --recherche).
  8. Journalisation d activite : entree directe consulter-lecons au registre.
  9. Integrite : lecons.db n est referencee QUE par les 2 outils (grep).
  10. Normes : ASCII strict + LF pur (outils + test).

Tags: outils, agents, garde-fou, anti-recurrence, preuve-negative
"""
import importlib.util
import io
import os
import py_compile
import re
import sqlite3
import subprocess
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

ENR_PY = os.path.join(TOOLS_DIR, "enregistrer", "enregistrer-lecon",
                      "enregistrer-lecon.py")
CON_PY = os.path.join(TOOLS_DIR, "consulter", "consulter-lecons",
                      "consulter-lecons.py")
BDD = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "lecons",
                   "lecons.db")
REGISTRE = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "traces",
                        "registre-usages-outils.jsonl")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0

# --- options ON/OFF + chrono ---
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
    print("=== CHRONO test-090 (total %.1fs) ===" % total)
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


def lancer(cmd, timeout=90):
    return PROTECTIONS.lancer_protege(cmd, timeout=timeout)


def agent_actif():
    chemin = os.path.join(PROJECT_ROOT, "AGENTS.md")
    with io.open(chemin, "r", encoding="utf-8") as f:
        contenu = f.read()
    m = re.search(r"## Sessions connues\n(.*?)(?=\n## |\Z)", contenu, re.S)
    if not m:
        return "janus"
    lignes = []
    for ligne in m.group(1).splitlines():
        ligne = ligne.strip()
        if not ligne.startswith("| session-"):
            continue
        cellules = [c.strip() for c in ligne.strip("|").split("|")]
        if len(cellules) >= 4:
            lignes.append(cellules)
    if not lignes:
        return "janus"
    lignes.sort(key=lambda c: c[3], reverse=True)
    return lignes[0][2].strip() or "janus"


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with io.open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== Garde-fou : BDD des lecons (enregistrer + consulter) ===")

    actif = agent_actif()
    autre = "vulcain" if actif.lower() != "vulcain" else "buffy"
    titre = "test-090-%d" % int(time.time())
    lecon = "lecon de test du garde-fou BDD (auto-nettoyee)."

    # 1. outils presents + compilent.
    if point_actif(1):
        t = time.monotonic()
        ok = os.path.isfile(ENR_PY) and os.path.isfile(CON_PY)
        for f in (ENR_PY, CON_PY):
            if os.path.isfile(f):
                try:
                    py_compile.compile(f, doraise=True)
                except Exception:
                    ok = False
        verifier("1. outils presents + compilent", ok)
        chrono_etape("1. outils", t)

    # 2. --version.
    if point_actif(2):
        t = time.monotonic()
        r1 = lancer([PYTHON, ENR_PY, "--version"])
        r2 = lancer([PYTHON, CON_PY, "--version"])
        verifier("2. --version des 2 outils",
                 r1.returncode == 0 and "v0.1.0" in r1.stdout
                 and r2.returncode == 0 and "v0.1.0" in r2.stdout,
                 "%s / %s" % (r1.stdout.strip(), r2.stdout.strip()))
        chrono_etape("2. version", t)

    # 3. creation OK.
    if point_actif(3):
        t = time.monotonic()
        r = lancer([PYTHON, ENR_PY, "--agent", actif, "--domaine", "test",
                    "--titre", titre, "--lecon", lecon, "--verdict", "OK"])
        verifier("3. enregistrer-lecon creation OK (id retourne)",
                 r.returncode == 0 and "id" in r.stdout,
                 r.stdout.strip()[:120])
        chrono_etape("3. creation", t)

    # 4. anti-usurpation.
    if point_actif(4):
        t = time.monotonic()
        r = lancer([PYTHON, ENR_PY, "--agent", autre, "--titre", "usurp",
                    "--lecon", "tentative usurpation"])
        verifier("4. anti-usurpation : --agent != actif -> code 1",
                 r.returncode == 1 and "anti-usurpation" in r.stdout,
                 "rc=%s" % r.returncode)
        chrono_etape("4. usurpation", t)

    # 5. ASCII strict.
    if point_actif(5):
        t = time.monotonic()
        r = lancer([PYTHON, ENR_PY, "--agent", actif, "--titre", "accent",
                    "--lecon", "lecon avec accent : \u00e9t\u00e9"])
        verifier("5. non-ASCII refuse -> code 1",
                 r.returncode == 1 and "non-ASCII" in r.stdout,
                 "rc=%s" % r.returncode)
        chrono_etape("5. ascii", t)

    # 6. anti-doublon.
    if point_actif(6):
        t = time.monotonic()
        r = lancer([PYTHON, ENR_PY, "--agent", actif, "--titre", titre,
                    "--lecon", lecon])
        verifier("6. anti-doublon : meme lecon -> code 1",
                 r.returncode == 1 and "doublon" in r.stdout,
                 "rc=%s" % r.returncode)
        chrono_etape("6. doublon", t)

    # 7. consulter-lecons retrouve la lecon.
    if point_actif(7):
        t = time.monotonic()
        r1 = lancer([PYTHON, CON_PY, "--agent", actif, "--toutes"])
        r2 = lancer([PYTHON, CON_PY, "--agent", actif, "--recherche",
                     "test-090"])
        verifier("7. consulter-lecons retrouve la lecon (toutes + recherche)",
                 r1.returncode == 0 and titre in r1.stdout
                 and r2.returncode == 0 and titre in r2.stdout,
                 "rc=%s/%s" % (r1.returncode, r2.returncode))
        chrono_etape("7. consulter", t)

    # 8. journalisation d activite.
    if point_actif(8):
        t = time.monotonic()
        present = False
        try:
            txt = io.open(REGISTRE, encoding="utf-8",
                          errors="replace").read()
            present = ("consulter-lecons" in txt and "consultation lecons"
                       in txt)
        except (IOError, OSError):
            present = False
        verifier("8. journalisation d activite (consultation directe au registre)",
                 present)
        chrono_etape("8. journalisation", t)

    # 9. integrite : lecons.db referencee QUE par les 2 outils.
    if point_actif(9):
        t = time.monotonic()
        refs = []
        for racine_dir, _, fichiers in os.walk(TOOLS_DIR):
            if "__pycache__" in racine_dir:
                continue
            # les tests ne sont pas des OUTILS : ils ne sont pas soumis a la
            # regle 'la BDD n est touchee que par les 2 outils'.
            rel = os.path.relpath(racine_dir, TOOLS_DIR)
            if "tester" in rel.split(os.sep):
                continue
            for f in fichiers:
                if not f.endswith(".py"):
                    continue
                chemin = os.path.join(racine_dir, f)
                try:
                    txt = io.open(chemin, encoding="utf-8",
                                  errors="replace").read()
                except (IOError, OSError):
                    continue
                if "lecons.db" in txt or "lecons/lecons.db" in txt:
                    rel = os.path.relpath(chemin, TOOLS_DIR)
                    refs.append(rel)
        legitimes = {
            "enregistrer/enregistrer-lecon/enregistrer-lecon.py",
            "consulter/consulter-lecons/consulter-lecons.py",
            # evaluer-progression (v0.1.0, catalogue) lit le compteur de
            # lecons pour mesurer la progression du projet : lecture seule
            # legitime de la BDD (ajoute 2026-08-19 apres sa creation par
            # la session llm-4).
            "evaluer/evaluer-progression/evaluer-progression.py",
        }
        intrus = [r for r in refs
                  if r.replace("\\", "/") not in legitimes]
        verifier("9. lecons.db referencee QUE par les 2 outils",
                 not intrus, "intrus=%s" % intrus[:3])
        chrono_etape("9. integrite", t)

    # nettoyage : supprimer la lecon de test (preuve auto-nettoyee).
    try:
        conn = sqlite3.connect(BDD)
        conn.execute("DELETE FROM lecons WHERE titre = ? AND lecon = ?",
                     (titre, lecon))
        conn.commit()
        conn.close()
    except sqlite3.Error:
        pass

    # 10. normes.
    if point_actif(10):
        t = time.monotonic()
        fichiers = [ENR_PY, CON_PY, os.path.abspath(__file__)]
        na = sum(ascii_count(f) for f in fichiers)
        crlf = sum(crlf_count(f) for f in fichiers)
        verifier("10. ASCII strict : 0 non-ASCII (outils + test)",
                 na == 0, "total=%d" % na)
        verifier("10b. LF pur : 0 CRLF (outils + test)",
                 crlf == 0, "total=%d" % crlf)
        chrono_etape("10. normes", t)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
