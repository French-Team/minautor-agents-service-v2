#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-072-c0-c0b-relecture.py
CHASSEUR DE VESTIGES V1 (migration v1->v2, 2026-09-05) : la relecture
obligatoire vivait dans les CASES v1 c0/c0b des parcours (type action +
question avec branches OUI->c0c / NON->c0). Les parcours v1 sont RETIRES :
la relecture est une REGLE des arbres v2 (regles D7 : RELIRE OBLIGATOIRE),
plus de cases.

Ce test PISTE les vestiges : si une structure v2 contient encore des cases
nommees c0/c0b/c0c (format v1) ou une cle "cases", le test ECHOUE.

Points verifies :
  1. Aucun fichier parcours-*.json (v1) ne subsiste dans les agents.
  2. Les structures v2 ne portent AUCUNE cle top-level "cases".
  3. Aucune case v1 (cle de case "c0", "c0b", "c0c" ou type action avec
     indices) dans les structures v2.
  4. La regle de relecture v2 est presente dans les arbres (D7/RELIRE).
  5. PREUVE NEGATIVE : une structure synthetique v1 (cases c0/c0b) est
     DETECTEE par le scan de vestiges.
  6. Normes : ASCII strict + LF pur (test + structures v2 scannees).
Tags: vestiges, v1, migration, relecture, garde-fou
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


def detecter_cases_v1(donnees, prefixe=""):
    """Detecte une case v1 (cle c0/c0b/c0c ou type action + indices)."""
    if isinstance(donnees, dict):
        for k, v in donnees.items():
            if k in ("c0", "c0b", "c0c") and isinstance(v, dict):
                return True
            if isinstance(v, dict) and isinstance(v.get("indices"), list) \
                    and v.get("type") in ("action", "fin", "question"):
                return True
            if detecter_cases_v1(v, prefixe + k + "."):
                return True
        return False
    if isinstance(donnees, list):
        return any(detecter_cases_v1(v, prefixe) for v in donnees)
    return False


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== Chasseur de vestiges v1 : c0/c0b relecture (format v1) ===")

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

    # 4. Aucune case c0/c0b/c0c ni case action+indices dans les structures v2
    avec_case = []
    for f in structures:
        try:
            d = json.load(io.open(f, encoding="utf-8"))
        except Exception:
            continue
        if detecter_cases_v1(d):
            avec_case.append(os.path.basename(f))
    verifier("4. aucune case c0/c0b/c0c v1 dans les structures v2",
             len(avec_case) == 0, "avec_case=%s" % avec_case[:5])

    # 5. La relecture v2 est une REGLE des arbres (D7 RELIRE OBLIGATOIRE)
    regles_relecture = []
    for f in glob.glob(os.path.join(AGENTS, "*", "parcours", "arbre-*.json")):
        try:
            d = json.load(io.open(f, encoding="utf-8"))
        except Exception:
            continue
        regles = (d.get("arbre", {}) or {}).get("regles", {}) if \
            isinstance(d.get("arbre"), dict) else {}
        texte = json.dumps(regles, ensure_ascii=True)
        if "RELIRE" in texte.upper() or "relecture" in texte.lower():
            regles_relecture.append(os.path.basename(f))
    verifier("5. regle de relecture v2 presente dans les arbres (%d)"
             % len(regles_relecture), len(regles_relecture) >= 15,
             "nb=%d" % len(regles_relecture))

    # 6. PREUVE NEGATIVE : une structure synthetique v1 est DETECTEE
    fake = {"parcours": {"agent": "x"}, "cases": {
        "c0": {"type": "action", "titre": "RELIRE OBLIGATOIRE",
               "suivant": "c0b"},
        "c0b": {"type": "question", "titre": "As-tu relu ?",
                "branches": [{"reponse": "OUI", "vers": "c0c"},
                             {"reponse": "NON", "vers": "c0"}]}}}
    verifier("6. PREUVE NEGATIVE : c0/c0b synthetique detectee",
             detecter_cases_v1(fake) and ("cases" in fake), "")

    # 7-8. Normes : ASCII strict + LF pur
    fichiers = [os.path.abspath(__file__)] + structures
    total_na = sum(ascii_count(f) for f in fichiers)
    verifier("7. ASCII strict : 0 non-ASCII (test + structures v2)",
             total_na == 0, "na=%d" % total_na)
    total_crlf = sum(crlf_count(f) for f in fichiers)
    verifier("8. LF pur : 0 CRLF (test + structures v2)",
             total_crlf == 0, "crlf=%d" % total_crlf)

    print()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())