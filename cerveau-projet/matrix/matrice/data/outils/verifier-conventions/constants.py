"""Constantes de l'outil verifier-conventions : chemins et valeurs.

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
"""
import sys
from pathlib import Path

REPERTOIRE_OUTIL = Path(__file__).resolve().parent
REPERTOIRE_PARENT = REPERTOIRE_OUTIL.parent
if (
    REPERTOIRE_PARENT.name != "outils"
    or REPERTOIRE_PARENT.parent.name != "data"
    or REPERTOIRE_PARENT.parent.parent.name != "matrice"
):
    raise RuntimeError(
        "Structure inattendue : "
        + str(REPERTOIRE_OUTIL)
        + " n'est pas dans matrice/data/outils/"
    )

REPERTOIRE_MATRICE = REPERTOIRE_PARENT.parent.parent
REPERTOIRE_OPERATEUR = REPERTOIRE_MATRICE.parent / "_operateur" / "optimus-prime"
REPERTOIRE_CONVENTIONS = REPERTOIRE_OPERATEUR / "conventions"

NOM_INDEX = "conventions-readme.md"
TYPE_ATTENDU = "convention"
APPARTIENT_A = "optimus-prime"

ENCODAGE = "utf-8"

# data/commun (motif unique M-076) : installe le dossier partage dans sys.path.
_courant = REPERTOIRE_OUTIL
for _ in range(30):
    if (_courant / "commun" / "racine.py").is_file():
        sys.path.insert(0, str(_courant / "commun"))
        break
    _courant = _courant.parent
else:
    raise RuntimeError("data/commun introuvable en remontant.")

from racine import detecter_racine  # noqa: E402

RACINE = detecter_racine(REPERTOIRE_OUTIL)
