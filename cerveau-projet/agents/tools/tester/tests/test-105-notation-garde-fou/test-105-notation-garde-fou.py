#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-105-notation-garde-fou.py

Garde-fou de la routine notation v1 (transposee de la v2, decision
utilisateur 2026-08-29 : creer les routines v1 inspirees des v2).
La routine depose une demande periodique d evaluation croisee des agents
dans l inbox de Cerberus.

Points verifies :
  1. notation.py existe et porte le triplet (--dry-run, protections/options).
  2. Anti-inondation : demande_deja_en_attente() - non-lue dans l inbox
     de Cerberus OU depot recent (fichier .notation_derniere.txt).
  3. Delai anti-reexecution (DELAI_DEPOT_SECONDES = 600).
  4. Format du message : objet [NOTATION], vers=cerberus, priorite 2, lu=False.
  5. manifest.json reference la routine notation (actif, 300 s, script).
  6. grades-v1.json donne un grade G3 a notation (colonne Grade encart v1).
  7. Execution reelle --dry-run : rc=0, sortie conforme, AUCUN ecriture
     (ni inbox, ni fichier timestamp, ni historique).
  8. Anti-inondation reelle : avec un .notation_derniere.txt recent, la
     routine ne depose pas (message 'deja en attente - rien depose').

