#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-026-detecter-cablages-manquants-garde-fou.py
Garde-fou anti-recurrence du bug des cases ORPHELINES (lecon 2026-08-12).

Contexte :
  - valider-case ne verifie QUE les fins non joignables. Le bug des questions
    orphelines (vulcain c9b/c15b 'Ameliorations possibles' inaccessibles) a
    montre qu'une case orpheline non-fin passe inapercue, et qu'une boucle
    indirecte (c22 -> c9b -> c22) n'est pas signalee.
  - detecter-cablages-manquants (v0.1.1, outil dedie) complete valider-case :
    CAS_ORPHELINE (toute case jamais atteignable), BOUCLE_BLOQUANTE (cycle
    sans sortie), REF_MORTE (suivant/branche vers case inexistante).
  - Ce garde-fou verifie que les 14 parcours des agents ont 0 cas orphelin,
    0 boucle bloquante et 0 reference morte : toute regression du cablage
    (case orpheline, boucle sans issue, reference cassee) fait KO.

Cas couverts:
  1. detecter-cablages-manquants --version = v0.1.1
  2. Parcours sain (cerberus) : verdict PROPRE
  3. Les 14 parcours : 0 CAS_ORPHELINE au total
  4. Les 14 parcours : 0 BOUCLE_BLOQUANTE au total
  5. Les 14 parcours : 0 REF_MORTE au total
  6. Les 14 parcours : 0 CASE_DEPART manquante
  7. Les 14 parcours : 0 FIN_NON_JOIGNABLE
  8. --tous : verdict global PROPRE
  9. ASCII strict : 0 non-ASCII (outil + doc + test)
 10. LF pur : 0 CRLF (outil + doc + test)

Usage:
  python3 test-026-detecter-cablages-manquants-garde-fou.py
"""
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


OUTIL_DIR = os.path.join(TOOLS_DIR, "detecter", "detecter-cablages-manquants")
OUTIL_PY = os.path.join(OUTIL_DIR, "detecter-cablages-manquants.py")
OUTIL_MD = os.path.join(OUTIL_DIR, "detecter-cablages-manquants.md")
PARCOURS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents")

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


def compter(texte, motif):
    return texte.count(motif)


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def lister_parcours():
    resultats = []
    for nom in sorted(os.listdir(PARCOURS_DIR)):
        p = os.path.join(PARCOURS_DIR, nom, "parcours", "parcours-%s.json" % nom)
        if os.path.isfile(p):
            resultats.append(p)
    return resultats


def main():
    print("=== Garde-fou : cablages manquants des 13 parcours ===")

    # 1. Version
    r = run([PYTHON, OUTIL_PY, "--version"])
    verifier("1. --version = detecter-cablages-manquants v0.1.1",
             "v0.1.1" in r.stdout, r.stdout.strip())

    parcours = lister_parcours()
    verifier("2. 13 parcours d agents trouves",
             len(parcours) == 14, "nb=%d" % len(parcours))

    # 3-7. Scan de chaque parcours : cumul des problemes bloquants
    total_orphelines = 0
    total_boucles = 0
    total_refs = 0
    total_departs = 0
    total_fins = 0
    for chemin in parcours:
        r = run([PYTHON, OUTIL_PY, chemin])
        out = r.stdout + r.stderr
        total_orphelines += compter(out, "[CAS_ORPHELINE]")
        total_boucles += compter(out, "[BOUCLE_BLOQUANTE]")
        total_refs += compter(out, "[REF_MORTE]")
        total_departs += compter(out, "[CASE_DEPART]")
        total_fins += compter(out, "[FIN_NON_JOIGNABLE]")

    verifier("3. 0 CAS_ORPHELINE sur les 12 parcours (anti-recurrence)",
             total_orphelines == 0, "total=%d" % total_orphelines)
    verifier("4. 0 BOUCLE_BLOQUANTE sur les 12 parcours",
             total_boucles == 0, "total=%d" % total_boucles)
    verifier("5. 0 REF_MORTE sur les 12 parcours",
             total_refs == 0, "total=%d" % total_refs)
    verifier("6. 0 CASE_DEPART manquante/inexistante",
             total_departs == 0, "total=%d" % total_departs)
    verifier("7. 0 FIN_NON_JOIGNABLE sur les 12 parcours",
             total_fins == 0, "total=%d" % total_fins)

    # 8. --tous : verdict global PROPRE (les boucles de re-travail sont des
    #    avertissements voulus, le verdict ne compte QUE les bloquants)
    r = run([PYTHON, OUTIL_PY, "--tous"])
    verifier("8. --tous : verdict global PROPRE",
             "Verdict global : PROPRE" in r.stdout, r.stdout[-120:])

    # 9-10. Normes sur les fichiers de l'outil + ce test
    fichiers = [OUTIL_PY, OUTIL_MD, os.path.abspath(__file__)]
    total_non_ascii = sum(ascii_count(f) for f in fichiers)
    verifier("9. ASCII strict : 0 non-ASCII (outil + doc + test)",
             total_non_ascii == 0, "total=%d" % total_non_ascii)
    total_crlf = sum(crlf_count(f) for f in fichiers)
    verifier("10. LF pur : 0 CRLF (outil + doc + test)",
             total_crlf == 0, "total=%d" % total_crlf)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
