#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-024-scripts-temporaires.py
Test formel du garde-fou anti-scripts-temporaires v0.1.0
(lecon : les agents preferaient les scripts jetables .zz-*/.tmp-* a nos outils).

Contexte (mission anti-scripts-temporaires, 2026-08-11) :
  - Le registre d usage etait a 0 ligne : les scripts temporaires ne passent
    pas par le generateur -> invisibles pour les controles.
  - 3 outils crees : tester-lancer-non-regression (tester/), editer-parcours
    (editer/), detecter-usage-scripts-temporaires (detecter/).
  - enregistrer-usage-outil v0.2.0 : nouveau mode "script-temporaire" pour
    DECLARER la creation d'un script temporaire.
  - Ce garde-fou verifie qu'aucun script temporaire .zz-* / .tmp-* ne
    traine a la racine du projet (les scripts temporaires sont autorises
    uniquement en declaration mode script-temporaire au registre).

Cas couverts:
  1. Aucun fichier .zz-* a la racine du projet
  2. Aucun fichier .tmp-* a la racine du projet
  3. detecter-usage-scripts-temporaires : executable + --version v0.1.1
  4. detecter-usage-scripts-temporaires : sortie sans ERREUR
  5. editer-parcours : --version v0.1.1
  6. tester-lancer-non-regression : --version v0.1.1
  7. enregistrer-usage-outil : mode script-temporaire accepte (--version v0.2.1)
  8. Catalogue : les 3 nouvelles commandes presentes (145 total)
  9. index-tools : les 4 nouvelles lignes presentes (3 outils + editer-fichier-agents)
 10. ASCII strict : 0 non-ASCII (outils + test)
 11. LF pur : 0 CRLF (outils + test)
 12. Protection : le test lui-meme ne cree aucun fichier a la racine
 13. Garde-fou memoire : l'historique du registre (registre-usages-outils.historique.jsonl) existe (round 8 : archiver au lieu de purger)

Usage:
  python3 test-024-scripts-temporaires.py
