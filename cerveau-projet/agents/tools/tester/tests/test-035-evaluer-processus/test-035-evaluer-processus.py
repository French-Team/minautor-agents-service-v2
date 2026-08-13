#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-035-evaluer-processus.py
GARDE-FOU : evaluer-processus detecte les derives de processus (fins de
mission erronees, outils hors carte, coherence fiche/carte) et le cerveau
est SAIN (0 probleme).

Contexte (2026-08-13, mission Themis axe C, Vulcain) :
  - Les derives successives (Morpheus consignes, Cerberus outils hors carte,
    regle de fiche contradictoire) ont montre qu un audit de processus est
    necessaire AVANT chaque validation.
  - Vulcain a cree evaluer-processus v0.2.0 qui croise les cartes (JSON), les
    fiches, AGENTS.md / AGENTS-historique.md et le REGISTRE des usages
    (source fiable, pas les lecons qui sont du bruit).
  - Les cartes morpheus/vulcain/janus ont ete corrigees (indices outils
    manquants ajoutes) pour rendre le cerveau sain.

Invariants verifies :
  1. L outil existe et compile
  2. --agent morpheus : 0 probleme (sain)
  3. --agent cerberus : 0 probleme (sain)
  4. Scan global (sans --agent) : 0 probleme
  5. --rapport ecrit un rapport markdown
  6. Normes : ASCII strict + LF pur (outil + test)
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

OUTIL = os.path.join(TOOLS_DIR, "evaluer", "evaluer-processus",
                     "evaluer-processus.py")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0


def charger_protections():
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
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


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def lancer(extra_args):
    """Lance l outil SOUS PROTECTION et retourne (code, stdout)."""
    proc = PROTECTIONS.lancer_protege(
        [PYTHON, OUTIL] + extra_args,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=PROJECT_ROOT, timeout=120,
    )
    return proc.returncode, proc.stdout + proc.stderr


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== test-035 : evaluer-processus (garde-fou derives de processus) ===")
    try:
        # 1. L outil existe et compile
        verifier("1. Outil present", os.path.isfile(OUTIL), OUTIL)
        rc = PROTECTIONS.lancer_protege(
            [PYTHON, "-m", "py_compile", OUTIL], cwd=PROJECT_ROOT).returncode
        verifier("1b. Compilation OK", rc == 0, "rc=%d" % rc)

        # 2-4. Le cerveau est sain : 0 probleme partout
        for agent in ["morpheus", "cerberus"]:
            code, out = lancer(["--agent", agent])
            propre = out.strip()
            sain = ("0 probleme" in propre and code == 0)
            verifier("2. --agent %s : 0 probleme (rc=0)" % agent,
                     sain, "rc=%d out=%s" % (code, propre[-60:]))

        code, out = lancer([])
        sain_global = ("0 probleme" in out and code == 0)
        verifier("3. Scan global : 0 probleme (rc=0)",
                 sain_global, "rc=%d out=%s" % (code, out.strip()[-60:]))

        # 5. --rapport ecrit un rapport markdown
        rapport = os.path.join(PROJECT_ROOT, ".tmp-test-035-rapport.md")
        if os.path.isfile(rapport):
            os.remove(rapport)
        code, out = lancer(["--agent", "morpheus", "--rapport", rapport])
        ecrit = os.path.isfile(rapport)
        contenu_ok = False
        if ecrit:
            with io.open(rapport, encoding="utf-8", errors="replace") as fh:
                contenu_ok = "Rapport" in fh.read()
            os.remove(rapport)
        verifier("4. --rapport ecrit un rapport markdown",
                 ecrit and contenu_ok, "rc=%d ecrit=%s" % (code, ecrit))
    except PROTECTIONS.ArretProtection as e:
        print("  [KO] ARRET PROTECTION : %s" % e.message)
        NB_KO += 1

    # 5. Normes ASCII strict + LF pur (outil + test)
    fichiers = [OUTIL, os.path.abspath(__file__)]
    total_non_ascii = sum(ascii_count(f) for f in fichiers)
    verifier("5. ASCII strict : 0 non-ASCII (outil + test)",
             total_non_ascii == 0, "total=%d" % total_non_ascii)
    total_crlf = sum(crlf_count(f) for f in fichiers)
    verifier("6. LF pur : 0 CRLF (outil + test)",
             total_crlf == 0, "total=%d" % total_crlf)

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
