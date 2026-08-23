# -*- coding: utf-8 -*-
"""fonctions/lancer.py - subprocess standardise : rc + captures + timeout."""
import subprocess
import sys


def lancer(commande, timeout=60, cwd=None):
    """Executer une commande. Retourne {rc, stdout, stderr, timeout}."""
    try:
        p = subprocess.run(commande, capture_output=True, text=True,
                           timeout=timeout, cwd=cwd)
        return {"rc": p.returncode, "stdout": p.stdout,
                "stderr": p.stderr, "timeout": False}
    except subprocess.TimeoutExpired:
        return {"rc": -1, "stdout": "", "stderr": "TIMEOUT",
                "timeout": True}
    except OSError as e:
        return {"rc": -2, "stdout": "", "stderr": str(e), "timeout": False}
