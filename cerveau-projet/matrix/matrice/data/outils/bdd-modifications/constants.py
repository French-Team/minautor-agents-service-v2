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

# LE CHAMP D'EMPREINTE D'UNE NOTE (friction du 2026-09-23) : une note n'attestait
# son fichier que par sa DATE -- une note ecrite pour une AUTRE ecriture blanchissait
# donc n'importe quel changement posterieur, et le controle d'attribution, qui
# IMPRIMAIT les deux empreintes sans les comparer, ne pouvait pas le voir. La note
# porte desormais l'empreinte SHA-256 du contenu AU MOMENT ou elle est prise : c'est
# ce qui permet de COMPARER au lieu de seulement dater. Le nom vit ICI : ecrit par
# `noter`, relu par le controle, une seule forme (M-076).
CHAMP_EMPREINTE = "empreinte"

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
