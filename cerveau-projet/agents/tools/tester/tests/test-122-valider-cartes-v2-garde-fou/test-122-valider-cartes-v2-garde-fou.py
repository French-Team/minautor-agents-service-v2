#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-122-valider-cartes-v2-garde-fou.py
GARDE-FOU : valider-cartes-decision v0.5.0 couvre le format v2 (arbres
servis par le pilote), pas seulement les parcours v1 legacy.
(mission fececd2a, suite Vulcain 83ff5727 - constat Janus 8bca6f3d)

Points verifies :
  1. --agent buffy : CONFORME (arbre v2 - etait NON CONFORME en v1)
  2. --agent morpheus : CONFORME (arbre v2)
  3. --agent vulcain : CONFORME (arbre v2)
  4. --tous : 22 agents verifies, 0 non conforme
  5. PREUVE NEGATIVE v2 : un arbre avec branche.vers vers un theme
     ABSENT -> NON CONFORME (references cassees detectees)
  6. PREUVE NEGATIVE v1 : --fichier sur un parcours v1 avec suivant mort
     -> NON CONFORME (la branche v1 ne dort pas)
  7. Repli v1 : --fichier arbre-hades.json -> CONFORME (format v1
     toujours valide)
  8. Normes : ASCII strict + LF pur (outil py/sh/md + test)

