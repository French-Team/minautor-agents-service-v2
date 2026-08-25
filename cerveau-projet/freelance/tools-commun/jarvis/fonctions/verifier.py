# -*- coding: ascii -*-
"""fonctions/verifier.py - UNE tache : verifier la coherence d AGENTS.md
(sous-commande jarvis.py verifier-coherence). Cote v2, la source de verite
est l outil v1 verifier-coherence-agents : celui-ci confronte les blocs
session d AGENTS.md (fichier racine commun) aux fichiers reels (arbres v2,
fiches, corrections, jarvis-data.json, table Sessions) et remonte les
decalages que le mecanisme de validation automatique (2026-08-25, chantier
ferrari) doit empecher de revenir.
"""

import os
import subprocess
import sys
from pathlib import Path

# P10 : la racine se DETECTE via os_path, elle ne se compte pas
_sys_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "..", "os_path", "fonctions")
sys.path.insert(0, _sys_dir)
from racine import trouver_racine  # noqa: E402

PROJECT_ROOT = Path(trouver_racine(__file__))
VERIFIER_V1 = PROJECT_ROOT / "cerveau-projet" / "agents" / "tools" / \
    "verifier" / "verifier-coherence-agents" / "verifier-coherence-agents.py"


def cmd_verifier(args):
    """jarvis.py verifier-coherence -- confronte AGENTS.md aux fichiers reels."""
    if not VERIFIER_V1.is_file():
        print("[JARVIS] ERREUR: outil v1 verifier-coherence-agents introuvable : "
              "%s" % VERIFIER_V1)
        sys.exit(2)
    cmd = [sys.executable, str(VERIFIER_V1), "--dry-run"]
    try:
        res = subprocess.run(cmd, cwd=str(PROJECT_ROOT),
                             capture_output=True, text=True,
                             encoding="utf-8", errors="replace", timeout=60)
    except Exception as exc:  # pragma: no cover
        print("[JARVIS] ERREUR lors de la verification : %s" % exc)
        sys.exit(2)
    print("[JARVIS] verifier-coherence :")
    if res.stdout:
        print(res.stdout.rstrip())
    if res.stderr:
        print(res.stderr.rstrip(), file=sys.stderr)
    # rc du verificateur : 0 = coherent, >=1 = incoherences trouvees
    sys.exit(res.returncode)