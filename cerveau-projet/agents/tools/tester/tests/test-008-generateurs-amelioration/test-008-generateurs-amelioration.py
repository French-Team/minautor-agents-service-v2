#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-008-generateurs-amelioration.py
Test formel de l'outil generateurs-amelioration v2.1.0 (categorie generateurs/).

Outil teste (cerveau-projet/agents/tools/generateurs/generateurs-amelioration/):
  .py + .sh (wrapper pur exec python3) + .md + spec/ + themes-amelioration.json
  Pose une checklist de questions par THEME avant toute amelioration :
  --theme <nom> (interactif) | --reponses 'q1=...;q2=...' (non-interactif)
  --liste | --aide | --version. AUCUN fichier cree (reflexion en session).

Cas couverts:
  1. --version py/sh identiques v2.1.0 + themes affiches (parite)
  2. --liste : theme ameliorer-outil affiche (14 questions)
  3. themes-amelioration.json : JSON valide + structure (version, themes,
     questions avec id/question/raison)
  4. --theme ameliorer-outil --reponses : mode non-interactif, 14 reponses
     recapitulatives ([X] q1..q14) + message FIN DU QUESTIONNAIRE
  5. --aide : usage affiche (requis par detecter-decalages-catalogue)
  6. Theme inconnu (--theme inexistant) : ERREUR + code non nul
  7. Parite py/sh : sorties identiques sur --version, --liste et --reponses
  8. ASCII strict : 0 non-ASCII sur les 5 fichiers de l outil
  9. Protection : l interrogation ne cree AUCUN fichier (aucun residu)

Usage:
  python3 test-008-generateurs-amelioration.py
"""
import importlib.util
import io
import json
import os
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
# ------------------------------------------------------------------
# OPTIONS ON/OFF + CHRONO (regle immuable v0.3.0, deploiement dynamique) :
#   --no-chrono            desactive le chrono (defaut : actif)
#   --isoler N             n execute que le point N (diagnostic cible)
#   --desactiver 1,3,5     saute les points listes (sans toucher au code)
# ------------------------------------------------------------------
CHRONO_ACTIF = "--no-chrono" not in sys.argv
ISOLE = None
DESACTIVES = []
for _i, _arg in enumerate(sys.argv):
    if _arg == "--isoler" and _i + 1 < len(sys.argv):
        try:
            ISOLE = int(sys.argv[_i + 1])
        except ValueError:
            pass
    if _arg == "--desactiver" and _i + 1 < len(sys.argv):
        for _p in sys.argv[_i + 1].split(','):
            try:
                DESACTIVES.append(int(_p))
            except ValueError:
                pass
ETAPES = []
T_START = __import__("time").monotonic()


def point_actif(numero):
    # True si le point N doit s executer (options on/off du test)
    if ISOLE is not None:
        return numero == ISOLE
    return numero not in DESACTIVES


def chrono_etape(nom, t_debut):
    # Enregistre la duree d une etape (no-op si --no-chrono)
    if CHRONO_ACTIF:
        ETAPES.append((nom, __import__("time").monotonic() - t_debut))


def bilan_chrono():
    # Affiche le bilan des durees : total + detail par etape
    if not CHRONO_ACTIF:
        return
    _total = __import__("time").monotonic() - T_START
    print("")
    print("=== CHRONO test (total %.1fs) ===" % _total)
    for _nom, _duree in ETAPES:
        print("  %-34s %6.2fs" % (_nom, _duree))


OUTIL_DIR = os.path.join(TOOLS_DIR, "generateurs", "generateurs-amelioration")
OUTIL_PY = os.path.join(OUTIL_DIR, "generateurs-amelioration.py")
OUTIL_SH = os.path.join(OUTIL_DIR, "generateurs-amelioration.sh")
OUTIL_MD = os.path.join(OUTIL_DIR, "generateurs-amelioration.md")
OUTIL_SPEC = os.path.join(OUTIL_DIR, "spec", "spec-generateurs-amelioration.001.01.ebauche.md")
THEMES_JSON = os.path.join(OUTIL_DIR, "themes-amelioration.json")

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
    return PROTECTIONS.lancer_protege(cmd, capture_output=True, text=True, timeout=timeout)


def ascii_count(chemin):
    """Compte les caracteres non-ASCII d'un fichier (0 = conforme)."""
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        txt = fh.read()
    return sum(1 for c in txt if ord(c) > 127)


