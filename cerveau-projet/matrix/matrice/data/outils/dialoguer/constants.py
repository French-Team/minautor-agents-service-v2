"""Constantes de l'outil dialoguer : interaction createur, Flux 2 seul.

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

ENCODAGE = "utf-8"

# Timeout question (secondes, 0 = persistant = pas de timeout)
TIMEOUT_QUESTION = 0

# Mode : Flux 2 seul (jamais cameleon)
FLUX = "optimus"

# EO-287 : le NOM de l outil de trace, jamais son chemin -- la resolution (et
# son refus nomme) vit dans data/commun/resolution_outils.py.
NOM_OUTIL_SUIVI = "suivi-optimus"

NOMS_OPTIONS_DIALOGUER = ("question", "choix", "timeout", "json")
NOMS_OPTIONS_PLAN = ("todos", "json")
