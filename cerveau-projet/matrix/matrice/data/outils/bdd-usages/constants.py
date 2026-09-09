"""Constantes de l'outil bdd-usages.

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
"""
import sys
from pathlib import Path

REPERTOIRE_OUTIL = Path(__file__).resolve().parent
# L'outil vit dans outils/bdd-usages/ ; la BDD vit deux niveaux au-dessus (dans data/).
REPERTOIRE_DATA = REPERTOIRE_OUTIL.parent.parent
if REPERTOIRE_DATA.name != "data":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_DATA) + " n'est pas le dossier data/"
    )

NOM_BDD = "usages-outils-combos.jsonl"
CHEMIN_BDD = REPERTOIRE_DATA / NOM_BDD

# Cles requises dans CHAQUE ligne de la BDD (controle structurel du verifier).
CLES_REQUISES = ("date", "outil", "commande", "code", "tags")

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
