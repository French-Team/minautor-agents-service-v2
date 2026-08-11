#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-016-migration-buffy.py
Test formel de la migration du parcours-buffy v0.3.0
(nouveau format : indices REFERENCES + cases ACTION).

Contexte (etape 6 generalisee de la spec-refonte-cartes-decision) :
  - parcours-buffy passe de v0.2.11 (0 erreur / 15 a alleger) a
    v0.3.0 (0 erreur / 0 a alleger / CONFORME valider-case)
  - 17 cases en surcharge de nombre reduites a <= 3 indices
  - textes regle longs migres en refs (pattern-2 ASCII, pattern-3
    combo, pattern-6 contexte, pattern-12 creation limitee, regles-
    perimetre-workspace) ou textes courts (< 160 car.)
  - 31 cases de pilotage 'indice' -> 'action' (enchaine sans question)
  - fiche buffy mise a jour (Pattern 14 : parcours v0.3.1)
  - test-009 adapte : temoin A ALLEGER bascule de buffy vers morpheus
  - v0.3.1 : branchement generateurs-ligne (case c10d, branche 'ligne' dans c10b)

Cas couverts:
  1. Version du parcours = 0.3.4
  2. Types : 32 action / 7 question / 2 controle / 9 fin, 0 indice
  3. valider-case : verdict CONFORME (0 erreur, 0 a alleger)
  4. valider-case --references : CONFORME (refs resolvables)
  5. Navigation chemin creation agent -> PARCOURS TERMINE
  6. Navigation chemin protocole -> PARCOURS TERMINE
  7. Case action enchaine SANS question (c0b -> c0c, pas de QUESTION)
  8. Refs resolues a la navigation (pattern-6, regles-perimetre-workspace)
  9. Aucun texte regle > 160 caracteres dans le parcours
 10. Aucune case avec plus de 3 indices
 11. Parcours inexistant : ERREUR + code non nul
 12. JSON invalide : ERREUR + code non nul
 13. Protection : aucun fichier cree dans le dossier outil
 14. ASCII strict : 0 non-ASCII (parcours + test + fiche)
 15. LF pur : 0 CRLF

Usage:
  python3 test-016-migration-buffy.py
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

OUTIL_DIR = os.path.join(TOOLS_DIR, "valider", "valider-case")
OUTIL_PY = os.path.join(OUTIL_DIR, "valider-case.py")
GP_PY = os.path.join(TOOLS_DIR, "guider", "guider-parcours", "guider-parcours.py")
PARCOURS = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "buffy",
                        "parcours", "parcours-buffy.json")
FICHE = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "buffy", "buffy.md")

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


