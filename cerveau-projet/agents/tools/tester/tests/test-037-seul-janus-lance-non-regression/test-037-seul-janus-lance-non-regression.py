#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-037-seul-janus-lance-non-regression.py
GARDE-FOU ANTI-RECURRENCE : SEUL la carte de Janus assigne
tester-lancer-non-regression (regle gouvernance 2026-08-13, demande
utilisateur).

Contexte (2026-08-13) :
  - L utilisateur a demande de verifier que SEUL Janus a le droit de lancer la
    non-regression complete (tester-lancer-non-regression) : sur une ligne de
    travail multi-agents, c est Janus a la fin qui la lance (dernier maillon
    avant Cerberus).
  - Il a aussi enonce une philosophie : les agents sont construits de la meme
    facon (meme template) mais chacun a SON identite et SON role - aucun
    interet a avoir des parcours identiques.
  - Audit Cerberus : les 11 cartes ont des signatures d ids TOUTES distinctes
    (principe identite deja respecte) ; 2 derives corrigees par Buffy :
    morpheus c12 (lanceur non-regression retire, tests individuels uniquement)
    et vulcain c8 (indice residuel retire). janus c4 Verifier les tests reste
    l UNIQUE carte avec tester-lancer-non-regression (legitime).
  - Fiche morpheus.md : REGLE ABSOLUE -- NON-REGRESSION JANUS ajoutee
    (Morpheus execute des tests individuels, JAMAIS la complete).

Invariants verifies :
  1. La carte janus (parcours-janus.json) contient tester-lancer-non-regression
     dans ses indices outil (Janus = controle final)
  2. AUCUNE des 10 autres cartes ne contient tester-lancer-non-regression dans
     ses indices outil (ni dans le texte des cases)
  3. La fiche morpheus.md contient la REGLE ABSOLUE -- NON-REGRESSION JANUS
     (anti-recurrence : Morpheus n execute que des tests individuels)
  4. Les 11 cartes ont des signatures de CONTENU TOUTES distinctes (identite
     des agents : meme construction - ids standards partages - mais jamais de
     parcours identiques en contenu). NB : le trio athena/promethee/minerve
     partage volontairement la MEME structure d ids (meme construction) avec
     des contenus differents (identites distinctes)
  5. Normes : ASCII strict + LF pur (cartes + fiche + test)
"""
import hashlib
import importlib.util
import io
import json
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

AGENTS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents")

# Les 11 agents (ordre stable pour la lecture)
AGENTS = [
    "cerberus", "buffy", "vulcain", "morpheus", "janus", "atlas",
    "themis", "clio", "athena", "promethee", "minerve",
]

OUTIL_NON_REGRESSION = "tester-lancer-non-regression"
FICHE_MORPHEUS = os.path.join(AGENTS_DIR, "morpheus", "morpheus.md")

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


def verifier(nom, ok, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if ok:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s -- %s" % (nom, detail))


def chemin_parcours(agent):
    return os.path.join(AGENTS_DIR, agent, "parcours", "parcours-%s.json" % agent)


def signature_contenu(cases):
    """Signature du CONTENU complet (ids + types + titres + suivants +
    branches) : identite reelle de la carte. Deux cartes au meme contenu =
    violation du principe d identite (jamais de parcours identiques)."""
    blocs = []
    for cid in sorted(cases.keys()):
        c = cases[cid]
        blocs.append("%s|%s|%s|%s|%s" % (
            cid, c.get("type"), c.get("titre"), c.get("suivant"),
            json.dumps(c.get("branches", []), sort_keys=True)))
    return hashlib.md5("\n".join(blocs).encode()).hexdigest()


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== Test formel seul-janus-lance-non-regression ===")

    # 1. Janus contient l outil (legitime)
    try:
        with io.open(chemin_parcours("janus"), encoding="utf-8") as fh:
            p_janus = json.load(fh)
        janus_contient = OUTIL_NON_REGRESSION in json.dumps(p_janus, ensure_ascii=True)
        verifier("1. La carte janus contient tester-lancer-non-regression (controle final)",
                 janus_contient, "introuvable dans parcours-janus.json")
    except Exception as e:
        p_janus = {}
        verifier("1. La carte janus contient tester-lancer-non-regression (controle final)",
                 False, str(e))

    # 2. Aucune des 10 autres cartes ne contient l outil
    derivees = []
    for agent in AGENTS:
        if agent == "janus":
            continue
        try:
            with io.open(chemin_parcours(agent), encoding="utf-8") as fh:
                p = json.load(fh)
            contenu = json.dumps(p, ensure_ascii=True)
            if OUTIL_NON_REGRESSION in contenu:
                derivees.append(agent)
        except Exception as e:
            derivees.append("%s(ERR %s)" % (agent, e))
    verifier("2. Aucune des 10 autres cartes ne contient tester-lancer-non-regression",
             len(derivees) == 0, "derivees=%s" % derivees)

    # 3. Fiche morpheus : REGLE ABSOLUE -- NON-REGRESSION JANUS
    try:
        fiche = io.open(FICHE_MORPHEUS, encoding="utf-8").read()
        verifier("3. Fiche morpheus : REGLE ABSOLUE -- NON-REGRESSION JANUS",
                 "NON-REGRESSION JANUS" in fiche and "SEUL JANUS" in fiche,
                 "regle introuvable")
    except Exception as e:
        verifier("3. Fiche morpheus : REGLE ABSOLUE -- NON-REGRESSION JANUS",
                 False, str(e))

    # 4. Identite : signatures de CONTENU TOUTES distinctes (jamais de parcours
    # identiques en contenu ; le partage des ids standards = meme construction
    # voulue, pas une violation)
    signatures = {}
    doublons = []
    for agent in AGENTS:
        try:
            with io.open(chemin_parcours(agent), encoding="utf-8") as fh:
                p = json.load(fh)
            sig = signature_contenu(p.get("cases", {}))
            if sig in signatures:
                doublons.append("%s==%s(%s)" % (signatures[sig], agent, sig[:8]))
            else:
                signatures[sig] = agent
        except Exception as e:
            doublons.append("%s(ERR %s)" % (agent, e))
    verifier("4. Les 11 cartes ont des signatures de CONTENU TOUTES distinctes (identite)",
             len(doublons) == 0 and len(signatures) == 11,
             "doublons=%s nb_sig=%d" % (doublons, len(signatures)))

    # 5. Normes : ASCII strict + LF pur (11 cartes + fiche morpheus + test)
    normes_ko = []
    for f in [chemin_parcours(a) for a in AGENTS] + [FICHE_MORPHEUS, os.path.abspath(__file__)]:
        try:
            txt = io.open(f, encoding="utf-8", errors="replace").read()
            if any(ord(c) > 127 for c in txt):
                normes_ko.append("%s non-ascii" % os.path.basename(f))
            raw = io.open(f, "rb").read()
            if b"\r\n" in raw:
                normes_ko.append("%s crlf" % os.path.basename(f))
        except Exception as e:
            normes_ko.append("%s ERR %s" % (os.path.basename(f), e))
    verifier("5. Normes ASCII strict + LF pur (11 cartes + fiche + test)",
             len(normes_ko) == 0, "ko=%s" % normes_ko)

    print()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
