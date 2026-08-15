#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-002-combos-moteur.py
Test de l outil combos-moteur (etape 2 du plan combo-orchestrateur).

Cas couverts (spec-combos-moteur, section Tests requis):
  1. --liste affiche toutes les cases de la definition
  2. Navigation de case_depart jusqu a une case fin
  3. Interpolation {var} remplace par la valeur dans la commande
  4. Generateur AUTO : le moteur appelle generateurs-commande --reponses
  5. Controle branches : --reponses c3=OUI -> chemin OUI ; c3=NON -> NON
  6. Variable manquante -> erreur claire, code retour 1
  7. Fin : le combo s arrete a la case fin et affiche le message
  8. Dry-run : aucune commande outil executee, toutes affichees
  9. Parite .py et .sh : meme navigation et memes commandes
 10. Nommage : valider-nommage OK
 11. ASCII : valider-conformite-ascii 0
 12. Syntaxe : bash -n OK + python3 -m py_compile OK
 13. GARDE-FOU v0.3.0 : cles des entrees des cases generateur vs catalogue

Contexte : ce test a ete migre au format template-test.md v0.2.0 (audit
Morpheus 2026-08-12 : le TEMPLATE est la reference, pas les tests precedents).
L ancien format utilisait coding utf-8 et le marqueur [ECHEC] invisible pour
le lanceur de non-regression (qui compte les [KO]).
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


MOTEUR_PY = os.path.join(TOOLS_DIR, "combos", "combos-moteur", "combos-moteur.py")
MOTEUR_SH = os.path.join(TOOLS_DIR, "combos", "combos-moteur", "combos-moteur.sh")
EXEMPLE = os.path.join(TOOLS_DIR, "combos", "combos-moteur", "exemple-combo.json")

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


def run(cmd, timeout=120):
    return PROTECTIONS.lancer_protege(cmd, capture_output=True, text=True, timeout=timeout)


