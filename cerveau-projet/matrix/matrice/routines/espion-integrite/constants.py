"""Constantes de l'espion-integrite : registre des BDD et valeurs de la boucle.

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
"""
from pathlib import Path

REPERTOIRE_ESPION = Path(__file__).resolve().parent
# L'espion vit dans routines/espion-integrite/ ; les BDD vivent dans data/.
REPERTOIRE_DATA = REPERTOIRE_ESPION.parent.parent / "data"
if REPERTOIRE_DATA.name != "data":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_DATA) + " n'est pas le dossier data/"
    )

# Registre des BDD de la Matrice : nom -> faite (True) ou a construire (False).
BDDS = {
    "modifications-par-fichier.json": True,
    "historiques-missions.jsonl": True,
    "lecons.json": True,
    "classeur-variables.json": True,
    "usages-outils-combos.jsonl": True,
    "activites-recentes.json": True,
    "historique-bdd.jsonl": True,
    "vivier-themes.json": True,
    "defcon-historique.jsonl": True,
    "pauses-session-matrix.jsonl": True,
}
# NOTA (M-080) : session-matrix-etat.json n'est PAS surveillee -- c'est un
# fichier EPHEMERE qui n'existe QUE pendant une pause (pose par pause-session,
# supprime a la reprise). Sa presence variable serait un faux ECART permanent.

NOM_JOURNAL = "espion-log.jsonl"
CHEMIN_JOURNAL = REPERTOIRE_ESPION / NOM_JOURNAL
NOM_PID = "espion.pid"
CHEMIN_PID = REPERTOIRE_ESPION / NOM_PID
NOM_DRAPEAU_ARRET = "boucle-arret.txt"
CHEMIN_DRAPEAU_ARRET = REPERTOIRE_ESPION / NOM_DRAPEAU_ARRET

INTERVALLE_DEFAUT_SECONDES = 300
SECONDES_PAR_TICK = 1.0
ENCODAGE = "utf-8"
