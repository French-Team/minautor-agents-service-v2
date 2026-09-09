"""Constantes de l'activateur de vie de la Matrice.

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
"""
import sys
from pathlib import Path

REPERTOIRE_ACTIVATEUR = Path(__file__).resolve().parent
REPERTOIRE_ROUTINES = REPERTOIRE_ACTIVATEUR.parent
if REPERTOIRE_ROUTINES.name != "routines" or REPERTOIRE_ROUTINES.parent.name != "matrice":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_ACTIVATEUR) + " n'est pas dans matrice/routines/"
    )

# data/commun (motif unique M-076) : installe le dossier partage dans sys.path
# (lancement.py : lancement detache invisible du server et de l'activateur).
# vie/ est sous matrice/routines/ : data/commun se rejoint via matrice/data/commun.
CHEMIN_COMMUN = REPERTOIRE_ROUTINES.parent / "data" / "commun"
if not (CHEMIN_COMMUN / "racine.py").is_file():
    raise RuntimeError(
        "data/commun introuvable : " + str(CHEMIN_COMMUN) + " n'est pas le dossier partage attendu"
    )
sys.path.insert(0, str(CHEMIN_COMMUN))

# Les deux boucles de fond de la Matrice (nom lisible -> dossier de la routine).
BOUCLES = (
    ("veille-flux", REPERTOIRE_ROUTINES / "veille-flux"),
    ("espion-integrite", REPERTOIRE_ROUTINES / "espion-integrite"),
)

# Commande de boucle de chaque routine (memes noms que ses propres verbes).
COMMANDE_VEILLE = "veille"
COMMANDE_ESPION = "boucle"

NOM_PID_VEILLE = "veille-flux.pid"
NOM_PID_ESPION = "espion.pid"
NOMS_PID = (NOM_PID_VEILLE, NOM_PID_ESPION)

ENCODAGE = "utf-8"
