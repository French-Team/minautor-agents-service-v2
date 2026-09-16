"""Constantes de l'outil corriger-ascii : chemins, carte de conversion, protections.

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
Racine (pattern v1) : DETECTEE en remontant jusqu'au dossier contenant AGENTS.md.
"""
import sys
from pathlib import Path

REPERTOIRE_OUTIL = Path(__file__).resolve().parent
REPERTOIRE_PARENT = REPERTOIRE_OUTIL.parent
if (
    REPERTOIRE_PARENT.name != "outils"
    or REPERTOIRE_PARENT.parent.name != "data"
    or REPERTOIRE_PARENT.parent.parent.name != "matrice"
):
    raise RuntimeError(
        "Structure inattendue : "
        + str(REPERTOIRE_OUTIL)
        + " n'est pas dans matrice/data/outils/"
    )


# data/commun (motif unique M-076) : le motif racine est PARTAGE, jamais recopie.
sys.path.insert(0, str(REPERTOIRE_OUTIL.parent.parent / "commun"))
from racine import detecter_racine  # noqa: E402

RACINE = detecter_racine(REPERTOIRE_OUTIL)
REPERTOIRE_MATRIX = RACINE / "cerveau-projet" / "matrix"

EXTENSIONS_CIBLES = (".md", ".py", ".json")
EXTENSIONS_JOURNAUX = (".jsonl",)
DOSSIERS_CIBLES = (
    REPERTOIRE_MATRIX / "matrice",
    REPERTOIRE_MATRIX / "_operateur",
    REPERTOIRE_MATRIX / "docs",
)
DOSSIERS_EXCLUS = ("__pycache__",)
SUFFIXES_EXCLUS = (".sha256", ".tmp")

# Un fichier possedant un etalon .sha256 n'est JAMAIS reecrit (BDD empreintee).
# Les fichiers .jsonl (journaux en ajout seul) ne sont pas cibles.
# MO-075 : ces deux exclusions etaient MUETTES -- le rapport ne disait pas qu'il
# excluait, donc 8 BDD et tous les journaux sortaient du champ SANS que personne
# ne le voie (540 fichiers scannes contre 569 pour garde-ascii). Elles sont
# desormais NOMMEES et RAPPORTEES (chacune avec son motif), sans etre reecrites.
SUFFIXE_ETALON = ".sha256"
MOTIF_BDD_EMPREINTE = "BDD empreintee (.sha256) -- jamais reecrite"
MOTIF_JOURNAL = "journal en ajout seul (.jsonl) -- non cible"

# Carte de conversion : caractere non-ASCII -> ASCII (echappements Unicode
# explicites, inalterables par l'edition). Tout caractere absent de la carte
# est LAISSE TEL QUEL et signale (probleme plus grave).
CARTE_CONVERSION = {
    "\u00e0": "a", "\u00e2": "a", "\u00e4": "a",
    "\u00e9": "e", "\u00e8": "e", "\u00ea": "e", "\u00eb": "e",
    "\u00ee": "i", "\u00ef": "i",
    "\u00f4": "o", "\u00f6": "o",
    "\u00f9": "u", "\u00fb": "u", "\u00fc": "u",
    "\u00e7": "c",
    "\u00ff": "y",
    "\u00c0": "A", "\u00c2": "A", "\u00c4": "A",
    "\u00c9": "E", "\u00c8": "E", "\u00ca": "E",
    "\u00ce": "I",
    "\u00d4": "O",
    "\u00d9": "U", "\u00db": "U",
    "\u00c7": "C",
    "\u0153": "oe", "\u0152": "OE",
    "\u2018": "'", "\u2019": "'",
    "\u201c": '"', "\u201d": '"',
    "\u00ab": "<", "\u00bb": ">",
    "\u2013": "-", "\u2014": "-",
    "\u2026": "...",
    "\u00a0": " ",
    "\u2192": "->",
}

ENCODAGE = "utf-8"
