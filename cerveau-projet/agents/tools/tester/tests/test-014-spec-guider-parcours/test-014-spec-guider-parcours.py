#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-014-spec-guider-parcours.py
Test formel de la spec-guider-parcours v0.6.1
(patterns REFERENCES, pas dupliques -- etape 7 de la spec-refonte-cartes-decision).

Contexte :
  - spec-guider-parcours passe a v0.6.0 : principe UNE PLACE POUR CHAQUE CHOSE
    documente (les patterns sont LA source de verite, les cases y POINTENT via
    un indice {"type": "ref", "ref": "pattern-<N>"})
  - 4 exemples inline transformes en refs (pattern-5/9/10/11)
  - incoherence de version corrigee (titre = Version = 0.6.1)
  - refs documentaires mises a jour (guider-parcours.md, vulcain.md)

Cas couverts:
  1. Version 0.6.1 coherente : titre ligne 7 == Version ligne 9
  2. Principe UNE PLACE POUR CHAQUE CHOSE documente
  3. Les 4 refs d exemple (pattern-5/9/10/11) resolvables (verifiees par
     valider-case sur un parcours qui les porte)
  4. Aucun indice regle > 160 caracteres dans les exemples de la spec
  5. Le type action documente dans les exemples (exemple minimal c2)
  6. Refs documentaires : guider-parcours.md et vulcain.md pointent v0.6.0
  7. Les 17 patterns toujours presents (aucun perdu)
  8. Non-regression : valider-case + guider-parcours fonctionnent toujours
  9. ASCII strict : 0 non-ASCII (spec + doc + test)
 10. LF pur : 0 CRLF

Usage:
  python3 test-014-spec-guider-parcours.py
"""
import io
import os
import shutil
import subprocess
import sys
import tempfile

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

SPEC = os.path.join(TOOLS_DIR, "guider", "guider-parcours", "spec",
                    "spec-guider-parcours.001.01.ebauche.md")
DOC = os.path.join(TOOLS_DIR, "guider", "guider-parcours", "guider-parcours.md")
FICHE_VULCAIN = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                             "vulcain", "vulcain.md")
GUIDER = os.path.join(TOOLS_DIR, "guider", "guider-parcours", "guider-parcours.py")
VALIDER_CASE = os.path.join(TOOLS_DIR, "valider", "valider-case", "valider-case.py")
PARCOURS_CERBERUS = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                                 "cerberus", "parcours", "parcours-cerberus.json")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0


def verifier(nom, condition, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s %s" % (nom, ("-- " + detail) if detail else ""))


def run(cmd, timeout=90):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        txt = fh.read()
    return sum(1 for c in txt if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def main():
    global NB_POINTS, NB_OK, NB_KO

    tmp = tempfile.mkdtemp(prefix="test-014-")
    try:
        print("=== Test formel spec-guider-parcours v0.6.1 ===")

        with io.open(SPEC, encoding="utf-8") as fh:
            spec = fh.read()
        lignes = spec.split("\n")

        # 1. Version coherente : titre (ligne 7) == Version (ligne 9)
        verifier("1a. Titre ligne 7 = v0.6.1", "v0.6.1" in lignes[6],
                 lignes[6][:80])
        verifier("1b. Version ligne 9 = 0.6.1",
                 lignes[8].strip().startswith("**Version** : 0.6.1"),
                 lignes[8].strip()[:60])

        # 2. Principe UNE PLACE POUR CHAQUE CHOSE
        verifier("2. Principe UNE PLACE POUR CHAQUE CHOSE documente",
                 "PRINCIPE UNE PLACE POUR CHAQUE CHOSE" in spec
                 and "source de verite" in spec)

        # 3. Les 4 refs d exemple resolvables (via valider-case sur cerberus
        #    qui porte deja des refs pattern resolues)
        r_vc = run([PYTHON, VALIDER_CASE, PARCOURS_CERBERUS, "--references",
                    "--dry-run"])
        verifier("3. Refs resolvables (valider-case CONFORME sur cerberus)",
                 r_vc.returncode == 0 and "CONFORME" in r_vc.stdout,
                 r_vc.stdout.strip()[:120])

        # 4. Aucun indice regle > 160 dans les exemples de la spec
        longs = 0
        for ligne in lignes:
            if '"type": "regle"' in ligne and '"texte": "' in ligne:
                deb = ligne.find('"texte": "') + len('"texte": "')
                fin = ligne.find('"', deb)
                if fin > deb and fin - deb > 160:
                    longs += 1
        verifier("4. Aucun indice regle > 160 dans les exemples",
                 longs == 0, "longs=%d" % longs)

        # 5. Type action documente dans l exemple minimal (c2)
        verifier("5. Exemple minimal c2 = type action + ref pattern-9",
                 '"c2"' in spec and '"type": "action"' in spec
                 and '"ref": "pattern-9"' in spec)

        # 6. Refs documentaires : guider-parcours.md et vulcain.md -> v0.6.0
        with io.open(DOC, encoding="utf-8") as fh:
            doc = fh.read()
        with io.open(FICHE_VULCAIN, encoding="utf-8") as fh:
            fiche = fh.read()
        verifier("6a. guider-parcours.md : Spec (v0.6.0)",
                 "(v0.6.0)" in doc and "spec-guider-parcours.001.01.ebauche.md" in doc,
                 doc.strip()[-80:])
        verifier("6b. vulcain.md : Spec du format (v0.6.0)",
                 "(v0.6.0)" in fiche and "Spec du format" in fiche,
                 fiche.strip()[-80:])

        # 7. Les 17 patterns toujours presents
        n_patterns = sum(1 for l in lignes if l.startswith("### Pattern "))
        verifier("7. 17 patterns presents", n_patterns == 17,
                 "patterns=%d" % n_patterns)

        # 8. Non-regression : guider-parcours navigue cerberus
        r_nav = run([PYTHON, GUIDER, PARCOURS_CERBERUS, "--reponses",
                     "OUI|accueil|OUI|OUI|NON|NON"])
        verifier("8. Non-regression : navigation cerberus -> PARCOURS TERMINE",
                 r_nav.returncode == 0 and "PARCOURS TERMINE" in r_nav.stdout,
                 r_nav.stdout.strip()[-100:])

        # 9. ASCII strict
        total_non_ascii = (ascii_count(SPEC) + ascii_count(DOC)
                           + ascii_count(FICHE_VULCAIN)
                           + ascii_count(os.path.abspath(__file__)))
        verifier("9. ASCII strict : 0 non-ASCII (spec + doc + fiche + test)",
                 total_non_ascii == 0, "total non-ASCII = %d" % total_non_ascii)

        # 10. LF pur
        total_crlf = (crlf_count(SPEC) + crlf_count(DOC)
                      + crlf_count(FICHE_VULCAIN)
                      + crlf_count(os.path.abspath(__file__)))
        verifier("10. LF pur : 0 CRLF (spec + doc + fiche + test)",
                 total_crlf == 0, "total CRLF = %d" % total_crlf)

        print("")
        print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
