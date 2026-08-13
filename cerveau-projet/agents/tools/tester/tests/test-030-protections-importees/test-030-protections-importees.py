#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-030-protections-importees.py
GARDE-FOU : chaque test-0XX DOIT importer les protections via le point
d entree unique tester-protections, et la protection STOP (fail-fast) doit
fonctionner reelement.

Contexte (demande utilisateur 2026-08-12) :
  - L audit a revele que les 29 tests n importaient AUCUNE protection : les
    anciennes protections (tester-protection-*) etaient des wrappers
    autonomes NON IMPORTABLES depuis un test .py.
  - L utilisateur exige : (1) chaque test DOIT importer les protections,
    (2) une protection STOP : quand un test finit en erreur, la suite
    s arrete au lieu de continuer betement.
  - Anti-recurrence : ce test verifie que CHAQUE test-0XX charge le module
    tester-protections (bloc PROTECTIONS = charger_protections()) et que la
    protection STOP leve bien ArretProtection sur un echec critique.

Invariants verifies :
  1. Le module tester-protections existe et est importable (VERSION)
  2. CHAQUE test-0XX contient le bloc PROTECTIONS = charger_protections()
  3. CHAQUE test-0XX passe ses executions par PROTECTIONS.lancer_protege
     (aucun subprocess.run restant)
  4. Protection STOP reelle : verifier_critique leve ArretProtection sur KO
  5. Protection timeout reelle : une boucle infinie est arretee
  6. Le lanceur supporte --fail-fast (stoppe la suite des le premier KO)
  7. Le template-test.md reference l import obligatoire des protections
  8. Normes : ASCII strict + LF pur sur ce test
"""
import importlib.util
import io
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

TESTS_DIR = os.path.join(TOOLS_DIR, "tester", "tests")
MODULE_PROT = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                           "tester-protections.py")
TEMPLATE = os.path.join(TOOLS_DIR, "tester", "template-test.md")
LANCER = os.path.join(TOOLS_DIR, "tester", "tester-lancer-non-regression",
                      "tester-lancer-non-regression.py")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0


def charger_protections():
    spec = importlib.util.spec_from_file_location("tester_protections",
                                                  MODULE_PROT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


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
    return PROTECTIONS.lancer_protege(cmd, timeout=timeout)


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def lister_tests():
    resultats = []
    if not os.path.isdir(TESTS_DIR):
        return resultats
    for nom in sorted(os.listdir(TESTS_DIR)):
        dossier = os.path.join(TESTS_DIR, nom)
        if not os.path.isdir(dossier):
            continue
        for fichier in sorted(os.listdir(dossier)):
            if fichier.startswith("test-0") and fichier.endswith(".py"):
                resultats.append(os.path.join(dossier, fichier))
    return resultats


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== test-030 : protections importees + protection STOP ===")
    try:
        # 1. Le module existe et est importable
        verifier("1. tester-protections importable (VERSION=%s)"
                 % PROTECTIONS.VERSION, bool(PROTECTIONS.VERSION), "")

        # 2-3. Chaque test-0XX importe et utilise les protections
        tests = lister_tests()
        verifier("2a. Le dossier tests/ contient des tests",
                 len(tests) > 0, "nb=%d" % len(tests))

        sans_import = []
        avec_subprocess = []
        for t in tests:
            with io.open(t, encoding="utf-8", errors="replace") as fh:
                texte = fh.read()
            if "PROTECTIONS = charger_protections()" not in texte:
                sans_import.append(os.path.basename(t))
            if "PROTECTIONS.lancer_protege(" not in texte \
                    and "subprocess.run(" not in texte:
                # ni l un ni l autre : test sans execution (tolere) ou sans
                # protections (signale si des commandes sont lancees)
                if "def run(" in texte or "subprocess" in texte:
                    avec_subprocess.append(os.path.basename(t))

        verifier("2b. Les %d tests importent les protections (bloc standard)"
                 % len(tests), len(sans_import) == 0,
                 "KO=%s" % sans_import)

        # 3. Aucun subprocess.run brut restant (toute execution protegee).
        # Le motif est construit par concatenation pour que ce garde-fou ne
        # contienne jamais le litteral lui-meme (auto-incrimination evitee) ;
        # et le fichier test-030 est exclu du scan (c est le garde-fou).
        motif_run = "subprocess." + "run("
        restants = []
        for t in tests:
            if os.path.basename(t) == "test-030-protections-importees.py":
                continue
            with io.open(t, encoding="utf-8", errors="replace") as fh:
                texte = fh.read()
            if motif_run in texte:
                restants.append(os.path.basename(t))
        verifier("3. Aucun subprocess.run brut restant (executions protegees)",
                 len(restants) == 0, "KO=%s" % restants)

        # 4. Protection STOP reelle : verifier_critique leve ArretProtection.
        # La sortie de verifier_critique est REDIRIGEE pour que le marqueur
        # [KO] qu elle affiche ne soit pas compte par le lanceur de
        # non-regression (qui compte les [KO] dans la sortie du test).
        import contextlib
        import io as io_mod
        stop_ok = False
        tampon = io_mod.StringIO()
        try:
            with contextlib.redirect_stdout(tampon):
                PROTECTIONS.verifier_critique("point critique KO", False, "x")
        except PROTECTIONS.ArretProtection:
            stop_ok = True
        verifier("4. verifier_critique leve ArretProtection sur KO (STOP)",
                 stop_ok, "")

        # 5. Protection timeout reelle : boucle infinie arretee
        import time
        t0 = time.time()
        timeout_ok = False
        try:
            PROTECTIONS.lancer_protege([PYTHON, "-c", "while True: pass"],
                                       timeout=3)
        except PROTECTIONS.ArretProtection:
            timeout_ok = True
        duree = time.time() - t0
        verifier("5. boucle infinie arretee par le timeout (%.1fs)" % duree,
                 timeout_ok and duree < 10, "duree=%.1fs" % duree)

        # 6. Le lanceur supporte --fail-fast
        lanceur_ok = False
        if os.path.isfile(LANCER):
            with io.open(LANCER, encoding="utf-8", errors="replace") as fh:
                lancer_texte = fh.read()
            lanceur_ok = "--fail-fast" in lancer_texte
        verifier("6. Le lanceur supporte --fail-fast (protection STOP suite)",
                 lanceur_ok, "")

        # 7. Le template reference l import obligatoire des protections
        template_ok = False
        if os.path.isfile(TEMPLATE):
            with io.open(TEMPLATE, encoding="utf-8", errors="replace") as fh:
                contenu_template = fh.read()
            template_ok = ("PROTECTIONS = charger_protections()"
                           in contenu_template)
        verifier("7. template-test.md impose l import des protections",
                 template_ok, "")
    except PROTECTIONS.ArretProtection as e:
        print("  [KO] ARRET PROTECTION : %s" % e.message)
        NB_KO += 1

    # 8. Normes ASCII strict + LF pur sur ce test + le module
    fichiers = [os.path.abspath(__file__), MODULE_PROT]
    total_non_ascii = sum(ascii_count(f) for f in fichiers)
    verifier("8. ASCII strict : 0 non-ASCII (test + module)",
             total_non_ascii == 0, "total=%d" % total_non_ascii)
    total_crlf = sum(crlf_count(f) for f in fichiers)
    verifier("9. LF pur : 0 CRLF (test + module)",
             total_crlf == 0, "total=%d" % total_crlf)

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