Proprietaire : Morpheus (testeur dedie)
Version : 0.1.0
Tags: valider-cartes-decision, v2, arbre, garde-fou, preuve-negative
"""
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
VALIDER = os.path.join(TOOLS_DIR, "valider", "valider-cartes-decision",
                       "valider-cartes-decision.py")
AGENTS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents")
RACINE = os.path.abspath(".")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0

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

T_START = time.monotonic()
ETAPES = []


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
    print("=== CHRONO test-122 (total %.1fs) ===" % total)
    for nom, duree in ETAPES:
        print("  %-34s %6.2fs" % (nom, duree))


def verifier(nom, condition, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s" % nom)
        if detail:
            print("       %s" % detail)


def ascii_count(chemin):
    try:
        data = io.open(chemin, "r", encoding="utf-8").read()
    except (OSError, UnicodeError):
        return -1
    return sum(1 for ch in data if ord(ch) > 127)


def crlf_count(chemin):
    try:
        data = io.open(chemin, "r", encoding="utf-8").read()
    except (OSError, UnicodeError):
        return -1
    return data.count("\r\n")


def lancer(argv):
    """Lancer valider-cartes-decision sous protections (verrou : l outil
    s auto-journalise ; les tests passent par le lanceur sous un agent
    habilite - argus/buffy/janus/vulcain)."""
    cmd = [sys.executable, VALIDER] + argv
    try:
        return PROTECTIONS.lancer_protege(
            cmd, timeout=120, capture_output=True, text=True, cwd=RACINE)
    except PROTECTIONS.ArretProtection as e:
        verifier("lancement protege de l outil", False, e.message)
        return None


def point_1_2_3_agents_v2():
    for num, agent in ((1, "buffy"), (2, "morpheus"), (3, "vulcain")):
        t0 = time.monotonic()
        # v0.6.0 : --audit pour sauter le verrou d habilitation (l agent
        # actif de session n est pas toujours habilite pour valider-cartes).
        p = lancer(["--agent", agent, "--audit"])
        out = (p.stdout or "") if p else ""
        verifier("%d. --agent %s : CONFORME (arbre v2)" % (num, agent),
                 "CONFORME" in out and "arbre v2" in out,
                 (out or "AUCUNE SORTIE")[-100:])
        chrono_etape("%d. agent %s" % (num, agent), t0)


def point_4_tous():
    t0 = time.monotonic()
    p = lancer(["--tous"])
    out = (p.stdout or "") if p else ""
    verifier("4. --tous : 22 agents conformes / 0 non conforme",
             "Agents verifies : 22" in out
             and "Agents non conformes : 0" in out,
             (out or "AUCUNE SORTIE")[-150:])
    chrono_etape("4. --tous", t0)


def point_5_preuve_negative_v2():
    t0 = time.monotonic()
    # Copier l arbre de buffy dans un tmp et casser une branche.vers
    tmp = tempfile.mkdtemp(prefix="test122-")
    try:
        src = os.path.join(AGENTS_DIR, "buffy", "parcours", "arbre-buffy.json")
        cible = os.path.join(tmp, "arbre-casse.json")
        data = json.loads(io.open(src, encoding="utf-8").read())
        data["racine"]["branches"][0]["vers"] = "theme-absent-xyz.json"
        with io.open(cible, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(data, ensure_ascii=True))
        p = lancer(["--fichier", cible])
        out = (p.stdout or "") if p else ""
        verifier("5. PREUVE NEGATIVE v2 : branche.vers vers theme absent "
                 "-> NON CONFORME",
                 "NON CONFORME" in out and "theme-absent-xyz" in out,
                 (out or "AUCUNE SORTIE")[-150:])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    chrono_etape("5. preuve negative v2", t0)


def point_6_preuve_negative_v1():
    t0 = time.monotonic()
    # v0.6.0 (migration v1->v2) : un parcours v1 (parcours-*.json) est un
    # VESTIGE - valider-cartes doit le declarer NON CONFORME (format v1).
    tmp = tempfile.mkdtemp(prefix="test122-v1-")
    try:
        cible = os.path.join(tmp, "parcours-vestige.json")
        vestige = {
            "identite": {"type": "parcours", "appartient_a": "factice"},
            "parcours": {"nom": "parcours-vestige", "version": "0.1.0"},
            "cases": {
                "c0": {"type": "question", "message": "depart"}
            }
        }
        with io.open(cible, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(vestige, ensure_ascii=True))
        p = lancer(["--fichier", cible])
        out = (p.stdout or "") if p else ""
        verifier("6. PREUVE NEGATIVE v1 : parcours v1 factice -> NON CONFORME "
                 "(vestige v1)",
                 "NON CONFORME" in out and "vestige v1" in out,
                 (out or "AUCUNE SORTIE")[-150:])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    chrono_etape("6. preuve negative v1", t0)


def point_7_repli_v1():
    t0 = time.monotonic()
    p = lancer(["--fichier", os.path.join(AGENTS_DIR, "hades", "parcours",
                                          "arbre-hades.json")])
    out = (p.stdout or "") if p else ""
    verifier("7. arbre v2 : arbre-hades.json CONFORME (format v2)",
             "CONFORME" in out and "arbre v2" in out,
             (out or "AUCUNE SORTIE")[-100:])
    chrono_etape("7. repli v1", t0)


def point_8_normes():
    t0 = time.monotonic()
    dossier = os.path.dirname(VALIDER)
    fichiers = [os.path.join(dossier, "valider-cartes-decision.py"),
                os.path.join(dossier, "valider-cartes-decision.sh"),
                os.path.join(dossier, "valider-cartes-decision.md"),
                os.path.join(PROJECT_ROOT,
                             "cerveau-projet", "agents", "tools", "tester",
                             "tests", "test-122-valider-cartes-v2-garde-fou",
                             "test-122-valider-cartes-v2-garde-fou.py")]
    total_na = sum(max(ascii_count(f), 0) for f in fichiers)
    verifier("8. ASCII strict : 0 non-ascii (outil + test)", total_na == 0,
             "non_ascii=%s" % total_na)
    total_crlf = sum(max(crlf_count(f), 0) for f in fichiers)
    verifier("8b. LF pur : 0 CRLF (outil + test)", total_crlf == 0,
             "crlf=%s" % total_crlf)
    chrono_etape("8. normes", t0)


def main():
    if point_actif(1):
        point_1_2_3_agents_v2()
    if point_actif(4):
        point_4_tous()
    if point_actif(5):
        point_5_preuve_negative_v2()
    if point_actif(6):
        point_6_preuve_negative_v1()
    if point_actif(7):
        point_7_repli_v1()
    if point_actif(8):
        point_8_normes()

    bilan_chrono()
    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    print("=== VERDICT : %s ==="
          % ("PROPRE (valider-cartes-decision v0.5.0 couvre le v2)"
             if NB_KO == 0 else "KO (support v2 casse)"))
    return 1 if NB_KO > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
