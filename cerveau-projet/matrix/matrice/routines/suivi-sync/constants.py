"""Constantes de la routine de synchronisation du suivi-optimus.

Sync les missions terminees (inbox.jsonl) vers le suivi-optimus.
"""
import sys
from pathlib import Path

REPERTOIRE_ROUTINE = Path(__file__).resolve().parent
sys.path.insert(0, str(REPERTOIRE_ROUTINE.parent / "data" / "commun"))

INTERVALLE_SECONDS = 60
ENCODAGE = "utf-8"

# Sources et destination.
CHEMIN_INBOX = REPERTOIRE_ROUTINE.parent.parent / "intercom" / "matrice" / "inbox.jsonl"
REPERTOIRE_OUTIL_SUIVI = REPERTOIRE_ROUTINE.parent.parent / "data" / "outils" / "suivi-optimus"
NOM_PID = "suivi-sync.pid"
CHEMIN_PID = REPERTOIRE_ROUTINE / NOM_PID

# Actions a synchroniser (ce qui interesse optimus-prime).
TYPES_INTERESSANTS = ("fin-mission", "retour-lot")

# La synchronisation evite les doublons en comparant les dates.
# Si la date de l'evenement inbox est <= la date du dernier evenement
# dans le suivi-optimus, on considere que c'est deja synchronise.
# On utilise une comparaison lexicographique (format ISO 8601).
# Note : les dates dans l'inbox sont au format "AAAA-MM-JJ HH:MM:SS".
# On les compare en tant que chaines (ordre chronologique preserve).