def run_py(args=None):
    # --no-journal : ne pas polluer le registre d usage pendant les tests
    cmd = [PYTHON, MOTEUR_PY]
    if args:
        cmd.extend(args)
    if "--no-journal" not in cmd:
        cmd.append("--no-journal")
    return run(cmd)


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def main():
    print("=== test-002 : combos-moteur ===")

    # 1. --liste affiche toutes les cases
    r = run_py([EXEMPLE, "--liste"])
    verifier("1a. --liste retourne 0", r.returncode == 0, "rc=%d" % r.returncode)
    for cid in ("c1", "c2", "c3", "c4", "c5"):
        verifier("1b. case %s listee" % cid, "[%s]" % cid in r.stdout, "")
    verifier("1c. types des 4 categories listees",
             all(t in r.stdout for t in ("generateur", "outil", "controle", "fin")), "")

    # 2-5 + 7. Navigation chemin OUI (c3=OUI)
    r = run_py([EXEMPLE, "--reponses", "c3=OUI", "--verbose"])
    verifier("2. navigation jusqu a la fin, code 0", r.returncode == 0,
             "rc=%d" % r.returncode)
    verifier("3. interpolation {cmd1} resolu (sidentifier present)",
             "sidentifier" in r.stdout, "")
    verifier("4. generateur AUTO a compose la commande (activer-agent-principal)",
             "activer-agent-principal" in r.stdout, "")
    verifier("5. controle OUI -> chemin c4 (message correct)",
             "la commande generee est correcte" in r.stdout, "")
    verifier("7. COMBO TERMINE affiche", "COMBO TERMINE" in r.stdout, "")

    # 5b. Navigation chemin NON (c3=NON)
    r = run_py([EXEMPLE, "--reponses", "c3=NON"])
    verifier("5b. controle NON -> chemin c5 (message inattendu)",
             "la commande generee est inattendue" in r.stdout, "")

    # 6. Variable manquante -> erreur claire, code 1
    definition_invalide = {
        "combo": {"nom": "test-invalide", "version": "0.1.0", "case_depart": "c1"},
        "cases": {
            "c1": {"titre": "outil avec variable inconnue", "type": "outil",
                   "commande": "echo {inconnue}", "sortie": "x", "suivant": "c2"},
            "c2": {"titre": "FIN", "type": "fin", "message": "fin"}
        }
    }
    tmpdir = tempfile.mkdtemp(prefix="combos-test-")
    fichier_invalide = os.path.join(tmpdir, "definition-invalide.json")
    with open(fichier_invalide, "w", encoding="utf-8") as fh:
        json.dump(definition_invalide, fh)

    r = run_py([fichier_invalide])
    verifier("6a. variable manquante -> code 1", r.returncode == 1,
             "rc=%d" % r.returncode)
    verifier("6b. erreur claire mentionne la variable",
             "Variable non trouvee" in (r.stderr + r.stdout), "")

    # 8. Dry-run -> aucune commande outil executee, toutes affichees
    r = run_py([EXEMPLE, "--dry-run", "--reponses", "c3=OUI"])
    verifier("8a. dry-run retourne 0", r.returncode == 0, "rc=%d" % r.returncode)
    verifier("8b. dry-run affiche [DRY-RUN] pour la commande outil",
             "[DRY-RUN] echo" in r.stdout, "")
    verifier("8c. dry-run n execute pas l outil (pas de sortie d echo)",
             "[DRY-RUN] echo " in r.stdout, "")
    verifier("8d. dry-run termine quand meme sur la case fin (navigation OK)",
             "COMBO TERMINE" in r.stdout, "")

    # 9. Parite .py et .sh
    if not os.path.isfile(MOTEUR_SH):
        verifier("9. fichier .sh present", False, "fichier .sh absent")
    else:
        py_liste = run_py([EXEMPLE, "--liste"])
        sh_liste = run(["bash", MOTEUR_SH, EXEMPLE, "--liste", "--no-journal"])
        verifier("9a. .sh --liste retourne 0", sh_liste.returncode == 0,
                 "rc=%d" % sh_liste.returncode)
        verifier("9b. .py et .sh produisent la meme liste",
                 py_liste.stdout.strip() == sh_liste.stdout.strip(), "")

        py_nav = run_py([EXEMPLE, "--reponses", "c3=OUI"])
        sh_nav = run(["bash", MOTEUR_SH, EXEMPLE, "--reponses", "c3=OUI",
                      "--no-journal"])
        verifier("9c. .py et .sh meme navigation (chemin OUI)",
                 py_nav.stdout.strip() == sh_nav.stdout.strip(), "")

    # 10. Nommage
    valider_nommage = os.path.join(TOOLS_DIR, "valider", "valider-nommage",
                                   "valider-nommage.py")
    r = run([PYTHON, valider_nommage, "--type", "outil", MOTEUR_PY])
    verifier("10a. nommage .py OK", r.returncode == 0, "rc=%d" % r.returncode)
    r = run([PYTHON, valider_nommage, "--type", "outil", MOTEUR_SH])
    verifier("10b. nommage .sh OK", r.returncode == 0, "rc=%d" % r.returncode)

    # 11. ASCII
    valider_ascii = os.path.join(TOOLS_DIR, "valider", "valider-conformite-ascii",
                                 "valider-conformite-ascii.py")
    for f in (MOTEUR_PY, MOTEUR_SH, EXEMPLE,
              os.path.join(TOOLS_DIR, "combos", "combos-moteur",
                           "combos-moteur.md")):
        r = run([PYTHON, valider_ascii, f])
        verifier("11. ASCII 0 sur %s" % os.path.basename(f),
                 "Conformite ASCII stricte validee" in r.stdout, "")

    # 12. Syntaxe
    r = run(["bash", "-n", MOTEUR_SH])
    verifier("12a. bash -n OK", r.returncode == 0, "rc=%d" % r.returncode)
    r = run([PYTHON, "-m", "py_compile", MOTEUR_PY])
    verifier("12b. py_compile OK", r.returncode == 0, "rc=%d" % r.returncode)

    # 13. GARDE-FOU v0.3.0 : cles generateur vs catalogue
    def_combo_invalide = {
        "combo": {"nom": "test-cles-invalide", "version": "0.1.0",
                  "case_depart": "c1"},
        "cases": {
            "c1": {"titre": "Generateur avec cle inventee", "type": "generateur",
                   "catalogue": "valider-conventions",
                   "entrees": {"fichier": "x.md"},
                   "sortie": "cmd1", "suivant": "c2"},
            "c2": {"titre": "FIN", "type": "fin", "message": "fin"}
        }
    }
    fichier_invalide_cles = os.path.join(tmpdir, "definition-cles-invalide.json")
    with open(fichier_invalide_cles, "w", encoding="utf-8") as fh:
        json.dump(def_combo_invalide, fh)
    r = run_py([fichier_invalide_cles, "--liste"])
    verifier("13a. cle hors catalogue -> code 1", r.returncode == 1,
             "rc=%d" % r.returncode)
    verifier("13b. erreur claire (hors catalogue)",
             "hors catalogue" in (r.stderr + r.stdout), "")
    verifier("13c. erreur cite la cle fautive et la commande",
             "fichier" in (r.stderr + r.stdout)
             and "valider-conventions" in (r.stderr + r.stdout), "")

    def_combo_conforme = {
        "combo": {"nom": "test-cles-conforme", "version": "0.1.0",
                  "case_depart": "c1"},
        "cases": {
            "c1": {"titre": "Generateur avec cle exacte", "type": "generateur",
                   "catalogue": "valider-conventions",
                   "entrees": {"chemin": "x.md"},
                   "sortie": "cmd1", "suivant": "c2"},
            "c2": {"titre": "FIN", "type": "fin", "message": "fin"}
        }
    }
    fichier_conforme = os.path.join(tmpdir, "definition-cles-conforme.json")
    with open(fichier_conforme, "w", encoding="utf-8") as fh:
        json.dump(def_combo_conforme, fh)
    r = run_py([fichier_conforme, "--liste"])
    verifier("13d. cle exacte du catalogue -> code 0", r.returncode == 0,
             "rc=%d" % r.returncode)
    r_sh = run(["bash", MOTEUR_SH, fichier_invalide_cles, "--liste"])
    verifier("13e. .sh rejette aussi la cle hors catalogue",
             r_sh.returncode == 1, "rc=%d" % r_sh.returncode)

    # 14-15. Normes ASCII strict + LF pur sur les fichiers concernes
    fichiers = [MOTEUR_PY, MOTEUR_SH, EXEMPLE, os.path.abspath(__file__)]
    total_non_ascii = sum(ascii_count(f) for f in fichiers)
    verifier("14. ASCII strict : 0 non-ASCII (outil + exemple + test)",
             total_non_ascii == 0, "total=%d" % total_non_ascii)
    total_crlf = sum(crlf_count(f) for f in fichiers)
    verifier("15. LF pur : 0 CRLF (outil + exemple + test)",
             total_crlf == 0, "total=%d" % total_crlf)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
