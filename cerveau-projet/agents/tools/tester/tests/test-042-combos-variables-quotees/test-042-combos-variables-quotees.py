#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-042-combos-variables-quotees.py
GARDE-FOU ANTI-RECURRENCE : dans les definitions-combo.json, chaque {var}
interpolee dans une commande de case outil DOIT etre quote (guillemets
simples ou doubles) - sauf quand la commande est EXACTEMENT {var} (commande
entiere generee, legitime sans quotes).

Contexte (2026-08-13) :
  - La regle anti-echappement etendue aux combos (combos-moteur.md v0.3.3)
    documente le piege : l interpolation {var} est BRUTE puis shlex.split
    decoupe la commande - une valeur avec apostrophe ou espaces non quote
    casse la commande en ValueError.
  - Analyse initiale : 14 definitions-combo.json, 51 commandes de cases
    outil : 22 commandes = exactement {var} (commandes entieres generees),
    21 sans variable, 8 commandes avec {var} NON quote en argument (corrigees
    par cette mission).
  - Demande utilisateur : un garde-fou verifie en permanence que les
    commandes des definitions-combo.json quotent leurs variables - si une
    nouvelle definition introduit {var} non quote, la non-regression le
    signale immediatement.

REGLE D AJOUT : toute NOUVELLE definition-combo.json (dans
cerveau-projet/agents/tools/combos/*/definition-combo.json) est scannee
automatiquement : commande = exactement {var} -> OK ; sinon chaque {var}
doit etre entre guillemets simples ou doubles -> sinon KO.

Invariants verifies :
  1. Toutes les definitions-combo.json existent (une par dossier combos)
  2. Chaque case outil avec commande est scannee
  3. Commande = exactement {var} -> OK (commande entiere generee)
  4. Sinon, chaque {var} est entre guillemets (simples ou doubles) -> sinon KO
  5. Normes : ASCII strict + LF pur (definitions + test)
Tags: outils, combos, garde-fou, anti-recurrence
"""
import glob
import importlib.util
import io
import json
import os
import re
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
COMBOS_DIR = os.path.join(TOOLS_DIR, "combos")
PYTHON = sys.executable

NB_POINTS = 0
NB_OK = 0
NB_KO = 0


def charger_protections():
    """Importe le point d entree unique des protections (test-030 le verifie)."""
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


def variables_non_quotees(commande):
    """Retourne la liste des {var} non quotes dans une commande.

    - commande = exactement {var} (commande entiere generee) -> OK ([]).
    - sinon, chaque {var} doit etre entoure de guillemets simples/doubles.
    """
    if not commande or re.fullmatch(r"\{[A-Za-z0-9_-]+\}", commande.strip()):
        return []
    non_quotees = []
    for m in re.finditer(r"\{([A-Za-z0-9_-]+)\}", commande):
        debut = m.start()
        avant = commande[max(0, debut - 1):debut]
        fin = m.end()
        apres = commande[fin:fin + 1]
        if avant not in ("'", '"') or apres not in ("'", '"'):
            non_quotees.append(m.group(1))
    return non_quotees


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== Test formel combos-variables-quotees ===")
    try:
        definitions = sorted(glob.glob(os.path.join(COMBOS_DIR, "*", "definition-combo.json")))
        verifier("1. Definitions-combo.json presentes (%d combos)" % len(definitions),
                 len(definitions) >= 14, "trouvees=%d" % len(definitions))

        total_cases_outil = 0
        total_non_quotees = 0
        for chemin in definitions:
            with io.open(chemin, encoding="utf-8") as fh:
                j = json.load(fh)
            nom = j.get("combo", {}).get("nom", os.path.basename(os.path.dirname(chemin)))
            for cid, case in j.get("cases", {}).items():
                if case.get("type") != "outil":
                    continue
                commande = case.get("commande")
                if not commande:
                    continue
                total_cases_outil += 1
                non_quotees = variables_non_quotees(commande)
                if non_quotees:
                    total_non_quotees += 1
                    verifier("2. %s %s : {var} quotes" % (nom, cid),
                             False, "non quotes: %s | %s" % (",".join(non_quotees), commande[:80]))

        verifier("3. %d commandes outil scannees, 0 {var} non quote"
                 % total_cases_outil, total_non_quotees == 0,
                 "non quotees=%d" % total_non_quotees)

        # Normes : ASCII strict + LF pur (definitions + test)
        fichiers = definitions + [os.path.abspath(__file__)]
        total_non_ascii = sum(ascii_count(f) for f in fichiers if os.path.isfile(f))
        verifier("4. ASCII strict : 0 non-ASCII (definitions + test)",
                 total_non_ascii == 0, "total=%d" % total_non_ascii)
        total_crlf = sum(crlf_count(f) for f in fichiers if os.path.isfile(f))
        verifier("5. LF pur : 0 CRLF (definitions + test)",
                 total_crlf == 0, "total=%d" % total_crlf)
    except PROTECTIONS.ArretProtection as e:
        print("  [KO] ARRET PROTECTION : %s" % e.message)
        NB_KO += 1

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
