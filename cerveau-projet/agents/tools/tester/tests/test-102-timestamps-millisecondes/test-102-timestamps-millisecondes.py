#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-102-timestamps-millisecondes.py

GARDE-FOU : activer-agent-principal ecrit des timestamps a 3 chiffres
(millisecondes) au lieu de 6 (microsecondes). La demande utilisateur
2026-08-25 exigeait le passage microsecondes (6) -> millisecondes (3) ;
le commit 4fbd28f avait corrige les DONNEES (AGENTS-historique.md,
variables-actuelles.md) mais pas l OUTIL qui les ecrit : les timestamps a
6 chiffres sont revenus des la premiere activation (cause racine
identifiee par Themis, rapport-diagnostic-microsecondes-2026-08-25.md).

Invariants verifies (v0.7.3) :
  1. .py : aucune occurrence de strftime avec %f sans troncature [:-3]
     (les 4 zones : profil session, sidentifier, activer, reactiver).
  2. .sh : get_timestamp utilise %3N (3 chiffres), pas %N (9 chiffres).
  3. Execution reelle (environnement isole) : sidentifier ecrit une
     entree d historique dont l heure porte EXACTEMENT 3 chiffres apres
     le point (HH:MM:SS.mmm), jamais 6.
  4. Parite py/sh : la meme entree par le .sh porte aussi 3 chiffres.
  5. Le format %3f est INVALIDE en Python (ValueError) : la correction
     ne doit jamais l utiliser (troncature [:-3] obligatoire).
  6. Normes : ASCII strict + LF pur sur le fichier de test.

Contre-exemple (a ne JAMAIS reintroduire) : toute entree d historique
avec 6 chiffres apres le point (\.[0-9]{6}) = regression microsecondes.

Proprietaire : Morpheus (testeur dedie)
Version : 0.1.0
Tags: outils, garde-fou, anti-recurrence, traces
"""
import importlib.util
import io
import os
import re
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

ACTIVER_PY = os.path.join(TOOLS_DIR, "activer", "activer-agent-principal",
                          "activer-agent-principal.py")
ACTIVER_SH = os.path.join(TOOLS_DIR, "activer", "activer-agent-principal",
                          "activer-agent-principal.sh")
AGENT_MD_TEMPLATE = os.path.join(PROJECT_ROOT, "AGENTS.md")
HISTORIQUE_TEMPLATE = os.path.join(PROJECT_ROOT, "AGENTS-historique.md")
CLASSEUR_TEMPLATE = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                                 "classeur-variables", "stockage",
                                 "variables-actuelles.md")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0

# ------------------------------------------------------------------
# OPTIONS ON/OFF + CHRONO (regle immuable v0.3.0) :
#   --no-chrono            desactive le chrono (defaut : actif)
#   --isoler N             n execute que le point N (diagnostic cible)
#   --desactiver 1,3,5     saute les points listes (sans toucher au code)
# ------------------------------------------------------------------
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


def creer_environnement_test():
    """Creer un environnement de test isole (copies des fichiers reels)."""
    tmpdir = tempfile.mkdtemp(prefix="test-102-")
    agents_file = os.path.join(tmpdir, "AGENTS.md")
    historique_file = os.path.join(tmpdir, "AGENTS-historique.md")
    classeur_file = os.path.join(tmpdir, "variables-actuelles.md")
    # FIX 2026-08-29 : sans surcharge, l encart REAL (AGENTS-activite-
    # recente.md) etait pollue par les entrees de test (test102py) avec
    # des raisons multi-lignes qui cassaient le tableau.
    activite_file = os.path.join(tmpdir, "AGENTS-activite-recente.md")

    shutil.copy2(AGENT_MD_TEMPLATE, agents_file)
    shutil.copy2(HISTORIQUE_TEMPLATE, historique_file)
    shutil.copy2(CLASSEUR_TEMPLATE, classeur_file)

    return tmpdir, agents_file, historique_file, classeur_file, activite_file


def nettoyer_environnement(tmpdir):
    """Nettoyer l'environnement de test."""
    if os.path.exists(tmpdir):
        shutil.rmtree(tmpdir)


def executer_activer(script, agents_file, historique_file, classeur_file,
                     activite_file, args):
    """Executer activer-agent-principal (py ou sh) avec environnement isole."""
    env = os.environ.copy()
    env["AGENTS_FILE"] = agents_file
    env["AGENTS_HISTORIQUE"] = historique_file
    env["CLASSEUR_STOCKAGE"] = classeur_file
    env["AGENTS_ACTIVITE_RECENTE"] = activite_file
    if script.endswith(".sh"):
        cmd = ["bash", script] + args
    else:
        cmd = [PYTHON, script] + args
    return PROTECTIONS.lancer_protege(cmd, capture_output=True, text=True,
                                      encoding="utf-8", errors="replace",
                                      env=env, timeout=30)


def lire_entrees_historique(historique_file, identifiant):
    """Extraire les lignes d entree contenant l identifiant (id LLM)."""
    entrees = []
    with io.open(historique_file, "r", encoding="utf-8",
                 errors="replace") as fh:
        for ligne in fh:
            if identifiant in ligne and "|" in ligne:
                entrees.append(ligne.rstrip("\n"))
    return entrees


