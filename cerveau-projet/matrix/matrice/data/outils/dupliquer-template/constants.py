"""Constantes de l'outil dupliquer-template.

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
"""
import re
import sys
from pathlib import Path

REPERTOIRE_OUTIL = Path(__file__).resolve().parent
REPERTOIRE_DATA = REPERTOIRE_OUTIL.parent.parent
if REPERTOIRE_DATA.name != "data":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_DATA) + " n'est pas le dossier data/"
    )
REPERTOIRE_OUTILS = REPERTOIRE_DATA / "outils"
REPERTOIRE_MATRICE = REPERTOIRE_DATA.parent
CHEMIN_MOULE = REPERTOIRE_MATRICE / "templates" / "outil-bdd"
SUFFIXE_MOULE = ".moule"

MOTIF_NOM = re.compile(r"^bdd-[a-z][a-z0-9-]*$")
MOTIF_NOM_THEME = re.compile(r"^theme-[a-z][a-z0-9-]*$")
MOTIF_JETON = re.compile(r"__[A-Z_]+__")

REPERTOIRE_TEMPLATES = REPERTOIRE_MATRICE / "templates"
MOULE_DEFAUT = "outil-bdd"
NOM_MOULE_PRINCIPAL = "main.py.moule"

NOMS_OPTIONS = ("moule", "nom", "bdd", "prefixe", "liste", "champ", "humain", "nom-affiche")

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
