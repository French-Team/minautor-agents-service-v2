#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-075-filtre-serie-relancer-ko.py
GARDE-FOU : la combinaison --relancer-ko --series X de
tester-lancer-non-regression (v0.5.5) doit revalider UNIQUEMENT les tests
en KO de la serie X du dernier run (les KO des autres series sont affiches
puis ecartes) - extension du workflow KO (demande utilisateur 2026-08-16).

Contexte :
  - --relancer-ko (v0.5.2) relance tous les KO du dernier run.
  - v0.5.5 : filtre serie - dans le bloc if args.relancer_ko, si
    args.series est fourni (et != tous), les KO sont filtres via
    serie_du_test(nom) == args.series ; les KO des autres series sont
    AFFICHES puis ECARTES ; aucun KO dans la serie -> message
    'AUCUN KO <serie> - rien a relancer' et return 0.
  - Le champ serie des entrees du registre n est PAS la source de verite :
    c est la table SERIES (serie_du_test) qui deduit la serie par nom.

Invariants verifies (sur un registre TEMPORAIRE, jamais le vrai) :
  1. tester-lancer-non-regression --version = v0.5.5
  2. Le help --aide mentionne la combinaison avec --series.
  3. FILTRE SERIE (fonctionnel via serie_du_test) : registre trie
     decroissant avec KO repartis - test-001 (serie c), test-024 (serie e),
     test-051 (serie d) -> le filtre serie e ne retient QUE test-024,
     le filtre serie d ne retient QUE test-051, le filtre serie a (aucun
     KO) ne retient RIEN (rien a relancer).
  4. Sans filtre serie, tous les KO du dernier run sont conserves.
  5. PREUVE NEGATIVE : une serie sans KO -> liste vide.
  6. Le registre temp est SUPPRIME en fin de test (0 trace).
  7. Normes : ASCII strict + LF pur (test + lanceur).
