#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-104-vigie-round-garde-fou.py

Garde-fou de la decision utilisateur 2026-08-28 (les deux en cascade) :
la routine vigie-round (detection des rounds casses) et la correction du
pilote Oracle (le pilote ne doit plus derouler tout l arbre ni activer
les maillons automatiquement).

Points verifies :
  1. vigie-round.py existe et porte le triplet (--dry-run, --seuil-minutes,
     --no-chrono).
  2. Detection session-orpheline : format 4W (QUI/QUOI/QUAND/OU).
  3. Detection chaine-en-attente (etat de carte etape=fin).
  4. Anti-spam (ALERTE_REPETITION_MINUTES + etat-vigie.json).
  5. manifest.json reference la routine vigie-round (actif, 60 s).
  6. Execution reelle --dry-run : rc=0, sortie conforme.
  7. Pilote Oracle : limite par defaut 1 pas (pas de deroulage complet).
  8. Pilote Oracle : mission + ordre de demarrer servis en tete.
  9. Pilote Oracle : plus d activation automatique des maillons.
 10. oracle.py : parser pilote --limite par defaut 1.

Proprietaire : Morpheus (testeur dedie)
Version : 0.1.0
Tags: vigie, round, oracle, pilote, garde-fou, anti-recurrence
"""
import importlib.util
import io
import json
import os
import re
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
VIGIE = os.path.join(ORACLE_DIR, "routines", "vigie-round.py")
VIGIE_DOC = os.path.join(ORACLE_DIR, "routines", "vigie-round.md")
MANIFEST = os.path.join(ORACLE_DIR, "routines", "manifest.json")
PILOTE = os.path.join(ORACLE_DIR, "fonctions", "pilote.py")
ORACLE_PY = os.path.join(ORACLE_DIR, "oracle.py")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0

# ------------------------------------------------------------------
# OPTIONS ON/OFF + CHRONO (regle immuable v0.3.0)
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


def bilan_chrono():
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - DEBUT_TEST
    print("")
    print("=== CHRONO test (total %.1fs) ===" % total)
    for nom, duree in ETAPES:
        print("  %-34s %6.2fs" % (nom, duree))


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


def point_1_vigie_existe_triplet():
    """1. vigie-round.py existe + triplet protections/options/chrono."""
    contenu = lire(VIGIE)
    ok = (os.path.isfile(VIGIE)
          and "--dry-run" in contenu
          and "--seuil-minutes" in contenu
          and "--no-chrono" in contenu
          and "def main()" in contenu)
    verifier("1. vigie-round.py existe avec triplet", ok,
             "dry-run=%s seuil=%s no-chrono=%s" % (
                 "--dry-run" in contenu, "--seuil-minutes" in contenu,
                 "--no-chrono" in contenu))


def point_2_4w_session_orpheline():
    """2. Detection session-orpheline au format 4W."""
    contenu = lire(VIGIE)
    ok = ("[session-orpheline]" in contenu
          and "QUI:" in contenu and "QUOI:" in contenu
          and "QUAND:" in contenu and "OU:" in contenu)
    verifier("2. detection session-orpheline format 4W", ok,
             "motifs manquants" if not ok else "")


def point_3_chaine_en_attente():
    """3. Detection chaine-en-attente (etat de carte etape=fin)."""
    contenu = lire(VIGIE)
    ok = ("[chaine-en-attente]" in contenu
          and "etape" in contenu and "fin" in contenu)
    verifier("3. detection chaine-en-attente", ok)


def point_4_anti_spam():
    """4. Anti-spam : ALERTE_REPETITION_MINUTES + etat-vigie.json."""
    contenu = lire(VIGIE)
    ok = ("ALERTE_REPETITION_MINUTES" in contenu
          and "etat-vigie.json" in contenu)
    verifier("4. anti-spam (30 min, etat-vigie.json)", ok)


def point_5_manifest():
    """5. manifest.json reference vigie-round actif toutes les 60 s."""
    try:
        data = json.loads(lire(MANIFEST))
    except ValueError:
        data = {}
    routines = data.get("routines_surveillance", [])
    vigie = None
    for r in routines:
        if r.get("nom") == "vigie-round":
            vigie = r
    ok = (vigie is not None
          and vigie.get("actif") is True
          and vigie.get("intervalles_secondes") == 60
          and vigie.get("script") == "vigie-round.py")
    verifier("5. manifest.json reference vigie-round (actif, 60 s)", ok,
             "non trouve" if vigie is None else "")


def point_6_execution_reelle():
    """6. Execution reelle --dry-run : rc=0 + sortie conforme."""
    r = run([PYTHON, VIGIE, "--dry-run", "--no-chrono"], timeout=60)
    ok = (r.returncode == 0 and "[VIGIE-ROUND]" in (r.stdout or ""))
    verifier("6. execution reelle --dry-run rc=0", ok,
             "rc=%d %s" % (r.returncode, (r.stdout or "")[:150]))


def point_7_limite_1():
    """7. Pilote : limite par defaut 1 pas."""
    contenu = lire(PILOTE)
    ok = ('getattr(args, "limite", 1)' in contenu
          and 'default=1' in contenu)
    verifier("7. pilote limite par defaut 1 pas", ok)


def point_8_mission_ordre_tete():
    """8. Pilote : mission + ordre de demarrer en tete du plateau."""
    contenu = lire(PILOTE)
    ok = ("TA MISSION :" in contenu and "ORDRE : DEMARRE" in contenu)
    verifier("8. pilote mission + ordre en tete", ok)


def point_9_pas_activation_auto():
    """9. Pilote : plus d activation automatique des maillons."""
    contenu = lire(PILOTE)
    # Le pilote ne doit plus executer l activation des maillons
    # automatiquement (le commentaire de correction est present, et la
    # fonction _activer_maillon ne doit plus etre appelee depuis
    # _executer_commande_oracle).
    ok = ("Activation laissee a l agent" in contenu
          and "DELEGATION a la case" in contenu)
    verifier("9. pilote plus d activation automatique des maillons", ok)


def point_10_oracle_parser_limite():
    """10. oracle.py : parser pilote --limite par defaut 1."""
    contenu = lire(ORACLE_PY)
    ok = ('--limite", type=int, default=1' in contenu)
    verifier("10. oracle.py parser pilote limite defaut 1", ok)


def main():
    print("=== test-104 : vigie-round + pilote Oracle corrige ===")

    points = [
        ("1. vigie existe + triplet", point_1_vigie_existe_triplet),
        ("2. detection orpheline 4W", point_2_4w_session_orpheline),
        ("3. detection chaine en attente", point_3_chaine_en_attente),
        ("4. anti-spam", point_4_anti_spam),
        ("5. manifest vigie-round", point_5_manifest),
        ("6. execution reelle dry-run", point_6_execution_reelle),
        ("7. pilote limite 1 pas", point_7_limite_1),
        ("8. pilote mission en tete", point_8_mission_ordre_tete),
        ("9. pilote pas activation auto", point_9_pas_activation_auto),
        ("10. oracle parser limite 1", point_10_oracle_parser_limite),
    ]
    for num, (nom, fn) in enumerate(points, start=1):
        if not point_actif(num):
            continue
        t_debut = time.monotonic()
        fn()
        chrono_etape(nom, t_debut)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
