#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-059-seul-morpheus-ecrit-les-tests.py
GARDE-FOU : SEUL Morpheus ecrit et execute les tests (regle gouvernance
2026-08-15, demande utilisateur : etendre le modele de confiance - chaque
exclusivite doit avoir sa regle immuable + son garde-fou complet).

Contexte :
  - La regle immuable "SEUL MORPHEUS ECRIT ET EXECUTE LES TESTS" existe dans
    regles-groupes-agents.md mais etait referencee vers test-037 qui ne
    verifie QUE la non-regression de Janus (point 3 : fiche morpheus) - AUCUN
    test ne verifiait le comportement de l exclusivite des TESTS.
  - Cette audit 2026-08-15 a revele la faille : tester-protections (le point
    d entree des protections, cree et maintenu par Morpheus) n avait pas de
    verrou carte/registre.

Invariants verifies :
  1. La table d habilitation de morpheus (habilitation-morpheus.json)
     contient tester-protections (le testeur = proprietaire des protections)
  2. AUCUNE table AUTRE que morpheus ET janus ne contient tester-protections :
     janus est autorise car il lance la non-regression (tester-lancer-
     non-regression importe les protections en interne) - mais AUCUN autre
     agent ne l a en table
  3. Le REGISTRE du jour courant ne contient AUCUNE declaration de
     tester-protections par un agent autre que morpheus (seul le testeur
     declare l outil ; janus declare tester-lancer-non-regression)
  4. La table morpheus reference le domaine tester/ (tester-protections
     pointe vers cerveau-projet/agents/tools/tester/, present dans
     index-tools.md)
  5. La regle immuable est documentee dans regles-groupes-agents.md
     (section SEUL MORPHEUS ECRIT ET EXECUTE LES TESTS)
  6. La fiche morpheus.md contient la REGLE ABSOLUE -- NON-REGRESSION JANUS
     (Morpheus execute des tests individuels, JAMAIS la complete)
  7. Normes : ASCII strict + LF pur (arbre + fiche + regle + test)
