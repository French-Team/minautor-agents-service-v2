"""Constantes de l'outil executer.

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
"""
import subprocess
import sys
from pathlib import Path

REPERTOIRE_OUTIL = Path(__file__).resolve().parent
REPERTOIRE_DATA = REPERTOIRE_OUTIL.parent.parent
if REPERTOIRE_DATA.name != "data":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_DATA) + " n'est pas le dossier data/"
    )

sys.path.insert(0, str(REPERTOIRE_DATA / "commun"))
from racine import detecter_racine  # noqa: E402

RACINE = detecter_racine(REPERTOIRE_OUTIL)

REPERTOIRE_MATRIX = RACINE / "matrix"
REPERTOIRE_MATRICE = RACINE / "cerveau-projet" / "matrix" / "matrice"
if not REPERTOIRE_MATRIX.is_dir():
    REPERTOIRE_MATRIX = RACINE / "matrix"
ALT_MATRIX = RACINE / "cerveau-projet" / "matrix"
if ALT_MATRIX.is_dir():
    REPERTOIRE_MATRIX_ALT = ALT_MATRIX
else:
    REPERTOIRE_MATRIX_ALT = REPERTOIRE_MATRIX

ENCODAGE = "utf-8"

# Timeout par defaut (secondes)
TIMEOUT_DEFAUT = 60

# Commandes interdites (pas de shell)
COMMANDES_INTERDITES = (
    "bash", "sh", "cmd", "powershell", "pwsh",
    "curl", "wget",
)

# Extensions Python reconnues
EXTENSIONS_PYTHON = (".py",)

# Flags subprocess
CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)

NOMS_OPTIONS_EXECUTER = ("cmd", "timeout", "contenu-chemin", "json", "verbose")
