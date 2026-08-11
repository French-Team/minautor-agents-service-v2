#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-006-cartographier-parcours.py
Test formel de l'outil cartographier-parcours v0.1.0 (categorie cartographier/).

Outil teste (cerveau-projet/agents/tools/cartographier/cartographier-parcours/):
  .py (lecture seule) + .sh (wrapper pur exec python3) + .md + spec/
  Genere la cartographie d'un parcours JSON dans un fichier markdown :
  arbre ASCII (1ere occurrence, [convergence], |-- / `--), impasses,
  boucles, chemins BFS (logique reutilisee de generateurs-carte analyser).

Cas couverts:
  1. --version py/sh identiques v0.1.0
  2. Generation reelle sur parcours-atlas (44 cases, 39 chemins) avec en-tete complet
  3. Parite py/sh : fichiers generes IDENTIQUES (diff)
  4. --sortie vers un chemin personnalise (.tmp-*)
  5. --dry-run ne cree rien
  6. Arbre : chaque case une seule fois, convergences [convergence], fins visibles
  7. ASCII strict sur les 4 fichiers outils + le fichier genere
  8. JSON invalide -> ERREUR claire
  9. Parcours inexistant -> ERREUR claire
 10. valider-nommage --type outil OK
 11. Protection : aucun fichier residuel dans le workspace apres les tests

Usage:
  python3 test-006-cartographier-parcours.py
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

OUTIL_DIR = os.path.join(TOOLS_DIR, "cartographier", "cartographier-parcours")
OUTIL_PY = os.path.join(OUTIL_DIR, "cartographier-parcours.py")
OUTIL_SH = os.path.join(OUTIL_DIR, "cartographier-parcours.sh")
OUTIL_MD = os.path.join(OUTIL_DIR, "cartographier-parcours.md")
OUTIL_SPEC = os.path.join(OUTIL_DIR, "spec", "spec-cartographier-parcours.001.01.ebauche.md")
PARCOURS_ATLAS = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "atlas", "parcours", "parcours-atlas.json")
VALIDER_ASCII = os.path.join(TOOLS_DIR, "valider", "valider-conformite-ascii", "valider-conformite-ascii.py")
VALIDER_NOMMAGE = os.path.join(TOOLS_DIR, "valider", "valider-nommage", "valider-nommage.py")

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


def run(cmd, timeout=60):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def ascii_count(chemin):
    """Compte les caracteres non-ASCII d'un fichier (0 = conforme)."""
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        txt = fh.read()
    return sum(1 for c in txt if ord(c) > 127)


def lister_cases(contenu):
    """Extrait les ids de cases vus dans l'arbre (sections '## Arbre')."""
    lignes = [l for l in contenu.split("\n") if l.startswith("-- ") or l.startswith("|-- ") or l.startswith("`-- ")]
    return lignes


def main():
    global NB_POINTS, NB_OK, NB_KO

    tmp = tempfile.mkdtemp(prefix="test-006-")
    try:
        print("=== Test formel cartographier-parcours v0.1.0 ===")

        # 1. --version py/sh identiques
        r_py = run([PYTHON, OUTIL_PY, "--version"])
        r_sh = run(["bash", OUTIL_SH, "--version"])
        verifier("1. --version py/sh identiques v0.1.0",
                 r_py.returncode == 0 and r_sh.returncode == 0
                 and "v0.1.0" in r_py.stdout and r_py.stdout.strip() == r_sh.stdout.strip(),
                 "py=%r sh=%r" % (r_py.stdout.strip(), r_sh.stdout.strip()))

        # 2. Generation reelle sur parcours-atlas (sortie par defaut)
        outil = os.path.join(os.path.dirname(PARCOURS_ATLAS), "cartographie-atlas.md")
        if os.path.exists(outil):
            os.remove(outil)
        r = run([PYTHON, OUTIL_PY, PARCOURS_ATLAS])
        ok_gen = os.path.exists(outil)
        contenu = ""
        if ok_gen:
            with io.open(outil, encoding="utf-8") as fh:
                contenu = fh.read()
        verifier("2a. Generation reelle sur parcours-atlas (fichier cree)",
                 ok_gen and r.returncode == 0, r.stdout.strip()[-80:])
        verifier("2b. En-tete complet (agent, version, depart, nb cases, nb chemins)",
                 ok_gen and all(m in contenu for m in
                                ("| Agent | atlas |", "| Version du parcours |",
                                 "| Case de depart | c0 |", "| Nombre de cases | 46 |",
                                 "| Nombre de chemins (depart -> fins) | 39 |")),
                 "en-tete partiel")
        verifier("2c. Sections presentes (arbre, impasses, boucles, chemins)",
                 ok_gen and all(m in contenu for m in
                                ("## Arbre des cases", "## Cases sans sortie",
                                 "## Boucles detectees", "## Chemins principaux")),
                 "sections manquantes")
        if os.path.exists(outil):
            os.remove(outil)

        # 3. Parite py/sh : fichiers generes IDENTIQUES
        f_py = os.path.join(tmp, "cart-py.md")
        f_sh = os.path.join(tmp, "cart-sh.md")
        r1 = run([PYTHON, OUTIL_PY, PARCOURS_ATLAS, "-o", f_py])
        r2 = run(["bash", OUTIL_SH, PARCOURS_ATLAS, "-o", f_sh])
        memes = os.path.exists(f_py) and os.path.exists(f_sh)
        diff = ""
        if memes:
            with io.open(f_py, encoding="utf-8") as fh:
                a = fh.read()
            with io.open(f_sh, encoding="utf-8") as fh:
                b = fh.read()
            diff = "identiques" if a == b else "DIVERGENT"
        verifier("3. Parite py/sh : fichiers generes identiques",
                 memes and diff == "identiques", diff)

        # 4. --sortie vers chemin personnalise (tmp)
        f_custom = os.path.join(tmp, "custom.md")
        r = run([PYTHON, OUTIL_PY, PARCOURS_ATLAS, "-o", f_custom])
        verifier("4. --sortie personnalise cree le fichier demande",
                 r.returncode == 0 and os.path.exists(f_custom))

        # 5. --dry-run ne cree rien
        f_dry = os.path.join(tmp, "dry.md")
        r = run([PYTHON, OUTIL_PY, PARCOURS_ATLAS, "-o", f_dry, "--dry-run"])
        verifier("5. --dry-run ne cree rien",
                 r.returncode == 0 and "[DRY-RUN]" in r.stdout and not os.path.exists(f_dry),
                 r.stdout.strip()[-60:])

        # 6. Arbre : chaque case une fois, convergence, fins
        lignes_arbre = [l for l in contenu.split("\n")
                        if l.startswith("-- ") or l.startswith("|-- ") or l.startswith("`-- ")
                        if "## Arbre" not in l]
        ids_vus = []
        for l in contenu.split("\n"):
            for m in ("[c0]", "[c1]", "[c2]", "[c11]", "[c29]"):
                if m + " " in l or (m + ")") in l:
                    pass
        # Comptage des occurrences d ids dans l'arbre (zone entre ## Arbre et ## Cases)
        zone_arbre = contenu.split("## Arbre des cases")[1].split("## Cases sans sortie")[0]
        c0_fois = zone_arbre.count("[c0]")
        c11_fois = zone_arbre.count("[c11]")
        convergence = "[convergence]" in zone_arbre
        verifier("6a. Chaque case apparait UNE fois dans l arbre (c0 x1, c11 x1)",
                 c0_fois == 1 and c11_fois == 1, "c0 x%d c11 x%d" % (c0_fois, c11_fois))
        verifier("6b. Convergences marquees [convergence]", convergence)
        verifier("6c. Fin visible (FIN - Reactiver Cerberus / Signaler le besoin)",
                 "FIN - Reactiver Cerberus" in zone_arbre or "Signaler le besoin" in zone_arbre,
                 "fins absentes")

        # 7. ASCII strict sur les fichiers outils + genere
        verifier("7a. ASCII 0 sur .py", ascii_count(OUTIL_PY) == 0, "py %d" % ascii_count(OUTIL_PY))
        verifier("7b. ASCII 0 sur .sh", ascii_count(OUTIL_SH) == 0, "sh %d" % ascii_count(OUTIL_SH))
        verifier("7c. ASCII 0 sur .md", ascii_count(OUTIL_MD) == 0, "md %d" % ascii_count(OUTIL_MD))
        verifier("7d. ASCII 0 sur spec", ascii_count(OUTIL_SPEC) == 0, "spec %d" % ascii_count(OUTIL_SPEC))
        verifier("7e. ASCII 0 sur le fichier genere", ascii_count(f_custom) == 0,
                 "genere %d" % ascii_count(f_custom))

        # 8. JSON invalide -> ERREUR
        mauvais = os.path.join(tmp, "mauvais.json")
        with io.open(mauvais, "w", encoding="ascii") as fh:
            fh.write("{ pas du json valide")
        r = run([PYTHON, OUTIL_PY, mauvais])
        verifier("8. JSON invalide -> ERREUR claire",
                 r.returncode == 1 and ("JSON invalide" in r.stderr or "ERREUR" in r.stderr),
                 r.stderr.strip()[-60:])

        # 9. Parcours inexistant -> ERREUR
        absent = os.path.join(tmp, "absent.json")
        r = run([PYTHON, OUTIL_PY, absent])
        verifier("9. Parcours inexistant -> ERREUR claire",
                 r.returncode == 1 and "introuvable" in r.stderr,
                 r.stderr.strip()[-60:])

        # 10. valider-nommage --type outil
        r = run([PYTHON, VALIDER_NOMMAGE, "--type", "outil", OUTIL_PY])
        verifier("10. valider-nommage --type outil OK", r.returncode == 0,
                 r.stdout.strip()[-60:])

        # 11. Protection : aucun residu dans le workspace
        residu = os.path.exists(os.path.join(os.path.dirname(PARCOURS_ATLAS), "cartographie-atlas.md"))
        verifier("11. Aucun fichier residuel dans le workspace (cartographie-atlas supprime)",
                 not residu)

    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("")
    print("=== RESULTAT : %d/%d OK ===" % (NB_OK, NB_POINTS))
    if NB_KO:
        print("VERDICT : A REVOIR (%d point(s) en echec)" % NB_KO)
        return 1
    print("VERDICT : VALIDE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
