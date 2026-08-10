#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-012-guider-parcours.py
Test formel de l outil guider-parcours v0.5.0 (categorie guider/).

Outil teste (cerveau-projet/agents/tools/guider/guider-parcours/):
  .py + .sh (wrapper pur exec python3) + .md + spec/
  Guide l agent case par case (jeu de piste) selon un parcours JSON.
  (Etape 5 de la spec-refonte-cartes-decision v0.1.1 : resolution des
  references d indices + implementation du type action + ordre d execution)

Consolidation v0.4.0 (2026-08-09) :
  - afficher_indices : indice {"type":"ref","ref":X} RESOLU a la navigation
    ([REFERENCE] X puis le contenu : titre + 3 lignes pour pattern-<N>,
    chemin trouve pour protocole-x/regle-x, existence pour un chemin relatif).
  - naviguer : type action implemente - s execute SANS question et enchaine
    automatiquement sur suivant (comportement identique a indice sans indices).
  - generateurs-case v0.3.1 : type action ajoute aux choix ajouter/editer.

Cas couverts:
  1. --version py/sh identiques v0.5.0 (parite)
  2. --liste : liste les cases d un squelette (sans naviguer)
  3. Resolution ref pattern-7 : [REFERENCE] + titre extrait de la spec
  4. Resolution ref chemin rvav : fichier existant
  5. Case action : creee via generateurs-case --type action, navigue SANS
     question et enchaine vers la fin (PARCOURS TERMINE)
  6. Squelette v0.3.0 navigue de c0 a la fin sans erreur (mode agent)
  7. Reprise --case : demarrer a une case precise (pas de relecture de c0)
  8. Erreur : parcours inexistant (ERREUR + code non nul)
  9. Erreur : JSON invalide (ERREUR + code non nul)
 10. Protection : aucun fichier cree dans le dossier outil
 11. ASCII strict : 0 non-ASCII sur les 4 fichiers de l outil

Usage:
  python3 test-012-guider-parcours.py
