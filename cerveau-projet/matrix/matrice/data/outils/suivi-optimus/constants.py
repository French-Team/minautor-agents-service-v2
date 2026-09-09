"""Constantes de l'outil suivi-optimus.

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
"""
import sys
from pathlib import Path

REPERTOIRE_OUTIL = Path(__file__).resolve().parent
# L'outil vit dans outils/suivi-optimus/ ; la BDD vit deux niveaux au-dessus (dans data/).
REPERTOIRE_DATA = REPERTOIRE_OUTIL.parent.parent
if REPERTOIRE_DATA.name != "data":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_DATA) + " n'est pas le dossier data/"
    )

NOM_BDD = "suivi-optimus.jsonl"
NOM_BDD_TMP = NOM_BDD + ".tmp"
CHEMIN_BDD = REPERTOIRE_DATA / NOM_BDD
CHEMIN_EMPREINTE = REPERTOIRE_DATA / (NOM_BDD + ".sha256")

# Actions fermees de la trace (anti-bruit : par EVENEMENT, jamais par fichier).
ACTIONS = (
    "debut",        # debut de mission
    "fin",          # fin de mission avec bilan
    "porte",        # porte officielle utilisee (pilote, lot, tresse, defcon, pause/reprise)
    "depot",        # mission deposee au vrac de l'entonnoir (E-XXX)
    "decision",     # GO / arbitrage du createur
    "decouverte",   # constat d'audit interne (ex : angle mort detecte)
    "bilan",        # bilan-periode demande et rendu
)

ENCODAGE = "utf-8"
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

# Vue markdown dediee (decision createur 2026-09-09) : visuel lisible de la
# trace, dans matrice/ (comme journal-multi-encarts.md), jamais edite a la main.
REPERTOIRE_MATRICE = RACINE / "cerveau-projet" / "matrix" / "matrice"
NOM_VUE = "suivi-optimus.md"
CHEMIN_VUE = REPERTOIRE_MATRICE / NOM_VUE