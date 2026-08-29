#!/usr/bin/env python3
# -*- coding: ascii -*-
"""test-redemarrer-session.py - Tests de non-regression de l'outil
redemarrer-session.

Teste :
  1. --help affiche l'aide (code 0)
  2. --version affiche la version (code 0)
  3. Syntaxe Python valide (py_compile)
  4. Format du .py : LF pur, ASCII strict (0 octet > 127)
  5. Erreur : sans argument -> code 1 + message clair
  6. Erreur : session invalide -> code 1
  7. La doc existe et est non vide
  8. --dry-run admin : affiche DEFCON 5 + reprise main, AUCUN effet
     (pas de trace DEFCON ajoutee, agent actif du bloc inchange)
"""

import os
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent.parent
OUTIL = RACINE / "outils-llm" / "redemarrer-session.py"
DOC = RACINE / "outils-llm" / "redemarrer-session.md"
AGENTS_MD = RACINE / "AGENTS.md"
DEFCON_V1 = RACINE / "cerveau-projet" / "agents" / "tools" / "oracle" / "files" / "defcon.jsonl"

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


def agent_actif_admin():
    contenu = AGENTS_MD.read_text(encoding="utf-8")
    idx = contenu.find("### Session : session-admin")
    if idx == -1:
        return ""
    bloc = contenu[idx:idx + 1200]
    import re
    m = re.search(r"\|\s*\*\*Nom Agent\*\*\s*\|\s*([^|]+)\s*\|", bloc)
    return m.group(1).strip() if m else ""


def nb_defcon5():
    if not DEFCON_V1.exists():
        return 0
    nb = 0
    for l in DEFCON_V1.read_text(encoding="utf-8").splitlines():
        if l.strip() and '"niveau": 5' in l:
            nb += 1
    return nb


print("=== test-redemarrer-session ===")

# 1. --help
r = run(["--help"])
check("--help code 0", r.returncode == 0, "(code %s)" % r.returncode)
check("--help affiche usage", "usage:" in (r.stdout or ""))

# 2. --version
r = run(["--version"])
check("--version code 0", r.returncode == 0)
check("--version affiche version", "redemarrer-session v" in (r.stdout or ""))

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

# 8. --dry-run admin : aucun effet
agent_avant = agent_actif_admin()
defcon_avant = nb_defcon5()
r = run(["glm5", "admin", "--dry-run", "--raison", "test non-regression"])
check("dry-run admin code 0 ou 2 (jamais 1)", r.returncode in (0, 2),
      "(code %s)" % r.returncode)
check("dry-run affiche DEFCON 5", "DEFCON 5" in (r.stdout or ""))
check("dry-run affiche reprise de main", "Reprendre la main" in (r.stdout or ""))
check("dry-run affiche protocole de secours", "PROTOCOLE DE SECOURS" in (r.stdout or ""))
check("dry-run : agent actif inchange", agent_actif_admin() == agent_avant,
      "(avant=%s apres=%s)" % (agent_avant, agent_actif_admin()))
check("dry-run : aucun DEFCON 5 ajoute", nb_defcon5() == defcon_avant,
      "(avant=%s apres=%s)" % (defcon_avant, nb_defcon5()))

print()
print("=== RESULTAT : %d OK / %d KO ===" % (PASS, FAIL))
sys.exit(1 if FAIL else 0)
