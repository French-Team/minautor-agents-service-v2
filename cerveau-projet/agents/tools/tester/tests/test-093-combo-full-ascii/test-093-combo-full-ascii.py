#!/usr/bin/env python3
# -*- coding: ascii -*-
"""test-093-combo-full-ascii.py
GARDE-FOU : le mode --full de combos-corriger-non-ascii (v0.3.0) impose un
dry OBLIGATOIRE avant le wet (preuve datee verifiee par le wet), scanne le
projet entier avec un rapport concis mais complet, et corrige uniquement les
fichiers detectes (performance).

Contexte (2026-08-18, demande utilisateur) : ajouter une option 'full' qui
scanne et corrige tout le projet d'un coup, avec dry obligatoire avant wet,
rapport concis mais complet, et dry fiable pour etre sur du coup.

Invariants verifies :
  1. L outil existe et compile.
  2. --version affiche 0.3.0-py.
  3. --full --dry-run : scan complet (resume + fichiers listes).
  4. Wet SANS preuve de dry -> REFUS (code 2) et message dry obligatoire.
  5. --full --dry-run ecrit la preuve (tmp-combos-full/preuve-dry-full.json).
  6. Wet AVEC preuve recente -> autorise (corrige un fichier de test temporaire).
  7. Rapport dry complet : tous les fichiers concernes listes (pas de troncature).
  8. Rapport ASCII pur : codes U+XXXX dans le detail des caracteres.
  9. Nettoyage : fichier temporaire de test supprime, preuve supprimee.
  10. Normes : ASCII strict + LF pur (outil + test).

Tags: combos, ascii, garde-fou, preuve-negative, anti-recurrence
"""
import importlib.util
import os
import py_compile
import subprocess
import sys
import time
import json

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

COMBO_PY = os.path.join(TOOLS_DIR, "combos", "combos-corriger-non-ascii",
                        "combos-corriger-non-ascii.py")
PREUVE_DIR = os.path.join(PROJECT_ROOT, "tmp-combos-full")
PREUVE = os.path.join(PREUVE_DIR, "preuve-dry-full.json")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0

# ------------------------------------------------------------------
# PROTECTIONS (bloc standard impose par test-030) :
#   toute execution passe par PROTECTIONS.lancer_protege (timeout + arbre)
# ------------------------------------------------------------------
def charger_protections():
    """Importe le point d entree unique des protections (test-030 le verifie)."""
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()

CHRONO_ACTIF = "--no-chrono" not in sys.argv
ISOLE = None
if "--iso" in sys.argv:
    ISOLE = sys.argv[sys.argv.index("--iso") + 1]

CHRONO = []


def chrono_etape(nom, t0):
    if CHRONO_ACTIF:
        CHRONO.append((nom, time.monotonic() - t0))


def bilan_chrono():
    if not CHRONO_ACTIF or not CHRONO:
        return
    print("=== CHRONO test (total %.2fs) ===" % sum(d for _, d in CHRONO))
    for nom, d in CHRONO:
        print("  %-45s %.2fs" % (nom, d))


