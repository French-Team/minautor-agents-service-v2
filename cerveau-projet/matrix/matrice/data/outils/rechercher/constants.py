"""Constantes de l'outil rechercher.

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

sys.path.insert(0, str(REPERTOIRE_DATA / "commun"))
from racine import detecter_racine  # noqa: E402

RACINE = detecter_racine(REPERTOIRE_OUTIL)

# Perimetre de BALAYAGE : le dossier matrix/ du projet. Deux emplacements ont
# existe -- un doublon PARASITE a RACINE/matrix (supprime par MO-037) et le vrai
# cerveau-projet/matrix. L'ancien code testait l'absence du parasite puis
# REASSIGNAIT la MEME valeur (non-op) : le jour ou le parasite est parti, le
# moteur est devenu AVEUGLE et repondait "0 resultat" a TOUTES les requetes --
# indiscernable d'une absence de resultat (MO-055). Meme lecon que le chemin
# mythique du questionnaire (MO-051) : un chemin se DETECTE, il ne se suppose pas.
CANDIDATS_MATRIX = (RACINE / "cerveau-projet" / "matrix", RACINE / "matrix")
REPERTOIRE_MATRIX = next(
    (candidat for candidat in CANDIDATS_MATRIX if candidat.is_dir()),
    CANDIDATS_MATRIX[0],
)
REPERTOIRE_MATRICE = REPERTOIRE_MATRIX / "matrice"
ALT_MATRIX = CANDIDATS_MATRIX[0]
REPERTOIRE_MATRIX_ALT = REPERTOIRE_MATRIX

ALLOWLIST_RACINE = ("AGENTS.md",)
ALLOWLIST_PREFIXES = ("demarrer-",)

ENCODAGE = "utf-8"
TAILLE_BLOC_LECTURE = 65536

# Zones invisibles L-016
ZONES_INVISIBLES = ("_operateur", "tmp-optimus", "suivi-optimus")

# Moteur recherche
DANS_VALEURS = ("fichiers", "bdd", "tous")
DEFAUT_DANS = "tous"
LIMITE_DEFAUT = 50
LIMITE_FICHIERS = 250  # global max (comme code_search)
LIMITE_PAR_FICHIER = 15
LIMITE_BDD = 100
# Lecture des sources JSONL : la plus grosse (usages) porte 67k lignes. Une coupe
# SILENCIEUSE etait une cecite (EO-106) : la limite est posee HAUT (elle couvre le
# reel) ET toute coupe restante est DITE par l'outil (`tronque`).
LIMITE_LIGNES_JSONL = 200000

# Un BINAIRE n'est pas du texte : lu tel quel il produit des U+FFFD (taux de
# remplacement) qui pourrissent les extraits et font crasher une sortie machine
# sur console cp1252 (EO-105). Exclusions par EXTENSION (liste fermee, source
# unique).
EXTENSIONS_IGNOREES = (".pid", ".sha256")
EXTENSIONS_BINAIRES = (
    ".db",
    ".sqlite",
    ".sqlite3",
    ".pyc",
    ".pyd",
    ".exe",
    ".dll",
    ".bin",
    ".zip",
    ".gz",
    ".tar",
    ".7z",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".ico",
    ".pdf",
    ".woff",
    ".woff2",
    ".ttf",
    ".pickle",
    ".pkl",
)

# BDD sources palier 1 (9 sources)
BDD_SOURCES = (
    "lecons",
    "modifications",
    "historiques",
    "historiques-optimus",
    "vivier",
    "activites",
    "usages",
    "classeur",
    "conservation",
)

FICHIER_PAR_SOURCE = {
    "lecons": "lecons.json",
    "modifications": "modifications-par-fichier.json",
    "historiques": "historiques-missions.jsonl",
    "historiques-optimus": "historiques-missions-optimus.jsonl",
    "vivier": "vivier-themes.json",
    "activites": "activites-recentes.json",
    "usages": "usages-outils-combos.jsonl",
    "classeur": "classeur-variables.json",
    "conservation": "conservation.json",
}

# FTS5 palier 2 (futur)
INDEX_SQLITE = "index-recherche.sqlite"
INDEX_EMPREINTE = "index-recherche.sqlite.sha256"

# Options DRAPEAU : presentes ou absentes, jamais suivies d'une valeur. Leurs
# NOMS sont declares ici et CONSOMMES par extraire_options -- la liste vivait
# recopiee dans la logique, donc chaque option ajoutee pouvait l'oublier.
NOM_OPTION_JSON = "json"
# `--prive` (EO-126) : INCLUT les zones invisibles L-016 dans le scan des
# FICHIERS, sinon le moteur est AVEUGLE dans la maison de son propre operateur
# (mesure du 2026-09-16 : POSTURE_PAR_TYPE = 0 resultat, alors que la valeur
# n'existe QUE dans _operateur/.../personnalites.py). Le drapeau est EXPLICITE et
# BORNE : sans lui le defaut ne bouge pas d'un pouce, donc le cameleon ne voit
# rien de plus. Il est reserve a la fenetre privee d'Optimus (cockpit, route
# /chercher), jamais a un appel qui pourrait fuir vers le flux 1.
NOM_OPTION_PRIVE = "prive"
NOMS_OPTIONS_DRAPEAU = (NOM_OPTION_JSON, NOM_OPTION_PRIVE, "indexer", "forcer")

# Un hit dit SUR QUOI il a matche : un NOM de fichier n'est pas une LIGNE de
# contenu (EO-126). Sans ce champ, une sortie machine ne peut pas distinguer les
# deux et son lecteur croit a une ligne -- numereo 0 comprise.
SUR_NOM = "nom"
SUR_CONTENU = "contenu"
# Une COMBINAISON de champs de carte d'identite n'est ni un nom ni une ligne :
# c'est le DOCUMENT qui repond. Le hit porte donc sa carte, et son `sur` le dit
# (un lecteur qui prendrait ce hit pour une ligne chercherait une `ligne 0`).
SUR_CARTE = "carte"

# `--champ` : recherche par COMBINAISON de champs de la carte d'identite. La
# demande est UNE valeur (`cle=valeur[;cle=valeur]`) -- et pas une option
# repetee, parce que le parseur PARTAGE garde UNE valeur par nom d'option : une
# option repetee serait ECRASEE en silence (mesure 2026-09-21). La repetition
# est donc REFUSEE et la bonne syntaxe est dite, jamais perdue (L-055).
NOM_OPTION_CHAMP = "champ"

NOMS_OPTIONS_RECHERCHER = ("requete", "dans", "tag", "mot-cle", "source", "periode",
                           NOM_OPTION_CHAMP, NOM_OPTION_JSON, NOM_OPTION_PRIVE, "limite")
NOMS_OPTIONS_INDEXER = ("forcer",)
