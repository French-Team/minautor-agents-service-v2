#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-023-grep-budget-pondere.py
Test formel du GREP CROISE des seuils BUDGET PONDERE (protocole-verification-
coherence v0.2.0, etape E7) : garde-fou non-regression automatique.

Contexte (mission 2026-08-11) :
  - Le protocole-verification-coherence v0.2.0 exige que les 5 seuils du
    budget pondere (100 / 0,5 / 1 / 3,0 / 160) soient IDENTIQUES dans les
    6 fichiers : 3 specs (refonte, valider-case, guider-parcours),
    valider-case.md et les 2 codes (valider-case.py, generateurs-case.py).
  - Anti-recurrence : l'ancienne regle "> 3 indices" / "plus de 3 indices"
    doit etre ABSENTE des 6 fichiers.
  - Ce test materialise l'etape E7 comme garde-fou automatique : toute
    divergence de seuil ou tout retour de l'ancienne regle = KO.

Les 6 fichiers couverts (chemin relatif racine projet) :
  1. cerveau-projet/docs-dev-cerveau-projet/spec-refonte-cartes-decision.001.01.ebauche.md
  2. cerveau-projet/agents/tools/valider/valider-case/spec/spec-valider-case.001.01.ebauche.md
  3. cerveau-projet/agents/tools/guider/guider-parcours/spec/spec-guider-parcours.001.01.ebauche.md
  4. cerveau-projet/agents/tools/valider/valider-case/valider-case.md
  5. cerveau-projet/agents/tools/valider/valider-case/valider-case.py
     (constantes : SEUIL_COURT = 100, BUDGET_INDICES = 3.0, SEUIL_TEXTE = 160)
  6. cerveau-projet/agents/tools/generateurs/generateurs-case/generateurs-case.py
     (constantes : SEUIL_COURT = 100, BUDGET_INDICES = 3.0, SEUIL_REGLE_DEFAUT = 160)

Points couverts:
  P1-P4   : spec-refonte : '100 car' / '0,5' / '3,0' / '160' presents
  P5-P8   : spec-valider-case : idem
  P9-P12  : spec-guider-parcours : idem
  P13-P16 : valider-case.md : idem
  P17-P19 : valider-case.py : SEUIL_COURT = 100 / BUDGET_INDICES = 3.0 / SEUIL_TEXTE = 160
  P20-P22 : generateurs-case.py : SEUIL_COURT = 100 / BUDGET_INDICES = 3.0 / SEUIL_REGLE_DEFAUT = 160
  P23     : anti-recurrence : '> 3 indices' ABSENT des 6 fichiers
  P24     : anti-recurrence : 'plus de 3 indices' ABSENT des 6 fichiers
  P25     : ASCII strict : 0 non-ASCII (test)
  P26     : LF pur : 0 CRLF (test)

Usage:
  python3 test-023-grep-budget-pondere.py
Tags: conventions, budget, garde-fou
"""
import importlib.util
import io
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")


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

FICHIERS_TEXTES = [
    os.path.join(PROJECT_ROOT, "cerveau-projet", "docs-dev-cerveau-projet",
                 "spec-refonte-cartes-decision.001.01.ebauche.md"),
    os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools", "valider",
                 "valider-case", "spec", "spec-valider-case.001.01.ebauche.md"),
    os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools", "guider",
                 "guider-parcours", "spec", "spec-guider-parcours.001.01.ebauche.md"),
    os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools", "valider",
                 "valider-case", "valider-case.md"),
]

VALIDER_CASE_PY = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools",
                               "valider", "valider-case", "valider-case.py")
GENERATEURS_CASE_PY = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools",
                                   "generateurs", "generateurs-case", "generateurs-case.py")

TOUS_FICHIERS = FICHIERS_TEXTES + [VALIDER_CASE_PY, GENERATEURS_CASE_PY]

# Valeurs attendues par fichier texte (grep contextuel : pas de chiffre nu)
VALEURS_TEXTE = [
    ("100 car", "100 car"),
    ("0,5", "0,5"),
    ("3,0", "3,0"),
    ("160", "160"),
]

# Constantes attendues par fichier code
CONSTANTES_VALIDER_CASE = [
    ("SEUIL_COURT = 100", "SEUIL_COURT = 100"),
    ("BUDGET_INDICES = 3.0", "BUDGET_INDICES = 3.0"),
    ("SEUIL_TEXTE = 160", "SEUIL_TEXTE = 160"),
]
CONSTANTES_GENERATEURS_CASE = [
    ("SEUIL_COURT = 100", "SEUIL_COURT = 100"),
    ("BUDGET_INDICES = 3.0", "BUDGET_INDICES = 3.0"),
    ("SEUIL_REGLE_DEFAUT = 160", "SEUIL_REGLE_DEFAUT = 160"),
]

ANCIENNES_REGLES = ["> 3 indices", "plus de 3 indices"]

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


def lire(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        txt = fh.read()
    return sum(1 for c in txt if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def nom_fichier(chemin):
    return os.path.basename(chemin)


def main():
    global NB_POINTS, NB_OK, NB_KO

    # P1-P16 : les 4 valeurs dans chacun des 4 fichiers textes
    for fic in FICHIERS_TEXTES:
        txt = lire(fic)
        base = nom_fichier(fic)
        for i, (cle, aff) in enumerate(VALEURS_TEXTE, start=1):
            verifier("P%d. %s : '%s' present" % (i, base, aff),
                     cle in txt)

    # P17-P19 : constantes valider-case.py
    txt_vc = lire(VALIDER_CASE_PY)
    for i, (cle, aff) in enumerate(CONSTANTES_VALIDER_CASE, start=1):
        verifier("P%d. valider-case.py : '%s' present" % (16 + i, aff),
                 cle in txt_vc)

    # P20-P22 : constantes generateurs-case.py
    txt_gc = lire(GENERATEURS_CASE_PY)
    for i, (cle, aff) in enumerate(CONSTANTES_GENERATEURS_CASE, start=1):
        verifier("P%d. generateurs-case.py : '%s' present" % (19 + i, aff),
                 cle in txt_gc)

    # P23-P24 : anti-recurrence : anciennes regles ABSENTES des 6 fichiers
    contenus = [lire(f) for f in TOUS_FICHIERS]
    verifier("P23. anti-recurrence : '> 3 indices' absent des 6 fichiers",
             all("> 3 indices" not in c for c in contenus))
    verifier("P24. anti-recurrence : 'plus de 3 indices' absent des 6 fichiers",
             all("plus de 3 indices" not in c for c in contenus))

    # P25 : ASCII strict (test)
    total_non_ascii = ascii_count(os.path.abspath(__file__))
    verifier("P25. ASCII strict : 0 non-ASCII (test)", total_non_ascii == 0,
             "total = %d" % total_non_ascii)

    # P26 : LF pur (test)
    total_crlf = crlf_count(os.path.abspath(__file__))
    verifier("P26. LF pur : 0 CRLF (test)", total_crlf == 0,
             "total = %d" % total_crlf)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
