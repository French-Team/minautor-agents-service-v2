"""Constantes de la routine vigie-portes (pour le serveur matrice).

Le serveur utilise ces constantes pour lancer et superviser la routine
vigie-portes comme les autres (veille-flux, espion-integrite, suivi-sync).

NOTE : les noms de PID et de drapeau ne sont PAS recopies ici. Ils vivent dans
`constants.py` (UNE SEULE table nom -> PID / nom -> drapeau, partagee avec
`vie/etat.py`) : deux listes = deux verites, et c'est exactement la faute qui a
fait planter l'etat avec un KeyError a l'ajout d'une routine (MO-043).
"""
from pathlib import Path

REPERTOIRE_VIE = Path(__file__).resolve().parent
REPERTOIRE_ROUTINES = REPERTOIRE_VIE.parent
REPERTOIRE_VIGIE_PORTES = REPERTOIRE_ROUTINES / "vigie-portes"

# La routine vigie-portes est supervisee par le serveur.
BOUCLES_VIGIE_PORTES = (("vigie-portes", REPERTOIRE_VIGIE_PORTES),)
