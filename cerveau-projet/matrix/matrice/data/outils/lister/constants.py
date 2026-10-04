"""Constantes de l'outil lister.

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
"""
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

ALLOWLIST_RACINE = ("AGENTS.md",)
ALLOWLIST_PREFIXES = ("demarrer-",)

ENCODAGE = "utf-8"
TAILLE_BLOC_LECTURE = 65536

# Zones invisibles L-016 (si appel Flux 1, filtre ; Optimus jamais filtre mais porte le filtre)
ZONES_INVISIBLES = ("_operateur", "tmp-optimus", "suivi-optimus")

NOMS_OPTIONS_LISTER = ("dossier", "filtre", "recursif", "json")
