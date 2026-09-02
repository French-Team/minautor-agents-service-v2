#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-112-detecter-fins-passives-garde-fou.py

GARDE-FOU FINS PASSIVES DES ARBRES V2 (decision utilisateur 2026-08-30,
modele aero) : TOUTE fin d un arbre v2 doit porter action=reactiver +
cible=oracle + la commande reactiver-fin <agent> --cible oracle. Une fin
passive (action=procedure sans commande, cible=cerberus, formulation
"attend le retour", theme qui clot sur fin-theme) COUPE la chaine du
round : l arbre se fige, rien ne continue (surtout en single-LLM).

L outil detecter-fins-passives (Vulcain, 2026-09-02) scanne
fins.json + theme-*.json de tous les agents et classifie les ecarts en
PASSIF (bloquant, RC=1) vs INFO (delegation/redirection a migrer, RC=0).

Points verifies :
  1. Triplet de l outil present (py + sh + md).
  2. --version fonctionne (py et sh).
  3. CAS CONFORME : argus/cerberus/nemesis (modele aero) -> 0 probleme,
     RC=0.
  4. PREUVE NEGATIVE : agent factice avec une fin passive
     (action=procedure sans commande) -> detecte PASSIF, RC=1.
  5. CAS INTERMEDIAIRE : delegation (action=activer) -> INFO non bloquante,
     RC=0 (pas de faux positif PASSIF).
  6. Sortie --json : champ "bloquant": true pour la fin passive.
  7. PARITE : le wrapper .sh rend le meme verdict que le .py.
  8. CLEANUP : le dossier d agents factices est supprime, aucun residu
     (rien sous tmp-dfp-*).
  9. Normes : ASCII strict + LF pur (outil py/sh + test).

