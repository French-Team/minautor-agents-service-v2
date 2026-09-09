"""Sac a dos embarque : chaque outil note LUI-MEME ses usages en BDD (M-076).

Porte unique respectee : la note part par l'outil bdd-usages (subprocess),
jamais d'ecriture directe du journal (proto-7). Un echec de notation
n'arrete JAMAIS l'outil (best-effort, comme la veille-flux).
bdd-usages ne se note pas lui-meme : le garde OUTIL_EXCLU interdit la recursion.
"""
import subprocess
import sys
import time
from pathlib import Path

REPERTOIRE_COMMUN = Path(__file__).resolve().parent
REPERTOIRE_DATA = REPERTOIRE_COMMUN.parent
OUTIL_EXCLU = "bdd-usages"
TAGS_SAC_A_DOS = "sac-a-dos"
CHEMIN_BDD_USAGES = REPERTOIRE_DATA / "outils" / OUTIL_EXCLU
TIMEOUT_NOTATION = 30


def noter_usage(arguments, code, duree_ms):
    """Note UN usage via bdd-usages (porte unique). Echec jamais bloquant."""
    nom_outil = Path(sys.argv[0]).resolve().parent.name
    if nom_outil == OUTIL_EXCLU:
        return
    commande = arguments[0] if arguments else "-"
    contenu = [
        sys.executable, "main.py", "noter",
        "--outil", nom_outil, "--commande", commande,
        "--code", str(code), "--duree", str(duree_ms),
        "--tags", TAGS_SAC_A_DOS,
    ]
    try:
        termine = subprocess.run(
            contenu,
            cwd=str(CHEMIN_BDD_USAGES),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=TIMEOUT_NOTATION,
        )
    except (OSError, subprocess.TimeoutExpired) as erreur:
        print("sac-a-dos : notation impossible (" + type(erreur).__name__ + ")", file=sys.stderr)
        return
    if termine.returncode != 0:
        print("sac-a-dos : notation refusee (code " + str(termine.returncode) + ")", file=sys.stderr)


def envelopper(principal, arguments):
    """Execute principal(arguments), chronometre, note l'usage, retourne le code."""
    debut = time.monotonic()
    code = principal(arguments)
    duree_ms = int((time.monotonic() - debut) * 1000)
    noter_usage(arguments, code, duree_ms)
    return code
