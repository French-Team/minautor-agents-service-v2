#!/usr/bin/env python3
"""resoudre-chemin.py -- Resoudre les chemins relatifs pour Oracle.

Quand un agent cree un fichier avec un chemin relatif (ex: tmp-buffy/script.py),
ce chemin est resolu par rapport a la RACINE DU PROJET, pas par rapport au
dossier de l'agent.

Usage:
    python3 resoudre-chemin.py <chemin> [--racine <racine>]
    python3 resoudre-chemin.py tmp-buffy/mon-script.py
    # -> /z/analyste-in-console/tmp-buffy/mon-script.py

Regles:
    - tmp-<agent>/ -> racine du projet / tmp-<agent>/
    - cerveau-projet/... -> tel quel (deja absolu depuis la racine)
    - chemin absolu -> tel quel
    - tout autre relatif -> racine du projet / chemin
"""

import os
import sys
from pathlib import Path


def resoudre_chemin(chemin, racine=None):
    """Resoudre un chemin relatif vers la racine du projet.

    Retourne le chemin absolu resolu.
    """
    if racine is None:
        racine = Path(__file__).resolve().parents[5]  # racine du projet (hors cerveau-projet/)
    else:
        racine = Path(racine)

    p = Path(chemin)

    # Chemin absolu -> tel quel
    if p.is_absolute():
        return str(p)

    # Deja depuis la racine (commence par cerveau-projet/ ou agents/)
    parts = p.parts
    if parts and parts[0] in ("cerveau-projet", "agents", "combos",
                               "pense-betes", "specs", "todos",
                               "AGENTS.md", "README.md"):
        return str(racine / p)

    # Dossier temporaire tmp-<agent>/ -> racine
    if parts and parts[0].startswith("tmp-"):
        return str(racine / p)

    # Tout autre relatif -> racine
    return str(racine / p)


def resoudre_commande(cmd, racine=None):
    """Resoudre les chemins dans une commande complete.

    Detecte les arguments qui ressemblent a des chemins et les resout.
    Retourne la commande corrigee.
    """
    if racine is None:
        racine = Path(__file__).resolve().parents[5]
    else:
        racine = Path(racine)

    mots = cmd.split()
    resultats = []
    for mot in mots:
        # Detecter les chemins (contient / ou \ ou termine par .py .sh .json .md)
        if ("/" in mot or "\\" in mot or
            mot.endswith((".py", ".sh", ".json", ".md", ".txt", ".yaml", ".yml"))):
            p = Path(mot)
            if not p.is_absolute():
                mot = str(resoudre_chemin(mot, racine))
        resultats.append(mot)
    return " ".join(resultats)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: resoudre-chemin.py <chemin> [--racine <racine>]")
        print("       resoudre-chemin.py --cmd <commande>")
        sys.exit(1)

    racine = None
    if "--racine" in sys.argv:
        idx = sys.argv.index("--racine")
        racine = sys.argv[idx + 1]
        sys.argv = sys.argv[:idx] + sys.argv[idx+2:]

    if sys.argv[1] == "--cmd" and len(sys.argv) > 2:
        cmd = " ".join(sys.argv[2:])
        print(resoudre_commande(cmd, racine))
    else:
        chemin = sys.argv[1]
        print(resoudre_chemin(chemin, racine))