Tags: agents, morpheus, garde-fou
"""
import glob
import importlib.util
import io
import json
import os
import sys
import time
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)
TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
AGENTS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents")
PYTHON = sys.executable
OUTIL_TEST = "tester-protections"
REGISTRE = os.path.join(AGENTS_DIR, "traces", "registre-usages-outils.jsonl")
FICHE_MORPHEUS = os.path.join(AGENTS_DIR, "morpheus", "morpheus.md")
REGLES = os.path.join(AGENTS_DIR, "regles-immuables", "general",
                      "regles-groupes-agents.md")
HABILITATION_DIR = os.path.join(AGENTS_DIR, "habilitation")
INDEX_TOOLS = os.path.join(TOOLS_DIR, "index-tools.md")
# Les agents (arbres reels : dossier parcours contenant arbre-<agent>.json)
AGENTS = sorted(a for a in os.listdir(AGENTS_DIR)
                if os.path.isfile(os.path.join(AGENTS_DIR, a, "parcours",
                                               "arbre-%s.json" % a)))


def outils_table(agent):
    """Ensemble des outils d une table d habilitation (None si absente)."""
    chemin = os.path.join(HABILITATION_DIR, "habilitation-%s.json" % agent)
    if not os.path.isfile(chemin):
        return None
    d = json.load(io.open(chemin, encoding="utf-8"))
    noms = set()
    for o in d.get("outils", []):
        noms.add((o.get("nom", "") if isinstance(o, dict) else o))
    return noms


NB_POINTS = 0
NB_OK = 0
NB_KO = 0
# ------------------------------------------------------------------
# OPTIONS ON/OFF + CHRONO (regle immuable v0.3.0) :
#   --no-chrono            desactive le chrono (defaut : actif)
#   --isoler N             n execute que le point N (diagnostic cible)
#   --desactiver 1,3,5     saute les points listes (sans toucher au code)
# ------------------------------------------------------------------
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
    print("=== CHRONO test-059 (total %.1fs) ===" % total)
    for nom, duree in ETAPES:
        print("  %-34s %6.2fs" % (nom, duree))


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


def lancer(cmd, timeout=60, **kwargs):
    return PROTECTIONS.lancer_protege(cmd, timeout=timeout, **kwargs)


def lire(chemin):
    with io.open(chemin, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def main():
    # --- 1. Morpheus contient tester-protections (legitime)
    if point_actif(1):
        t = time.monotonic()
        noms = outils_table("morpheus")
        verifier("1. table morpheus contient tester-protections",
                 noms is not None and OUTIL_TEST in noms,
                 "introuvable dans habilitation-morpheus.json")
        chrono_etape("1. table morpheus", t)

    # --- 2. Seuls morpheus ET janus (non-regression) ont tester-protections
    if point_actif(2):
        t = time.monotonic()
        autorises = {"morpheus", "janus"}
        derivees = []
        for agent in AGENTS:
            noms = outils_table(agent)
            if noms is None:
                continue
            if OUTIL_TEST in noms and agent not in autorises:
                derivees.append(agent)
        verifier("2. tester-protections uniquement dans morpheus + janus (non-regression)",
                 len(derivees) == 0, "derivees=%s" % derivees)
        chrono_etape("2. exclusivite tables", t)

    # --- 3. Registre du jour : seul morpheus declare tester-protections
    if point_actif(3):
        t = time.monotonic()
        import datetime as _dt059
        jour = _dt059.date.today().strftime("%Y-%m-%d")
        derivees = []
        try:
            with io.open(REGISTRE, encoding="utf-8") as fh:
                for ligne in fh:
                    ligne = ligne.strip()
                    if not ligne:
                        continue
                    try:
                        entree = json.loads(ligne)
                    except Exception:
                        continue
                    if entree.get("outil") != OUTIL_TEST:
                        continue
                    if not str(entree.get("date", "")).startswith(jour):
                        continue
                    agent = entree.get("agent", "?")
                    if agent != "morpheus":
                        derivees.append("%s (%s)" % (agent, entree.get("date", "")))
        except Exception as e:
            derivees.append("ERR %s" % e)
        verifier("3. registre du jour : seul morpheus declare tester-protections",
                 len(derivees) == 0, "derivees=%s" % derivees)
        chrono_etape("3. registre", t)

    # --- 4. La table morpheus reference le domaine tester/ (via
    #      tester-protections, pointe dans index-tools.md)
    if point_actif(4):
        t = time.monotonic()
        noms = outils_table("morpheus")
        index = lire(INDEX_TOOLS)
        verifier("4. table morpheus reference le domaine tester/ (tester-protections)",
                 noms is not None and OUTIL_TEST in noms
                 and "tester/tester-protections/" in index,
                 "chemin tester/tester-protections/ introuvable dans index-tools.md")
        chrono_etape("4. domaine tests", t)

    # --- 5. Regle immuable documentee
    if point_actif(5):
        t = time.monotonic()
        try:
            regles = lire(REGLES)
            verifier("5. regle immuable documentee (SEUL MORPHEUS ECRIT ET EXECUTE LES TESTS)",
                     "SEUL MORPHEUS ECRIT ET EXECUTE LES TESTS" in regles,
                     "section introuvable dans regles-groupes-agents.md")
        except Exception as e:
            verifier("5. regle immuable documentee", False, str(e))
        chrono_etape("5. regle immuable", t)

    # --- 6. Fiche morpheus : REGLE ABSOLUE -- NON-REGRESSION JANUS
    if point_actif(6):
        t = time.monotonic()
        try:
            fiche = lire(FICHE_MORPHEUS)
            verifier("6. fiche morpheus : REGLE ABSOLUE -- NON-REGRESSION JANUS",
                     "NON-REGRESSION JANUS" in fiche and "SEUL JANUS" in fiche,
                     "regle introuvable")
        except Exception as e:
            verifier("6. fiche morpheus : REGLE ABSOLUE -- NON-REGRESSION JANUS",
                     False, str(e))
        chrono_etape("6. fiche morpheus", t)

    # --- 7. Normes : ASCII strict + LF pur
    if point_actif(7):
        t = time.monotonic()
        normes_ko = []
        for f in [os.path.join(AGENTS_DIR, "morpheus", "parcours",
                               "arbre-morpheus.json"), FICHE_MORPHEUS, REGLES,
                  os.path.abspath(__file__)]:
            try:
                txt = lire(f)
                if any(ord(c) > 127 for c in txt):
                    normes_ko.append("%s non-ascii" % os.path.basename(f))
                raw = open(f, "rb").read()
                if b"\r\n" in raw:
                    normes_ko.append("%s crlf" % os.path.basename(f))
            except Exception as e:
                normes_ko.append("%s ERR %s" % (os.path.basename(f), e))
        verifier("7. normes ASCII strict + LF pur (carte + fiche + regle + test)",
                 len(normes_ko) == 0, "ko=%s" % normes_ko)
        chrono_etape("7. normes", t)

    bilan_chrono()
    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    print("VERDICT : %s" % ("CONFORME" if NB_KO == 0 else "NON CONFORME"))
    print("BILAN : seul Morpheus ecrit et execute les tests si 0 KO")
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