def main():
    global NB_POINTS, NB_OK, NB_KO

    tmp = tempfile.mkdtemp(prefix="test-008-")
    try:
        print("=== Test formel generateurs-amelioration v2.1.0 ===")

        # 1. --version py/sh identiques (parite) + version des themes affichee
        r_py = run([PYTHON, OUTIL_PY, "--version"])
        r_sh = run(["bash", OUTIL_SH, "--version"])
        verifier("1. --version py/sh identiques v2.1.0 + themes affiches",
                 r_py.returncode == 0 and r_sh.returncode == 0
                 and "v2.1.0" in r_py.stdout
                 and "themes v2.3.0" in r_py.stdout
                 and r_py.stdout.strip() == r_sh.stdout.strip(),
                 "py=%r sh=%r" % (r_py.stdout.strip(), r_sh.stdout.strip()))

        # 2. --liste : theme ameliorer-outil (14 questions)
        r_liste = run([PYTHON, OUTIL_PY, "--liste"])
        verifier("2a. --liste retourne 0",
                 r_liste.returncode == 0, r_liste.stderr.strip()[-80:])
        verifier("2b. Theme ameliorer-outil affiche (14 questions)",
                 "ameliorer-outil" in r_liste.stdout
                 and "14 questions" in r_liste.stdout,
                 r_liste.stdout.strip()[-120:])

        # 3. themes-amelioration.json : JSON valide + structure
        try:
            with io.open(THEMES_JSON, encoding="utf-8") as fh:
                themes = json.load(fh)
            ok_json = True
        except Exception as e:
            ok_json = False
            themes = {}
        theme = None
        for t in themes.get("themes", []):
            if t.get("nom") == "ameliorer-outil":
                theme = t
        questions = theme.get("questions", []) if theme else []
        verifier("3a. themes-amelioration.json : JSON valide", ok_json)
        verifier("3b. Structure {version, themes[]} valide",
                 "version" in themes and len(themes.get("themes", [])) >= 1)
        verifier("3c. Theme ameliorer-outil : 14 questions",
                 theme is not None and len(questions) == 14,
                 "nb questions = %d" % (len(questions) if theme else -1))
        verifier("3d. Chaque question a id/question/raison",
                 all(q.get("id") and q.get("question") and q.get("raison")
                     for q in questions))

        # 4. Interrogation non-interactive (--reponses) : recapitulatif complet
        reponses = ";".join("q%d=reponse %d" % (i, i) for i in range(1, 15))
        r_int = run([PYTHON, OUTIL_PY, "--theme", "ameliorer-outil",
                     "--reponses", reponses])
        sortie = r_int.stdout
        verifier("4a. Interrogation retourne 0",
                 r_int.returncode == 0, r_int.stderr.strip()[-80:])
        verifier("4b. Recapitulatif : 14 cases cochees ([X] q1..q14)",
                 all("[X] q%d" % i in sortie for i in range(1, 15)),
                 "cases manquantes")
        verifier("4c. Message FIN DU QUESTIONNAIRE present",
                 "FIN DU QUESTIONNAIRE" in sortie)
        verifier("4d. 14 reponses recapitulatives affichees",
                 all("-> reponse %d" % i in sortie for i in range(1, 15)),
                 "reponses manquantes")

        # 5. --aide : usage affiche (requis par detecter-decalages-catalogue)
        r_aide = run([PYTHON, OUTIL_PY, "--aide"])
        verifier("5a. --aide retourne 0",
                 r_aide.returncode == 0, r_aide.stderr.strip()[-80:])
        verifier("5b. --aide affiche l usage (USAGE + --theme)",
                 "USAGE" in r_aide.stdout and "--theme" in r_aide.stdout)

        # 6. Theme inconnu : ERREUR + code non nul
        r_inc = run([PYTHON, OUTIL_PY, "--theme", "inexistant"])
        verifier("6a. Theme inconnu : code non nul",
                 r_inc.returncode != 0,
                 "code=%d" % r_inc.returncode)
        verifier("6b. Theme inconnu : message d erreur clair",
                 "theme" in r_inc.stdout.lower() and "inconnu" in r_inc.stdout.lower(),
                 r_inc.stdout.strip()[-120:])

        # 7. Parite py/sh : sorties identiques
        r_sh_liste = run(["bash", OUTIL_SH, "--liste"])
        verifier("7a. Parite --liste py/sh identiques",
                 r_liste.stdout.strip() == r_sh_liste.stdout.strip())
        r_sh_int = run(["bash", OUTIL_SH, "--theme", "ameliorer-outil",
                        "--reponses", reponses])
        verifier("7b. Parite interrogation py/sh identiques",
                 r_int.stdout.strip() == r_sh_int.stdout.strip(),
                 "py=%d octets sh=%d octets" % (len(r_int.stdout), len(r_sh_int.stdout)))

        # 8. ASCII strict : 0 non-ASCII sur les 5 fichiers de l outil
        fichiers = [OUTIL_PY, OUTIL_SH, OUTIL_MD, OUTIL_SPEC, THEMES_JSON]
        total_non_ascii = sum(ascii_count(f) for f in fichiers)
        verifier("8. ASCII strict : 0 non-ASCII (5 fichiers)",
                 total_non_ascii == 0,
                 "total non-ASCII = %d" % total_non_ascii)

        # 9. Protection : aucune creation de fichier pendant l interrogation
        contenu_dossier = set(os.listdir(OUTIL_DIR))
        r_prot = run([PYTHON, OUTIL_PY, "--theme", "ameliorer-outil",
                      "--reponses", reponses])
        contenu_apres = set(os.listdir(OUTIL_DIR))
        verifier("9. Protection : aucun fichier cree dans le dossier outil",
                 r_prot.returncode == 0 and contenu_dossier == contenu_apres,
                 "cree: %s" % (contenu_apres - contenu_dossier))

        print("")
        bilan_chrono()
        print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
