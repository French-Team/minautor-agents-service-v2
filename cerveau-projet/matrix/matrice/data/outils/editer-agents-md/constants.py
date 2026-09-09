"""Constantes de l'outil editer-agents-md.

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

# AGENTS.md vit a la RACINE du workspace : detecte par remontee (pattern v1, L-013).
NOM_AGENTS_MD = "AGENTS.md"

# L'encart session-matrix est un BLOC DELIMITE : l'outil ne remplace QUE ce bloc,
# jamais le reste du fichier (les encarts v1/v2 et le marbre sont intouchables).
MARQUEUR_DEBUT = "<!-- session-matrix:DEBUT (v3, gere par l'outil matrice editer-agents-md) -->"
MARQUEUR_FIN = "<!-- session-matrix:FIN -->"

# Point d'insertion : juste avant la configuration active du cerveau (fin de la zone sessions).
LIGNE_ANCRE = "## Configuration Active"

# Etalon d'integrite : AGENTS.md est hors data/, son empreinte vit dans data/.
NOM_EMPREINTE = "agents-md-empreinte.txt"
CHEMIN_EMPREINTE = REPERTOIRE_DATA / NOM_EMPREINTE
NOM_AGENTS_TMP = "AGENTS.md.tmp"

ENCODAGE = "utf-8"
TAILLE_BLOC_LECTURE = 65536

# data/commun (motif unique M-076) : le motif racine est PARTAGE, jamais recopie.
sys.path.insert(0, str(REPERTOIRE_DATA / "commun"))
from racine import detecter_racine  # noqa: E402
