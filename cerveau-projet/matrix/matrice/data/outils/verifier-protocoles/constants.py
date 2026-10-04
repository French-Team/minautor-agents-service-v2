"""Constantes de l'outil verifier-protocoles : chemins et valeurs.

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

# La ZONE DES SOURCES du createur (docs/) se LIT chez son domicile unique, elle ne se
# recopie JAMAIS (M-076) : c est le MEME domicile que la porte ECRIRE consomme pour la
# REFUSER en la nommant (MO-377). Le garde du marbre en a besoin parce qu un index de
# l operateur peut CITER cette zone pour dire d ou une discipline vient -- et que la
# Matrice ne peut PAS reparer une cible qu elle n ecrit jamais (MO-489).
from zone_sources import (  # noqa: E402,F401  (re-export pour commun.py)
    MOTIF_ZONE_SOURCES,
    NOM_ZONE_SOURCES,
    est_zone_sources,
)

RACINE = detecter_racine(REPERTOIRE_OUTIL)
REPERTOIRE_OPERATEUR = (
    RACINE / "cerveau-projet" / "matrix" / "_operateur" / "optimus-prime"
)
REPERTOIRE_PROTOCOLES = REPERTOIRE_OPERATEUR / "protocoles"

NOM_INDEX = "protocoles-readme.md"
TYPE_ATTENDU = "protocole"
APPARTIENT_A = "optimus-prime"

ENCODAGE = "utf-8"
