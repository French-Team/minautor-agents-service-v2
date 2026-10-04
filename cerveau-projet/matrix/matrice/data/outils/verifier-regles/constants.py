"""Constantes de l'outil verifier-regles : chemins et valeurs.

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
Racine (pattern v1) : DETECTEE en remontant jusqu'au dossier contenant AGENTS.md.
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


# data/commun (motif unique M-076) : le motif racine est PARTAGE, jamais recopie.
sys.path.insert(0, str(REPERTOIRE_OUTIL.parent.parent / "commun"))
from racine import detecter_racine  # noqa: E402

RACINE = detecter_racine(REPERTOIRE_OUTIL)

# La ZONE DES SOURCES du createur se LIT chez son domicile unique, elle ne se
# recopie JAMAIS (M-076) : c'est le MEME domicile que la porte ECRIRE consomme
# pour la REFUSER en la nommant (MO-377) et que le jugement des citations
# consomme pour l'EXEMPTER en la disant (EO-479). Ce re-export n'apporte rien :
# il rend au consommateur ce qu'il consomme, comme verifier-protocoles le fait.
from zone_sources import MOTIF_ZONE_SOURCES, NOM_ZONE_SOURCES  # noqa: E402,F401
REPERTOIRE_OPERATEUR = (
    RACINE / "cerveau-projet" / "matrix" / "_operateur" / "optimus-prime"
)
REPERTOIRE_REGLES = REPERTOIRE_OPERATEUR / "regles-immuables"

NOM_INDEX = "regles-immuables-readme.md"
TYPE_ATTENDU = "regle-immuable"
APPARTIENT_A = "optimus-prime"

ENCODAGE = "utf-8"