"""
import io
import json
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

OUTIL_DIR = os.path.join(TOOLS_DIR, "guider", "guider-parcours")
OUTIL_PY = os.path.join(OUTIL_DIR, "guider-parcours.py")
OUTIL_SH = os.path.join(OUTIL_DIR, "guider-parcours.sh")
OUTIL_MD = os.path.join(OUTIL_DIR, "guider-parcours.md")
OUTIL_SPEC = os.path.join(OUTIL_DIR, "spec", "spec-guider-parcours.001.01.ebauche.md")
GEN_CASE = os.path.join(TOOLS_DIR, "generateurs", "generateurs-case", "generateurs-case.py")
GEN_CARTE = os.path.join(TOOLS_DIR, "generateurs", "generateurs-carte", "generateurs-carte.py")

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


def main():
    global NB_POINTS, NB_OK, NB_KO

    tmp = tempfile.mkdtemp(prefix="test-012-")
    try:
        print("=== Test formel guider-parcours v0.5.0 (etape 5 refonte) ===")

        # 1. --version py/sh identiques (parite)
        r_py = run([PYTHON, OUTIL_PY, "--version"])
        r_sh = run(["bash", OUTIL_SH, "--version"])
        verifier("1. --version py/sh identiques v0.5.0",
                 r_py.returncode == 0 and r_sh.returncode == 0
                 and "v0.5.0" in r_py.stdout
                 and r_py.stdout.strip() == r_sh.stdout.strip(),
                 "py=%r sh=%r" % (r_py.stdout.strip(), r_sh.stdout.strip()))

        # Preparation : squelette v0.3.0 (contient des refs) via generateurs-carte
        travail = os.path.join(tmp, "parcours.json")
        r_creer = run([PYTHON, GEN_CARTE, "creer", travail, "--agent", "test"])
        verifier("0. Squelette cree (generateurs-carte)",
                 r_creer.returncode == 0, r_creer.stdout[-120:])

        # 2. --liste : liste les cases sans naviguer
        r_liste = run([PYTHON, OUTIL_PY, travail, "--liste"])
        verifier("2. --liste retourne 0 + affiche des cases",
                 r_liste.returncode == 0
                 and "c0" in r_liste.stdout
                 and "c9" in r_liste.stdout,
                 r_liste.stdout.strip()[-120:])

        # 3. Resolution ref pattern-7 (case c2 du squelette)
        r_ref = run([PYTHON, OUTIL_PY, travail, "--case", "c2", "--reponses", "a-definir"])
        verifier("3a. Navigation c2 OK",
                 r_ref.returncode == 0, r_ref.stdout.strip()[-150:])
        verifier("3b. [REFERENCE] pattern-7 affiche",
                 "[REFERENCE]" in r_ref.stdout and "pattern-7" in r_ref.stdout,
                 r_ref.stdout.strip()[-200:])
        verifier("3c. Titre du pattern extrait (Modele de case compose)",
                 "Modele de case compose" in r_ref.stdout,
                 r_ref.stdout.strip()[-200:])

        # 4. Resolution ref chemin rvav (case c2b)
        r_rvav = run([PYTHON, OUTIL_PY, travail, "--case", "c2b"])
        verifier("4a. Navigation c2b OK",
                 r_rvav.returncode == 0, r_rvav.stdout.strip()[-150:])
        verifier("4b. Reference rvav resolue (fichier existant)",
                 "rvav-workflow" in r_rvav.stdout
                 and "fichier existant" in r_rvav.stdout,
                 r_rvav.stdout.strip()[-200:])

        # 5. Case action : creee via generateurs-case, navigue sans question
        travail2 = os.path.join(tmp, "parcours2.json")
        run([PYTHON, GEN_CARTE, "creer", travail2, "--agent", "test"])
        r_act = run([PYTHON, GEN_CASE, travail2, "ajouter",
                     "--type", "action", "--titre", "ACTION TEST",
                     "--suivant", "c9", "--case", "c8"])
        verifier("5a. Case action creee (generateurs-case --type action)",
                 r_act.returncode == 0, r_act.stdout.strip()[-150:])
        cases = json.load(io.open(travail2, encoding="utf-8"))["cases"]
        verifier("5b. c8 type action + suivant c9",
                 cases.get("c8", {}).get("type") == "action"
                 and cases.get("c8", {}).get("suivant") == "c9",
                 json.dumps(cases.get("c8"), ensure_ascii=True))
        r_nav = run([PYTHON, OUTIL_PY, travail2, "--case", "c8"])
        verifier("5c. Case action enchaine SANS question vers la fin",
                 r_nav.returncode == 0
                 and "PARCOURS TERMINE" in r_nav.stdout
                 and "c9" in r_nav.stdout,
                 r_nav.stdout.strip()[-200:])
        verifier("5d. Aucune QUESTION affichee pour la case action",
                 "QUESTION" not in r_nav.stdout,
                 r_nav.stdout.strip()[-200:])

        # 6. Squelette navigue de c0 a la fin sans erreur (mode agent)
        r_nav0 = run([PYTHON, OUTIL_PY, travail, "--reponses", "OUI|a-definir"])
        verifier("6. Navigation c0 -> fin sans erreur",
                 r_nav0.returncode == 0
                 and ("PARCOURS TERMINE" in r_nav0.stdout
                      or "QUESTION POUR L AGENT" in r_nav0.stdout),
                 r_nav0.stdout.strip()[-200:])

        # 7. Reprise --case : demarrer a une case precise
        r_case = run([PYTHON, OUTIL_PY, travail, "--case", "c2"])
        verifier("7. --case c2 demarre a c2 (pas de relecture c0)",
                 r_case.returncode == 0
                 and "Exemple d'action" in r_case.stdout
                 and "Relecture" not in r_case.stdout.split("Exemple d'action")[0],
                 r_case.stdout.strip()[-200:])

        # 8. Parcours inexistant : ERREUR
        r_abs = run([PYTHON, OUTIL_PY, os.path.join(tmp, "absent.json")])
        verifier("8. Parcours inexistant : ERREUR + code non nul",
                 r_abs.returncode != 0 and "ERREUR" in (r_abs.stdout + r_abs.stderr),
                 "code=%d" % r_abs.returncode)

        # 9. JSON invalide : ERREUR
        invalide = os.path.join(tmp, "invalide.json")
        with io.open(invalide, "w", encoding="utf-8") as fh:
            fh.write("{ ceci n est pas du json ")
        r_inv = run([PYTHON, OUTIL_PY, invalide])
        verifier("9. JSON invalide : ERREUR + code non nul",
                 r_inv.returncode != 0 and "ERREUR" in (r_inv.stdout + r_inv.stderr),
                 "code=%d" % r_inv.returncode)

        # 10. Protection : aucun fichier cree dans le dossier outil
        avant = set(os.listdir(OUTIL_DIR))
        run([PYTHON, OUTIL_PY, travail, "--liste"])
        apres = set(os.listdir(OUTIL_DIR))
        verifier("10. Protection : aucun fichier cree dans le dossier outil",
                 avant == apres, "cree: %s" % (apres - avant))

        # 11. ASCII strict : 0 non-ASCII sur les 4 fichiers de l outil
        total_non_ascii = sum(ascii_count(f) for f in
                              (OUTIL_PY, OUTIL_SH, OUTIL_MD, OUTIL_SPEC))
        verifier("11. ASCII strict : 0 non-ASCII (4 fichiers)",
                 total_non_ascii == 0, "total non-ASCII = %d" % total_non_ascii)

        print("")
        print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
