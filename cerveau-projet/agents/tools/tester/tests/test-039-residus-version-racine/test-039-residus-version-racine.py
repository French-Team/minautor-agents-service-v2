#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-039-residus-version-racine.py
GARDE-FOU ANTI-RECURRENCE : aucun fichier de version accidentel a la racine
du projet (lecon Buffy 2026-08-13 : des fichiers nommes "0.2.1" et "v0.2.6"
- sorties redirigees par erreur de activer-agent-principal - trainaient a la
racine, sans lien avec la version reelle du projet).

Contexte (2026-08-13) :
  - Les fichiers "0.2.1" et "v0.2.6" a la racine etaient des RESIDUS
    accidentels : le contenu d une sortie de commande (activer-agent-principal)
    avait ete redirige vers des fichiers nommes comme des versions.
  - La version reelle du README vit desormais dans
    cerveau-projet/agents/clio/version-readme.txt (source de verite dediee,
    maintenue par Clio) et le statut dans statut-projet.txt.
  - Ce garde-fou verifie qu aucun fichier dont le nom ressemble a une version
    semver pure (ex : 0.2.1, v0.2.6) n apparait a la racine.

Invariants verifies :
  1. Aucun fichier a la racine dont le nom matche ^v?[0-9]+\\.[0-9]+\\.[0-9]+$
     (version semver pure = residu accidentel)
  2. La source de verite de version existe (clio/version-readme.txt)
  3. La source de verite de statut existe (clio/statut-projet.txt)
  4. Normes : ASCII strict + LF pur (test)
"""
import importlib.util
import io
import os
import re
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")

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


def verifier(nom, ok, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if ok:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s -- %s" % (nom, detail))


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== Test formel residus-version-racine ===")

    # 1. Aucun fichier de version semver pure a la racine
    motif = re.compile(r"^v?[0-9]+\.[0-9]+\.[0-9]+$")
    residus = [f for f in os.listdir(PROJECT_ROOT)
               if os.path.isfile(os.path.join(PROJECT_ROOT, f)) and motif.match(f)]
    verifier("1. Aucun fichier de version accidentel a la racine",
             len(residus) == 0, "residus=%s" % residus)

    # 2. Source de verite version presente
    f_version = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "clio", "version-readme.txt")
    try:
        v = io.open(f_version, encoding="utf-8").read().strip()
        verifier("2. Source version-readme.txt presente (%s)" % v,
                 bool(re.match(r"^[0-9]+\.[0-9]+\.[0-9]+$", v)), "contenu=%r" % v)
    except Exception as e:
        verifier("2. Source version-readme.txt presente", False, str(e))

    # 3. Source de verite statut presente
    f_statut = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "clio", "statut-projet.txt")
    try:
        s = io.open(f_statut, encoding="utf-8").read().strip()
        verifier("3. Source statut-projet.txt presente (%s)" % s,
                 bool(re.match(r"^[a-z]+$", s)), "contenu=%r" % s)
    except Exception as e:
        verifier("3. Source statut-projet.txt presente", False, str(e))

    # 4. Normes : ASCII strict + LF pur (test)
    normes_ko = []
    for f in [os.path.abspath(__file__)]:
        try:
            txt = io.open(f, encoding="utf-8", errors="replace").read()
            if any(ord(c) > 127 for c in txt):
                normes_ko.append("%s non-ascii" % os.path.basename(f))
            raw = io.open(f, "rb").read()
            if b"\r\n" in raw:
                normes_ko.append("%s crlf" % os.path.basename(f))
        except Exception as e:
            normes_ko.append("%s ERR %s" % (os.path.basename(f), e))
    verifier("4. Normes ASCII strict + LF pur (test)",
             len(normes_ko) == 0, "ko=%s" % normes_ko)

    print()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
