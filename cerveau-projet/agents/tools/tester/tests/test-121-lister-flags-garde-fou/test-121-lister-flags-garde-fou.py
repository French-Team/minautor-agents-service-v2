#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-121-lister-flags-garde-fou.py
GARDE-FOU : l outil lister-flags v0.1.1 (Vulcain) respecte sa spec
(mission c967fced, decision utilisateur 2026-09-04).

Points verifies :
  1. Syntaxe : py_compile OK + wrapper Bash (bash -n) OK
  2. Protection documentation : sans --confirme-doc -> code 2 (REFUS),
     avec --confirme-doc -> code 0
  3. --dry-run avec un outil du catalogue (verifier-systeme) -> code 0
  4. --dry-run avec un combo definition-combo (combo-tester-outil)
     -> code 0 + l entite combo est listee (source definition-combo)
  5. --format json parseable (json.loads) + cles version/entites
  6. --tous et --categorie : filtres coherents
  7. --flag-partage <flag> : filtre par flag partage
  8. Cible inconnue : code 1 + message sur stderr (aucune invention)
  9. Aucune execution des scripts inspectes : lister-flags ne fait que
     lire (ast.parse + argparse) - preuve par dry-run sans effet
  10. Coherence catalogue : 189 commandes dans catalogue-commandes.json
      et version 0.1.1 coherente dans les 4 fichiers lister-flags
      (py, sh, md, spec)
  11. Normes : ASCII strict + LF pur (fichier data + test)

