"""Constantes de l'outil lire.

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
"""
import sys
from pathlib import Path

REPERTOIRE_OUTIL = Path(__file__).resolve().parent
REPERTOIRE_DATA = REPERTOIRE_OUTIL.parent.parent
if REPERTOIRE_DATA.name != "data":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_DATA) + " n'est pas le dossier data/"
    )

# data/commun (motif unique M-076) : le motif racine est PARTAGE, jamais recopie.
sys.path.insert(0, str(REPERTOIRE_DATA / "commun"))
from racine import detecter_racine  # noqa: E402

RACINE = detecter_racine(REPERTOIRE_OUTIL)

# Perimetre lecture : matrix/ seul, sauf allowlist racine.
REPERTOIRE_MATRIX = RACINE / "matrix"
REPERTOIRE_MATRICE = RACINE / "cerveau-projet" / "matrix" / "matrice"
# Fallback : detecter selon l'existence reelle (compat Windows racine)
if not REPERTOIRE_MATRIX.is_dir():
    REPERTOIRE_MATRIX = RACINE / "matrix"
ALLOWLIST_RACINE = ("AGENTS.md",)
ALLOWLIST_PREFIXES = ("demarrer-",)

ENCODAGE = "utf-8"
ENCODAGE_ERREUR = "strict"
TAILLE_BLOC_LECTURE = 65536

# La TETE INCONNUE (forme non reconnue pour cette extension -- un `.json`, un
# fichier sans marqueur) ne rend pas le fichier ENTIER en silence : elle rend ce
# bloc de lignes et le DIT. Mesure du 2026-09-30 : sur un `.json`, `--tete auto`
# rendait 205/205 lignes et l annonce ne disait RIEN puisque rien n avait ete
# tronque -- l appelant croyait avoir lu une tete et avait lu le fichier complet.
TETE_INCONNUE = 40

# Options CLI.
NOMS_OPTIONS_FICHIER = ("fichier", "fichiers", "dossier", "lignes", "hash", "filtre", "recursif")
