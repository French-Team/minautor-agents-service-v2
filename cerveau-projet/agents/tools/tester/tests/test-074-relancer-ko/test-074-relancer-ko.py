#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-074-relancer-ko.py
GARDE-FOU : l option --relancer-ko de tester-lancer-non-regression (v0.5.5)
doit relancer UNIQUEMENT les tests en KO du DERNIER run journalise
(registre-tests.jsonl, champ run_id) - mecanisation du workflow KO
(demande utilisateur 2026-08-16) : isole le probleme, revalide le test,
valide la serie, puis seulement la suite complete.

Contexte :
  - Janus relancait la suite complete (90s+) a chaque KO au lieu d isoler
    le test KO : Vulcain a ajoute --relancer-ko + champ run_id dans
    registre-tests.jsonl (timestamp du debut du run) + fonction
    ko_du_dernier_run(racine, registre="") qui collecte les tests
    KO/ERREUR/TIMEOUT du run le plus recent.
  - Ce test verrouille : version 0.5.5, option dans --aide, fonction
    ko_du_dernier_run testable (parametre registre), preuve negative
    (un run avec 2 KO prime sur un run ancien avec 1 KO), run sans KO
    -> liste vide, purge du registre temp (0 trace).

Invariants verifies :
  1. tester-lancer-non-regression --version = v0.5.5
  2. L option --relancer-ko est presente dans --aide.
  3. La fonction ko_du_dernier_run existe et accepte un parametre registre
     (testable sur un fichier arbitraire, jamais sur le vrai registre).
  4. PREUVE NEGATIVE : un registre temp avec un run recent contenant 2 KO
     et un run ANCIEN contenant 1 KO -> ko_du_dernier_run retourne
     EXACTEMENT les 2 KO du run recent (l ancien KO n est pas retenu).
  5. Un run sans KO -> liste vide (rien a relancer).
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
NB_POINTS = 8


def point_actif(numero):
    return True


def chrono_etape(nom, t_debut):
    ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - T_START
    print("")
    print("=== CHRONO test-074 (total %.1fs) ===" % total)
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


def main():
    print("=== Garde-fou : --relancer-ko de tester-lancer-non-regression v0.5.5 ===")

    # 1. Version v0.5.5
    t0 = time.monotonic()
    code, out = run([sys.executable, LANCEUR_PY, "--version"])
    verifier("1. tester-lancer-non-regression --version v0.5.5",
             code == 0 and "v0.5.5" in out, out.strip()[-40:])
    chrono_etape("1. version", t0)

    # 2. Option --relancer-ko presente dans --aide
    t0 = time.monotonic()
    code, out = run([sys.executable, LANCEUR_PY, "--aide"])
    verifier("2. option --relancer-ko presente dans --aide",
             "--relancer-ko" in out, out[-160:] if "--relancer-ko" not in out else "")
    chrono_etape("2. option --aide", t0)

    # 3. Fonction ko_du_dernier_run testable (parametre registre)
    t0 = time.monotonic()
    lanceur = charger_lanceur()
    import inspect
    sig = inspect.signature(lanceur.ko_du_dernier_run)
    a_fonction = callable(lanceur.ko_du_dernier_run)
    a_param = "registre" in sig.parameters
    verifier("3. ko_du_dernier_run existe + parametre registre",
             a_fonction and a_param, "params=%s" % list(sig.parameters))
    chrono_etape("3. fonction testable", t0)

    # 4. PREUVE NEGATIVE : run recent 2 KO prime sur run ancien 1 KO
    t0 = time.monotonic()
    tmp = tempfile.mkdtemp(prefix="tmp-test074-")
    try:
        reg = os.path.join(tmp, "registre-tests.jsonl")
        entrees = [
            # run RECENT : 2 KO + 2 OK
            {"date": "2026-08-16 15:00:01", "agent": "janus", "serie": "a",
             "test": "test-001-evaluer-agents-coherence.py", "verdict": "OK",
             "duree": 1.0, "run_id": "20260816-145959"},
            {"date": "2026-08-16 15:00:02", "agent": "janus", "serie": "a",
             "test": "test-002-combos-moteur.py", "verdict": "KO",
             "duree": 2.0, "run_id": "20260816-145959"},
            {"date": "2026-08-16 15:00:03", "agent": "janus", "serie": "b",
             "test": "test-007-figer-lf.py", "verdict": "KO",
             "duree": 3.0, "run_id": "20260816-145959"},
            {"date": "2026-08-16 15:00:04", "agent": "janus", "serie": "a",
             "test": "test-003-*.py", "verdict": "OK",
             "duree": 1.5, "run_id": "20260816-145959"},
            # run ANCIEN : 1 KO (ne doit PAS etre retenu)
            {"date": "2026-08-16 14:00:01", "agent": "janus", "serie": "a",
             "test": "test-004-*.py", "verdict": "KO",
             "duree": 2.0, "run_id": "20260816-135959"},
        ]
        # tri decroissant par date (comme trier_registre_tests en production)
        entrees.sort(key=lambda e: e["date"], reverse=True)
        with io.open(reg, "w", encoding="utf-8", newline="\n") as fh:
            for e in entrees:
                fh.write(json.dumps(e, ensure_ascii=True) + "\n")
        rid, ko = lanceur.ko_du_dernier_run(PROJECT_ROOT, reg)
        attendu = ["test-002-combos-moteur.py", "test-007-figer-lf.py"]
        verifier("4. preuve negative : seuls les 2 KO du run recent (ancien exclu)",
                 rid == "20260816-145959" and sorted(ko) == sorted(attendu),
                 "run=%s ko=%s" % (rid, sorted(ko)))
        chrono_etape("4. preuve negative", t0)

        # 5. Run sans KO -> liste vide
        t0 = time.monotonic()
        reg2 = os.path.join(tmp, "registre-vert.jsonl")
        with io.open(reg2, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps({"date": "2026-08-16 16:00:01", "agent": "janus",
                                 "serie": "a", "test": "test-001.py", "verdict": "OK",
                                 "duree": 1.0, "run_id": "20260816-155959"},
                                ensure_ascii=True) + "\n")
        rid2, ko2 = lanceur.ko_du_dernier_run(PROJECT_ROOT, reg2)
        verifier("5. run sans KO -> liste vide (rien a relancer)",
                 ko2 == [], "ko=%s" % ko2)
        chrono_etape("5. run sans KO", t0)
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
        "PROPRE (--relancer-ko verrouille)" if NB_KO == 0 else "KO A CORRIGER"))
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