Proprietaire : Morpheus (testeur dedie)
Version : 0.1.0
Tags: detecter-fins-passives, modele-aero, arbres-v2, garde-fou, vulcain
"""
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

CERVEau = os.path.join(PROJECT_ROOT, "cerveau-projet")
TOOLS_DIR = os.path.join(CERVEau, "agents", "tools")
PYTHON = sys.executable

OUTIL_DIR = os.path.join(TOOLS_DIR, "detecter",
                         "detecter-fins-passives")
PY = os.path.join(OUTIL_DIR, "detecter-fins-passives.py")
SH = os.path.join(OUTIL_DIR, "detecter-fins-passives.sh")
MD = os.path.join(OUTIL_DIR, "detecter-fins-passives.md")

# Dossier d agents factices (jamais dans le vrai cerveau-projet).
TMP_BASE = os.path.join(tempfile.gettempdir(), "tmp-dfp-test-112")

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


def _ecrire(chemin, contenu):
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with io.open(chemin, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(contenu)


def _agent_factice(nom, specs_fins, themes=None):
    """Cree un agent factice avec parcours/fins.json (+ themes optionnels)."""
    base = os.path.join(TMP_BASE, nom)
    _ecrire(os.path.join(base, "parcours", "fins.json"),
            json.dumps({"fins": specs_fins}, ensure_ascii=True, indent=1))
    for nom_theme, fin_case in (themes or {}).items():
        _ecrire(os.path.join(base, "parcours", nom_theme),
                json.dumps({"fin": {"case": fin_case}}, ensure_ascii=True,
                           indent=1))
    return base


def _nettoyer():
    shutil.rmtree(TMP_BASE, ignore_errors=True)


def point_1_triplet():
    ok = os.path.isfile(PY) and os.path.isfile(SH) and os.path.isfile(MD)
    verifier("1. triplet outil present (py + sh + md)", ok,
             "py=%s sh=%s md=%s" % (os.path.isfile(PY),
                                    os.path.isfile(SH), os.path.isfile(MD)))


def point_2_version():
    r_py = run([PYTHON, PY, "--version"], timeout=30)
    r_sh = run(["bash", SH, "--version"], timeout=30)
    ok = ("0.1.0" in (r_py.stdout or "") and "0.1.0" in (r_sh.stdout or ""))
    verifier("2. --version py + sh annoncent 0.1.0", ok,
             "py=%r sh=%r" % (r_py.stdout, r_sh.stdout))


def point_3_conforme():
    r = run([PYTHON, PY, "--agents", "argus", "cerberus", "nemesis"],
            timeout=60)
    sortie = (r.stdout or "") + (r.stderr or "")
    ok = (r.returncode == 0 and "[PASSIF]" not in sortie
          and "aucune fin passive" in sortie)
    verifier("3. argus/cerberus/nemesis (modele aero) -> 0 PASSIF, RC=0",
             ok, "RC=%d %r" % (r.returncode, sortie[-200:]))


def point_4_preuve_negative():
    _agent_factice("zz-passif", {
        "fin-attente": {"action": "procedure", "description": "attend le retour"},
        "fin-ok": {"action": "reactiver", "cible": "oracle",
                   "commande": "python3 oracle.py reactiver-fin zz-passif --cible oracle"},
    })
    r = run([PYTHON, PY, TMP_BASE, "--agents", "zz-passif", "--json"],
            timeout=30)
    ok = (r.returncode == 1)
    if ok and r.stdout:
        try:
            donnees = json.loads(r.stdout)
            types = [p["type"] for p in donnees["problemes"]
                     if p["agent"] == "zz-passif"]
            ok = (any(t.startswith("PROCEDURE_SANS_COMMANDE") for t in types)
                  or any(t.startswith("FORMULATION_PASSIVE") for t in types))
        except ValueError:
            ok = False
    verifier("4. fin passive factice -> detectee PASSIF, RC=1", ok,
             "RC=%d %r" % (r.returncode, (r.stdout or "")[-300:]))


def point_5_intermediaire():
    _agent_factice("zz-deleg", {
        "fin-delegation": {"action": "activer", "cible": "janus"},
    })
    r = run([PYTHON, PY, TMP_BASE, "--agents", "zz-deleg", "--json"],
            timeout=30)
    ok = (r.returncode == 0)
    if ok and r.stdout:
        try:
            donnees = json.loads(r.stdout)
            ok = all(not p["bloquant"] for p in donnees["problemes"])
        except ValueError:
            ok = False
    verifier("5. delegation (action=activer) -> INFO non bloquante, RC=0",
             ok, "RC=%d %r" % (r.returncode, (r.stdout or "")[-300:]))


def point_6_json():
    _agent_factice("zz-passif-json", {
        "fin-attente": {"action": "procedure"},
    })
    r = run([PYTHON, PY, TMP_BASE, "--agents", "zz-passif-json", "--json"],
            timeout=30)
    ok = (r.returncode == 1 and r.stdout and '"bloquant": true' in r.stdout)
    verifier("6. --json porte bloquant:true pour la fin passive", ok,
             "RC=%d %r" % (r.returncode, (r.stdout or "")[-200:]))


def point_7_parite():
    _agent_factice("zz-parite", {
        "fin-attente": {"action": "procedure"},
    })
    r_py = run([PYTHON, PY, TMP_BASE, "--agents", "zz-parite", "--json"],
               timeout=30)
    r_sh = run(["bash", SH, TMP_BASE, "--agents", "zz-parite", "--json"],
               timeout=30)
    try:
        j_py = json.loads(r_py.stdout) if r_py.stdout else {}
        j_sh = json.loads(r_sh.stdout) if r_sh.stdout else {}
        ok = (r_py.returncode == 1 and r_sh.returncode == 1
              and j_py.get("problemes") == j_sh.get("problemes"))
    except ValueError:
        ok = False
    verifier("7. parite .py / .sh (meme verdict, RC=1)", ok,
             "py_RC=%d sh_RC=%d" % (r_py.returncode, r_sh.returncode))


def point_8_cleanup():
    _nettoyer()
    ok = not os.path.exists(TMP_BASE)
    verifier("8. dossier factice supprime (aucun residu tmp-dfp-*)", ok)


def point_9_normes():
    fichiers = [PY, SH, os.path.abspath(__file__)]
    total_non_ascii = 0
    total_crlf = 0
    for f in fichiers:
        data = open(f, "rb").read()
        total_non_ascii += len([c for c in data if c > 127])
        total_crlf += data.count(b"\r\n")
    ok = total_non_ascii == 0 and total_crlf == 0
    verifier("9. ASCII strict + LF pur (py + sh + test)", ok,
             "non_ascii=%d crlf=%d" % (total_non_ascii, total_crlf))


def main():
    print("=== test-112 : detecter-fins-passives (garde-fou arbres v2) ===")

    points = [
        ("1. triplet present", point_1_triplet),
        ("2. version", point_2_version),
        ("3. cas conforme", point_3_conforme),
        ("4. preuve negative", point_4_preuve_negative),
        ("5. cas intermediaire", point_5_intermediaire),
        ("6. mode json", point_6_json),
        ("7. parite sh", point_7_parite),
        ("8. cleanup", point_8_cleanup),
        ("9. normes", point_9_normes),
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