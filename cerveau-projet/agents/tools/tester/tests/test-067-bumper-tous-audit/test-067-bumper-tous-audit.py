#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-067-bumper-tous-audit.py
GARDE-FOU : l audit des versions du bumper (mettre-a-jour-versions --tous)
doit donner 0 outil incoherent a chaque non-regression.

Contexte (demande utilisateur 2026-08-16) :
  - Le round bumper a revele 11 outils incoherents (supprimer-fichier .sh
    0.3.1 vs .py 0.3.2, combos-analyse-projet .sh 0.1.2 vs .py 0.1.3, etc.)
    caches pendant des semaines a cause d un motif md trop strict.
  - Demande : lancer le bumper --tous apres chaque round pour detecter les
    incoherences caches PLUS TOT. Ce garde-fou institutionnalise l audit :
    chaque non-regression lance --tous (dry-run, instantane ~0s) et exige
    0 outil incoherent.

Invariants verifies :
  1. mettre-a-jour-versions.py existe, compile, --version v0.1.3
  2. --tous (dry-run) : 0 outil incoherent (verdict OK)
  3. PREUVE NEGATIVE : desynchroniser temporairement la version d un .md
     (ecart injecte), relancer --tous -> KO detecte, puis restaurer
  4. Normes : ASCII strict + LF pur (outil + test)
"""
import importlib.util
import io
import os
import shutil
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

BUMPER_DIR = os.path.join(TOOLS_DIR, "mettre-a-jour", "mettre-a-jour-versions")
BUMPER_PY = os.path.join(BUMPER_DIR, "mettre-a-jour-versions.py")
BUMPER_MD = os.path.join(BUMPER_DIR, "mettre-a-jour-versions.md")

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
    print("=== CHRONO test-067 (total %.1fs) ===" % total)
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


def main():
    print("=== Garde-fou : audit des versions bumper --tous (0 incoherent) ===")

    # 1. Outil present + compile + version
    t0 = time.monotonic()
    verifier("1. bumper present", os.path.isfile(BUMPER_PY), "")
    code, out = run([PYTHON, "-m", "py_compile", BUMPER_PY])
    verifier("1b. compilation OK", code == 0, out[-80:])
    code, out = run([PYTHON, BUMPER_PY, "--version"])
    verifier("1c. --version v0.1.3",
             code == 0 and "v0.1.3" in out, out.strip()[-40:])
    chrono_etape("1. outil", t0)

    # 2. --tous dry-run : 0 outil incoherent
    t0 = time.monotonic()
    code, out = run([PYTHON, BUMPER_PY, "--tous"], timeout=120)
    ok_zero = ("0 outil(s) incoherent(s)" in out and "Verdict : OK" in out)
    verifier("2. --tous dry-run : 0 outil incoherent (verdict OK)",
             code == 0 and ok_zero, out[-100:])
    chrono_etape("2. audit --tous", t0)

    # 3. PREUVE NEGATIVE : desynchroniser un .md temporairement -> KO
    t0 = time.monotonic()
    # cible : la doc du bumper elle-meme (version connue 0.1.3)
    texte_original = io.open(BUMPER_MD, encoding="utf-8", errors="replace").read()
    faux = texte_original.replace("**Version** : 0.1.3", "**Version** : 9.9.9", 1)
    if faux == texte_original:
        faux = texte_original.replace("**Version :** 0.1.3", "**Version :** 9.9.9", 1)
    try:
        if faux != texte_original:
            with io.open(BUMPER_MD, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(faux)
            code, out = run([PYTHON, BUMPER_PY, "--tous"], timeout=120)
            detecte = ("1 outil(s) incoherent(s)" in out or "INCOHERENT" in out)
            verifier("3. preuve negative : ecart injecte detecte (KO)",
                     detecte, out[-100:])
        else:
            verifier("3. preuve negative : ecart injecte detecte (KO)",
                     False, "motif version 0.1.3 introuvable dans la doc")
    finally:
        with io.open(BUMPER_MD, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(texte_original)
    # apres restauration : --tous redevient 0 incoherent
    code, out = run([PYTHON, BUMPER_PY, "--tous"], timeout=120)
    restaure = ("0 outil(s) incoherent(s)" in out and "Verdict : OK" in out)
    verifier("3b. apres restauration : 0 incoherent (OK)",
             restaure, out[-100:])
    chrono_etape("3. preuve negative", t0)

    # 4. Normes ASCII + LF
    t0 = time.monotonic()
    na_total = 0
    crlf_total = 0
    for f in (BUMPER_PY, BUMPER_MD, os.path.abspath(__file__)):
        d = io.open(f, encoding="utf-8", errors="replace").read()
        na_total += sum(1 for c in d if ord(c) > 127)
        crlf_total += d.count("\r")
    verifier("4. ASCII strict : 0 non-ASCII (outil + test)", na_total == 0, "na=%d" % na_total)
    verifier("4b. LF pur : 0 CRLF (outil + test)", crlf_total == 0, "crlf=%d" % crlf_total)
    chrono_etape("4. normes", t0)

    bilan_chrono()
    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    print("=== VERDICT : %s ===" % ("PROPRE (0 incoherence de version)" if NB_KO == 0 else "KO A CORRIGER"))
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
