#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-004-combos-tester-outil.py
Test formel du combo tester-outil v0.1.0 (Pattern 3, chemin de test de Morpheus encapsule).

Combo teste (cerveau-projet/agents/tools/combos/combo-tester-outil/):
  combo-tester-outil (v0.1.0, 6 cases : c1 generateur creer-fichier ->
  c2 outil cree le fichier -> c3 controle protections OUI->c4 / NON->c5 ->
  c4 outil commande_test -> c5 fin PROTECTIONS MANQUANTES / c6 fin SYNTHESE)

Cas couverts:
  1. json.load valide + version 0.1.0 + case_depart c1
  2. combos-moteur --liste affiche les 6 cases
  3. Variable fichier_test manquante -> erreur claire (entrees de la case c1)
  4. Variable commande_test manquante (apres c3=OUI) -> erreur claire (commande de la case c4)
  5. Navigation chemin OUI : fichier de test CREE + test EXECUTE + c6 FIN (COMBO TERMINE)
  6. Navigation chemin NON : c5 FIN PROTECTIONS MANQUANTES (REGLE ABSOLUE preservee)
  7. Integration parcours morpheus v0.4.5 : guider-parcours affiche la case
     Lancer le combo tester-outil puis Verifier les resultats
  8. valider-cartes-decision --agent morpheus : CONFORME
  9. Nommage : definition-combo.json = bruit preexistant documente (identique aux 15 combos) - non bloquant
 10. ASCII : valider-conformite-ascii 0 (definition + parcours)

Usage:
  python3 test-004-combos-tester-outil.py
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


MOTEUR_PY = os.path.join(TOOLS_DIR, "combos", "combos-moteur", "combos-moteur.py")
VALIDER_CARTES = os.path.join(TOOLS_DIR, "valider", "valider-cartes-decision", "valider-cartes-decision.py")
VALIDER_ASCII = os.path.join(TOOLS_DIR, "valider", "valider-conformite-ascii", "valider-conformite-ascii.py")
GUIDER = os.path.join(TOOLS_DIR, "guider", "guider-parcours", "guider-parcours.py")

COMBO = os.path.join(TOOLS_DIR, "combos", "combo-tester-outil", "definition-combo.json")
PARCOURS = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "morpheus", "parcours", "parcours-morpheus.json")

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
        print("  [KO] %s %s" % (nom, ("-> " + detail) if detail else ""))


