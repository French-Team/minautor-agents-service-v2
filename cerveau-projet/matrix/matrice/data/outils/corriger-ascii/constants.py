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
)
DOSSIERS_EXCLUS = ("__pycache__",)

# Zone de SOURCES du createur : LECTURE SEULE. C'est la MEME decision que
# `garde-ascii` (EXCLUS_DIRS) -- mais elle etait ecrite la-bas et PAS ici, donc
# deux scans du projet se contredisaient : l'un exemptait `docs/`, l'autre le
# ciblait et levait une alerte "caractere non convertible (decision du createur
# requise)" pour un arbitrage DEJA rendu (friction 81, EO-135).
# Mesure du 2026-09-17 : AUCUN caractere de `docs/` n'est convertible (emojis et
# degre hors carte) -- ce scan n'y corrigeait rien, il n'y faisait que crier.
# Le motif est NOMME et RAPPORTE, jamais tu : une exclusion muette est un angle
# mort qu'aucune suite ne voit (doctrine de cet outil).
# HORS CHAMP -- et ce n'est PAS une exemption. Deux notions distinctes :
#   - un EXEMPTE est VU puis JAMAIS reecrit, et son motif est JUSTIFIE sur le
#     disque (un etalon `.sha256`, ou un journal `.jsonl`) ;
#   - une zone HORS CHAMP n'est pas PARCOURUE du tout (aucun fichier a classer).
# Les deux vivaient dans la MEME liste : une exclusion de PERIMETRE portait donc
# le contrat d'une exemption de REECRITURE. Mesure du 2026-09-17 : le garde
# `verifier-exemptions-visibles` exige DEUX motifs d'exemption justifies par le
# disque -- y verser un dossier entier faisait echouer la non-regression (maillon
# 12). Une exclusion de perimetre se DECLARE ici ; une exemption de reecriture se
# JUSTIFIE sur le disque. Deux maisons, jamais la meme.
DOSSIERS_HORS_CHAMP = (
    (REPERTOIRE_MATRIX / "docs",
     "zone de SOURCES du createur (lecture seule, decision createur)"),
)
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
# La carte n'est plus un domicile de cet outil : elle vit dans la couche
# PARTAGEE (matrice/data/commun/carte_ascii.py), ou DEUX consommateurs la lisent
# -- ce scan de maintenance et la porte `ecrire`, passage oblige de toute
# ecriture. Recopiee, elle aurait ete deux verites (l'une corrigeant ce que
# l'autre ignorait) : c'est le module partage qui la porte depuis MO-210
# (revision createur 2026-09-19). L'import est local : constants a installe
# data/commun dans sys.path plus haut dans ce fichier.
from carte_ascii import CARTE_CONVERSION  # noqa: E402,F401  (re-export pour les categories)

ENCODAGE = "utf-8"
