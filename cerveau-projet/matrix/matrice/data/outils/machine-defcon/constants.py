"""Constantes de l'outil machine-defcon : chemins et echelle defcon fermee.

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

# Le niveau courant vit dans le classeur-variables (cle defcon) : UNE source de verite.
CLE_DEFCON = "defcon"
CHEMIN_CLASSEUR = REPERTOIRE_DATA / "classeur-variables.json"
CHEMIN_EMPREINTE_CLASSEUR = REPERTOIRE_DATA / "classeur-variables.json.sha256"
NOM_CLASSEUR_TMP = "classeur-variables.tmp"

# Journal append-only des transitions (une ligne JSON par transition).
NOM_JOURNAL = "defcon-historique.jsonl"
CHEMIN_JOURNAL = REPERTOIRE_DATA / NOM_JOURNAL

ENCODAGE = "utf-8"
INDENTATION_JSON = 2
TAILLE_BLOC_LECTURE = 65536

# L'echelle defcon est FERMEE (decision createur, convention des crochets).
# 1 = reserve (jamais atteint : la descente s'arrete a 2), 2 = normal,
# 3 = surveiller puis valider, 4 = suivi de bout en bout, 5 = max.
NIVEAU_NORMAL = 2
NIVEAUX = (1, 2, 3, 4, 5)
NIVEAUX_MONTABLES = (3, 4, 5)
DESCENTES_PERMISES = ((5, 4), (4, 3))

NOMS_NIVEAUX = {
    1: "reserve (non defini par l'operateur)",
    2: "normal",
    3: "surveiller puis valider (la validation clot def3)",
    4: "suivi des problemes a resoudre, de bout en bout",
    5: "stop de l'agent par defaut (cameleon a venir), optimus-prime reveille",
}

# A defcon 5, seul ce theme reste injectable (garde posee dans le pilote).
THEME_DEFCON = "DEFCON"

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
