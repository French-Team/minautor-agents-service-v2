#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-107-compteurs-garde-fou.py

Garde-fou des routines de comptage de tokens v1 (transposees des v2,
2026-08-29) : compter-entree et compter-sortie.

Ces routines sont des COLLECTEURS : elles mesurent les tokens ENTREE
(fichiers lus par le LLM) et SORTIE (sources de sortie) et journalisent
dans data/journal-entree.jsonl / data/journal-sortie.jsonl + un
historique markdown partage (data/tokens-historique-v1.md).

Points verifies :
  1. Les 2 scripts existent (main, mesure, journalisation).
  2. manifest.json les reference (actif, 300 s, script).
  3. grades-v1.json leur donne G3.
  4. compter-entree journalise une entree JSONL valide dans
     data/journal-entree.jsonl (date, tokens, octets, fichiers, delta).
  5. compter-sortie journalise une entree JSONL valide dans
     data/journal-sortie.jsonl (date, tokens, octets, sources, delta).
  6. L historique tokens-historique-v1.md recoit une ligne pour chaque
     execution (type entree / sortie).
  7. Chaque entree JSONL est un dict parseable avec tokens >= 0.
  8. Les scripts sont ASCII (convention v1).

Proprietaire : Morpheus (testeur dedie)
Version : 0.1.0
Tags: compteur, tokens, entree, sortie, routine, garde-fou
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
DATA_DIR = os.path.join(ROUTINES_DIR, "data")
MANIFEST = os.path.join(ROUTINES_DIR, "manifest.json")
GRADES = os.path.join(ORACLE_DIR, "grades-v1.json")

COMPTERS = {
    "compter-entree": {
        "script": os.path.join(ROUTINES_DIR, "compter-entree.py"),
        "journal": os.path.join(DATA_DIR, "journal-entree.jsonl"),
        "champ_nb": "fichiers",
    },
    "compter-sortie": {
        "script": os.path.join(ROUTINES_DIR, "compter-sortie.py"),
        "journal": os.path.join(DATA_DIR, "journal-sortie.jsonl"),
        "champ_nb": "sources",
    },
}
HISTORIQUE = os.path.join(DATA_DIR, "tokens-historique-v1.md")

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


def run(cmd, timeout=120):
    return PROTECTIONS.lancer_protege(cmd, capture_output=True, text=True,
                                      encoding="utf-8", errors="replace",
                                      timeout=timeout)


