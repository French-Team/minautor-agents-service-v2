"""Constantes de la routine suivi-sync (pour le serveur matrice).

Le serveur utilise ces constantes pour superviser la routine suivi-sync comme
les autres (veille-flux, espion-integrite, vigie-profil, vigie-portes).

NOTE : les declarations RECOPIEES qui vivaient ici ont ete retirees --
`commander_suivi_sync`, `pid_de_suivi_sync`, `NOM_PID_SUIVI_SYNC` et
`NOM_DRAPEAU_SUIVI_SYNC`. Doctrine : deux tables = deux verites. L'ORDRE de
lancement vit desormais dans `constants.py` (COMMANDE_PAR_NOM) et les noms de
PID / drapeau dans sa table unique. `commander_suivi_sync` etait de surcroit
FAUX : il annoncait `["main.py"]` alors que le motif de lancement partage
(`data/commun/lancement.py`) ajoute DEJA `main.py` -- tel quel, il aurait lance
`python main.py main.py`. C'est ce meme motif de recopie qui a fait tourner les
routines a 60 s au lieu de leur temps declare.
"""
from pathlib import Path

REPERTOIRE_VIE = Path(__file__).resolve().parent
REPERTOIRE_ROUTINES = REPERTOIRE_VIE.parent
REPERTOIRE_SUIVI_SYNC = REPERTOIRE_ROUTINES / "suivi-sync"

# La routine suivi-sync est supervisee par le serveur.
BOUCLES_SUIVI_SYNC = (("suivi-sync", REPERTOIRE_SUIVI_SYNC),)
