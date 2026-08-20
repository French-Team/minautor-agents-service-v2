#!/bin/bash
# D6 (Buffy) : remplacer session-llm-1 par <session> dans les 16 cartes via
# editer-parcours --modifier-case (respecte le verrou cartes-lock).
# Usage : bash d6-remplacer-session.sh <agent> [--wet]
# Sans --wet : dry-run (affiche les modifications simulees).

AGENT="$1"
MODE="$2"
RACINE="$(cd "$(dirname "$0")/../../.." && pwd)"
RACINE="$(cd "$RACINE/.." && pwd)"  # le workspace est AU-DESSUS de cerveau-projet
OUTIL="$RACINE/cerveau-projet/agents/tools/editer/editer-parcours/editer-parcours.py"

python3 - "$AGENT" "$MODE" "$OUTIL" << 'PYEOF'
import json, os, subprocess, sys

agent = sys.argv[1]
mode = sys.argv[2]
outil = sys.argv[3]
racine = os.getcwd()
chemin = os.path.join(racine, "cerveau-projet", "agents", agent,
                      "parcours", "parcours-%s.json" % agent)
if not os.path.isfile(chemin):
    sys.exit("carte introuvable: %s" % chemin)

p = json.load(open(chemin, encoding="utf-8"))
cases = p.get("cases", {})
a_modifier = [cid for cid, c in cases.items()
              if "session-llm-1" in json.dumps(c, ensure_ascii=True)]
modifiees = 0
for idx, cid in enumerate(sorted(a_modifier)):
    c = cases[cid]
    s = json.dumps(c, ensure_ascii=True)
    if "session-llm-1" not in s:
        continue
    derniere = (idx == len(a_modifier) - 1)
    # remplacement dans tous les champs (recursif)
    def remplace(obj):
        if isinstance(obj, dict):
            return {k: remplace(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [remplace(x) for x in obj]
        if isinstance(obj, str):
            return obj.replace("session-llm-1", "<session>")
        return obj
    nouveau = remplace(c)
    cmd = [sys.executable, outil, "--agent", agent, "--modifier-case", cid,
           "--contenu", json.dumps(nouveau, ensure_ascii=False)]
    if mode == "--wet":
        cmd += ["--wet"]
        if derniere:
            cmd += ["--bump"]  # un seul bump par carte, sur la derniere case
    r = subprocess.run(cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    out = (r.stdout or "") + (r.stderr or "")
    if r.returncode != 0:
        print("[ERREUR] %s %s : %s" % (agent, cid, out[-200:]))
        sys.exit(1)
    # extraire la ligne de modification
    ligne = [l.strip() for l in out.splitlines() if "MODIFY" in l or "DRY-RUN" in l]
    print("[OK] %s %s : %s" % (agent, cid, ligne[0] if ligne else "modifiee"))
    modifiees += 1
print("=== %s : %d case(s) traitee(s) (mode %s)" % (agent, modifiees, mode or "dry-run"))
PYEOF