def lire(chemin):
    try:
        with io.open(chemin, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def _lignes_jsonl(chemin):
    """Lignes JSONL valides (dict) d un fichier."""
    resultats = []
    for ligne in lire(chemin).splitlines():
        ligne = ligne.strip()
        if not ligne:
            continue
        try:
            m = json.loads(ligne)
        except ValueError:
            continue
        if isinstance(m, dict):
            resultats.append(m)
    return resultats


def point_1_existence():
    ok = True
    for nom, info in COMPTERS.items():
        contenu = lire(info["script"])
        if not (os.path.isfile(info["script"])
                and "def main()" in contenu
                and "journal" in contenu
                and "tokens-historique" in contenu):
            ok = False
    verifier("1. compter-entree/sortie existent (main, journal, historique)",
             ok)


def point_2_manifest():
    try:
        data = json.loads(lire(MANIFEST))
    except ValueError:
        data = {}
    routines = {r.get("nom"): r for r in data.get("routines_surveillance", [])}
    ok = True
    details = []
    for nom in COMPTERS:
        r = routines.get(nom)
        if not (r and r.get("actif") is True
                and r.get("intervalles_secondes") == 600
                and r.get("script") == "%s.py" % nom):
            ok = False
            details.append(nom)
    verifier("2. manifest reference les 2 compteurs (actif, 600 s)", ok,
             "KO=%s" % ",".join(details) if details else "")


def point_3_grade():
    try:
        data = json.loads(lire(GRADES))
    except ValueError:
        data = {}
    routines = data.get("routines", {})
    manquants = [n for n in COMPTERS if routines.get(n) != "G3"]
    ok = not manquants
    verifier("3. grades-v1 G3 pour les 2 compteurs", ok,
             "manquants=%s" % ",".join(manquants) if manquants else "")


def _executer_compteur(nom):
    """Executer un compteur et retourner (rc, sortie)."""
    info = COMPTERS[nom]
    return run([PYTHON, info["script"]], timeout=180)


def point_4_entree_journalise():
    """4. compter-entree ajoute UNE entree JSONL valide."""
    journal = COMPTERS["compter-entree"]["journal"]
    avant = len(_lignes_jsonl(journal))
    r = _executer_compteur("compter-entree")
    apres = _lignes_jsonl(journal)
    ok = (r.returncode == 0
          and len(apres) == avant + 1
          and apres[-1].get("tokens", -1) >= 0
          and "date" in apres[-1] and "octets" in apres[-1]
          and "fichiers" in apres[-1] and "delta" in apres[-1])
    verifier("4. compter-entree journalise JSONL valide (+1 ligne)", ok,
             "rc=%d avant=%d apres=%d %s" % (
                 r.returncode, avant, len(apres),
                 (r.stdout or "")[:120]))


def point_5_sortie_journalise():
    """5. compter-sortie ajoute UNE entree JSONL valide."""
    journal = COMPTERS["compter-sortie"]["journal"]
    avant = len(_lignes_jsonl(journal))
    r = _executer_compteur("compter-sortie")
    apres = _lignes_jsonl(journal)
    ok = (r.returncode == 0
          and len(apres) == avant + 1
          and apres[-1].get("tokens", -1) >= 0
          and "date" in apres[-1] and "octets" in apres[-1]
          and "sources" in apres[-1] and "delta" in apres[-1])
    verifier("5. compter-sortie journalise JSONL valide (+1 ligne)", ok,
             "rc=%d avant=%d apres=%d %s" % (
                 r.returncode, avant, len(apres),
                 (r.stdout or "")[:120]))


def point_6_historique():
    """6. tokens-historique-v1.md recoit une ligne entree ET une sortie."""
    avant = len(lire(HISTORIQUE).splitlines())
    r_e = _executer_compteur("compter-entree")
    r_s = _executer_compteur("compter-sortie")
    apres = lire(HISTORIQUE).splitlines()
    ok = (r_e.returncode == 0 and r_s.returncode == 0
          and len(apres) >= avant + 2
          and any("| entree |" in l for l in apres[-4:])
          and any("| sortie |" in l for l in apres[-4:]))
    verifier("6. historique recoit une ligne entree et une sortie", ok,
             "avant=%d apres=%d" % (avant, len(apres)))


def point_7_jsonl_parse():
    """7. Toutes les lignes des 2 journaux sont des dict avec tokens >= 0."""
    ok = True
    details = []
    for nom, info in COMPTERS.items():
        entrees = _lignes_jsonl(info["journal"])
        if not entrees:
            ok = False
            details.append("%s-vide" % nom)
            continue
        for e in entrees:
            if e.get("tokens", -1) < 0 or not e.get("date"):
                ok = False
                details.append("%s-champ-invalide" % nom)
                break
    verifier("7. journaux JSONL parseables (tokens>=0, date)", ok,
             ";".join(details) if details else "")


def point_8_ascii():
    ok = True
    for nom, info in COMPTERS.items():
        contenu = lire(info["script"])
        if any(ord(c) > 127 for c in contenu):
            ok = False
    verifier("8. scripts ASCII (convention v1)", ok)


def main():
    print("=== test-107 : garde-fou compteurs tokens v1 ===")
    points = [
        ("1. existence (main, journal, historique)", point_1_existence),
        ("2. manifest {actif, 300s}", point_2_manifest),
        ("3. grades G3", point_3_grade),
        ("4. entree journalise JSONL", point_4_entree_journalise),
        ("5. sortie journalise JSONL", point_5_sortie_journalise),
        ("6. historique entree+sortie", point_6_historique),
        ("7. JSONL parseables", point_7_jsonl_parse),
        ("8. ASCII", point_8_ascii),
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
            print("  %-42s %6.2fs" % (nom, duree))

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())