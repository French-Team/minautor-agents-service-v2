"""Constantes de la routine verifier-liens-cartes (pour le serveur matrice).

Meme motif que suivi-sync et vigie-portes : la routine se DECLARE ici, et
`constants.py` assemble la liste unique des routines supervisees. Les PID, les
drapeaux, l ordre de lancement et la cadence vivent dans les tables uniques de
`constants.py` -- rien n est recopie ici (deux tables = deux verites).
"""
from pathlib import Path

REPERTOIRE_VIE = Path(__file__).resolve().parent
REPERTOIRE_ROUTINES = REPERTOIRE_VIE.parent
REPERTOIRE_VERIFIER_LIENS_CARTES = REPERTOIRE_ROUTINES / "verifier-liens-cartes"

# La routine verifier-liens-cartes est supervisee par le serveur.
BOUCLES_VERIFIER_LIENS_CARTES = (
    ("verifier-liens-cartes", REPERTOIRE_VERIFIER_LIENS_CARTES),
)
