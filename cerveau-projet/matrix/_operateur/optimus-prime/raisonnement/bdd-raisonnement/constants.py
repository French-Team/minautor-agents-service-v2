"""Constantes de l'outil bdd-raisonnement (zone INVISIBLE -- L-016).

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
SURCHARGE PRIVEE : ce fichier REMPLACE constants.py du moule outil-bdd quand le
generateur est appele avec --zone privee. La BDD et l'outil vivent dans la ZONE
INVISIBLE (le cameleon ne les lit jamais).
"""
import sys
from pathlib import Path

REPERTOIRE_OUTIL = Path(__file__).resolve().parent
# La BDD vit UN niveau au-dessus de l'outil, dans le dossier du raisonnement.
REPERTOIRE_BDD = REPERTOIRE_OUTIL.parent

NOM_BDD = "segments.json"
NOM_BDD_TMP = NOM_BDD + ".tmp"
CHEMIN_BDD = REPERTOIRE_BDD / NOM_BDD
CHEMIN_EMPREINTE = REPERTOIRE_BDD / (NOM_BDD + ".sha256")

PREFIXE_ID = "RS"

ENCODAGE = "utf-8"
INDENTATION_JSON = 2
TAILLE_BLOC_LECTURE = 65536

# data/commun (motif unique M-076) : installe le dossier PARTAGE dans sys.path
# (options, racine, sac_a_dos). La Matrice est la racine qui porte
# `matrice/data/commun/options.py`.
_courant = REPERTOIRE_OUTIL
for _ in range(40):
    if (_courant / "matrice" / "data" / "commun" / "options.py").is_file():
        sys.path.insert(0, str(_courant / "matrice" / "data" / "commun"))
        break
    if _courant.parent == _courant:
        raise RuntimeError("matrice/data/commun introuvable en remontant.")
    _courant = _courant.parent
else:
    raise RuntimeError("matrice/data/commun introuvable en remontant.")

from racine import detecter_racine  # noqa: E402

RACINE = detecter_racine(REPERTOIRE_OUTIL)
