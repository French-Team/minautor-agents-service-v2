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

# AVAL des missions : il y en a DEUX, crees expres pour ne pas melanger les flux
# (voir `_operateur/optimus-prime/pilote/constants.py` : "Historique dedie
# Optimus, jamais historiques-missions.jsonl du cameleon").
# `[bilan]` doit les lire TOUS LES DEUX : ne lire que celui du cameleon fait
# afficher "0 mission" des que flux2 est selectionne, alors que les missions
# Optimus existent (constat MO-061 : 15 missions d'Optimus le 2026-09-13,
# bilan annoncant 0). On n'ecrit JAMAIS dans ces journaux : lecture seule.
SOURCES_HISTORIQUES = (
    ("cameleon", "historiques-missions.jsonl"),
    ("optimus", "historiques-missions-optimus.jsonl"),
)
NOM_USAGES = "usages-outils-combos.jsonl"
NOM_ACTIVITES = "activites-recentes.json"
NOM_DEFCON = "defcon-historique.jsonl"
CHEMIN_HISTORIQUES = REPERTOIRE_DATA / NOM_HISTORIQUES
CHEMINS_HISTORIQUES = tuple(
    (etiquette, REPERTOIRE_DATA / nom) for etiquette, nom in SOURCES_HISTORIQUES
)
CHEMIN_USAGES = REPERTOIRE_DATA / NOM_USAGES
CHEMIN_ACTIVITES = REPERTOIRE_DATA / NOM_ACTIVITES
CHEMIN_DEFCON = REPERTOIRE_DATA / NOM_DEFCON

# Periodes fermees (decision createur : dernieres heures = 6 h, mois = 30 jours).
PERIODES_HEURES = {"1h": 1, "heures": 6, "24h": 24, "3j": 72, "semaine": 168, "mois": 720}

FORMAT_DATE = "%Y-%m-%d %H:%M:%S"

# Presentation : lignes max detaillees par section du bilan.
LIMITE_LIGNES = 8
TOP_USAGES = 5

# BUDGET DECLARE DE L'OUTIL (MO-100) : la duree d'un bilan se juge contre CE
# budget, et contre rien d'autre. Il vivait jusqu'ici dans le cockpit
# (`SEUILS_PERFS["bilan_periode_ms"]`), c'est-a-dire chez l'observateur, qui
# comparait a un nombre que l'outil n'avait jamais promis -- meme faute que le
# seuil de la veille corrige en MO-097. Mesure du 2026-09-15 : 114 ms pour
# `bilan --periode heures` ; le budget est declaree avec une large marge pour
# crier sur une DERIVE (lecture d'une periode plus longue, journal qui grossit),
# pas sur le cout normal. L'outil le PUBLIE dans sa sortie (voir afficher_bilan).
BUDGET_PASSE_MS = 500

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
