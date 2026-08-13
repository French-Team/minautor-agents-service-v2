#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-010-generateurs-case.py
Test formel de l outil generateurs-case v0.4.2 (categorie generateurs/).

Outil teste (cerveau-projet/agents/tools/generateurs/generateurs-case/):
  .py + .sh (wrapper pur exec python3) + .md + spec/ (creee a la refonte)
  Genere, edite et supprime des cases d une carte de decision (parcours JSON).
  (Etape 3 de la spec-refonte-cartes-decision v0.1.1 : modele compose complet
  + option --ref pour les indices de type REFERENCE au lieu des textes inline
  + v0.3.1 etape 5 : type action ajoute aux choix question/indice/action/controle/fin)

Refonte v0.3.0 (2026-08-09) :
  - ajouter-bloc : decision + branches min 2 (OUI/NON + --branche repetable)
    + deviation + rejoint, indices par REFERENCES (--ref-deviation/--ref-rejoint,
    defaut pattern-7) au lieu des textes inline -> valider-case ne signale plus
    de surcharge sur le bloc genere.
  - --ref <ref> (repetable) sur ajouter/editer : indice {"type": "ref", "ref": X}
  - Validation auto : appel interne valider-case --modele apres chaque commande.

Cas couverts:
  1. --version py/sh identiques v0.4.2 (parite)
  2. --aide : usage complet avec les options cles (--ref, --branche, ajouter-bloc)
  3. ajouter-bloc modele compose complet : 3 branches (OUI/NON/PEUT_ETRE)
  4. Indices deviation/rejoint = references pattern-7 (0 texte inline)
  5. --ref sur ajouter : indices {"type":"ref","ref":"pattern-12"} et protocole-tests
  6. --ref-deviation/--ref-rejoint personnalises (pattern-12)
  7. Validation auto : valider-case --modele appele et CONFORME (0 a alleger sur le bloc)
  8. --dry-run : aucune modification du fichier
  9. Parcours inexistant : ERREUR claire + code non nul
 10. JSON invalide : ERREUR claire + code non nul
 11. Protection : aucun fichier cree dans le dossier outil
 12. ASCII strict : 0 non-ASCII sur les 4 fichiers de l outil (+ spec)

Usage:
  python3 test-010-generateurs-case.py
"""
import importlib.util
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

def charger_protections():
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

PROTECTIONS = charger_protections()


OUTIL_DIR = os.path.join(TOOLS_DIR, "generateurs", "generateurs-case")
OUTIL_PY = os.path.join(OUTIL_DIR, "generateurs-case.py")
OUTIL_SH = os.path.join(OUTIL_DIR, "generateurs-case.sh")
OUTIL_MD = os.path.join(OUTIL_DIR, "generateurs-case.md")
OUTIL_SPEC = os.path.join(OUTIL_DIR, "spec", "spec-generateurs-case.001.01.ebauche.md")
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
    return PROTECTIONS.lancer_protege(cmd, capture_output=True, text=True, timeout=timeout)


def ascii_count(chemin):
    """Compte les caracteres non-ASCII d'un fichier (0 = conforme)."""
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        txt = fh.read()
    return sum(1 for c in txt if ord(c) > 127)


def charger_cases(chemin):
    with io.open(chemin, encoding="utf-8") as fh:
        return json.load(fh)["cases"]