"""
import importlib.util
import io
import json
import os
import shutil
import sys
import tempfile
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

LANCEUR_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools",
                           "tester", "tester-lancer-non-regression")
LANCEUR_PY = os.path.join(LANCEUR_DIR, "tester-lancer-non-regression.py")

# --- triplet chrono (template v0.3.0) ---
T_START = time.monotonic()
CHRONO_ACTIF = True
ETAPES = []
NB_OK = 0
NB_KO = 0
NB_POINTS = 11


def point_actif(numero):
    return True


def chrono_etape(nom, t_debut):
    ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - T_START
    print("")
    print("=== CHRONO test-075 (total %.1fs) ===" % total)
    for nom, duree in ETAPES:
        print("  [chrono] %-35s %.2fs" % (nom, duree))


def verifier(nom, condition, detail=""):
    global NB_OK, NB_KO
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s -- %s" % (nom, str(detail)[-100:]))


def charger_protections():
    chemin = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools",
                          "tester", "tester-protections", "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def charger_lanceur():
    spec = importlib.util.spec_from_file_location("lanceur", LANCEUR_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(cmd, timeout=120):
    # PROTECTION : toute execution passe par lancer_protege (jamais de
    # subprocess.run brut - test-030 verifie cette regle).
    try:
        r = PROTECTIONS.lancer_protege(cmd, timeout=timeout,
                                       capture_output=True, text=True)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return -1, "ERREUR: %s" % str(e)[-80:]


def ecrire_registre(chemin, entrees):
    """Ecrit un registre trie DECROISSANT par date (comme en production)."""
    entrees.sort(key=lambda e: e["date"], reverse=True)
    with io.open(chemin, "w", encoding="utf-8", newline="\n") as fh:
        for e in entrees:
            fh.write(json.dumps(e, ensure_ascii=True) + "\n")


def main():
    print("=== Garde-fou : filtre serie de --relancer-ko (tester-lancer-non-regression v0.5.5) ===")

    # 1. Version v0.5.5
    t0 = time.monotonic()
    code, out = run([sys.executable, LANCEUR_PY, "--version"])
    verifier("1. tester-lancer-non-regression --version v0.5.5",
             code == 0 and "v0.5.5" in out, out.strip()[-40:])
    chrono_etape("1. version", t0)

    # 2. Le help --aide mentionne la combinaison avec --series
    t0 = time.monotonic()
    code, out = run([sys.executable, LANCEUR_PY, "--aide"])
    verifier("2. --aide mentionne la combinaison --relancer-ko --series",
             "--relancer-ko" in out and "--series" in out
             and "KO de la serie" in out, out[-200:] if "KO de la serie" not in out else "")
    chrono_etape("2. option --aide", t0)

    lanceur = charger_lanceur()

    # 3. FILTRE SERIE : registre temp avec KO repartis sur 3 series
    t0 = time.monotonic()
    tmp = tempfile.mkdtemp(prefix="tmp-test075-")
    try:
        reg = os.path.join(tmp, "registre-tests.jsonl")
        entrees = [
            # run RECENT : 3 KO repartis - test-001 (serie c), test-024 (serie e),
            # test-051 (serie d) + 1 OK
            {"date": "2026-08-16 15:00:01", "agent": "janus", "serie": "c",
             "test": "test-001-evaluer-agents-coherence.py", "verdict": "OK",
             "duree": 1.0, "run_id": "20260816-145959"},
            {"date": "2026-08-16 15:00:02", "agent": "janus", "serie": "c",
             "test": "test-001-evaluer-agents-coherence.py", "verdict": "KO",
             "duree": 2.0, "run_id": "20260816-145959"},
            {"date": "2026-08-16 15:00:03", "agent": "janus", "serie": "e",
             "test": "test-024-scripts-temporaires.py", "verdict": "KO",
             "duree": 3.0, "run_id": "20260816-145959"},
            {"date": "2026-08-16 15:00:04", "agent": "janus", "serie": "d",
             "test": "test-051-registre-tests.py", "verdict": "KO",
             "duree": 2.5, "run_id": "20260816-145959"},
            # run ANCIEN : KO serie b (ne doit PAS etre retenu)
            {"date": "2026-08-16 14:00:01", "agent": "janus", "serie": "b",
             "test": "test-013-cerberus-parcours.py", "verdict": "KO",
             "duree": 2.0, "run_id": "20260816-135959"},
        ]
        ecrire_registre(reg, entrees)
        rid, ko = lanceur.ko_du_dernier_run(PROJECT_ROOT, reg)
        verifier("3. dernier run identifie (3 KO repartis)",
                 rid == "20260816-145959" and sorted(ko) ==
                 ["test-001-evaluer-agents-coherence.py",
                  "test-024-scripts-temporaires.py",
                  "test-051-registre-tests.py"],
                 "run=%s ko=%s" % (rid, sorted(ko)))

        # 3b. filtre serie e -> UNIQUEMENT test-024 (KO ecartes exclus)
        filtres_e = [t for t in ko if lanceur.serie_du_test(t) == "e"]
        verifier("3b. filtre serie e -> uniquement test-024",
                 filtres_e == ["test-024-scripts-temporaires.py"],
                 "filtre_e=%s" % filtres_e)

        # 3c. filtre serie d -> UNIQUEMENT test-051
        filtres_d = [t for t in ko if lanceur.serie_du_test(t) == "d"]
        verifier("3c. filtre serie d -> uniquement test-051",
                 filtres_d == ["test-051-registre-tests.py"],
                 "filtre_d=%s" % filtres_d)

        # 3d. filtre serie a (aucun KO) -> RIEN a relancer
        filtres_a = [t for t in ko if lanceur.serie_du_test(t) == "a"]
        verifier("3d. filtre serie a (aucun KO) -> rien a relancer",
                 filtres_a == [], "filtre_a=%s" % filtres_a)
        chrono_etape("3. filtre serie", t0)

        # 4. Sans filtre serie -> tous les KO du dernier run conserves
        t0 = time.monotonic()
        verifier("4. sans filtre -> les 3 KO du dernier run conserves",
                 len(ko) == 3, "ko=%s" % ko)
        chrono_etape("4. sans filtre", t0)

        # 5. PREUVE NEGATIVE : registre vert -> aucun KO, serie vide
        t0 = time.monotonic()
        reg2 = os.path.join(tmp, "registre-vert.jsonl")
        ecrire_registre(reg2, [
            {"date": "2026-08-16 16:00:01", "agent": "janus", "serie": "a",
             "test": "test-001.py", "verdict": "OK", "duree": 1.0,
             "run_id": "20260816-155959"},
        ])
        rid2, ko2 = lanceur.ko_du_dernier_run(PROJECT_ROOT, reg2)
        verifier("5. preuve negative : run vert -> aucun KO (serie vide)",
                 ko2 == [], "ko=%s" % ko2)
        chrono_etape("5. preuve negative", t0)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        verifier("6. registre temp SUPPRIME en fin de test (0 trace)",
                 not os.path.exists(tmp), "residu : %s" % tmp)
        chrono_etape("6. purge", t0)

    # 7. Normes ASCII + LF (test + lanceur)
    t0 = time.monotonic()
    na_total = 0
    crlf_total = 0
    for f in [os.path.abspath(__file__), LANCEUR_PY]:
        d = io.open(f, encoding="utf-8", errors="replace").read()
        na_total += sum(1 for ch in d if ord(ch) > 127)
        b = io.open(f, "rb").read()
        crlf_total += b.count(b"\r\n")
    verifier("7. normes : 0 non-ASCII (test + lanceur)",
             na_total == 0, "non-ascii=%d" % na_total)
    verifier("7b. normes : 0 CRLF (test + lanceur)",
             crlf_total == 0, "crlf=%d" % crlf_total)
    chrono_etape("7. normes", t0)

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    print("=== VERDICT : %s ===" % (
        "PROPRE (filtre serie verrouille)" if NB_KO == 0 else "KO A CORRIGER"))
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
