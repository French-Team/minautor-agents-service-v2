"""Constantes du pilote : chemins et valeurs.

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
"""
from pathlib import Path

REPERTOIRE_PILOTE = Path(__file__).resolve().parent
REPERTOIRE_MATRICE = REPERTOIRE_PILOTE.parent
if REPERTOIRE_MATRICE.name != "matrice":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_MATRICE) + " n'est pas le dossier matrice/"
    )

REPERTOIRE_DATA = REPERTOIRE_MATRICE / "data"
REPERTOIRE_INTERCOM = REPERTOIRE_MATRICE / "intercom"

NOM_FILE = "file-missions.json"
CHEMIN_FILE = REPERTOIRE_PILOTE / NOM_FILE

# Entonnoir (echelon 4) : la tresse de la file principale (doit rester
# synchronise avec entonnoir/listes.py NOM_ENTONNOIR).
NOM_ENTONNOIR = "entonnoir-files.json"
CHEMIN_ENTONNOIR = REPERTOIRE_PILOTE / NOM_ENTONNOIR
NOM_HISTORIQUE = "historiques-missions.jsonl"
CHEMIN_HISTORIQUE = REPERTOIRE_DATA / NOM_HISTORIQUE

# Registre des THEMES de mission (genere depuis le moule theme-bdd).
# Consomme par charger_themes_utiles (doctrine lecons_utiles) : jamais bloquant.
NOM_THEMES = "vivier-themes.json"
CHEMIN_THEMES = REPERTOIRE_DATA / NOM_THEMES

# Mise en securite defcon (variable tenue par l'outil machine-defcon).
CLE_DEFCON = "defcon"
NIVEAU_DEFCON_MAX = 5
THEME_DEFCON = "DEFCON"
CHEMIN_CLASSEUR_VARIABLES = REPERTOIRE_DATA / "classeur-variables.json"

# Protocole de pause session-matrix (M-080) : l'etat serialise pose par
# l'outil pause-session au niveau data/. S'il existe, la session est EN PAUSE.
NOM_ETAT_PAUSE = "session-matrix-etat.json"
CHEMIN_ETAT_PAUSE = REPERTOIRE_DATA / NOM_ETAT_PAUSE

BOITE_PILOTE_OUT = REPERTOIRE_INTERCOM / "pilote" / "outbox.jsonl"
BOITE_MATRICE_IN = REPERTOIRE_INTERCOM / "matrice" / "inbox.jsonl"

STATUT_EN_ATTENTE = "en-attente"
STATUT_EN_COURS = "en-cours"
STATUT_TERMINEE = "terminee"

ENCODAGE = "utf-8"
INDENTATION_JSON = 2
