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

# La ZONE DES SOURCES du createur se LIT chez son domicile unique, elle ne se
# recopie JAMAIS (M-076) : c'est le MEME domicile que la porte ECRIRE consomme
# pour la REFUSER en la nommant (MO-377) et que le jugement des citations
# consomme pour l'EXEMPTER en la disant (EO-479). Ce re-export n'apporte rien :
# il rend au consommateur ce qu'il consomme, comme verifier-protocoles le fait.
from zone_sources import MOTIF_ZONE_SOURCES, NOM_ZONE_SOURCES  # noqa: E402,F401
