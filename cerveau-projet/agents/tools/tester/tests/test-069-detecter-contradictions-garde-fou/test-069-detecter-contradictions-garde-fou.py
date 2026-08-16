#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-069-detecter-contradictions-garde-fou.py
GARDE-FOU : les ameliorations de detecter-contradictions v0.1.3
(option --fichier, audit regles croise, audit git GIT_RESIDU_ACTUEL,
audit --coherence, table REGLE_PROTOCOLE complete)
sont operationnelles et ne peuvent pas regresser.

Contexte (mission 2026-08-16) :
  - Suite au test de comportement reel d Argus, 3 limites de v0.1.0 :
    1) scan fixe des parcours -> option --fichier <chemin> ajoutee
       (audit d UN parcours JSON arbitraire, preuve negative possible)
    2) audit regles superficiel -> audit regles CROISE sur le contenu
       (CONTRADICTION_REGLE : SEUL vs PEUT/JAMAIS entre 2 fichiers)
    3) audit git limite -> GIT_RESIDU_ACTUEL (residus presents a la racine)

Invariants verifies :
  1. detecter-contradictions --version = v0.1.3
  2. --fichier : une copie de parcours avec REF_MORTE + CAS_ORPHELINE
     injectees est DETECTEE (preuve negative : injection detectee)
  3. Regles croisees : 2 affirmations opposees (SEUL X vs X PEUT) dans
     2 fichiers -> CONTRADICTION_REGLE detectee (fonctions internes)
  4. --git : un residu temporaire cree a la racine -> GIT_RESIDU_ACTUEL
     detecte, puis SUPPRIME (0 residu en fin de test)
  5. Normes : ASCII strict + LF pur (outil + test)
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

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

DETECT_DIR = os.path.join(TOOLS_DIR, "detecter", "detecter-contradictions")
DETECT_PY = os.path.join(DETECT_DIR, "detecter-contradictions.py")
PARCOURS_CERBERUS = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                                 "cerberus", "parcours", "parcours-cerberus.json")

# --- triplet chrono (template v0.3.0) ---
T_START = time.monotonic()
CHRONO_ACTIF = True
ETAPES = []
NB_OK = 0
NB_KO = 0
NB_POINTS = 10


def point_actif(numero):
    return True