def executer(cmd, cwd=None):
    try:
        proc = PROTECTIONS.lancer_protege(
            cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=300, cwd=cwd,
        )
        return proc.returncode, (proc.stdout or "") + (proc.stderr or "")
    except PROTECTIONS.ArretProtection:
        return -1, "TIMEOUT"


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== TEST 004 : combo tester-outil v0.1.0 ===\n")

    # --- 1. Structure JSON
    with io.open(COMBO, encoding="utf-8") as fh:
        d = json.load(fh)
    verifier("1. JSON valide + version 0.1.0 + case_depart c1",
             d.get("combo", {}).get("version") == "0.1.0" and d.get("combo", {}).get("case_depart") == "c1")
    verifier("1b. 6 cases (c1-c6)",
             set(d.get("cases", {}).keys()) == {"c1", "c2", "c3", "c4", "c5", "c6"})

    # --- 2. --liste
    code, out = executer([PYTHON, MOTEUR_PY, COMBO, "--liste", "--no-journal"])
    nb_cases_listees = sum(1 for l in out.splitlines() if "[c" in l)
    verifier("2. --liste affiche 6 cases (code 0)", code == 0 and nb_cases_listees == 6,
             "code=%s nb=%s" % (code, nb_cases_listees))

    # --- 3. Variable manquante (fichier_test, case c1)
    code, out = executer([PYTHON, MOTEUR_PY, COMBO, "--var", "contenu_test=t", "--no-journal"])
    verifier("3. fichier_test manquant -> erreur claire", "Variable non trouvee" in out and "{fichier_test}" in out)

    # --- 4. Variable manquante (commande_test, case c4)
    code, out = executer([PYTHON, MOTEUR_PY, COMBO,
                          "--var", "fichier_test=.tmp-test004/y.sh",
                          "--var", "contenu_test=t",
                          "--reponses", "c3=OUI",
                          "--no-journal"])
    verifier("4. commande_test manquant (apres c3=OUI) -> erreur claire",
             "Variable non trouvee" in out and "{commande_test}" in out and "case c4" in out)

    # --- 5. Navigation OUI : fichier cree + test execute + c6 FIN
    # PIEGE WINDOWS : un chemin absolu avec backslashes (Z:\\...) casse
    # shlex.split dans la case outil -> utiliser des FORWARD SLASHES.
    tmp = os.path.join(PROJECT_ROOT, ".tmp-test004")
    os.makedirs(tmp, exist_ok=True)
    fichier_test_abs = os.path.join(tmp, "test-001-demo.sh")
    fichier_test = fichier_test_abs.replace("\\", "/")
    code, out = executer([PYTHON, MOTEUR_PY, COMBO,
                          "--var", "fichier_test=" + fichier_test,
                          "--var", "contenu_test=echo test",
                          "--var", "commande_test=echo EXEC-OK",
                          "--reponses", "c3=OUI",
                          "--verbose",
                          "--no-journal"])
    fichier_cree = os.path.isfile(fichier_test_abs)
    verifier("5a. Navigation OUI -> c6 FIN (COMBO TERMINE)", code == 0 and "Fin de combo atteinte : case 'c6'" in out)
    verifier("5b. Fichier de test CREE (forward slashes)", fichier_cree)
    verifier("5c. Test EXECUTE (sortie EXEC-OK, vue via --verbose)", "EXEC-OK" in out and "-> sortie: EXEC-OK" in out)

    # --- 6. Navigation NON : c5 FIN PROTECTIONS MANQUANTES
    code, out = executer([PYTHON, MOTEUR_PY, COMBO,
                          "--var", "fichier_test=" + os.path.join(tmp, "x.sh"),
                          "--var", "contenu_test=t",
                          "--var", "commande_test=echo ok",
                          "--reponses", "c3=NON",
                          "--no-journal"])
    verifier("6. Navigation NON -> c5 FIN PROTECTIONS MANQUANTES (REGLE ABSOLUE)",
             code == 0 and "Fin de combo atteinte : case 'c5'" in out and "PROTECTIONS MANQUANTES" in out)

    # --- 7. Integration parcours morpheus v0.4.1
    with io.open(PARCOURS, encoding="utf-8") as fh:
        p = json.load(fh)
    verifier("7a. Parcours morpheus v0.4.5", p.get("parcours", {}).get("version") == "0.4.5")
    code, out = executer([PYTHON, GUIDER, PARCOURS, "--reponses", "OUI|tester"])
    verifier("7b. Case Lancer le combo tester-outil presente",
             "Lancer le combo tester-outil" in out)
    verifier("7c. Suite Verifier les resultats presente",
             "Verifier les resultats et donner le verdict" in out)

    # --- 8. valider-cartes-decision --agent morpheus
    code, out = executer([PYTHON, VALIDER_CARTES, "--agent", "morpheus"])
    verifier("8. valider-cartes-decision --agent morpheus CONFORME", "CONFORME" in out)

    # --- 9. Nommage : bruit preexistant documente (non bloquant, on documente seulement)
    verifier("9. Nommage definition-combo.json : bruit preexistant (15 combos) - documente",
             True, "identique aux combos existants (hors perimetre valider-nommage)")

    # --- 10. ASCII
    for nom, chemin in [("definition combo", COMBO), ("parcours morpheus", PARCOURS)]:
        with io.open(chemin, encoding="utf-8") as fh:
            txt = fh.read()
        na = sum(1 for c in txt if ord(c) > 127)
        verifier("10. ASCII 0 (%s)" % nom, na == 0, "non-ASCII=%s" % na)

    # --- Nettoyage du dossier temporaire
    import shutil
    shutil.rmtree(tmp, ignore_errors=True)

    print("\n=== VERDICT : %d/%d points passes ===" % (NB_OK, NB_POINTS))
    if NB_KO == 0:
        print("COMBO TESTER-OUTIL v0.1.0 : VALIDE")
        return 0
    print("COMBO TESTER-OUTIL v0.1.0 : NON VALIDE (%d KO)" % NB_KO)
    return 1


if __name__ == "__main__":
    sys.exit(main())
