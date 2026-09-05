#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-071-cases-lecons-outil-correction.py
CHASSEUR DE VESTIGES V1 (migration v1->v2, 2026-09-05) : la regle v1
"toute case d'ecriture de lecon/rapport porte un outil de correction"
vivait dans les CASES des parcours v1 (type action + indices outil). Les
parcours v1 sont RETIRES : les structures actives sont les arbres v2
(arbre-*.json + theme-*.json + fins.json) qui n'ont PAS de cases.

Ce test PISTE les vestiges : si une structure v2 contient encore une case
v1 de type "action" avec des indices (format v1), le test ECHOUE : c est un
vestige a purger.

Points verifies :
  1. Aucun fichier parcours-*.json (v1) ne subsiste dans les agents.
  2. Les structures v2 ne portent AUCUNE cle top-level "cases".
  3. Les structures v2 ne portent AUCUNE case avec indices de type outil
     (format v1 des cases d'ecriture).
  4. PREUVE NEGATIVE : une structure synthetique v1 (avec cases + indices
     outil) est DETECTEE par le scan de vestiges.
  5. Normes : ASCII strict + LF pur (test + structures v2 scannees).
Tags: vestiges, v1, migration, lecons, garde-fou
"""
import glob
import importlib.util
import io
import json
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
AGENTS = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents")

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


def verifier(nom, condition, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s %s" % (nom, ("-- " + detail) if detail else ""))


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def structures_v2():
    """Arbres + themes + fins des agents v1 (structures actives v2)."""
    resultats = []
    for motif in ("arbre-*.json", "theme-*.json", "fins.json"):
        resultats.extend(glob.glob(os.path.join(AGENTS, "*", "parcours", motif)))
    return sorted(set(resultats))


def contient_case_v1(donnees):
    """Detecte une case v1 (type action + indices) dans une structure JSON."""
    if isinstance(donnees, dict):
        if isinstance(donnees.get("indices"), list) and \
                donnees.get("type") in ("action", "fin", "question"):
            return True
        return any(contient_case_v1(v) for v in donnees.values())
    if isinstance(donnees, list):
        return any(contient_case_v1(v) for v in donnees)
    return False


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== Chasseur de vestiges v1 : cases lecons/outils (format v1) ===")

    # 1. Aucun parcours-*.json v1 ne subsiste
    vestiges_parcours = glob.glob(os.path.join(AGENTS, "*", "parcours",
                                               "parcours-*.json"))
    verifier("1. aucun parcours-*.json v1 ne subsiste",
             len(vestiges_parcours) == 0, "vestiges=%s" % vestiges_parcours[:5])

    # 2. Les structures v2 ne portent AUCUNE cle top-level "cases"
    structures = structures_v2()
    verifier("2. structures v2 detectees (%d)" % len(structures),
             len(structures) >= 100, "nb=%d" % len(structures))
    avec_cases = []
    for f in structures:
        try:
            d = json.load(io.open(f, encoding="utf-8"))
        except Exception:
            continue
        if isinstance(d, dict) and "cases" in d:
            avec_cases.append(os.path.basename(f))
    verifier("3. aucune structure v2 avec cle top-level 'cases'",
             len(avec_cases) == 0, "avec_cases=%s" % avec_cases[:5])

    # 4. Aucune case v1 (type action + indices) dans les structures v2
    avec_case = []
    for f in structures:
        try:
            d = json.load(io.open(f, encoding="utf-8"))
        except Exception:
            continue
        if contient_case_v1(d):
            avec_case.append(os.path.basename(f))
    verifier("4. aucune case v1 (action/indices) dans les structures v2",
             len(avec_case) == 0, "avec_case=%s" % avec_case[:5])

    # 5. PREUVE NEGATIVE : une structure synthetique v1 est DETECTEE
    fake = {"parcours": {"agent": "x"}, "cases": {
        "c1": {"type": "action", "titre": "Ecrire une lecon",
               "indices": [{"type": "outil", "nom": "ajouter-contenu-fichier"}]}}}
    verifier("5. PREUVE NEGATIVE : case v1 synthetique detectee",
             contient_case_v1(fake) and ("cases" in fake), "")

    # 6-7. Normes : ASCII strict + LF pur
    fichiers = [os.path.abspath(__file__)] + structures
    total_na = sum(ascii_count(f) for f in fichiers)
    verifier("6. ASCII strict : 0 non-ASCII (test + structures v2)",
             total_na == 0, "na=%d" % total_na)
    total_crlf = sum(crlf_count(f) for f in fichiers)
    verifier("7. LF pur : 0 CRLF (test + structures v2)",
             total_crlf == 0, "crlf=%d" % total_crlf)

    print()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())