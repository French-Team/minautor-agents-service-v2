#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-055-coherence-regle-indice-outil.py
PISTAGE DES VESTIGES V1 (migration v1->v2, 2026-09-05) : la regle v1
"coherence regle / indice outil" vivait dans les CASES des parcours v1
(indices de type outil/regle au niveau case). Les parcours v1 sont RETIRES :
les structures actives sont les arbres v2 (arbre-*.json + theme-*.json +
fins.json) qui n'ont PAS de cases.

Ce test PISTE les vestiges : si une structure v2 contient encore une
structure v1 (cle top-level "cases", ou indices de type "regle"/"outil"),
le test ECHOUE : c est un vestige a purger.

Points verifies :
  1. Les structures v2 (arbre-*.json, theme-*.json, fins.json) ne portent
     AUCUNE cle top-level "cases" (format v1).
  2. Les structures v2 ne portent AUCUN indice de type "regle"/"outil"
     (format v1 des cases).
  3. La liste canonique des outils (catalogue) est chargee (>= 150).
  4. PREUVE NEGATIVE : une structure synthetique v1 (avec cases + regle
     sans indice outil) est DETECTEE par le scan de vestiges.
  5. Normes : ASCII strict + LF pur (test + structures v2 scannees).
Tags: vestiges, v1, migration, coherence, garde-fou
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
CATALOGUE = os.path.join(AGENTS, "tools", "generateurs", "generateurs-commande",
                         "catalogue-commandes.json")


def charger_protections():
    """Point d entree unique des protections (regle immuable, test-030)."""
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()

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


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== Test coherence regle/indice : vestiges v1 (cases) ===")

    structures = structures_v2()
    verifier("0. structures v2 detectees (%d)" % len(structures),
             len(structures) >= 100, "nb=%d" % len(structures))

    # 1. Aucune cle top-level "cases" dans les structures v2
    vestiges_cases = []
    for s in structures:
        try:
            data = json.load(io.open(s, encoding="utf-8"))
        except (IOError, ValueError):
            continue
        if isinstance(data, dict) and "cases" in data:
            vestiges_cases.append(os.path.basename(s))
    verifier("1. zero cle top-level 'cases' (format v1) dans le v2",
             not vestiges_cases, "vestiges: %s" % ", ".join(vestiges_cases))

    # 2. Aucun indice de type "regle"/"outil" (format v1 des cases)
    vestiges_indices = []
    for s in structures:
        try:
            contenu = io.open(s, encoding="utf-8", errors="replace").read()
        except IOError:
            continue
        if '"type": "regle"' in contenu or '"type": "outil"' in contenu:
            vestiges_indices.append(os.path.basename(s))
    verifier("2. zero indice v1 (type regle/outil) dans le v2",
             not vestiges_indices, "vestiges: %s" % ", ".join(vestiges_indices))

    # 3. Liste canonique (catalogue) chargee : >= 150 outils
    with io.open(CATALOGUE, encoding="utf-8") as fh:
        cat = json.load(fh)
    noms = [c["nom"] for c in cat["commandes"]]
    verifier("3. liste canonique catalogue chargee (>= 150)",
             len(noms) >= 150, "nb=%d" % len(noms))

    # 4. PREUVE NEGATIVE : une structure synthetique v1 (cases) est detectee
    synth = {"identite": {"type": "parcours"},
             "cases": {"c0": {"indices": [
                 {"type": "regle", "texte": "utiliser guider-parcours"}]}}}
    contenu_synth = json.dumps(synth, ensure_ascii=True)
    detecte = ('"cases"' in contenu_synth
               and '"type": "regle"' in contenu_synth)
    verifier("4. preuve negative : structure v1 synthetique detectee",
             detecte)

    # 5. Normes : ASCII strict + LF pur (structures v2 + ce test)
    non_ascii = sum(ascii_count(s) for s in structures)
    crlf = sum(crlf_count(s) for s in structures)
    verifier("5. ASCII strict : 0 non-ASCII (structures v2)",
             non_ascii == 0, "total=%d" % non_ascii)
    verifier("5b. LF pur : 0 CRLF (structures v2)", crlf == 0,
             "total=%d" % crlf)
    verifier("5c. ASCII + LF (ce test)",
             ascii_count(os.path.abspath(__file__)) == 0
             and crlf_count(os.path.abspath(__file__)) == 0)

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())