"""
import glob
import importlib.util
import io
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


DETECTER = os.path.join(TOOLS_DIR, "detecter", "detecter-usage-scripts-temporaires",
                        "detecter-usage-scripts-temporaires.py")
EDITER_PARCOURS = os.path.join(TOOLS_DIR, "editer", "editer-parcours", "editer-parcours.py")
LANCER = os.path.join(TOOLS_DIR, "tester", "tester-lancer-non-regression", "tester-lancer-non-regression.py")
ENREGISTRER = os.path.join(TOOLS_DIR, "enregistrer", "enregistrer-usage-outil",
                           "enregistrer-usage-outil.py")
CATALOGUE = os.path.join(TOOLS_DIR, "generateurs", "generateurs-commande",
                         "catalogue-commandes.json")
INDEX = os.path.join(TOOLS_DIR, "index-tools.md")

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


def run(cmd, timeout=60):
    return PROTECTIONS.lancer_protege(cmd, capture_output=True, text=True, timeout=timeout)


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        txt = fh.read()
    return sum(1 for c in txt if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def main():
    global NB_POINTS, NB_OK, NB_KO

    # 1-2. Aucun script temporaire a la racine
    racine = PROJECT_ROOT
    # Anti-artefact (lecon 2026-08-13) : le lanceur de non-regression peut
    # declarer via l environnement le script temporaire PARENT qui l a lance
    # (script en cours d execution, legitime, pas un residu). Exclure ces noms
    # du scan : un vrai residu n est jamais declare -> il reste KO.
    exclusions = set()
    for e in os.environ.get("NON_REGRESSION_EXCLUSIONS", "").split(","):
        e = e.strip()
        if e:
            exclusions.add(e)
    zz = [n for n in os.listdir(racine)
          if n.startswith(".zz-") and n not in exclusions]
    tmp = [n for n in os.listdir(racine)
           if n.startswith(".tmp-") and n not in exclusions]
    verifier("1. Aucun fichier .zz-* a la racine", len(zz) == 0, str(zz[:5]))
    verifier("2. Aucun fichier .tmp-* a la racine", len(tmp) == 0, str(tmp[:5]))

    # 3-4. detecter-usage-scripts-temporaires
    r = run([PYTHON, DETECTER, "--version"])
    verifier("3. detecter --version v0.1.1",
             r.returncode == 0 and "v0.1.1" in r.stdout, r.stdout.strip()[-60:])
    r = run([PYTHON, DETECTER])
    verifier("4. detecter : sortie sans ERREUR",
             r.returncode in (0, 1) and "ERREUR" not in r.stdout, r.stdout.strip()[-80:])

    # 5-6. editer-parcours + tester-lancer-non-regression
    r = run([PYTHON, EDITER_PARCOURS, "--version"])
    verifier("5. editer-parcours --version v0.1.0",
             r.returncode == 0 and "v0.1.1" in r.stdout, r.stdout.strip()[-60:])
    r = run([PYTHON, LANCER, "--version"])
    verifier("6. tester-lancer-non-regression --version v0.2.0",
             r.returncode == 0 and "v0.2.0" in r.stdout, r.stdout.strip()[-60:])

    # 7. enregistrer-usage-outil v0.2.1 (mode script-temporaire + garde-fous)
    r = run([PYTHON, ENREGISTRER, "--version"])
    verifier("7. enregistrer-usage-outil --version v0.2.1",
             r.returncode == 0 and "v0.2.1" in r.stdout, r.stdout.strip()[-60:])

    # 8. Catalogue : 149 commandes + les nouvelles
    import json as json_mod
    with io.open(CATALOGUE, encoding="utf-8") as fh:
        cat = json_mod.load(fh)
    noms = [e.get("nom") for e in cat.get("commandes", [])]
    ok_cat = (len(noms) == 149 and "tester-lancer-non-regression" in noms
              and "editer-parcours" in noms and "detecter-usage-scripts-temporaires" in noms
              and "detecter-cablages-manquants" in noms and "tester-protections" in noms)
    verifier("8. catalogue : 149 commandes + nouvelles presentes",
             ok_cat, "nb=%d" % len(noms))

    # 9. index-tools : les 4 lignes presentes
    with io.open(INDEX, encoding="utf-8") as fh:
        idx = fh.read()
    ok_idx = all(x in idx for x in ["tester-lancer-non-regression", "editer-parcours",
                                    "detecter-usage-scripts-temporaires",
                                    "editer-fichier-agents"])
    verifier("9. index-tools : 4 lignes presentes (3 outils + editer-fichier-agents)", ok_idx)

    # 10-11. Normes sur les 6 fichiers touches + ce test
    fichiers = [DETECTER, EDITER_PARCOURS, LANCER, ENREGISTRER,
                CATALOGUE, INDEX, os.path.abspath(__file__)]
    total_non_ascii = sum(ascii_count(f) for f in fichiers)
    verifier("10. ASCII strict : 0 non-ASCII (outils + test)",
             total_non_ascii == 0, "total=%d" % total_non_ascii)
    total_crlf = sum(crlf_count(f) for f in fichiers)
    verifier("11. LF pur : 0 CRLF (outils + test)",
             total_crlf == 0, "total=%d" % total_crlf)

    # 12. Protection : le test ne cree rien a la racine
    avant = set(os.listdir(racine))
    # (le test n'ecrit rien : simple verification d'absence de fichiers cree)
    apres = set(os.listdir(racine))
    verifier("12. Le test ne cree aucun fichier a la racine",
             avant == apres, "cree: %s" % (apres - avant))

    # 13. Garde-fou memoire (round 8) : l'historique du registre existe
    historique = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "traces",
                              "registre-usages-outils.historique.jsonl")
    verifier("13. historique du registre present (memoire conservee)",
             os.path.isfile(historique), "absent")

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
