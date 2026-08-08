#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test-001-evaluer-agents-coherence.sh
Test des corrections apportees a evaluer-agents et evaluer-coherence.

Corrections testees:
  1. evaluer-agents exclut __pycache__ des outils manquants
  2. evaluer-coherence utilise le projet root pour cible_racine
  3. evaluer-coherence exclut les commandes systeme (cat, grep, sed, basher)

Usage:
  python3 cervel-projet/agents/tools/tester/tests/test-001-evaluer-agents-coherence/test-001-evaluer-agents-coherence.py
"""
import os
import re
import subprocess
import sys
import tempfile
import json

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

passed = 0
failed = 0
results = []


def assert_eq(name, actual, expected):
    global passed, failed
    if actual == expected:
        passed += 1
        results.append(f"  [OK] {name}")
    else:
        failed += 1
        results.append(f"  [ECHEC] {name}: attendu={expected}, obtenu={actual}")


def run_tool(tool_path, args=None):
    """Execute un outil .py et retourne (stdout, code_retour)."""
    cmd = [PYTHON, tool_path]
    if args:
        cmd.extend(args)
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return proc.stdout, proc.stderr, proc.returncode


# ============================================================
# PARTIE 1: Tests de evaluer-agents
# ============================================================

print("=== Tests evaluer-agents ===")
print("")

evaluer_agents_py = os.path.join(TOOLS_DIR, "evaluer", "evaluer-agents", "evaluer-agents.py")

# Test 1: evaluer-agents doit exclure __pycache__ des faux positifs
stdout, stderr, rc = run_tool(evaluer_agents_py)
nb_pycache_erreurs = stdout.count("Outil __pycache__")
assert_eq(
    "Test 1: evaluer-agents exclut __pycache__ des erreurs",
    nb_pycache_erreurs,
    0,
)
print(f"  [INFO] Faux positifs __pycache__ detectes: {nb_pycache_erreurs}")

# Test 2: score evaluer-agents doit etre > 50/100 (era 23/100 avant correction)
m = re.search(r"Score agents : (\d+)/100", stdout)
if m:
    score = int(m.group(1))
    assert_eq(
        "Test 2: score evaluer-agents > 50/100 (corrige de 23)",
        score > 50,
        True,
    )
    print(f"  [INFO] Score evaluer-agents: {score}/100")
else:
    failed += 1
    results.append("  [ECHEC] Test 2: score evaluer-agents non trouve dans la sortie")

# Test 3: evaluer-agents doit toujours signaler generateurs-commande (outil incomplet reel)
assert_eq(
    "Test 3: evaluer-agents signale generateur-commande (outil incomplet)",
    "generateurs-commande" in stdout,
    True,
)

# Test 4: pas de faux avertissement "Agent actif 'themis'" dans le score (c'est normal)
#    On verifie que l'outil fonctionne sans crash
assert_eq(
    "Test 4: evaluer-agents execute sans crash",
    rc,
    0,
)

print("")
print("  Resultats:")
for r in results[:4]:
    print(r)

# ============================================================
# PARTIE 2: Tests de evaluer-coherence
# ============================================================

print("")
print("=== Tests evaluer-coherence ===")
print("")

evaluer_coherence_py = os.path.join(TOOLS_DIR, "evaluer", "evaluer-coherence", "evaluer-coherence.py")

# Test 5: evaluer-coherence doit exclure cat, grep, sed, basher des outils casses
stdout2, stderr2, rc2 = run_tool(evaluer_coherence_py)

# Compter les faux positifs commandes-systeme
cmd_systeme_signales = []
for cmd in ("cat", "grep", "sed", "basher"):
    pattern = f"`{cmd}` reference par"
    if pattern in stdout2:
        cmd_systeme_signales.append(cmd)

assert_eq(
    "Test 5: evaluer-coherence exclut cat/grep/sed/basher des outils casses",
    len(cmd_systeme_signales),
    0,
)
if cmd_systeme_signales:
    print(f"  [INFO] Commandes systeme encore signalees: {cmd_systeme_signales}")

# Test 6: evaluer-coherence doit signaler 'Tous les outils references existent'
assert_eq(
    "Test 6: evaluer-coherence dit 'Tous les outils references existent'",
    "Tous les outils references existent" in stdout2,
    True,
)

# Test 7: le faux positif lien 'agents/conventions/structures/' doit etre resolu
#    (ces fichiers existent sous cerveau-projet/pense-betes/...)
liens_faux_positifs = [
    "agents/conventions/structures/convention-classeur-variables.md",
    "agents/conventions/structures/convention-structures.md",
]
liens_still_casses = [l for l in liens_faux_positifs if l in stdout2]
assert_eq(
    "Test 7: faux positifs liens structures resolus (existe sous cerveau-projet/)",
    len(liens_still_casses),
    0,
)
if liens_still_casses:
    print(f"  [INFO] Liens faux positifs encore detects: {liens_still_casses}")

# Test 8: evaluer-coherence doit toujours fonctionner sans crash
assert_eq(
    "Test 8: evaluer-coherence execute sans crash",
    rc2,
    0,
)

print("")
print("  Resultats:")
for r in results[4:]:
    print(r)

# ============================================================
# PARTIE 3: Score global
# ============================================================

print("")
print("=== Rapport final ===")
total = passed + failed
print(f"Total: {total}")
print(f"Reussis: {passed}")
print(f"Echecs: {failed}")
if failed == 0:
    print("VERDICT: REUSSI (toutes les corrections sont efficaces)")
else:
    print("VERDICT: ECHEC (des corrections ne sont pas efficaces)")

sys.exit(0 if failed == 0 else 1)