def extraire_fraction(entree):
    """Extraire la fraction decimale (chiffres apres le dernier point)."""
    m = re.search(r"\.(\d+)", entree)
    if not m:
        return None
    return m.group(1)


def point_1_py_pas_de_microsecondes():
    """1. .py : aucun %f sans troncature [:-3] (4 zones corrigees)."""
    with io.open(ACTIVER_PY, "r", encoding="utf-8", errors="replace") as fh:
        contenu = fh.read()
    # Toutes les occurrences de strftime avec %f doivent porter [:-3]
    occurrences = re.findall(r'strftime\("%Y-%m-%d %H:%M:%S\.%f"\)(?!\[:-3\])',
                             contenu)
    verifier("1. .py : 0 strftime %f sans troncature [:-3]",
             len(occurrences) == 0,
             "trouvees=%d" % len(occurrences))


def point_2_sh_3n_pas_n():
    """2. .sh : get_timestamp utilise %3N (3 chiffres), pas %N nu."""
    with io.open(ACTIVER_SH, "r", encoding="utf-8", errors="replace") as fh:
        contenu = fh.read()
    a_3n = re.search(r'date \+"%Y-%m-%d %H:%M:%S\.%3N"', contenu) is not None
    a_n_nu = re.search(r'date \+"%Y-%m-%d %H:%M:%S\.%N"', contenu) is not None
    verifier("2. .sh : get_timestamp en %3N (pas %N nu)",
             a_3n and not a_n_nu,
             "3N=%s N_nu=%s" % (a_3n, a_n_nu))


def point_3_execution_py_3_chiffres():
    """3. Execution reelle .py : entree d historique a 3 chiffres."""
    tmpdir, agents_file, historique_file, classeur_file, activite_file = \
        creer_environnement_test()
    try:
        identifiant = "test102py"
        r = executer_activer(ACTIVER_PY, agents_file, historique_file,
                             classeur_file, activite_file,
                             ["sidentifier", identifiant, "session-test102"])
        entrees = lire_entrees_historique(historique_file, identifiant)
        ok = (r.returncode == 0 and len(entrees) >= 1)
        if ok:
            fraction = extraire_fraction(entrees[0])
            ok = fraction is not None and len(fraction) == 3
            verifier("3. .py : timestamp a 3 chiffres (millisecondes)", ok,
                     "fraction=%s entree=%s" % (fraction, entrees[0][:80]))
        else:
            verifier("3. .py : timestamp a 3 chiffres (millisecondes)", ok,
                     "rc=%d nb_entrees=%d %s"
                     % (r.returncode, len(entrees), r.stdout[:120]))
    finally:
        nettoyer_environnement(tmpdir)


def point_4_execution_sh_3_chiffres():
    """4. Execution reelle .sh : entree d historique a 3 chiffres.
    NB : le .sh ecrit le NOM DE SESSION (pas l id LLM) dans l entree
    d historique - on cherche par le nom de session."""
    tmpdir, agents_file, historique_file, classeur_file, activite_file = \
        creer_environnement_test()
    try:
        identifiant = "test102sh"
        r = executer_activer(ACTIVER_SH, agents_file, historique_file,
                             classeur_file, activite_file,
                             ["sidentifier", identifiant, "session-test102"])
        entrees = lire_entrees_historique(historique_file, "session-test102")
        ok = (r.returncode == 0 and len(entrees) >= 1)
        if ok:
            fraction = extraire_fraction(entrees[0])
            ok = fraction is not None and len(fraction) == 3
            verifier("4. .sh : timestamp a 3 chiffres (millisecondes)", ok,
                     "fraction=%s entree=%s" % (fraction, entrees[0][:80]))
        else:
            verifier("4. .sh : timestamp a 3 chiffres (millisecondes)", ok,
                     "rc=%d nb_entrees=%d %s"
                     % (r.returncode, len(entrees), r.stdout[:120]))
    finally:
        nettoyer_environnement(tmpdir)


def point_5_pas_de_3f():
    """5. %3f est INVALIDE en Python : la correction ne doit jamais l utiliser."""
    with io.open(ACTIVER_PY, "r", encoding="utf-8", errors="replace") as fh:
        contenu = fh.read()
    verifier("5. .py : 0 occurrence de %3f (format invalide en Python)",
             "%3f" not in contenu)


def point_6_normes():
    """6. Normes : ASCII strict + LF pur sur le fichier de test."""
    with io.open(os.path.abspath(__file__), "rb") as fh:
        brut = fh.read()
    ascii_ok = all(b < 128 for b in brut)
    lf_ok = b"\r\n" not in brut
    verifier("6. normes : ASCII strict + LF pur", ascii_ok and lf_ok,
             "ascii=%s lf=%s" % (ascii_ok, lf_ok))


def main():
    print("=== test-102 : timestamps a 3 chiffres (millisecondes) "
          "dans activer-agent-principal ===")

    points = [
        ("1. .py sans %f nu", point_1_py_pas_de_microsecondes),
        ("2. .sh en %3N", point_2_sh_3n_pas_n),
        ("3. execution .py", point_3_execution_py_3_chiffres),
        ("4. execution .sh", point_4_execution_sh_3_chiffres),
        ("5. pas de %3f", point_5_pas_de_3f),
        ("6. normes", point_6_normes),
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
