#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-020-combos-clio.py
Test formel des 3 combos Clio (Pattern 3, crees pour le test reel de la
grosse mise a jour conservative du README : savoir CE QUI A CHANGE puis
corriger compteurs, tables et badges).

Combos testes (cerveau-projet/agents/tools/combos/):
  1. combos-analyse-projet (orchestre py/sh/md, v0.1.2) : etat reel du projet
     (agents, outils par categorie) + ecarts README vs realite
  2. combo-maj-readme (encapsule definition-combo.json, v0.1.0, 5 cases) :
     PETITE MAJ - verifier -> maj (si ecarts) -> ASCII
  3. combos-maj-readme-massive (orchestre py/sh/md, v0.1.5) : GROSSE MAJ
     conservative - analyse -> verifier -> maj -> correctifs -> ASCII
     (badge header Outils-N affichage + href alignes automatiquement)

Cas couverts:
  1. Nommage : py/sh/md des 2 orchestres + definition-combo.json du encapsule
  2. Versions 0.1.0 des 3 combos (--version orchestres, JSON encapsule)
  3. JSON valide : combo-maj-readme (nom, version, case_depart c1, 5 cases)
  4. combos-analyse-projet : execution reelle sans --rapport (ETAT REEL + ECARTS,
     agents reels detectes, code 0)
  5. combos-maj-readme-massive : execution reelle sans --rapport (etapes 1-5,
     code 0) - mode conservatif
  6. combos-moteur --liste combo-maj-readme : 5 cases affichees
  7. combos-moteur --dry-run c2=OUI : verifier -> maj -> ascii -> FIN c5
  8. combos-moteur --dry-run c2=NON : verifier -> ascii -> FIN c5
  9. Parite .sh : les 2 .sh orchestres deleguent au .py (--help)
 10. ASCII : valider-conformite-ascii 0 sur les 7 fichiers des combos
 11. LF pur : 0 CRLF sur les 7 fichiers

Usage:
  python3 test-020-combos-clio.py
