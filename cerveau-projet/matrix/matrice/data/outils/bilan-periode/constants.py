"""Constantes de l'outil bilan-periode : chemins, periodes fermees, formes.

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
"""
import sys
from pathlib import Path

REPERTOIRE_OUTIL = Path(__file__).resolve().parent
REPERTOIRE_DATA = REPERTOIRE_OUTIL.parent.parent
if REPERTOIRE_DATA.name != "data":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_OUTIL) + " n'est pas dans data/outils/"
    )

# Sources horodatees (LECTURE SEULE : bilan-periode n'ecrit jamais).
NOM_HISTORIQUES = "historiques-missions.jsonl"
NOM_USAGES = "usages-outils-combos.jsonl"
NOM_ACTIVITES = "activites-recentes.json"
NOM_DEFCON = "defcon-historique.jsonl"
CHEMIN_HISTORIQUES = REPERTOIRE_DATA / NOM_HISTORIQUES
CHEMIN_USAGES = REPERTOIRE_DATA / NOM_USAGES
CHEMIN_ACTIVITES = REPERTOIRE_DATA / NOM_ACTIVITES
CHEMIN_DEFCON = REPERTOIRE_DATA / NOM_DEFCON

# Periodes fermees (decision createur : dernieres heures = 6 h, mois = 30 jours).
PERIODES_HEURES = {"1h": 1, "heures": 6, "24h": 24, "3j": 72, "semaine": 168, "mois": 720}

FORMAT_DATE = "%Y-%m-%d %H:%M:%S"

# Presentation : lignes max detaillees par section du bilan.
LIMITE_LIGNES = 8
TOP_USAGES = 5

ENCODAGE = "utf-8"

# data/commun (motif unique M-076) : installe le dossier partage dans sys.path.
_courant = REPERTOIRE_OUTIL
for _ in range(30):
    if (_courant / "commun" / "racine.py").is_file():
        sys.path.insert(0, str(_courant / "commun"))
        break
    _courant = _courant.parent
else:
    raise RuntimeError("data/commun introuvable en remontant.")

from racine import detecter_racine  # noqa: E402

RACINE = detecter_racine(REPERTOIRE_OUTIL)
