#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-011-generateurs-carte.py
Test formel de l outil generateurs-carte v0.3.0 (categorie generateurs/).

Outil teste (cerveau-projet/agents/tools/generateurs/generateurs-carte/):
  .py + .sh (wrapper pur exec python3) + .md + spec/ (creee a la refonte)
  Agit sur une CARTE DE DECISION COMPLETE (parcours JSON) : creer un squelette,
  analyser les chemins, detecter les anomalies, dupliquer un chemin.
  (Etape 4 de la spec-refonte-cartes-decision v0.1.1 : squelette ALLEGE
  + delegation au validateur-case + references conservees a la duplication)

Refonte v0.3.0 (2026-08-09) :
  - creer : squelette ALLEGE -- les 8 textes de regles inline longs remplaces
    par des REFERENCES resolvables (protocole-activation, pattern-N,
    chemin rvav-workflow.md) -> la carte neuve nait CONFORME (0 a alleger).
  - detecter : verifications deleguees au validateur-case (source unique).
  - dupliquer-chemin : conserve les references telles quelles.
  - validation auto : valider-case --modele --references apres chaque ecriture.

Cas couverts:
  1. --version py/sh identiques v0.3.0 (parite)
  2. --aide : usage complet avec les 4 actions
  3. creer un squelette : CONFORME (erreurs 0, a alleger 0)
  4. Les indices portent des references (0 texte inline > 160 car)
  5. Refs resolvables (protocole-activation, pattern-6/10/3/7/2, rvav)
  6. detecter : delegation au validateur-case (ligne "valider-case" affichee)
  7. dupliquer-chemin : refs conservees (dc1 -> pattern-10, aucun texte inline)
  8. --dry-run : aucune modification du fichier
  9. Parcours inexistant : ERREUR claire + code non nul
 10. JSON invalide : ERREUR claire + code non nul
 11. Protection : aucun fichier cree dans le dossier outil
 12. ASCII strict : 0 non-ASCII sur les 4 fichiers de l outil (+ spec)

Usage:
  python3 test-011-generateurs-carte.py
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

OUTIL_DIR = os.path.join(TOOLS_DIR, "generateurs", "generateurs-carte")
OUTIL_PY = os.path.join(OUTIL_DIR, "generateurs-carte.py")
OUTIL_SH = os.path.join(OUTIL_DIR, "generateurs-carte.sh")
OUTIL_MD = os.path.join(OUTIL_DIR, "generateurs-carte.md")
OUTIL_SPEC = os.path.join(OUTIL_DIR, "spec", "spec-generateurs-carte.001.01.ebauche.md")

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
    """Compte les caracteres non-ASCII d'un fichier (0 = conforme)."""
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        txt = fh.read()
    return sum(1 for c in txt if ord(c) > 127)


def charger(chemin):
    with io.open(chemin, encoding="utf-8") as fh:
        return json.load(fh)