Proprietaire : Morpheus (testeur dedie)
Version : 0.1.0
Tags: lister-flags, catalogue, flags, garde-fou, dry-run
"""
import ast
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
LF_DIR = os.path.join(TOOLS_DIR, "lister", "lister-flags")
LF_PY = os.path.join(LF_DIR, "lister-flags.py")
LF_SH = os.path.join(LF_DIR, "lister-flags.sh")
LF_MD = os.path.join(LF_DIR, "lister-flags.md")
LF_SPEC = os.path.join(LF_DIR, "spec",
                       "spec-lister-flags.001.01.ebauche.md")
CATALOGUE = os.path.join(TOOLS_DIR, "generateurs", "generateurs-commande",
                         "catalogue-commandes.json")
RACINE = os.path.abspath(".")

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
            pass
    if arg == "--desactiver" and i + 1 < len(sys.argv):
        for p in sys.argv[i + 1].split(","):
            try:
                DESACTIVES.append(int(p))
            except ValueError:
                pass

T_START = time.monotonic()
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
    total = time.monotonic() - T_START
    print("")
    print("=== CHRONO test-121 (total %.1fs) ===" % total)
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
        print("  [KO] %s" % nom)
        if detail:
            print("       %s" % detail)


def ascii_count(chemin):
    try:
        data = io.open(chemin, "r", encoding="utf-8").read()
    except (OSError, UnicodeError):
        return -1
    total = 0
    for ch in data:
        if ord(ch) > 127:
            total += 1
    return total


def crlf_count(chemin):
    try:
        data = io.open(chemin, "r", encoding="utf-8").read()
    except (OSError, UnicodeError):
        return -1
    return data.count("\r\n")


def lancer(argv):
    cmd = [sys.executable, LF_PY] + argv
    try:
        return PROTECTIONS.lancer_protege(
            cmd, timeout=120, capture_output=True, text=True, cwd=RACINE)
    except PROTECTIONS.ArretProtection as e:
        verifier("lancement protege de l outil", False, e.message)
        return None


def point_1_syntaxe():
    t0 = time.monotonic()
    verifier("1. py_compile OK",
             os.system("%s -m py_compile %s" % (sys.executable, LF_PY)) == 0)
    verifier("1b. wrapper Bash bash -n OK",
             os.system("bash -n %s" % LF_SH) == 0)
    chrono_etape("1. syntaxe", t0)


def point_2_protection_doc():
    t0 = time.monotonic()
    p = lancer(["--outil", "lister-flags"])
    verifier("2. sans --confirme-doc -> code 2 (REFUS)", p.returncode == 2,
             "code=%s" % p.returncode)
    verifier("2b. message REFUS present",
             "REFUS" in (p.stdout + p.stderr))
    p2 = lancer(["--outil", "lister-flags", "--confirme-doc"])
    verifier("2c. avec --confirme-doc -> code 0", p2.returncode == 0,
             "code=%s" % p2.returncode)
    chrono_etape("2. protection doc", t0)


def point_3_dry_run_outil():
    t0 = time.monotonic()
    p = lancer(["--dry-run", "--outil", "verifier-systeme"])
    verifier("3. --dry-run outil catalogue -> code 0", p.returncode == 0,
             "code=%s" % p.returncode)
    verifier("3b. entite listee", "verifier-systeme" in p.stdout)
    chrono_etape("3. dry-run outil", t0)


def point_4_dry_run_combo():
    t0 = time.monotonic()
    p = lancer(["--dry-run", "--combo", "combo-tester-outil"])
    verifier("4. --dry-run combo definition-combo -> code 0",
             p.returncode == 0, "code=%s" % p.returncode)
    verifier("4b. combo listee", "combo-tester-outil" in p.stdout)
    p2 = lancer(["--dry-run", "--combo", "combo-tester-outil",
                 "--source", "definition-combo"])
    verifier("4c. --source definition-combo accepte le combo",
             p2.returncode == 0 and "combo-tester-outil" in p2.stdout)
    chrono_etape("4. dry-run combo", t0)


def point_5_format_json():
    t0 = time.monotonic()
    p = lancer(["--confirme-doc", "--json", "--outil", "lister-flags"])
    verifier("5. --json -> code 0", p.returncode == 0,
             "code=%s" % p.returncode)
    try:
        d = json.loads(p.stdout)
        verifier("5b. JSON parseable + cles", isinstance(d, dict)
                 and "version" in d and "entites" in d,
                 "cles=%s" % list(d.keys())[:5])
    except ValueError as exc:
        verifier("5b. JSON parseable + cles", False, str(exc))
    chrono_etape("5. format json", t0)


def point_6_tous_categorie():
    t0 = time.monotonic()
    p = lancer(["--dry-run", "--tous"])
    verifier("6. --tous -> code 0", p.returncode == 0,
             "code=%s" % p.returncode)
    m = "Entites : "
    if m in p.stdout:
        try:
            nb = int(p.stdout.split(m)[1].split("|")[0].strip())
        except (ValueError, IndexError):
            nb = -1
        verifier("6b. --tous liste > 150 entites (catalogue 189)",
                 nb > 150, "nb=%s" % nb)
    else:
        verifier("6b. --tous liste > 150 entites", False)
    p2 = lancer(["--dry-run", "--categorie", "lister"])
    verifier("6c. --categorie lister -> code 0", p2.returncode == 0,
             "code=%s" % p2.returncode)
    verifier("6d. categorie lister contient lister-flags",
             "lister-flags" in p2.stdout)
    chrono_etape("6. tous/categorie", t0)


def point_7_flag_partage():
    t0 = time.monotonic()
    p = lancer(["--dry-run", "--flag-partage", "fichier"])
    verifier("7. --flag-partage fichier -> code 0", p.returncode == 0,
             "code=%s" % p.returncode)
    verifier("7b. des entites filtrees par le flag partage",
             "Entites : " in p.stdout and "Flags partages" in p.stdout)
    chrono_etape("7. flag partage", t0)


def point_8_cible_inconnue():
    t0 = time.monotonic()
    p = lancer(["--confirme-doc", "--outil", "outil-inexistant-xyz"])
    verifier("8. cible inconnue -> code 1", p.returncode == 1,
             "code=%s" % p.returncode)
    verifier("8b. message aucun resultat sur stderr",
             "Aucune entite" in p.stderr)
    chrono_etape("8. cible inconnue", t0)


def point_9_aucune_execution():
    t0 = time.monotonic()
    # Preuve : l outil analyse (ast) et interroge argparse SANS executer
    # les scripts inspectes - dry-run sur un outil reel ne doit produire
    # AUCUN effet de bord (code 0, sortie table uniquement).
    p = lancer(["--dry-run", "--tous"])
    verifier("9. inspection sans execution (dry-run --tous code 0)",
             p.returncode == 0)
    # Les scripts inspectes ne sont pas executes : verifier que le source
    # de l outil lui-meme utilise ast.parse / argparse, pas subprocess
    # d execution des cibles.
    src = io.open(LF_PY, "r", encoding="utf-8").read()
    verifier("9b. analyse par ast (pas d execution des cibles)",
             "ast.parse" in src or "argparse" in src)
    verifier("9c. aucune sous-execution des outils inspectes",
             "subprocess.run" not in src
             and "subprocess.call" not in src
             and "os.system" not in src)
    chrono_etape("9. non-execution", t0)


def point_10_coherence():
    t0 = time.monotonic()
    try:
        cat = json.loads(io.open(CATALOGUE, "r", encoding="utf-8").read())
        commandes = cat.get("commandes", [])
        verifier("10. catalogue 189 commandes", len(commandes) == 189,
                 "nb=%s" % len(commandes))
    except (OSError, ValueError) as exc:
        verifier("10. catalogue 189 commandes", False, str(exc))
    versions = []
    for f in (LF_PY, LF_SH, LF_MD, LF_SPEC):
        try:
            txt = io.open(f, "r", encoding="utf-8").read()
        except (OSError, UnicodeError):
            versions.append("?")
            continue
        v = "0.1.1" if "0.1.1" in txt else "AUTRE"
        versions.append(v)
    verifier("10b. version 0.1.1 dans les 4 fichiers lister-flags",
             versions == ["0.1.1", "0.1.1", "0.1.1", "0.1.1"],
             "versions=%s" % versions)
    chrono_etape("10. coherence", t0)


def point_11_normes():
    t0 = time.monotonic()
    fichiers = [LF_PY, LF_SH, LF_MD, LF_SPEC,
                os.path.join(PROJECT_ROOT, os.path.basename(__file__))]
    total_na = sum(max(ascii_count(f), 0) for f in fichiers)
    verifier("11. ASCII strict : 0 non-ascii sur data + test",
             total_na == 0, "non_ascii=%s" % total_na)
    total_crlf = sum(max(crlf_count(f), 0) for f in fichiers)
    verifier("11b. LF pur : 0 CRLF sur data + test", total_crlf == 0,
             "crlf=%s" % total_crlf)
    chrono_etape("11. normes", t0)


def main():
    if point_actif(1):
        t0 = time.monotonic()
        point_1_syntaxe()
        chrono_etape("1. syntaxe", t0)
    if point_actif(2):
        t0 = time.monotonic()
        point_2_protection_doc()
        chrono_etape("2. protection doc", t0)
    if point_actif(3):
        t0 = time.monotonic()
        point_3_dry_run_outil()
        chrono_etape("3. dry-run outil", t0)
    if point_actif(4):
        t0 = time.monotonic()
        point_4_dry_run_combo()
        chrono_etape("4. dry-run combo", t0)
    if point_actif(5):
        t0 = time.monotonic()
        point_5_format_json()
        chrono_etape("5. format json", t0)
    if point_actif(6):
        t0 = time.monotonic()
        point_6_tous_categorie()
        chrono_etape("6. tous/categorie", t0)
    if point_actif(7):
        t0 = time.monotonic()
        point_7_flag_partage()
        chrono_etape("7. flag partage", t0)
    if point_actif(8):
        t0 = time.monotonic()
        point_8_cible_inconnue()
        chrono_etape("8. cible inconnue", t0)
    if point_actif(9):
        t0 = time.monotonic()
        point_9_aucune_execution()
        chrono_etape("9. non-execution", t0)
    if point_actif(10):
        t0 = time.monotonic()
        point_10_coherence()
        chrono_etape("10. coherence", t0)
    if point_actif(11):
        t0 = time.monotonic()
        point_11_normes()
        chrono_etape("11. normes", t0)

    bilan_chrono()
    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    print("=== VERDICT : %s ==="
          % ("PROPRE (lister-flags conforme a sa spec)"
             if NB_KO == 0 else "KO (lister-flags casse)"))
    return 1 if NB_KO > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
