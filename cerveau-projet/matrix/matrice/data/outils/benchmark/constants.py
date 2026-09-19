"""Constantes de l'outil benchmark : mise a l'epreuve des actions.

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

ENCODAGE = "utf-8"

# Allowlist racine
ALLOWLIST_RACINE = ("AGENTS.md",)
ALLOWLIST_PREFIXES = ("demarrer-",)

# Zones invisibles L-016
ZONES_INVISIBLES = ("_operateur", "tmp-optimus", "suivi-optimus")

# 9 epreuves (les memes pour tout)
EPREUVES = (
    "perimetre",    # 1. Perimetre matrix/
    "lf",           # 2. LF L-001
    "sha",          # 3. SHA avant/apres
    "validation",   # 4. py_compile/json
    "ascii",        # 5. ASCII
    "bdd",          # 6. BDD modifications
    "relecture",    # 7. Relecture L-009
    "bak",          # 8. .bak horodate
    "invisibilite", # 9. L-016 fuite
)

# Actions testees (MO-008)
ACTIONS = ("creer", "ajouter", "modifier", "supprimer")

NOMS_OPTIONS_BENCHMARK = ("fichier", "dossier", "recursif", "filtre", "integration", "json")
