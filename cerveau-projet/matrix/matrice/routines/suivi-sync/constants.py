"""Constantes de la routine de synchronisation du suivi-optimus.

Sync les missions terminees (inbox.jsonl) vers le suivi-optimus.
"""
import sys
from pathlib import Path

REPERTOIRE_ROUTINE = Path(__file__).resolve().parent

# data/commun (motif unique M-076) : l'insertion montait d'UN CRAN DE TROP
# (`matrice/routines/data/commun`, dossier inexistant) : elle etait MORTE depuis
# toujours. Rien ne le voyait parce que suivi-sync n'avait jamais eu besoin du
# module partage ; la premiere tentative d'import l'a revele.
REPERTOIRE_COMMUN = REPERTOIRE_ROUTINE.parent.parent / "data" / "commun"
if not (REPERTOIRE_COMMUN / "attente.py").is_file():
    raise RuntimeError(
        "Motif attente introuvable : " + str(REPERTOIRE_COMMUN / "attente.py")
    )
sys.path.insert(0, str(REPERTOIRE_COMMUN))

INTERVALLE_SECONDS = 60
# Nom CANONIQUE de la cadence declaree, lu par `vie etat` : on LIT la cadence
# au lieu de l'attendre (attendre n'est pas verifier). Meme valeur, meme objet.
INTERVALLE_DECLARE_SECONDES = INTERVALLE_SECONDS
ENCODAGE = "utf-8"

# Sources et destination.
CHEMIN_INBOX = REPERTOIRE_ROUTINE.parent.parent / "intercom" / "matrice" / "inbox.jsonl"
REPERTOIRE_OUTIL_SUIVI = REPERTOIRE_ROUTINE.parent.parent / "data" / "outils" / "suivi-optimus"
NOM_PID = "suivi-sync.pid"
CHEMIN_PID = REPERTOIRE_ROUTINE / NOM_PID
NOM_DRAPEAU_ARRET = "suivi-sync.arret"
CHEMIN_DRAPEAU_ARRET = REPERTOIRE_ROUTINE / NOM_DRAPEAU_ARRET

# ETAT COURT DE LA PASSE (friction 28, 2026-09-14) : le BATTEMENT d'une routine
# est un ETAT, pas une histoire -- il s'ecrit ICI, a chaque passe et ECRASE.
# Sans ce temoin, suivi-sync etait la SEULE routine dont le rythme reel n'etait
# mesurable nulle part : ni journal, ni etat de passe (elle n'ecrit que son PID,
# une fois). `verifier-cadence` le lit et le compare a la cadence DECLAREE
# ci-dessus -- c'est la troisieme jambe : declarer, publier, MESURER.
NOM_ETAT = "suivi-sync-etat.json"
CHEMIN_ETAT = REPERTOIRE_ROUTINE / NOM_ETAT
# Combien de dernieres passes l'etat garde : assez pour un ecart MEDIAN (une
# passe en retard ou un redemarrage ne doivent pas faire croire a une derive),
# et borne pour que l'etat reste un etat (une poignee d'horodatages).
# La FABRIQUE de l'anneau (ajout + borne) et sa LECTURE (ecart median) sont le
# moteur PARTAGE `data/commun/battement.py` : la routine ne declare QUE sa
# longueur, elle ne recopie pas le decoupage (L-029 : un moteur recopie quatre
# fois diverge quatre fois).
PASSES_GARDEES_ETAT = 5
# Clef de l'anneau DANS l'etat : un seul nom, ecrit ET relu par sa constante.
CLE_ANNEAU_PASSES = "dernieres_passes"
# Format UNIQUE des horodatages (journal + etat) : le temps s'ecrit a un seul
# endroit, le meme des deux cotes (ecriture et relecture du battement).
FORMAT_HORODATAGE = "%Y-%m-%d %H:%M:%S"
ENCODAGE_ETAT = "utf-8"

# Actions a synchroniser (ce qui interesse optimus-prime).
TYPES_INTERESSANTS = ("fin-mission", "retour-lot")

# La synchronisation evite les doublons en comparant les dates.
# Si la date de l'evenement inbox est <= la date du dernier evenement
# dans le suivi-optimus, on considere que c'est deja synchronise.
# On utilise une comparaison lexicographique (format ISO 8601).
# Note : les dates dans l'inbox sont au format "AAAA-MM-JJ HH:MM:SS".
# On les compare en tant que chaines (ordre chronologique preserve).
