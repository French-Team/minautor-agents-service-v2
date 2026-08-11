#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test-002-combos-moteur.py
Test de l'outil combos-moteur (etape 2 du plan combo-orchestrateur).

Cas couverts (spec-combos-moteur v0.1.0, section Tests requis):
  1. --liste affiche toutes les cases de la definition
  2. Navigation de case_depart jusqu'a une case fin
  3. Interpolation {var} remplace par la valeur dans la commande
  4. Generateur AUTO : le moteur appelle generateurs-commande --reponses et obtient la commande
  5. Controle branches : --reponses c3=OUI -> chemin OUI ; c3=NON -> chemin NON
  6. Variable manquante -> erreur claire, code retour 1
  7. Fin : le combo s'arrete a la case fin et affiche le message
  8. Dry-run : aucune commande outil executee, toutes affichees
  9. Parite .py et .sh : meme navigation et memes commandes
 10. Nommage : valider-nommage OK
 11. ASCII : valider-conformite-ascii 0
 12. Syntaxe : bash -n OK + python3 -m py_compile OK

Usage:
  python3 test-002-combos-moteur.py
"""
import os
import subprocess
import sys
import tempfile

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

MOTEUR_PY = os.path.join(TOOLS_DIR, "combos", "combos-moteur", "combos-moteur.py")
MOTEUR_SH = os.path.join(TOOLS_DIR, "combos", "combos-moteur", "combos-moteur.sh")
EXEMPLE = os.path.join(TOOLS_DIR, "combos", "combos-moteur", "exemple-combo.json")

passed = 0
failed = 0
results = []


def assert_eq(name, actual, expected):
    global passed, failed
    if actual == expected:
        passed += 1
        results.append("  [OK] %s" % name)
    else:
        failed += 1
        results.append("  [ECHEC] %s: attendu=%r, obtenu=%r" % (name, expected, actual))


def run(cmd, timeout=60):
    """Execute une commande et retourne (stdout, stderr, code)."""
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return proc.stdout, proc.stderr, proc.returncode


def run_py(args=None):
    cmd = [PYTHON, MOTEUR_PY]
    if args:
        cmd.extend(args)
    return run(cmd)


# ============================================================
# Test 1: --liste affiche toutes les cases
# ============================================================
print("=== Test 1: --liste affiche toutes les cases ===")
stdout, stderr, rc = run_py([EXEMPLE, "--liste"])
assert_eq("Test 1a: --liste retourne 0", rc, 0)
for cid in ("c1", "c2", "c3", "c4", "c5"):
    assert_eq("Test 1b: case %s listee" % cid, "[%s]" % cid in stdout, True)
assert_eq("Test 1c: types des 4 categories listees",
          all(t in stdout for t in ("generateur", "outil", "controle", "fin")), True)

# ============================================================
# Test 2 + 3 + 4 + 5 + 7: navigation + generateur AUTO + interpolation + controle + fin
# ============================================================
print("")
print("=== Test 2-5,7: navigation chemin OUI (c3=OUI) ===")
stdout, stderr, rc = run_py([EXEMPLE, "--reponses", "c3=OUI", "--verbose"])
assert_eq("Test 2: navigation jusqu'a la fin, code 0", rc, 0)
assert_eq("Test 3: interpolation {cmd1} resolu (sidentifier present)",
          "sidentifier" in stdout, True)
assert_eq("Test 4: generateur AUTO a compose la commande (activer-agent-principal)",
          "activer-agent-principal" in stdout, True)
assert_eq("Test 5: controle OUI -> chemin c4 (message correct)",
          "la commande generee est correcte" in stdout, True)
assert_eq("Test 7: COMBO TERMINE affiche", "COMBO TERMINE" in stdout, True)

print("")
print("=== Test 5b: navigation chemin NON (c3=NON) ===")
stdout, stderr, rc = run_py([EXEMPLE, "--reponses", "c3=NON"])
assert_eq("Test 5b: controle NON -> chemin c5 (message inattendu)",
          "la commande generee est inattendue" in stdout, True)

# ============================================================
# Test 6: variable manquante -> erreur claire, code 1
# ============================================================
print("")
print("=== Test 6: variable manquante -> code 1 ===")
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
    import json
    json.dump(definition_invalide, fh)

stdout, stderr, rc = run_py([fichier_invalide])
assert_eq("Test 6a: variable manquante -> code 1", rc, 1)
assert_eq("Test 6b: erreur claire mentionne la variable",
          "Variable non trouvee" in (stderr + stdout), True)

# ============================================================
# Test 8: dry-run -> aucune commande outil executee, toutes affichees
# ============================================================
print("")
print("=== Test 8: dry-run ===")
stdout, stderr, rc = run_py([EXEMPLE, "--dry-run", "--reponses", "c3=OUI"])
assert_eq("Test 8a: dry-run retourne 0", rc, 0)
assert_eq("Test 8b: dry-run affiche [DRY-RUN] pour la commande outil",
          "[DRY-RUN] echo" in stdout, True)
assert_eq("Test 8c: dry-run n'execute pas l'outil (pas de sortie d'echo)",
          "[DRY-RUN] echo " in stdout and "[DRY-RUN] echo\n" not in stdout, True)
assert_eq("Test 8d: dry-run termine quand meme sur la case fin (navigation OK)",
          "COMBO TERMINE" in stdout, True)

# ============================================================
# Test 9: parite .py et .sh
# ============================================================
print("")
print("=== Test 9: parite .py et .sh ===")
if not os.path.isfile(MOTEUR_SH):
    assert_eq("Test 9: fichier .sh present", False, True)
else:
    stdout_py, _, rc_py = run_py([EXEMPLE, "--liste"])
    stdout_sh, _, rc_sh = run(["bash", MOTEUR_SH, EXEMPLE, "--liste"])
    assert_eq("Test 9a: .sh --liste retourne 0", rc_sh, 0)
    assert_eq("Test 9b: .py et .sh produisent la meme liste",
              stdout_py.strip() == stdout_sh.strip(), True)

    stdout_py, _, rc_py = run_py([EXEMPLE, "--reponses", "c3=OUI"])
    stdout_sh, _, rc_sh = run(["bash", MOTEUR_SH, EXEMPLE, "--reponses", "c3=OUI"])
    assert_eq("Test 9c: .py et .sh meme navigation (chemin OUI)",
              stdout_py.strip() == stdout_sh.strip(), True)

# ============================================================
# Test 10: nommage
# ============================================================
print("")
print("=== Test 10: nommage ===")
valider_nommage = os.path.join(TOOLS_DIR, "valider", "valider-nommage", "valider-nommage.py")
_, _, rc = run([PYTHON, valider_nommage, "--type", "outil", MOTEUR_PY])
assert_eq("Test 10a: nommage .py OK", rc, 0)
_, _, rc = run([PYTHON, valider_nommage, "--type", "outil", MOTEUR_SH])
assert_eq("Test 10b: nommage .sh OK", rc, 0)

# ============================================================
# Test 11: ASCII
# ============================================================
print("")
print("=== Test 11: ASCII ===")
valider_ascii = os.path.join(TOOLS_DIR, "valider", "valider-conformite-ascii", "valider-conformite-ascii.py")
for f in (MOTEUR_PY, MOTEUR_SH, EXEMPLE,
          os.path.join(TOOLS_DIR, "combos", "combos-moteur", "combos-moteur.md"),
          os.path.join(TOOLS_DIR, "combos", "combos-moteur", "spec", "spec-combos-moteur.001.01.ebauche.md")):
    stdout, _, rc = run([PYTHON, valider_ascii, f])
    assert_eq("Test 11: ASCII 0 sur %s" % os.path.basename(f),
              "Conformite ASCII stricte validee" in stdout, True)

# ============================================================
# Test 12: syntaxe
# ============================================================
print("")
print("=== Test 12: syntaxe ===")
_, stderr, rc = run(["bash", "-n", MOTEUR_SH])
assert_eq("Test 12a: bash -n OK", rc, 0)
_, stderr, rc = run([PYTHON, "-m", "py_compile", MOTEUR_PY])
assert_eq("Test 12b: py_compile OK", rc, 0)

# ============================================================
# Test 13: GARDE-FOU v0.3.0 -- cles des entrees des cases generateur vs catalogue
# ============================================================
print("")
print("=== Test 13: garde-fou cles generateur vs catalogue (v0.3.0) ===")
import json
# 13a: combo avec une cle hors catalogue -> REJETE (code 1 + erreur claire)
def_combo_invalide = {
    "combo": {"nom": "test-cles-invalide", "version": "0.1.0", "case_depart": "c1"},
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
stdout, stderr, rc = run_py([fichier_invalide_cles, "--liste"])
assert_eq("Test 13a: cle hors catalogue -> code 1", rc, 1)
assert_eq("Test 13b: erreur claire (hors catalogue)",
          "hors catalogue" in (stderr + stdout), True)
assert_eq("Test 13c: erreur cite la cle fautive et la commande",
          "fichier" in (stderr + stdout) and "valider-conventions" in (stderr + stdout), True)
# 13d: combo avec une cle conforme -> ACCEPTE (code 0)
def_combo_conforme = {
    "combo": {"nom": "test-cles-conforme", "version": "0.1.0", "case_depart": "c1"},
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
stdout, stderr, rc = run_py([fichier_conforme, "--liste"])
assert_eq("Test 13d: cle exacte du catalogue -> code 0", rc, 0)
# 13e: parite sh (le garde-fou est embarque dans le .sh aussi)
stdout_sh, stderr_sh, rc_sh = run(["bash", MOTEUR_SH, fichier_invalide_cles, "--liste"])
assert_eq("Test 13e: .sh rejette aussi la cle hors catalogue", rc_sh, 1)

# ============================================================
# Rapport final
# ============================================================
print("")
print("=== Rapport final ===")
total = passed + failed
print("Total: %d" % total)
print("Reussis: %d" % passed)
print("Echecs: %d" % failed)
print("")
for r in results:
    print(r)
if failed == 0:
    print("")
    print("VERDICT: REUSSI (combos-moteur valide)")
else:
    print("")
    print("VERDICT: ECHEC (des comportements ne sont pas conformes)")
    sys.exit(1)

sys.exit(0)