Proprietaire : Morpheus (testeur dedie)
Version : 0.1.0
Tags: notation, routine, garde-fou, anti-inondation, evaluation
"""
import importlib.util
import io
import json
import os
import subprocess
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

CERVEau = os.path.join(PROJECT_ROOT, "cerveau-projet")
TOOLS_DIR = os.path.join(CERVEau, "agents", "tools")
PYTHON = sys.executable

ORACLE_DIR = os.path.join(TOOLS_DIR, "oracle")
ROUTINES_DIR = os.path.join(ORACLE_DIR, "routines")
NOTATION = os.path.join(ROUTINES_DIR, "notation.py")
MANIFEST = os.path.join(ROUTINES_DIR, "manifest.json")
GRADES = os.path.join(ORACLE_DIR, "grades-v1.json")
INBOX_CERBERUS = os.path.join(ORACLE_DIR, "inbox", "cerberus.jsonl")
STATE_FILE = os.path.join(ROUTINES_DIR, ".notation_derniere.txt")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0

CHRONO_ACTIF = "--no-chrono" not in sys.argv
ISOLE = None
DESACTIVES = []
for i, arg in enumerate(sys.argv):
    if arg == "--isoler" and i + 1 < len(sys.argv):
        try:
            ISOLE = int(sys.argv[i + 1])
        except ValueError:
            ISOLE = None
    if arg == "--desactiver" and i + 1 < len(sys.argv):
        DESACTIVES = [int(x) for x in sys.argv[i + 1].split(",")
                      if x.strip().isdigit()]

DEBUT_TEST = time.monotonic()
ETAPES = []


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
    return PROTECTIONS.lancer_protege(cmd, capture_output=True, text=True,
                                      encoding="utf-8", errors="replace",
                                      timeout=timeout)


def lire(chemin):
    try:
        with io.open(chemin, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def _snap_inbox():
    """Nombre de messages [NOTATION] dans l inbox de Cerberus.
    On compte UNIQUEMENT les messages de cette routine (objet '[NOTATION]'),
    pas le total de l inbox : le daemon en arriere-plan ecrit d autres alertes
    (vigie, sante, live...) entre deux mesures - compter les lignes totales
    rendrait le test faux-negatif/flaky."""
    if not os.path.isfile(INBOX_CERBERUS):
        return 0
    n = 0
    for l in lire(INBOX_CERBERUS).splitlines():
        l = l.strip()
        if not l:
            continue
        if "[NOTATION]" in l:
            n += 1
    return n


def point_1_notation_existe():
    contenu = lire(NOTATION)
    ok = (os.path.isfile(NOTATION)
          and "--dry-run" in contenu
          and "demande_deja_en_attente" in contenu
          and "def main()" in contenu)
    verifier("1. notation.py existe avec --dry-run + anti-inondation", ok)


def point_2_anti_inondation():
    contenu = lire(NOTATION)
    ok = ("demande_deja_en_attente" in contenu
          and "not m.get(\"lu\")" in contenu
          and ".notation_derniere" in contenu)
    verifier("2. anti-inondation (non-lue OR depot recent)", ok)


def point_3_delai():
    contenu = lire(NOTATION)
    ok = ("DELAI_DEPOT_SECONDES" in contenu
          and "600" in contenu)
    verifier("3. delai anti-reexecution 600 s", ok)


def point_4_format_message():
    contenu = lire(NOTATION)
    ok = ("\"[NOTATION]\"" in contenu
          and "\"vers\": \"cerberus\"" in contenu
          and "priorite" in contenu and "2" in contenu
          and "\"lu\": False" in contenu)
    verifier("4. format message (objet [NOTATION], vers cerberus, P2, lu=False)", ok)


def point_5_manifest():
    try:
        data = json.loads(lire(MANIFEST))
    except ValueError:
        data = {}
    routines = data.get("routines_surveillance", [])
    notr = None
    for r in routines:
        if r.get("nom") == "notation":
            notr = r
    ok = (notr is not None
          and notr.get("actif") is True
          and notr.get("intervalles_secondes") == 300
          and notr.get("script") == "notation.py")
    verifier("5. manifest.json reference notation (actif, 300 s)", ok,
             "non trouve" if notr is None else "")


def point_6_grade():
    try:
        data = json.loads(lire(GRADES))
    except ValueError:
        data = {}
    ok = data.get("routines", {}).get("notation") == "G3"
    verifier("6. grades-v1 donne G3 a notation", ok,
             "grade=%s" % data.get("routines", {}).get("notation"))


def point_7_execution_dry_run():
    """7. --dry-run : rc=0 ET aucun effet de bord (inbox, timestamp,
    historique inchanges)."""
    av_inbox = _snap_inbox()
    av_state = os.path.isfile(STATE_FILE)
    r = run([PYTHON, NOTATION, "--dry-run"], timeout=60)
    ap_inbox = _snap_inbox()
    ap_state = os.path.isfile(STATE_FILE)
    ok = (r.returncode == 0
          and "[NOTATION]" in (r.stdout or "")
          and ap_inbox == av_inbox
          and ap_state == av_state)
    verifier("7. --dry-run rc=0 sans effet de bord", ok,
             "rc=%d inbox=%d->%d state=%s->%s %s" % (
                 r.returncode, av_inbox, ap_inbox, av_state, ap_state,
                 (r.stdout or "")[:120]))


def point_8_anti_inondation_reelle():
    """8. Avec un .notation_derniere.txt recent, ne depose pas."""
    av_inbox = _snap_inbox()
    try:
        with io.open(STATE_FILE, "w", encoding="utf-8") as fh:
            fh.write(str(time.time()))
        r = run([PYTHON, NOTATION, "--dry-run"], timeout=60)
        ap_inbox = _snap_inbox()
        ok = ("deja en attente" in (r.stdout or "")
              and ap_inbox == av_inbox)
        verifier("8. anti-inondation reelle (depot recent bloque)", ok,
                 "rc=%d %s" % (r.returncode, (r.stdout or "")[:120]))
    finally:
        if os.path.isfile(STATE_FILE):
            os.remove(STATE_FILE)


def main():
    print("=== test-105 : garde-fou routine notation v1 ===")
    points = [
        ("1. notation existe + triplet", point_1_notation_existe),
        ("2. anti-inondation", point_2_anti_inondation),
        ("3. delai 600 s", point_3_delai),
        ("4. format message", point_4_format_message),
        ("5. manifest notation", point_5_manifest),
        ("6. grade G3", point_6_grade),
        ("7. dry-run sans effet de bord", point_7_execution_dry_run),
        ("8. anti-inondation reelle", point_8_anti_inondation_reelle),
    ]
    for num, (nom, fn) in enumerate(points, start=1):
        if not point_actif(num):
            continue
        t_debut = time.monotonic()
        fn()
        if CHRONO_ACTIF:
            ETAPES.append((nom, time.monotonic() - t_debut))

    if CHRONO_ACTIF:
        total = time.monotonic() - DEBUT_TEST
        print("")
        print("=== CHRONO test (total %.1fs) ===" % total)
        for nom, duree in ETAPES:
            print("  %-34s %6.2fs" % (nom, duree))

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())