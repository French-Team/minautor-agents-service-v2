#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-082-pas-de-tmp-systeme-garde-fou.py
GARDE-FOU : AUCUNE ECRITURE HORS WORKSPACE (jamais de /tmp systeme)
(demande utilisateur 2026-08-16, protocole creation-scripts-temporaires
v0.2.11) :

  - le dossier tmp-AGENT/ est le SEUL endroit ou ecrire pendant une mission,
    y compris les journaux (.log) et captures de sortie
  - les OUTILS de production (.py / .sh) et les COMBOS (definition-combo.json)
    ne doivent JAMAIS contenir de redirection d ecriture ou de chemin de
    journal vers le /tmp du systeme
  - les vieux .sh de tests d outils legacy (outils/*/*/tests/) sont EXCLUS
    du scan (dette documentee, hors suite non-regression)

Invariants verifies :
  1. Le scan parcourt le code de production (outils .py/.sh + combos .json)
     en EXCLUANT les dossiers tests/
  2. Le scan detecte les 3 motifs de violation : > /tmp, " /tmp, :-/tmp
  3. PREUVE NEGATIVE A : un fichier .py temp avec '> /tmp/x.log' est detecte
  4. PREUVE NEGATIVE B : un fichier .sh temp avec ':-/tmp/test-logs' est detecte
  5. PREUVE NEGATIVE C : un fichier DANS un dossier tests/ avec '> /tmp' est
     IGNORE (exclusion legacy)
  6. Le code de production ACTUEL est propre (0 violation)
  7. Les fichiers de production sont listes en verbose (traeabilite)
  8. Normes : ASCII strict + LF pur (test)
  9. Le dossier temp est SUPPRIME en fin de test (0 trace)
