#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-001-evaluer-agents-coherence.py
Test des corrections apportees a evaluer-agents et evaluer-coherence.

Corrections testees:
  1. evaluer-agents exclut __pycache__ des outils manquants
  2. evaluer-coherence utilise le projet root pour cible_racine
  3. evaluer-coherence exclut les commandes systeme (cat, grep, sed, basher)

Contexte : ce test a ete migre au format template-test.md v0.2.0 (audit
Morpheus 2026-08-12 : le TEMPLATE est la reference, pas les tests precedents).
L ancien format utilisait coding utf-8 et le marqueur [ECHEC] invisible pour
le lanceur de non-regression (qui compte les [KO]).
Tags: outils, evaluer
"""
import importlib.util
import io
import json
import os
import re
import subprocess
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

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


EVALUER_AGENTS_PY = os.path.join(TOOLS_DIR, "evaluer", "evaluer-agents", "evaluer-agents.py")
EVALUER_COHERENCE_PY = os.path.join(TOOLS_DIR, "evaluer", "evaluer-coherence", "evaluer-coherence.py")

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
    return PROTECTIONS.lancer_protege(cmd, capture_output=True, text=True, timeout=timeout)


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def main():
    print("=== test-001 : corrections evaluer-agents / evaluer-coherence ===")

    # 1-4. Tests de evaluer-agents
    r = run([PYTHON, EVALUER_AGENTS_PY])
    stdout = r.stdout

    nb_pycache = stdout.count("Outil __pycache__")
    verifier("1. evaluer-agents exclut __pycache__ des erreurs",
             nb_pycache == 0, "nb_pycache=%d" % nb_pycache)

    m = re.search(r"Score agents : (\d+)/100", stdout)
    if m:
        score = int(m.group(1))
        verifier("2. score evaluer-agents > 50/100 (corrige de 23)",
                 score > 50, "score=%d" % score)
    else:
        verifier("2. score evaluer-agents > 50/100", False,
                 "score introuvable dans la sortie")

    verifier("3. evaluer-agents signale generateurs-commande (outil incomplet)",
             "generateurs-commande" in stdout, "")

    verifier("4. evaluer-agents execute sans crash", r.returncode == 0,
             "rc=%d" % r.returncode)

    # 5-8. Tests de evaluer-coherence
    r2 = run([PYTHON, EVALUER_COHERENCE_PY])
    stdout2 = r2.stdout

    cmd_systeme = [c for c in ("cat", "grep", "sed", "basher")
                   if ("`%s` reference par" % c) in stdout2]
    verifier("5. evaluer-coherence exclut cat/grep/sed/basher des outils casses",
             len(cmd_systeme) == 0, "signales=%s" % cmd_systeme)

    verifier("6. evaluer-coherence dit 'Tous les outils references existent'",
             "Tous les outils references existent" in stdout2, "")

    liens = ["agents/conventions/structures/convention-classeur-variables.md",
             "agents/conventions/structures/convention-structures.md"]
    liens_casses = [l for l in liens if l in stdout2]
    verifier("7. faux positifs liens structures resolus (existe sous cerveau-projet/)",
             len(liens_casses) == 0, "encore=%s" % liens_casses)

    verifier("8. evaluer-coherence execute sans crash", r2.returncode == 0,
             "rc=%d" % r2.returncode)

    # 9-10. Normes ASCII strict + LF pur sur les fichiers concernes
    fichiers = [EVALUER_AGENTS_PY, EVALUER_COHERENCE_PY,
                os.path.abspath(__file__)]
    total_non_ascii = sum(ascii_count(f) for f in fichiers)
    verifier("9. ASCII strict : 0 non-ASCII (outils + test)",
             total_non_ascii == 0, "total=%d" % total_non_ascii)
    total_crlf = sum(crlf_count(f) for f in fichiers)
    verifier("10. LF pur : 0 CRLF (outils + test)",
             total_crlf == 0, "total=%d" % total_crlf)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