def chrono_etape(nom, t_debut):
    ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - T_START
    print("")
    print("=== CHRONO test-069 (total %.1fs) ===" % total)
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
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def run(cmd, timeout=90):
    try:
        r = PROTECTIONS.lancer_protege(cmd, timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return -1, "ERREUR: %s" % str(e)[-80:]


def charger_outil():
    """Charger detecter-contradictions comme module (fonctions internes)."""
    spec = importlib.util.spec_from_file_location("dc", DETECT_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    print("=== Garde-fou : detecter-contradictions v0.1.3 (5 ameliorations) ===")

    # 1. Version v0.1.3
    t0 = time.monotonic()
    code, out = run([PYTHON, DETECT_PY, "--version"])
    verifier("1. detecter-contradictions --version v0.1.3",
             code == 0 and "v0.1.3" in out, out.strip()[-40:])
    chrono_etape("1. version", t0)

    # 2. --fichier : preuve negative (REF_MORTE + CAS_ORPHELINE injectees)
    t0 = time.monotonic()
    tmp = tempfile.mkdtemp(prefix="tmp-test069-")
    try:
        src = json.load(io.open(PARCOURS_CERBERUS, encoding="utf-8"))
        cases = src["cases"]
        cible = None
        for cid, c in cases.items():
            if isinstance(c, dict) and c.get("suivant"):
                cible = cid
                break
        if cible:
            cases[cible]["suivant"] = "cZZ-inexistante"
        cases["cZZ-orpheline"] = {"id": "cZZ-orpheline", "type": "action",
                                  "titre": "Case orpheline injectee",
                                  "suivant": cible}
        bogue = os.path.join(tmp, "parcours-bogue.json")
        with io.open(bogue, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(src, fh, ensure_ascii=True, indent=1)
        code, out = run([PYTHON, DETECT_PY, "--fichier", bogue], timeout=60)
        a_ref = "REF_MORTE" in out and "cZZ-inexistante" in out
        a_orph = "CAS_ORPHELINE" in out and "cZZ-orpheline" in out
        verifier("2. --fichier : REF_MORTE detectee (injection)",
                 a_ref, out[-140:] if not a_ref else "")
        verifier("2b. --fichier : CAS_ORPHELINE detectee (injection)",
                 a_orph, out[-140:] if not a_orph else "")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    chrono_etape("2. --fichier preuve negative", t0)

    # 2c. --coherence : l audit tourne. Etat reel : PROPRE (0 contradiction)
    #     - la correction OUI -> c0c est en place ET les 2 references marbre
    #     manquantes (SEUL CLIO, LE MODELE DE CONFIANCE) ont ete ajoutees,
    #     la table REGLE_PROTOCOLE est complete (8/8 regles croisees).
    t0 = time.monotonic()
    code, out = run([PYTHON, DETECT_PY, "--coherence"], timeout=60)
    a_audit = code in (0, 1)
    a_propre = "Aucune contradiction detectee" in out and "PROPRE" in out
    a_zero_majeur = "MAJEUR" not in out
    verifier("2c. --coherence : etat reel PROPRE (0 contradiction)",
             a_audit and a_propre and a_zero_majeur,
             out[-160:] if not (a_audit and a_propre and a_zero_majeur) else "")
    verifier("2d. --coherence : 0 REGLE_SANS_REFERENCE (table 8/8 complete)",
             "REGLE_SANS_REFERENCE" not in out, out[-160:])
    chrono_etape("2c. --coherence", t0)

    # 3. Regles croisees : 2 affirmations opposees -> CONTRADICTION_REGLE
    t0 = time.monotonic()
    dc = charger_outil()
    tmp2 = tempfile.mkdtemp(prefix="tmp-test069-")
    try:
        f1 = os.path.join(tmp2, "regle-a.md")
        f2 = os.path.join(tmp2, "regle-b.md")
        with io.open(f1, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("SEUL janus lance la non-regression complete\n")
        with io.open(f2, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("janus peut lancer la non-regression complete\n")
        affs = dc._extraire_affirmations(f1) + dc._extraire_affirmations(f2)
        conflits = dc._detecter_conflits(affs)
        a_conflit = any(r[1] == "CONTRADICTION_REGLE" for r in conflits)
        verifier("3. regles croisees : CONTRADICTION_REGLE (SEUL vs PEUT)",
                 a_conflit,
                 "conflits=%s" % [r[1] for r in conflits])
    finally:
        shutil.rmtree(tmp2, ignore_errors=True)
    chrono_etape("3. regles croisees", t0)

    # 4. --git : GIT_RESIDU_ACTUEL sur un residu cree a la racine
    t0 = time.monotonic()
    residu = os.path.join(PROJECT_ROOT, "tmp-residutest")
    cree = False
    try:
        if not os.path.exists(residu):
            os.mkdir(residu)
            cree = True
        code, out = run([PYTHON, DETECT_PY, "--git"], timeout=60)
        a_residu = "GIT_RESIDU_ACTUEL" in out and "tmp-residutest" in out
        verifier("4. --git : GIT_RESIDU_ACTUEL detecte (residu injecte)",
                 a_residu, out[-160:] if not a_residu else "")
    finally:
        if cree:
            shutil.rmtree(residu, ignore_errors=True)
        # 0 residu en fin de test : le dossier cree n existe plus
        verifier("4b. residu injecte SUPPRIME en fin de test (0 trace)",
                 not os.path.exists(residu),
                 "residu encore present : %s" % residu)
    chrono_etape("4. --git residu actuel", t0)

    # 5. Normes ASCII + LF (outil + test)
    t0 = time.monotonic()
    na_total = 0
    crlf_total = 0
    for f in (DETECT_PY, os.path.abspath(__file__)):
        d = io.open(f, encoding="utf-8", errors="replace").read()
        na_total += sum(1 for c in d if ord(c) > 127)
        crlf_total += d.count("\r")
    verifier("5. ASCII strict : 0 non-ASCII (outil + test)",
             na_total == 0, "na=%d" % na_total)
    verifier("5b. LF pur : 0 CRLF (outil + test)",
             crlf_total == 0, "crlf=%d" % crlf_total)
    chrono_etape("5. normes", t0)

    bilan_chrono()
    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    print("=== VERDICT : %s ===" % (
        "PROPRE (5 ameliorations verrouillees)" if NB_KO == 0 else "KO A CORRIGER"))
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
