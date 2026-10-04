"""Constantes de l'outil maintenir : Optimus traite les signalements maintenance.

Optimus lit la boite maintenance/matrice/inbox.jsonl, traite les signalements
selon leur niveau d'importance, et met a jour l'etat.
"""
import sys
from pathlib import Path

REPERTOIRE_OUTIL = Path(__file__).resolve().parent
REPERTOIRE_DATA = REPERTOIRE_OUTIL.parent.parent
if REPERTOIRE_DATA.name != "data":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_DATA) + " n'est pas le dossier data/"
    )

sys.path.insert(0, str(REPERTOIRE_DATA / "commun"))
from racine import detecter_racine  # noqa: E402

RACINE = detecter_racine(REPERTOIRE_OUTIL)
# Detection robuste : remonter jusqu'a cerveau-projet/matrix/
REPERTOIRE_MATRIX = None
for p in [REPERTOIRE_OUTIL, *REPERTOIRE_OUTIL.parents]:
    if p.name == "matrix" and (p / "matrice" / "data").is_dir():
        REPERTOIRE_MATRIX = p
        break
if REPERTOIRE_MATRIX is None:
    REPERTOIRE_MATRIX = RACINE / "cerveau-projet" / "matrix"
REPERTOIRE_OPERATEUR = REPERTOIRE_MATRIX / "_operateur"

ENCODAGE = "utf-8"

# Boite maintenance (Optimus lit ici)
BOITE_MAINTENANCE_IN = REPERTOIRE_OPERATEUR / "maintenance" / "matrice" / "inbox.jsonl"
BOITE_MAINTENANCE_OUT = REPERTOIRE_OPERATEUR / "maintenance" / "pilote" / "outbox.jsonl"

# Historique des traitements
HISTORIQUE = REPERTOIRE_OPERATEUR / "maintenance" / "historique-traitements.jsonl"

# Niveaux d'importance (miroir de signaler)
NIVEAUX = {
    "critique": {"ordre": 1, "desc": "Panne totale, reparation immediate"},
    "haute": {"ordre": 2, "desc": "Bug bloquant, reparation prioritaire"},
    "moyenne": {"ordre": 3, "desc": "Amelioration manquante, planifiee"},
    "basse": {"ordre": 4, "desc": "Souhait, file d'attente"},
}

NOMS_OPTIONS = ("lister", "traiter", "etat", "json")