"""
import importlib.util
import io
import os
import re
import shutil
import sys
import tempfile
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")

# --- triplet chrono (template v0.3.0) ---
T_START = time.monotonic()
CHRONO_ACTIF = True
ETAPES = []
NB_OK = 0
NB_KO = 0
NB_POINTS = 9

# Motifs de violation : redirections d ecriture / chemins de journal vers
# le /tmp systeme. La mention en commentaire du type "jamais /tmp systeme"
# (sans guillemet ni redirection) n est PAS un motif.
MOTIFS = re.compile(r">\s?/tmp|[\"']/tmp|:-/tmp")


def point_actif(numero):
    return True


def chrono_etape(nom, t_debut):
    ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - T_START
    print("")
    print("=== CHRONO test-082 (total %.1fs) ===" % total)
    for nom, duree in ETAPES:
        print("  [chrono] %-35s %.2fs" % (nom, duree))


def verifier(nom, condition, detail=""):
    global NB_OK, NB_KO
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s -- %s" % (nom, str(detail)[-120:]))


def charger_protections():
    chemin = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools",
                          "tester", "tester-protections", "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def run(cmd, timeout=60):
    try:
        r = PROTECTIONS.lancer_protege(cmd, timeout=timeout,
                                       capture_output=True, text=True)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return -1, "ERREUR: %s" % str(e)[-80:]


def compter_non_ascii(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for ch in fh.read() if ord(ch) > 127)


def scanner_code(racine, extensions, exclure_tests=True):
    """Retourne la liste des (fichier, ligne, numero) en violation."""
    violations = []
    for dossier, sous, fichiers in os.walk(racine):
        if exclure_tests and os.path.basename(dossier) == "tests":
            sous[:] = []
            continue
        for nom in fichiers:
            if not nom.endswith(extensions):
                continue
            chemin = os.path.join(dossier, nom)
            try:
                lignes = io.open(chemin, encoding="utf-8",
                                 errors="replace").read().splitlines()
            except Exception:
                continue
            for numero, ligne in enumerate(lignes, 1):
                if MOTIFS.search(ligne):
                    violations.append((chemin, numero, ligne.strip()))
    return violations


def main():
    print("=== Garde-fou : aucune ecriture hors workspace (/tmp systeme) ===")

    # 1. le scan parcourt le code de production en excluant tests/
    t0 = time.monotonic()
    prod_py = scanner_code(TOOLS_DIR, (".py",), exclure_tests=True)
    prod_sh = scanner_code(TOOLS_DIR, (".sh",), exclure_tests=True)
    combos = scanner_code(os.path.join(TOOLS_DIR, "combos"), (".json",),
                          exclure_tests=True)
    verifier("1. scan parcourt .py/.sh + combos (hors tests/)",
             isinstance(prod_py, list) and isinstance(prod_sh, list)
             and isinstance(combos, list),
             "types=%s/%s/%s" % (type(prod_py).__name__,
                                 type(prod_sh).__name__,
                                 type(combos).__name__))
    chrono_etape("1. scan structure", t0)

    # 2. les 3 motifs sont couverts par la regex
    t0 = time.monotonic()
    ok_a = MOTIFS.search('> /tmp/nr.log') is not None
    ok_b = MOTIFS.search('LOG_DIR = "/tmp/test-logs"') is not None
    ok_c = MOTIFS.search('PROTECTION_LOG_DIR=${PROTECTION_LOG_DIR:-/tmp/test-logs}') is not None
    ok_d = MOTIFS.search("jamais /tmp systeme en commentaire") is None
    verifier("2. motifs >/tmp, \"/tmp, :-/tmp detectes (commentaire ignore)",
             ok_a and ok_b and ok_c and ok_d,
             "a=%s b=%s c=%s d=%s" % (ok_a, ok_b, ok_c, ok_d))
    chrono_etape("2. motifs", t0)

    tmp = tempfile.mkdtemp(prefix="tmp-test082-")
    try:
        # 3. PREUVE NEGATIVE A : un .py avec > /tmp/x.log est detecte
        t0 = time.monotonic()
        fake_py = os.path.join(tmp, "outil-truque.py")
        with io.open(fake_py, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("#!/usr/bin/env python3\n")
            fh.write("# -*- coding: ascii -*-\n")
            fh.write('os.system("run-test > /tmp/x.log 2>&1")\n')
        vio_a = scanner_code(tmp, (".py",), exclure_tests=True)
        verifier("3. PREUVE NEGATIVE A : .py avec > /tmp detecte",
                 len(vio_a) == 1 and "outil-truque.py" in vio_a[0][0],
                 "vio=%s" % vio_a)
        chrono_etape("3. preuve A", t0)

        # 4. PREUVE NEGATIVE B : un .sh avec :-/tmp est detecte
        t0 = time.monotonic()
        fake_sh = os.path.join(tmp, "outil-truque.sh")
        with io.open(fake_sh, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("#!/bin/bash\n")
            fh.write('LOG_DIR=${LOG_DIR:-/tmp/test-logs}\n')
        vio_b = scanner_code(tmp, (".sh",), exclure_tests=True)
        verifier("4. PREUVE NEGATIVE B : .sh avec :-/tmp detecte",
                 len(vio_b) == 1 and "outil-truque.sh" in vio_b[0][0],
                 "vio=%s" % vio_b)
        chrono_etape("4. preuve B", t0)

        # 5. PREUVE NEGATIVE C : un .sh dans tests/ est IGNORE (legacy)
        t0 = time.monotonic()
        fake_test = os.path.join(tmp, "tests")
        os.makedirs(fake_test)
        with io.open(os.path.join(fake_test, "legacy.sh"), "w",
                     encoding="utf-8", newline="\n") as fh:
            fh.write("#!/bin/bash\n")
            fh.write("BASE=\"/tmp/test-legacy\"\n")
        vio_c = scanner_code(tmp, (".sh",), exclure_tests=True)
        verifier("5. PREUVE NEGATIVE C : tests/ exclu (legacy ignore)",
                 len(vio_c) == 1 and "legacy.sh" not in vio_c[0][0],
                 "vio=%s" % vio_c)
        chrono_etape("5. preuve C", t0)

        # 6. le code de production ACTUEL est propre (0 violation)
        t0 = time.monotonic()
        toutes = prod_py + prod_sh + combos
        verifier("6. code de production ACTUEL propre (0 violation)",
                 len(toutes) == 0,
                 "violations=%d : %s" % (len(toutes),
                                         [os.path.basename(v[0]) for v in toutes[:5]]))
        chrono_etape("6. production propre", t0)

        # 7. trace des fichiers scannes (verbose)
        t0 = time.monotonic()
        nb_py = sum(1 for d, _, fs in os.walk(TOOLS_DIR)
                    if os.path.basename(d) != "tests"
                    for f in fs if f.endswith(".py"))
        nb_sh = sum(1 for d, _, fs in os.walk(TOOLS_DIR)
                    if os.path.basename(d) != "tests"
                    for f in fs if f.endswith(".sh"))
        verifier("7. scan effectif (fichiers .py + .sh hors tests/)",
                 nb_py > 50 and nb_sh > 10,
                 "py=%d sh=%d" % (nb_py, nb_sh))
        chrono_etape("7. volume scanne", t0)

        # 8. normes ASCII + LF (test)
        t0 = time.monotonic()
        test_chemin = os.path.abspath(__file__)
        ok_ascii = compter_non_ascii(test_chemin) == 0
        ok_lf = open(test_chemin, "rb").read().count(b"\r\n") == 0
        verifier("8. normes ASCII + LF (test)",
                 ok_ascii and ok_lf, "ascii=%s lf=%s" % (ok_ascii, ok_lf))
        chrono_etape("8. normes", t0)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # 9. le dossier temp est supprime (0 trace)
    verifier("9. dossier temp supprime (0 trace)",
             not os.path.exists(tmp), "tmp=%s" % tmp)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
