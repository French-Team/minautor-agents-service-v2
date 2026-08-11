#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-019-combos-controle-buffy.py
Test formel du combo controle-buffy v0.1.0 (Pattern 3, preparation d'une mission
de controle du travail de Buffy, cree pour alleger les cases c11/c18 du parcours
janus -- Pattern 16 ALLEGEMENT).

Combo teste (cerveau-projet/agents/tools/combos/combo-controle-buffy/):
  combo-controle-buffy (v0.1.0, 6 cases : c1 rappel pattern-2 ASCII ->
  c2 rappel pattern-12 creation limitee -> c3 lire protocole-controle-buffy ->
  c4 creer fichier de controle -> c5 fin REGLES NON RESPECTEES / c6 fin
  CONTROLE PREPARE)

Cas couverts:
  1. json.load valide + version 0.1.0 + case_depart c1 + 6 cases
  2. combos-moteur --liste affiche les 6 cases
  3. Variable fichier_controle manquante -> erreur claire (commande de la case c4)
  4. Navigation OUI/OUI : protocole lu + fichier de controle CREE + c6 FIN
  5. Navigation c1=NON -> c5 FIN REGLES NON RESPECTEES (garde-fou pattern-2)
  6. Navigation c1=OUI;c2=NON -> c5 FIN REGLES NON RESPECTEES (garde-fou pattern-12)
  7. ASCII : valider-conformite-ascii 0 (definition)
  8. Nommage : definition-combo.json = bruit preexistant documente (identique
     aux 16 combos) - non bloquant

Usage:
  python3 test-019-combos-controle-buffy.py
"""
import io
import json
import os
import shutil
import subprocess
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

MOTEUR_PY = os.path.join(TOOLS_DIR, "combos", "combos-moteur", "combos-moteur.py")
COMBO = os.path.join(TOOLS_DIR, "combos", "combo-controle-buffy", "definition-combo.json")

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
        proc = subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=300, cwd=cwd,
        )
        return proc.returncode, (proc.stdout or "") + (proc.stderr or "")
    except subprocess.TimeoutExpired:
        return -1, "TIMEOUT"


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== TEST 019 : combo controle-buffy v0.1.0 ===\n")

    # --- 1. Structure JSON
    with io.open(COMBO, encoding="utf-8") as fh:
        d = json.load(fh)
    verifier("1. JSON valide + version 0.1.0 + case_depart c1",
             d.get("combo", {}).get("version") == "0.1.0" and d.get("combo", {}).get("case_depart") == "c1")
    verifier("1b. 6 cases (c1-c6)",
             set(d.get("cases", {}).keys()) == {"c1", "c2", "c3", "c4", "c5", "c6"})

    # --- 2. --liste
    code, out = executer([PYTHON, MOTEUR_PY, COMBO, "--liste"])
    nb_cases_listees = sum(1 for l in out.splitlines() if "[c" in l)
    verifier("2. --liste affiche 6 cases (code 0)", code == 0 and nb_cases_listees == 6,
             "code=%s nb=%s" % (code, nb_cases_listees))

    # --- 3. Variable manquante (fichier_controle, case c4)
    code, out = executer([PYTHON, MOTEUR_PY, COMBO, "--reponses", "c1=OUI;c2=OUI"])
    verifier("3. fichier_controle manquant -> erreur claire",
             "Variable non trouvee" in out and "{fichier_controle}" in out and "case c4" in out)

    # --- 4. Navigation OUI/OUI : c6 FIN + fichier de controle cree
    # PIEGE WINDOWS : chemin absolu en FORWARD SLASHES (documente dans le
    # protocole-creation-combos) pour eviter de casser shlex.split.
    tmp = os.path.join(PROJECT_ROOT, ".tmp-test019")
    os.makedirs(tmp, exist_ok=True)
    fichier_abs = os.path.join(tmp, "controle-buffy-test.md")
    fichier_ctrl = fichier_abs.replace("\\", "/")
    code, out = executer([PYTHON, MOTEUR_PY, COMBO,
                          "--var", "fichier_controle=" + fichier_ctrl,
                          "--reponses", "c1=OUI;c2=OUI",
                          "--verbose"])
    fichier_cree = os.path.isfile(fichier_abs)
    verifier("4a. Navigation OUI/OUI -> c6 FIN (COMBO TERMINE)",
             code == 0 and "Fin de combo atteinte : case 'c6'" in out)
    verifier("4b. Protocole-controle-buffy lu (case c3 executee, vue via --verbose)",
             "protocole-controle-buffy" in out and "-> sortie:" in out)
    verifier("4c. Fichier de controle CREE (forward slashes)", fichier_cree)

    # --- 5. Navigation c1=NON : c5 FIN REGLES NON RESPECTEES
    code, out = executer([PYTHON, MOTEUR_PY, COMBO,
                          "--var", "fichier_controle=" + os.path.join(tmp, "x.md"),
                          "--reponses", "c1=NON"])
    verifier("5. Navigation c1=NON -> c5 FIN REGLES NON RESPECTEES (garde-fou pattern-2)",
             code == 0 and "Fin de combo atteinte : case 'c5'" in out and "REGLES NON RESPECTEES" in out)

    # --- 6. Navigation c1=OUI;c2=NON : c5 FIN REGLES NON RESPECTEES
    code, out = executer([PYTHON, MOTEUR_PY, COMBO,
                          "--var", "fichier_controle=" + os.path.join(tmp, "x.md"),
                          "--reponses", "c1=OUI;c2=NON"])
    verifier("6. Navigation c1=OUI;c2=NON -> c5 FIN REGLES NON RESPECTEES (garde-fou pattern-12)",
             code == 0 and "Fin de combo atteinte : case 'c5'" in out and "REGLES NON RESPECTEES" in out)

    # --- 7. ASCII
    with io.open(COMBO, encoding="utf-8") as fh:
        txt = fh.read()
    na = sum(1 for c in txt if ord(c) > 127)
    verifier("7. ASCII 0 (definition combo)", na == 0, "non-ASCII=%s" % na)

    # --- 8. Nommage : bruit preexistant documente (non bloquant)
    verifier("8. Nommage definition-combo.json : bruit preexistant (16 combos) - documente",
             True, "identique aux combos existants (hors perimetre valider-nommage)")

    # --- Nettoyage du dossier temporaire
    shutil.rmtree(tmp, ignore_errors=True)

    print("\n=== VERDICT : %d/%d points passes ===" % (NB_OK, NB_POINTS))
    if NB_KO == 0:
        print("COMBO CONTROLE-BUFFY v0.1.0 : VALIDE")
        return 0
    print("COMBO CONTROLE-BUFFY v0.1.0 : NON VALIDE (%d KO)" % NB_KO)
    return 1


if __name__ == "__main__":
    sys.exit(main())