def main():
    global NB_POINTS, NB_OK, NB_KO

    tmp = tempfile.mkdtemp(prefix="test-011-")
    try:
        print("=== Test formel generateurs-carte v0.3.0 (etape 4 refonte) ===")

        # 1. --version py/sh identiques (parite)
        r_py = run([PYTHON, OUTIL_PY, "--version"])
        r_sh = run(["bash", OUTIL_SH, "--version"])
        verifier("1. --version py/sh identiques v0.3.0",
                 r_py.returncode == 0 and r_sh.returncode == 0
                 and "v0.3.0" in r_py.stdout
                 and r_py.stdout.strip() == r_sh.stdout.strip(),
                 "py=%r sh=%r" % (r_py.stdout.strip(), r_sh.stdout.strip()))

        # 2. --aide : usage complet avec les 4 actions
        r_aide = run([PYTHON, OUTIL_PY, "--aide"])
        verifier("2a. --aide retourne 0",
                 r_aide.returncode == 0, r_aide.stderr.strip()[-80:])
        verifier("2b. --aide liste les 4 actions",
                 all(a in r_aide.stdout for a in
                     ("creer", "analyser", "detecter", "dupliquer-chemin")),
                 r_aide.stdout.strip()[-200:])

        # 3. creer une carte squelette : CONFORME
        travail = os.path.join(tmp, "parcours-test.json")
        r_creer = run([PYTHON, OUTIL_PY, "creer", travail, "--agent", "test"])
        verifier("3a. creer retourne 0",
                 r_creer.returncode == 0, r_creer.stdout.strip()[-150:])
        verifier("3b. Validation auto appelle valider-case",
                 "valider-case" in r_creer.stdout, r_creer.stdout.strip()[-200:])
        verifier("3c. Verdict CONFORME (0 erreur, 0 a alleger)",
                 "CONFORME" in r_creer.stdout
                 and "erreurs: 0" in r_creer.stdout
                 and "a alleger: 0" in r_creer.stdout,
                 r_creer.stdout.strip()[-200:])

        # 4. Indices = references (0 texte inline > 160 car)
        d = charger(travail)
        texte_long = 0
        for cid, case in d["cases"].items():
            for ind in case.get("indices", []):
                texte = ind.get("texte", "")
                if isinstance(texte, str) and len(texte) > 160:
                    texte_long += 1
        verifier("4. Aucun texte inline > 160 car dans le squelette",
                 texte_long == 0, "textes longs: %d" % texte_long)

        # 5. Refs resolvables presentes (cle ref)
        refs = []
        for cid, case in d["cases"].items():
            for ind in case.get("indices", []):
                if ind.get("type") == "ref" and ind.get("ref"):
                    refs.append(ind["ref"])
        verifier("5a. Des references presentes dans le squelette",
                 len(refs) >= 6, "refs: %s" % refs)
        verifier("5b. Refs de base couvertes (protocole-activation, pattern, rvav)",
                 any(r == "protocole-activation" for r in refs)
                 and any(r.startswith("pattern-") for r in refs)
                 and any("rvav" in r for r in refs),
                 "refs: %s" % refs)

        # 6. detecter : delegation au validateur-case
        r_det = run([PYTHON, OUTIL_PY, "detecter", travail])
        verifier("6. detecter affiche la delegation validateur-case",
                 r_det.returncode == 0
                 and "deleguees au validateur-case" in r_det.stdout
                 and "valider-case" in r_det.stdout,
                 r_det.stdout.strip()[-200:])

        # 7. dupliquer-chemin : refs conservees
        r_dup = run([PYTHON, OUTIL_PY, "dupliquer-chemin", travail,
                     "--debut", "c1", "--fin", "c9", "--prefixe", "d"])
        verifier("7a. dupliquer-chemin retourne 0",
                 r_dup.returncode == 0, r_dup.stdout.strip()[-150:])
        d2 = charger(travail)
        copies = [cid for cid in d2["cases"] if cid.startswith("d")]
        verifier("7b. Copies creees (prefixe d)",
                 len(copies) >= 2, "copies: %s" % copies)
        refs_copies = []
        textes_copies = 0
        for cid in copies:
            for ind in d2["cases"][cid].get("indices", []):
                if ind.get("type") == "ref":
                    refs_copies.append(ind["ref"])
                if ind.get("type") == "regle":
                    textes_copies += 1
        verifier("7c. Refs conservees dans les copies",
                 any(r == "pattern-10" for r in refs_copies), "refs: %s" % refs_copies)
        verifier("7d. Aucun texte regle inline duplique",
                 textes_copies == 0, "textes: %d" % textes_copies)

        # 8. --dry-run : aucune modification
        travail2 = os.path.join(tmp, "p2.json")
        run([PYTHON, OUTIL_PY, "creer", travail2, "--agent", "test"])
        avant = open(travail2, "rb").read()
        r_dry = run([PYTHON, OUTIL_PY, "dupliquer-chemin", travail2,
                     "--debut", "c1", "--fin", "c9", "--prefixe", "d", "--dry-run"])
        apres = open(travail2, "rb").read()
        verifier("8. --dry-run sans modification",
                 r_dry.returncode == 0 and avant == apres,
                 "dry-run a modifie le fichier")

        # 9. Parcours inexistant : ERREUR
        r_abs = run([PYTHON, OUTIL_PY, "analyser", os.path.join(tmp, "absent.json")])
        verifier("9. Parcours inexistant : ERREUR + code non nul",
                 r_abs.returncode != 0 and "ERREUR" in (r_abs.stdout + r_abs.stderr),
                 "code=%d" % r_abs.returncode)

        # 10. JSON invalide : ERREUR
        invalide = os.path.join(tmp, "invalide.json")
        with io.open(invalide, "w", encoding="utf-8") as fh:
            fh.write("{ ceci n est pas du json ")
        r_inv = run([PYTHON, OUTIL_PY, "analyser", invalide])
        verifier("10. JSON invalide : ERREUR + code non nul",
                 r_inv.returncode != 0 and "ERREUR" in (r_inv.stdout + r_inv.stderr),
                 "code=%d" % r_inv.returncode)

        # 11. Protection : aucun fichier cree dans le dossier outil
        avant = set(os.listdir(OUTIL_DIR))
        run([PYTHON, OUTIL_PY, "analyser", travail])
        apres = set(os.listdir(OUTIL_DIR))
        verifier("11. Protection : aucun fichier cree dans le dossier outil",
                 avant == apres, "cree: %s" % (apres - avant))

        # 12. ASCII strict : 0 non-ASCII sur les 4 fichiers + spec
        total_non_ascii = sum(ascii_count(f) for f in
                              (OUTIL_PY, OUTIL_SH, OUTIL_MD, OUTIL_SPEC))
        verifier("12. ASCII strict : 0 non-ASCII (4 fichiers + spec)",
                 total_non_ascii == 0, "total non-ASCII = %d" % total_non_ascii)

        print("")
        print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