"""
import importlib.util
import io
import json
import os
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


MOTEUR_PY = os.path.join(TOOLS_DIR, "combos", "combos-moteur", "combos-moteur.py")
ANALYSE_PY = os.path.join(TOOLS_DIR, "combos", "combos-analyse-projet", "combos-analyse-projet.py")
MASSIVE_PY = os.path.join(TOOLS_DIR, "combos", "combos-maj-readme-massive", "combos-maj-readme-massive.py")
MAJ_JSON = os.path.join(TOOLS_DIR, "combos", "combo-maj-readme", "definition-combo.json")

FICHIERS = [
    ("combos-analyse-projet.py", os.path.join(TOOLS_DIR, "combos", "combos-analyse-projet", "combos-analyse-projet.py")),
    ("combos-analyse-projet.sh", os.path.join(TOOLS_DIR, "combos", "combos-analyse-projet", "combos-analyse-projet.sh")),
    ("combos-analyse-projet.md", os.path.join(TOOLS_DIR, "combos", "combos-analyse-projet", "combos-analyse-projet.md")),
    ("combos-maj-readme-massive.py", os.path.join(TOOLS_DIR, "combos", "combos-maj-readme-massive", "combos-maj-readme-massive.py")),
    ("combos-maj-readme-massive.sh", os.path.join(TOOLS_DIR, "combos", "combos-maj-readme-massive", "combos-maj-readme-massive.sh")),
    ("combos-maj-readme-massive.md", os.path.join(TOOLS_DIR, "combos", "combos-maj-readme-massive", "combos-maj-readme-massive.md")),
    ("combo-maj-readme/definition-combo.json", MAJ_JSON),
]

TOTAL = 0
KO = 0


def check(cond, nom, detail=""):
    global TOTAL, KO
    TOTAL += 1
    if cond:
        print("[OK] " + nom + (" " + detail if detail else ""))
    else:
        KO += 1
        print("[KO] " + nom + (" " + detail if detail else ""))


def run(cmd, timeout=300):
    return PROTECTIONS.lancer_protege(cmd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=timeout)


# 1. Nommage
for nom, p in FICHIERS:
    check(os.path.isfile(p), "nommage %s" % nom)

# 2. Versions
r = run([PYTHON, ANALYSE_PY, "--version"])
check(r.returncode == 0 and "combos-analyse-projet 0.1.2" in (r.stdout or r.stderr),
      "version combos-analyse-projet 0.1.2")
r = run([PYTHON, MASSIVE_PY, "--version"])
check(r.returncode == 0 and "combos-maj-readme-massive 0.1.5" in (r.stdout or r.stderr),
      "version combos-maj-readme-massive 0.1.5")

# 3. JSON valide
try:
    d = json.load(io.open(MAJ_JSON, encoding="utf-8", newline=""))
    check(d["combo"].get("nom") == "combo-maj-readme", "json nom combo-maj-readme")
    check(d["combo"].get("version") == "0.1.0", "json version 0.1.0")
    check(d["combo"].get("case_depart") == "c1", "json case_depart c1")
    check(len(d.get("cases", {})) == 5, "json 5 cases")
except Exception as e:
    check(False, "json combo-maj-readme valide", str(e))

# 4. combos-analyse-projet execution reelle
r = run([PYTHON, ANALYSE_PY, PROJECT_ROOT], timeout=300)
out = (r.stdout or "") + (r.stderr or "")
check(r.returncode == 0, "analyse-projet code 0", str(r.returncode))
check("ETAT REEL" in out and "ECARTS" in out, "analyse-projet sortie (ETAT REEL + ECARTS)")
check("Agents reels" in out, "analyse-projet agents reels detectes")
check("Outils reels" in out, "analyse-projet outils reels detectes")

# 5. combos-maj-readme-massive execution reelle (mode --audit : la session
# porte l agent qui lance la non-regression, pas clio ; le mode audit du
# combo verifie la table d habilitation sans l identite reelle - v0.2.0)
r = run([PYTHON, MASSIVE_PY, PROJECT_ROOT, "--agent", "clio", "--audit"], timeout=600)
out = (r.stdout or "") + (r.stderr or "")
check(r.returncode == 0, "maj-readme-massive code 0", str(r.returncode))
for etape in ("Etape 1/5", "Etape 2/5", "Etape 3/5", "Etape 4/5", "Etape 5/5"):
    check(etape in out, "maj-readme-massive " + etape)
check("SYNTHESE" in out and "conservative" in out, "maj-readme-massive synthese conservative")

# 6. combos-moteur --liste
r = run([PYTHON, MOTEUR_PY, MAJ_JSON, "--liste"])
out = (r.stdout or "") + (r.stderr or "")
check(r.returncode == 0, "combos-moteur --liste code 0")
check("c1" in out and "c5" in out, "combos-moteur --liste cases c1..c5")

# 7. dry-run c2=OUI (verifier -> maj -> ascii -> FIN)
r = run([PYTHON, MOTEUR_PY, MAJ_JSON, "--dry-run", "--reponses", "c2=OUI"])
out = (r.stdout or "") + (r.stderr or "")
check("--verifier" in out and "--maj" in out and "valider-conformite-ascii" in out,
      "dry-run c2=OUI enchaene verifier+maj+ascii")
check("COMBO TERMINE" in out and "c5" in out, "dry-run c2=OUI fin c5")

# 8. dry-run c2=NON (verifier -> ascii -> FIN)
r = run([PYTHON, MOTEUR_PY, MAJ_JSON, "--dry-run", "--reponses", "c2=NON"])
out = (r.stdout or "") + (r.stderr or "")
# la navigation ne doit pas EXECUTER --maj (la description du combo peut le mentionner)
check("--verifier" in out and "valider-conformite-ascii" in out
      and "DRY-RUN] python3 " in out and "--maj" not in out.split("DRY-RUN]")[1],
      "dry-run c2=NON enchaene verifier+ascii sans maj")
check("COMBO TERMINE" in out, "dry-run c2=NON fin")

# 9. Parite .sh
for nom, p in FICHIERS:
    if nom.endswith(".sh"):
        r = run(["bash", p, "--help"])
        check(r.returncode == 0, "parite sh %s" % nom)

# 10/11. ASCII + LF sur les 7 fichiers
for nom, p in FICHIERS:
    t = io.open(p, encoding="utf-8", newline="").read()
    na = sum(1 for c in t if ord(c) > 127)
    raw = open(p, "rb").read()
    crlf = raw.count(b"\r\n")
    check(na == 0, "ascii %s" % nom, "non-ASCII=%d" % na)
    check(crlf == 0, "lf pur %s" % nom, "CRLF=%d" % crlf)

bilan_chrono()
print()
print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (TOTAL - KO, KO, TOTAL))
sys.exit(1 if KO else 0)
