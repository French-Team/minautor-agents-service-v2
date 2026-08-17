#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-040-catalogue-index-synchronise.py
GARDE-FOU ANTI-RECURRENCE : chaque outil ajoute au catalogue
(catalogue-commandes.json) doit avoir son script present sur disque, sa doc
.md dans le meme dossier, et son entree dans index-tools.md.

Contexte (2026-08-13) :
  - Demande utilisateur : chaque outil ajoute au catalogue doit avoir sa doc
    et son entree index-tools a jour (meme construction, jamais de trou).
  - Etat initial (Buffy) : 137 scripts uniques au catalogue (0 script
    manquant, 0 doc manquante) mais 27 entrees index-tools absentes
    (4 outils reels + 23 tests). Buffy a tout indexe : section Tests
    (tester/tests/) creee avec 39 tests, stats total 118 -> 166, test-007
    adapte.
  - Ce garde-fou verifie en permanence la triple coherence : script -> doc
    -> index. Toute commande du catalogue pointant vers un script sans doc
    ou sans entree index est une derive a corriger immediatement.

Invariants verifies :
  1. Chaque script reference par le catalogue existe sur disque
     (dedoublonnage par script unique : plusieurs commandes peuvent
     pointer vers le meme outil, ex : activer-agent-principal 5x)
  2. Chaque outil a sa doc .md dans le meme dossier que le script
     (nom du dossier + .md)
  3. Chaque outil a son entree dans index-tools.md (backticks nom-outil
     ou chemin /nom-outil/)
  4. Normes : ASCII strict + LF pur (catalogue + index + test)
Tags: outils, catalogue, garde-fou, anti-recurrence
"""
import importlib.util
import io
import json
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
CATALOGUE = os.path.join(TOOLS_DIR, "generateurs", "generateurs-commande", "catalogue-commandes.json")
INDEX = os.path.join(TOOLS_DIR, "index-tools.md")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0


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


def verifier(nom, ok, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if ok:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s -- %s" % (nom, detail))


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== Test formel catalogue-index-synchronise ===")

    # 0. Charger le catalogue (JSON valide)
    try:
        with io.open(CATALOGUE, encoding="utf-8") as fh:
            cat = json.load(fh)
        commandes = cat.get("commandes", [])
    except Exception as e:
        verifier("0. Catalogue JSON charge", False, str(e))
        commandes = []

    # dedoublonner par script unique
    scripts = {}
    for c in commandes:
        s = c.get("script", "")
        if s:
            scripts.setdefault(s, c.get("nom"))
    verifier("0. Catalogue charge (%d commandes -> %d scripts uniques)" %
             (len(commandes), len(scripts)), len(scripts) > 0)

    # 1. Chaque script existe sur disque
    manquants_script = [s for s in scripts if not os.path.exists(
        os.path.join(PROJECT_ROOT, s))] if os.path.isabs(os.path.join(PROJECT_ROOT, next(iter(scripts), ''))) or True else []
    manquants_script = []
    for s in scripts:
        p = os.path.join(PROJECT_ROOT, s) if not os.path.isabs(s) else s
        if not os.path.exists(p):
            manquants_script.append(s)
    verifier("1. Chaque script du catalogue existe sur disque (%d/%d)" %
             (len(scripts) - len(manquants_script), len(scripts)),
             len(manquants_script) == 0, "manquants=%s" % manquants_script[:5])

    # 2. Chaque outil a sa doc .md (nom du dossier + .md)
    manquants_doc = []
    for s in scripts:
        dossier = os.path.dirname(s)
        nom_outil = os.path.basename(dossier)
        doc = os.path.join(dossier, nom_outil + ".md")
        p = os.path.join(PROJECT_ROOT, doc) if not os.path.isabs(doc) else doc
        if not os.path.exists(p):
            manquants_doc.append(nom_outil)
    verifier("2. Chaque outil a sa doc .md (%d/%d)" %
             (len(scripts) - len(manquants_doc), len(scripts)),
             len(manquants_doc) == 0, "manquants=%s" % manquants_doc[:5])

    # 3. Chaque outil a son entree index-tools
    try:
        idx = io.open(INDEX, encoding="utf-8").read()
    except Exception as e:
        idx = ""
        verifier("3. Chaque outil a son entree index-tools", False, str(e))
    manquants_index = []
    for s in scripts:
        nom_outil = os.path.basename(os.path.dirname(s))
        if ("`" + nom_outil + "`") not in idx and ("/" + nom_outil + "/") not in idx:
            manquants_index.append(nom_outil)
    verifier("3. Chaque outil a son entree index-tools (%d/%d)" %
             (len(scripts) - len(manquants_index), len(scripts)),
             len(manquants_index) == 0, "manquants=%s" % manquants_index[:5])

    # 4. Normes : ASCII strict + LF pur (catalogue + index + test)
    normes_ko = []
    for f in [CATALOGUE, INDEX, os.path.abspath(__file__)]:
        try:
            txt = io.open(f, encoding="utf-8", errors="replace").read()
            if any(ord(c) > 127 for c in txt):
                normes_ko.append("%s non-ascii" % os.path.basename(f))
            raw = io.open(f, "rb").read()
            if b"\r\n" in raw:
                normes_ko.append("%s crlf" % os.path.basename(f))
        except Exception as e:
            normes_ko.append("%s ERR %s" % (os.path.basename(f), e))
    verifier("4. Normes ASCII strict + LF pur (catalogue + index + test)",
             len(normes_ko) == 0, "ko=%s" % normes_ko)

    print()
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
