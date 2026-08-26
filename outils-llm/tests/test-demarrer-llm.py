#!/usr/bin/env python3
# -*- coding: ascii -*-
"""test-demarrer-llm.py - Tests de non-regression de l'outil demarrer-llm.

Teste :
  1. --help affiche l'aide (code 0)
  2. --version affiche la version (code 0)
  3. Syntaxe Python valide (py_compile)
  4. Format du .py : LF pur, ASCII strict (0 octet > 127)
  5. Erreur : sans argument -> code 1 + message clair
  6. Erreur : session invalide -> code 1
  7. La doc existe et est non vide
  8. Le demarrer.md ordonne l'utilisation de l'outil
"""

import os
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent.parent
OUTIL = RACINE / "outils-llm" / "demarrer-llm.py"
DOC = RACINE / "outils-llm" / "demarrer-llm.md"
DEMARRER = RACINE / "demarrer.md"

PASS = 0
FAIL = 0


def check(nom, condition, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1
        print("  [OK] %s" % nom)
    else:
        FAIL += 1
        print("  [KO] %s %s" % (nom, detail))


def run(args, cwd=None):
    return subprocess.run([sys.executable, str(OUTIL)] + args,
                          capture_output=True, text=True, cwd=cwd or str(RACINE))


print("=== test-demarrer-llm ===")

# 1. --help
r = run(["--help"])
check("--help code 0", r.returncode == 0, "(code %s)" % r.returncode)
check("--help affiche usage", "usage:" in (r.stdout or ""))

# 2. --version
r = run(["--version"])
check("--version code 0", r.returncode == 0)
check("--version affiche version", "demarrer-llm v" in (r.stdout or ""))

# 3. Syntaxe
import py_compile
try:
    py_compile.compile(str(OUTIL), doraise=True)
    check("syntaxe Python", True)
except py_compile.PyCompileError as e:
    check("syntaxe Python", False, str(e))

# 4. Format .py
d = OUTIL.read_bytes()
check("LF pur (0 CRLF)", d.count(b"\r\n") == 0, "(CRLF=%s)" % d.count(b"\r\n"))
check("ASCII strict", len([c for c in d if c > 127]) == 0,
      "(%s octets >127)" % len([c for c in d if c > 127]))

# 5. Erreur sans argument
r = run([])
check("sans argument -> code 1", r.returncode == 1, "(code %s)" % r.returncode)
check("sans argument -> message clair", "id et session obligatoires" in (r.stdout or ""))

# 6. Erreur session invalide
r = run(["glm5", "invalide"])
check("session invalide -> code 1", r.returncode == 1, "(code %s)" % r.returncode)

# 7. Doc
check("doc existe", DOC.exists())
check("doc non vide", DOC.exists() and DOC.stat().st_size > 100)

# 8. demarrer.md ordonne l'outil
check("demarrer.md cite l'outil", DEMARRER.exists() and "demarrer-llm.py" in DEMARRER.read_text(encoding="utf-8"))

print()
print("=== RESULTAT : %s OK / %s KO ===" % (PASS, FAIL))
sys.exit(0 if FAIL == 0 else 1)
