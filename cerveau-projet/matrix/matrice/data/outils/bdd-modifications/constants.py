"""Constantes de l'outil bdd-modifications.

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
"""
import sys
from pathlib import Path

REPERTOIRE_OUTIL = Path(__file__).resolve().parent
# L'outil vit dans outils/bdd-modifications/ ; la BDD vit deux niveaux au-dessus (dans data/).
REPERTOIRE_DATA = REPERTOIRE_OUTIL.parent.parent
if REPERTOIRE_DATA.name != "data":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_DATA) + " n'est pas le dossier data/"
    )

NOM_BDD = "modifications-par-fichier.json"
NOM_BDD_TMP = NOM_BDD + ".tmp"
CHEMIN_BDD = REPERTOIRE_DATA / NOM_BDD
CHEMIN_EMPREINTE = REPERTOIRE_DATA / (NOM_BDD + ".sha256")

ACTIONS_PERMISES = ("cree", "modifie", "corrige", "supprime")

ENCODAGE = "utf-8"
INDENTATION_JSON = 2
TAILLE_BLOC_LECTURE = 65536

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
