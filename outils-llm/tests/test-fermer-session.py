#!/usr/bin/env python3
# -*- coding: ascii -*-
"""test-fermer-session.py - Tests de non-regression de l'outil fermer-session.

Teste :
  1. --help affiche l'aide (code 0)
  2. --version affiche la version (code 0)
  3. Syntaxe Python valide (py_compile)
  4. Format du .py : LF pur, ASCII strict (0 octet > 127)
  5. Erreur : sans argument -> code 1 + message clair
  6. Erreur : session invalide -> code 1
  7. La doc existe et est non vide
  8. --dry-run admin : NE TOUCHE A AUCUN SERVEUR (aucun pidfile supprime)
  9. --dry-run freelance : idem (aucun pidfile supprime)
"""

import os
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent.parent
OUTIL = RACINE / "outils-llm" / "fermer-session.py"
DOC = RACINE / "outils-llm" / "fermer-session.md"

# pidfiles des serveurs (verifier qu'ils ne sont PAS touches par --dry-run)
PID_ORACLE = RACINE / "cerveau-projet" / "agents" / "tools" / "oracle" / "oracle-server.pid"
PID_ROUTINES_V1 = RACINE / "cerveau-projet" / "agents" / "tools" / "oracle" / "routines-server.pid"
PID_ROUTINES_V2 = RACINE / "cerveau-projet" / "freelance" / "tools-commun" / "jarvis" / "routines-server.pid"

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


print("=== test-fermer-session ===")

# 1. --help
r = run(["--help"])
check("--help code 0", r.returncode == 0, "(code %s)" % r.returncode)
check("--help affiche usage", "usage:" in (r.stdout or ""))

# 2. --version
r = run(["--version"])
check("--version code 0", r.returncode == 0)
check("--version affiche version", "fermer-session v" in (r.stdout or ""))

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
check("doc existe", DOC.is_file())
check("doc non vide", DOC.stat().st_size > 100 if DOC.is_file() else False)

# 8/9. --dry-run : aucun serveur touche (pidfiles intacts)
etat_avant = {str(p): p.exists() for p in (PID_ORACLE, PID_ROUTINES_V1, PID_ROUTINES_V2)}
r = run(["glm5", "admin", "--dry-run"])
check("dry-run admin code 0 ou 2 (jamais 1)", r.returncode in (0, 2),
      "(code %s)" % r.returncode)
check("dry-run admin affiche VERIFICATION", "VERIFICATION" in (r.stdout or ""))
etat_apres = {str(p): p.exists() for p in (PID_ORACLE, PID_ROUTINES_V1, PID_ROUTINES_V2)}
check("dry-run admin : pidfiles intacts",
      etat_apres == etat_avant, "(avant=%s apres=%s)" % (etat_avant, etat_apres))

r = run(["freebuff", "freelance", "--dry-run"])
check("dry-run freelance code 0 ou 2 (jamais 1)", r.returncode in (0, 2),
      "(code %s)" % r.returncode)
check("dry-run freelance affiche VERIFICATION", "VERIFICATION" in (r.stdout or ""))
etat_apres = {str(p): p.exists() for p in (PID_ORACLE, PID_ROUTINES_V1, PID_ROUTINES_V2)}
check("dry-run freelance : pidfiles intacts",
      etat_apres == etat_avant, "(avant=%s apres=%s)" % (etat_avant, etat_apres))

print()
print("=== RESULTAT : %d OK / %d KO ===" % (PASS, FAIL))
sys.exit(1 if FAIL else 0)
