"""Constantes de l'outil bdd-conventions-matrice.

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
"""
import sys
from pathlib import Path

REPERTOIRE_OUTIL = Path(__file__).resolve().parent
# L'outil vit dans outils/bdd-conventions-matrice/ ; la BDD vit deux niveaux au-dessus (dans data/).
REPERTOIRE_DATA = REPERTOIRE_OUTIL.parent.parent
if REPERTOIRE_DATA.name != "data":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_DATA) + " n'est pas le dossier data/"
    )

NOM_BDD = "conventions-matrice.json"
NOM_BDD_TMP = NOM_BDD + ".tmp"
CHEMIN_BDD = REPERTOIRE_DATA / NOM_BDD
CHEMIN_EMPREINTE = REPERTOIRE_DATA / (NOM_BDD + ".sha256")

ENCODAGE = "utf-8"
INDENTATION_JSON = 2
TAILLE_BLOC_LECTURE = 65536

# Prefixe des ids de cette BDD : UNE FAMILLE = UN PREFIXE (regle CV-009).
# `CV-` = conventions de la Matrice. Le prefixe `C-` SEUL est reserve au champ
# `constat` de historiques-missions.jsonl (reste fige du lot 2026-09-11, ni
# ecrit ni lu par aucun outil) : ne JAMAIS le re-emettre.
PREFIXE_ID = "CV-"
LARGEUR_NUMERO = 3

# data/commun (motif unique M-076) : le motif racine est PARTAGE, jamais recopie.
sys.path.insert(0, str(REPERTOIRE_DATA / "commun"))
from racine import detecter_racine  # noqa: E402

RACINE = detecter_racine(REPERTOIRE_OUTIL)