def main():
    global NB_POINTS, NB_OK, NB_KO

    tmp = tempfile.mkdtemp(prefix="test-016-")
    try:
        print("=== Test formel migration parcours-buffy v0.3.0 ===")

        with io.open(PARCOURS, encoding="utf-8") as fh:
            d = json.load(fh)

        # 1. Version
        verifier("1. Version du parcours = 0.3.4",
                 d["parcours"].get("version") == "0.3.4",
                 d["parcours"].get("version"))

        # 2. Types
        types = {}
        for c in d["cases"].values():
            types[c.get("type")] = types.get(c.get("type"), 0) + 1
        verifier("2a. 34 cases action (31 pilotage + c10d generateurs-ligne + c15c/c15d Pattern 17)",
                 types.get("action") == 34, str(types))
        verifier("2b. 8 questions + 2 controles + 10 fins (Pattern 17 ajoute c15b question + c15e fin)",
                 types.get("question") == 8 and types.get("controle") == 2
                 and types.get("fin") == 10, str(types))
        verifier("2c. 0 case indice restante (toutes converties en action)",
                 types.get("indice", 0) == 0, str(types))

        # 3. valider-case : CONFORME
        r = run([PYTHON, OUTIL_PY, PARCOURS, "--dry-run"])
        verifier("3a. valider-case retourne 0", r.returncode == 0,
                 r.stdout.strip()[-100:])
        verifier("3b. Verdict CONFORME (0 erreur, 0 a alleger)",
                 "CONFORME" in r.stdout and "erreurs: 0" in r.stdout
                 and "a alleger: 0" in r.stdout,
                 r.stdout.strip()[:120])
        verifier("3c. Aucune surcharge restante",
                 "a alleger:" in r.stdout
                 and int(r.stdout.split("a alleger:")[1].split("|")[0].strip()) == 0,
                 r.stdout.strip()[:120])

        # 4. --references : CONFORME (refs resolvables)
        r_ref = run([PYTHON, OUTIL_PY, PARCOURS, "--references", "--dry-run"])
        verifier("4. --references : CONFORME (refs resolvables)",
                 r_ref.returncode == 0 and "CONFORME" in r_ref.stdout,
                 r_ref.stdout.strip()[:120])

        # 5. Navigation chemin creation agent (OUI -> creer) -> TERMINE
        r_nav = run([PYTHON, GP_PY, PARCOURS, "--reponses",
                     "OUI|creer|OUI|OUI|OUI|OUI"])
        verifier("5. Navigation chemin creation agent -> PARCOURS TERMINE",
                 "PARCOURS TERMINE" in r_nav.stdout,
                 r_nav.stdout.strip()[-150:])

        # 6. Navigation chemin protocole (OUI -> protocole) -> TERMINE
        r_nav2 = run([PYTHON, GP_PY, PARCOURS, "--reponses",
                      "OUI|protocole|OUI|OUI|OUI|OUI"])
        verifier("6. Navigation chemin protocole -> PARCOURS TERMINE",
                 "PARCOURS TERMINE" in r_nav2.stdout,
                 r_nav2.stdout.strip()[-150:])

        # 7. Case action enchaine sans question (c0b -> c0c)
        r_act = run([PYTHON, GP_PY, PARCOURS, "--reponses", "NON"])
        verifier("7. c0b (action) enchaine sans question vers c0c",
                 "PARCOURS TERMINE" not in r_act.stdout
                 and r_act.stdout.strip() != "",
                 r_act.stdout.strip()[-120:])

        # 8. Refs resolues a la navigation (pattern-6, regles-perimetre)
        verifier("8a. Ref pattern-6 resolue a la navigation",
                 "pattern-6" in r_nav.stdout or "CONTEXTE TEMPS REEL" in r_nav.stdout,
                 r_nav.stdout.strip()[:150])
        verifier("8b. Ref fichier regles-perimetre-workspace resolue",
                 "regles-perimetre-workspace" in r_nav.stdout,
                 r_nav.stdout.strip()[:150])

        # 9. Aucun texte regle > 160 caracteres
        trop_long = []
        for k, c in d["cases"].items():
            for i, ind in enumerate(c.get("indices", [])):
                if isinstance(ind, dict) and ind.get("type") == "regle":
                    t = ind.get("texte", "")
                    if len(t) > 160:
                        trop_long.append("%s#%d (%d)" % (k, i, len(t)))
        verifier("9. Aucun texte regle > 160 caracteres",
                 not trop_long, "; ".join(trop_long[:5]))

        # 10. Aucune case avec plus de 3 indices
        trop_ind = [k for k, c in d["cases"].items()
                    if len(c.get("indices", [])) > 3]
        verifier("10. Aucune case avec plus de 3 indices",
                 not trop_ind, "; ".join(trop_ind[:5]))

        # 11. Parcours inexistant : ERREUR
        r_abs = run([PYTHON, OUTIL_PY, os.path.join(tmp, "absent.json")])
        verifier("11. Parcours inexistant : ERREUR + code non nul",
                 r_abs.returncode != 0 and "ERREUR" in (r_abs.stdout + r_abs.stderr),
                 "code=%d" % r_abs.returncode)

        # 12. JSON invalide : ERREUR
        invalide = os.path.join(tmp, "invalide.json")
        with io.open(invalide, "w", encoding="utf-8") as fh:
            fh.write("{ ceci n est pas du json ")
        r_inv = run([PYTHON, OUTIL_PY, invalide])
        verifier("12. JSON invalide : ERREUR + code non nul",
                 r_inv.returncode != 0 and "ERREUR" in (r_inv.stdout + r_inv.stderr),
                 "code=%d" % r_inv.returncode)

        # 13. Protection : aucun fichier cree dans le dossier outil
        avant = set(os.listdir(OUTIL_DIR))
        run([PYTHON, OUTIL_PY, PARCOURS, "--dry-run"])
        apres = set(os.listdir(OUTIL_DIR))
        verifier("13. Protection : aucun fichier cree dans le dossier outil",
                 avant == apres, "cree: %s" % (apres - avant))

        # 14. ASCII strict : 0 non-ASCII (parcours + test + fiche)
        total_non_ascii = (ascii_count(PARCOURS) + ascii_count(FICHE)
                           + ascii_count(os.path.abspath(__file__)))
        verifier("14. ASCII strict : 0 non-ASCII (parcours + fiche + test)",
                 total_non_ascii == 0, "total = %d" % total_non_ascii)

        # 15. LF pur : 0 CRLF (parcours)
        raw = open(PARCOURS, "rb").read()
        verifier("15. LF pur : 0 CRLF (parcours)",
                 raw.count(b"\r\n") == 0, "CRLF = %d" % raw.count(b"\r\n"))

        print("")
        print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