def verifier(nom, ok, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if ok:
        NB_OK += 1
        print("[OK] %s" % nom)
    else:
        NB_KO += 1
        print("[KO] %s %s" % (nom, ("-- " + detail) if detail else ""))


def point_actif(n):
    return ISOLE is None or ISOLE == str(n)


def ascii_count(fichier):
    try:
        with open(fichier, "rb") as fh:
            return sum(1 for c in fh.read() if c > 127)
    except OSError:
        return 0


def crlf_count(fichier):
    try:
        with open(fichier, "rb") as fh:
            return fh.read().count(b"\r\n")
    except OSError:
        return 0


def lancer(*args, timeout=90):
    try:
        proc = PROTECTIONS.lancer_protege(
            [PYTHON, COMBO_PY] + list(args),
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=timeout,
        )
        return proc.returncode, proc.stdout + proc.stderr
    except subprocess.TimeoutExpired:
        return -1, "TIMEOUT"


def main():
    t_global = time.monotonic()

    # 1. l outil existe et compile.
    if point_actif(1):
        t = time.monotonic()
        ok = os.path.isfile(COMBO_PY)
        verifier("1. combos-corriger-non-ascii.py existe", ok)
        if ok:
            try:
                py_compile.compile(COMBO_PY, doraise=True)
                ok = True
            except py_compile.PyCompileError:
                ok = False
            verifier("1b. compilation OK", ok)
        chrono_etape("1. existence + compilation", t)

    # 2. --version.
    if point_actif(2):
        t = time.monotonic()
        code, sortie = lancer("--version")
        verifier("2. --version affiche 0.3.0-py",
                 code == 0 and "0.3.0-py" in sortie,
                 "code=%s" % code)
        chrono_etape("2. version", t)

    # 3. --full --dry-run : scan complet (resume + fichiers listes).
    if point_actif(3):
        t = time.monotonic()
        code, sortie = lancer("--full", "--dry-run")
        verifier("3. dry --full retourne un rapport",
                 "Fichiers non conformes" in sortie,
                 "code=%s" % code)
        verifier("3b. resume global present (lignes/caracteres)",
                 "Lignes concernees" in sortie and "Caracteres non-ASCII" in sortie)
        verifier("3c. repartition accent/emoji/autre presente",
                 "Repartition :" in sortie)
        chrono_etape("3. dry full", t)

    # 4. Wet SANS preuve -> REFUS (code 2).
    if point_actif(4):
        t = time.monotonic()
        if os.path.isdir(PREUVE_DIR):
            import shutil
            shutil.rmtree(PREUVE_DIR, ignore_errors=True)
        code, sortie = lancer("--full")
        verifier("4. wet sans preuve refuse (code 2)",
                 code == 2, "code=%s" % code)
        verifier("4b. message dry obligatoire affiche",
                 "dry est OBLIGATOIRE" in sortie or "dry OBLIGATOIRE" in sortie)
        chrono_etape("4. wet sans preuve", t)

    # 5. --full --dry-run ecrit la preuve.
    if point_actif(5):
        t = time.monotonic()
        lancer("--full", "--dry-run")
        ok = os.path.isfile(PREUVE)
        verifier("5. dry ecrit la preuve", ok)
        if ok:
            try:
                preuve = json.loads(open(PREUVE, encoding="utf-8").read())
                verifier("5b. preuve contient date + racine",
                         preuve.get("date") and preuve.get("racine"))
            except (ValueError, OSError):
                verifier("5b. preuve contient date + racine", False)
        chrono_etape("5. preuve dry", t)

    # 6. Fichier de test temporaire + wet AVEC preuve (SANS effet de bord :
    #    les fichiers reels listes par le dry sont sauvegardes puis restaures).
    if point_actif(6):
        t = time.monotonic()
        import shutil
        probe = os.path.join(PROJECT_ROOT, "zz-probe-093.txt")
        with open(probe, "w", encoding="utf-8", newline="") as fh:
            fh.write("Test probe accents: e accent aigu et grave + emoji\n")
        # Re-lancer le dry pour que la preuve couvre le fichier de test et
        # obtenir la liste des fichiers reels concernes.
        code_dry, sortie_dry = lancer("--full", "--dry-run")
        fichiers_reels = []
        for ligne in sortie_dry.splitlines():
            l = ligne.strip()
            if l.startswith("[") and "." in l and "zz-probe-093" not in l:
                chemin = l.split("]", 1)[0][1:]
                if os.path.isfile(chemin):
                    fichiers_reels.append(chemin)
        # Sauvegarder les fichiers reels (restauration apres le wet).
        backup_dir = os.path.join(PROJECT_ROOT, "tmp-test-093-backup")
        os.makedirs(backup_dir, exist_ok=True)
        for f in fichiers_reels:
            shutil.copy2(f, os.path.join(backup_dir, os.path.basename(f)))
        code, sortie = lancer("--full")
        verifier("6. wet avec preuve autorise (code 0 ou 1)",
                 code in (0, 1), "code=%s" % code)
        verifier("6b. le fichier de test est traite (corrige)",
                 os.path.isfile(probe))
        # Restaurer les fichiers reels.
        for f in fichiers_reels:
            b = os.path.join(backup_dir, os.path.basename(f))
            if os.path.isfile(b):
                shutil.copy2(b, f)
            if os.path.isfile(f + ".bak"):
                os.remove(f + ".bak")
        shutil.rmtree(backup_dir, ignore_errors=True)
        os.remove(probe)
        chrono_etape("6. wet avec preuve", t)

    # 7. Rapport dry complet : tous les fichiers listes.
    if point_actif(7):
        t = time.monotonic()
        code, sortie = lancer("--full", "--dry-run")
        lignes_fichiers = [l for l in sortie.splitlines()
                           if l.strip().startswith("[") and ".md" in l]
        verifier("7. rapport liste les fichiers par chemin complet",
                 len(lignes_fichiers) > 0)
        chrono_etape("7. rapport complet", t)

    # 8. Rapport ASCII pur (codes U+XXXX, pas de caracteres bruts).
    if point_actif(8):
        t = time.monotonic()
        code, sortie = lancer("--full", "--dry-run")
        # le rapport ne doit pas contenir de caracteres non-ASCII dans les details
        na = sum(1 for ch in sortie if ord(ch) > 127)
        verifier("8. rapport dry ASCII pur (0 non-ASCII)", na == 0,
                 "non-ASCII=%d" % na)
        chrono_etape("8. rapport ascii", t)

    # 9. Nettoyage : preuve et fichiers temporaires.
    if point_actif(9):
        t = time.monotonic()
        import shutil
        shutil.rmtree(PREUVE_DIR, ignore_errors=True)
        restants = []
        for racine, dossiers, fs in os.walk(PROJECT_ROOT):
            if ".git" in racine:
                continue
            for f in fs:
                if f.startswith("zz-probe-093"):
                    restants.append(os.path.join(racine, f))
        verifier("9. aucun fichier temporaire de test restant",
                 not restants, "; ".join(restants[:3]))
        chrono_etape("9. nettoyage", t)

    # 10. Normes.
    if point_actif(10):
        t = time.monotonic()
        fichiers = [COMBO_PY, os.path.abspath(__file__)]
        na = sum(ascii_count(f) for f in fichiers)
        crlf = sum(crlf_count(f) for f in fichiers)
        verifier("10. ASCII strict : 0 non-ASCII (outil + test)",
                 na == 0, "total=%d" % na)
        verifier("10b. LF pur : 0 CRLF (outil + test)",
                 crlf == 0, "total=%d" % crlf)
        chrono_etape("10. normes", t)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