def main():
    global NB_POINTS, NB_OK, NB_KO

    tmp = tempfile.mkdtemp(prefix="test-010-")
    try:
        print("=== Test formel generateurs-case v0.4.2 (etape 3 refonte) ===")

        # Copie de travail du parcours (jamais les vrais parcours)
        travail = os.path.join(tmp, "parcours.json")
        shutil.copyfile(PARCOURS_CERBERUS, travail)

        # 1. --version py/sh identiques (parite)
        r_py = run([PYTHON, OUTIL_PY, "x", "liste", "--version"])
        r_sh = run(["bash", OUTIL_SH, "x", "liste", "--version"])
        verifier("1. --version py/sh identiques v0.4.0",
                 r_py.returncode == 0 and r_sh.returncode == 0
                 and "v0.4.2" in r_py.stdout
                 and r_py.stdout.strip() == r_sh.stdout.strip(),
                 "py=%r sh=%r" % (r_py.stdout.strip(), r_sh.stdout.strip()))

        # 2. --aide : usage complet avec options cles
        r_aide = run([PYTHON, OUTIL_PY, "--aide"])
        verifier("2a. --aide retourne 0",
                 r_aide.returncode == 0, r_aide.stderr.strip()[-80:])
        verifier("2b. --aide racine liste ajouter-bloc (sous-commande)",
                 "ajouter-bloc" in r_aide.stdout
                 and "liste" in r_aide.stdout
                 and "supprimer" in r_aide.stdout,
                 r_aide.stdout.strip()[-200:])
        r_bloc_aide = run([PYTHON, OUTIL_PY, "x", "ajouter-bloc", "--aide"])
        verifier("2c. Aide ajouter-bloc expose --ref-deviation/--ref-rejoint/--branche",
                 r_bloc_aide.returncode == 0
                 and all(opt in r_bloc_aide.stdout for opt in
                         ("--ref-deviation", "--ref-rejoint", "--branche")),
                 r_bloc_aide.stdout.strip()[-200:])

        # 3. ajouter-bloc : modele compose complet (3 branches)
        r_bloc = run([PYTHON, OUTIL_PY, travail, "ajouter-bloc",
                      "--titre", "Test bloc", "--question", "Une question ?",
                      "--suite", "c13", "--apres", "c12",
                      "--branche", "PEUT_ETRE:c14"])
        verifier("3a. ajouter-bloc retourne 0",
                 r_bloc.returncode == 0, r_bloc.stdout.strip()[-150:])
        cases = charger_cases(travail)
        decision = [k for k, c in cases.items() if c.get("titre") == "Test bloc"]
        verifier("3b. Decision trouvee", len(decision) == 1, "ids: %s" % decision)
        id_dec = decision[0]
        branche = cases[id_dec].get("branches", [])
        verifier("3c. Decision a 3 branches (OUI/NON/PEUT_ETRE)",
                 len(branche) == 3 and branche[0]["reponse"] == "OUI"
                 and branche[1]["reponse"] == "NON"
                 and branche[2]["reponse"] == "PEUT_ETRE",
                 json.dumps(branche, ensure_ascii=True))

        # 4. Indices deviation/rejoint = references pattern-7 (0 texte inline)
        id_dev = id_dec + "a"
        id_rej = id_dec + "b"
        inds_dev = cases[id_dev].get("indices", [])
        inds_rej = cases[id_rej].get("indices", [])
        verifier("4a. Deviation porte un indice ref pattern-7",
                 len(inds_dev) == 1 and inds_dev[0].get("type") == "ref"
                 and inds_dev[0].get("ref") == "pattern-7",
                 json.dumps(inds_dev, ensure_ascii=True))
        verifier("4b. Rejoint porte un indice ref pattern-7",
                 len(inds_rej) == 1 and inds_rej[0].get("type") == "ref"
                 and inds_rej[0].get("ref") == "pattern-7",
                 json.dumps(inds_rej, ensure_ascii=True))
        verifier("4c. Aucun texte inline de regle dans deviation/rejoint",
                 all(ind.get("type") != "regle"
                     for ind in inds_dev + inds_rej),
                 json.dumps(inds_dev + inds_rej, ensure_ascii=True))

        # 4d. Type action : ajoute avec suivant (etape 5, spec-refonte critere 7)
        r_act = run([PYTHON, OUTIL_PY, travail, "ajouter",
                     "--type", "action", "--titre", "Action test",
                     "--suivant", "c13", "--case", "c40"])
        verifier("4d. ajouter --type action OK",
                 r_act.returncode == 0, r_act.stdout.strip()[-150:])
        cases = charger_cases(travail)
        verifier("4e. Case action porte suivant c13",
                 cases.get("c40", {}).get("type") == "action"
                 and cases.get("c40", {}).get("suivant") == "c13",
                 json.dumps(cases.get("c40"), ensure_ascii=True))

        # 5. --ref sur ajouter : indices de type reference
        r_ref = run([PYTHON, OUTIL_PY, travail, "ajouter",
                     "--type", "indice", "--titre", "Test ref",
                     "--suivant", "c13",
                     "--ref", "pattern-12", "--ref", "protocole-tests"])
        verifier("5a. ajouter --ref retourne 0",
                 r_ref.returncode == 0, r_ref.stdout.strip()[-150:])
        cases = charger_cases(travail)
        test_ref = [k for k, c in cases.items() if c.get("titre") == "Test ref"]
        verifier("5b. Case --ref trouvee", len(test_ref) == 1)
        inds_ref = cases[test_ref[0]].get("indices", [])
        verifier("5c. Indices de type ref pattern-12 + protocole-tests",
                 len(inds_ref) == 2
                 and inds_ref[0] == {"type": "ref", "ref": "pattern-12"}
                 and inds_ref[1] == {"type": "ref", "ref": "protocole-tests"},
                 json.dumps(inds_ref, ensure_ascii=True))

        # 6. --ref-deviation/--ref-rejoint personnalises
        travail2 = os.path.join(tmp, "parcours2.json")
        shutil.copyfile(PARCOURS_CERBERUS, travail2)
        r_ref2 = run([PYTHON, OUTIL_PY, travail2, "ajouter-bloc",
                      "--titre", "Bloc refs custom", "--suite", "c13",
                      "--ref-deviation", "pattern-12",
                      "--ref-rejoint", "protocole-tests"])
        verifier("6a. ajouter-bloc refs custom retourne 0",
                 r_ref2.returncode == 0, r_ref2.stdout.strip()[-150:])
        cases2 = charger_cases(travail2)
        id_dec2 = [k for k, c in cases2.items() if c.get("titre") == "Bloc refs custom"][0]
        inds_dev2 = cases2[id_dec2 + "a"].get("indices", [])
        inds_rej2 = cases2[id_dec2 + "b"].get("indices", [])
        verifier("6b. --ref-deviation pattern-12 applique",
                 inds_dev2[0].get("ref") == "pattern-12",
                 json.dumps(inds_dev2, ensure_ascii=True))
        verifier("6c. --ref-rejoint protocole-tests applique",
                 inds_rej2[0].get("ref") == "protocole-tests",
                 json.dumps(inds_rej2, ensure_ascii=True))

        # 7. Validation auto : valider-case --modele appele et CONFORME
        verifier("7a. Validation auto appelle valider-case",
                 "valider-case" in r_bloc.stdout
                 and "--modele" in r_bloc.stdout,
                 r_bloc.stdout.strip()[-200:])
        verifier("7b. Verdict CONFORME (0 a alleger sur le bloc genere)",
                 "CONFORME" in r_bloc.stdout
                 and "a alleger: 0" in r_bloc.stdout,
                 r_bloc.stdout.strip()[-200:])

        # 8. --dry-run : aucune modification
        travail3 = os.path.join(tmp, "parcours3.json")
        shutil.copyfile(PARCOURS_CERBERUS, travail3)
        avant = open(travail3, "rb").read()
        r_dry = run([PYTHON, OUTIL_PY, travail3, "ajouter-bloc",
                     "--titre", "DRY", "--suite", "c13", "--dry-run"])
        apres = open(travail3, "rb").read()
        verifier("8. --dry-run sans modification",
                 r_dry.returncode == 0 and avant == apres,
                 "dry-run a modifie le fichier")

        # 9. Parcours inexistant : ERREUR
        r_abs = run([PYTHON, OUTIL_PY, os.path.join(tmp, "absent.json"), "liste"])
        verifier("9. Parcours inexistant : ERREUR + code non nul",
                 r_abs.returncode != 0 and "ERREUR" in (r_abs.stdout + r_abs.stderr),
                 "code=%d" % r_abs.returncode)

        # 10. JSON invalide : ERREUR
        invalide = os.path.join(tmp, "invalide.json")
        with io.open(invalide, "w", encoding="utf-8") as fh:
            fh.write("{ ceci n est pas du json ")
        r_inv = run([PYTHON, OUTIL_PY, invalide, "liste"])
        verifier("10. JSON invalide : ERREUR + code non nul",
                 r_inv.returncode != 0 and "ERREUR" in (r_inv.stdout + r_inv.stderr),
                 "code=%d" % r_inv.returncode)

        # 11. Protection : aucun fichier cree dans le dossier outil
        avant = set(os.listdir(OUTIL_DIR))
        run([PYTHON, OUTIL_PY, travail, "liste"])
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
