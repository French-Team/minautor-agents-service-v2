"""Constantes de l'outil journal-multi-encarts.

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
Le journal est un VISUEL genere depuis les BDD : jamais edite a la main.
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
REPERTOIRE_MATRICE = RACINE / "cerveau-projet" / "matrix" / "matrice"

# Lecture BORNEE des journaux de routines (MO-078) : cet outil lisait
# journal-veille.txt EN ENTIER (3,85 Mo / 44 050 lignes mesures le 2026-09-13)
# pour n'en afficher que les 5 derniers evenements de passe. Une queue de 256 Ko
# suffit largement et rend le cout constant. La FENETRE ne se declare plus ici
# (MO-099) : elle vient du moteur PARTAGE (data/commun/rotation_journal.py), qui
# la DEDUIT de la borne que le journal lu declare lui-meme.

# Journal v3 : NOUVEAU fichier propre a la v3, dans matrix/ (jamais les fichiers v1/v2).
NOM_JOURNAL = "journal-multi-encarts.md"
CHEMIN_JOURNAL = REPERTOIRE_MATRICE / NOM_JOURNAL

# Sources d'etat (lecture seule, jamais d'ecriture ici).
CHEMIN_FILE_MISSIONS = REPERTOIRE_MATRICE / "pilote" / "file-missions.json"
CHEMIN_ENTONNOIR_FILES = REPERTOIRE_MATRICE / "pilote" / "entonnoir-files.json"
CHEMIN_CLASSEUR_VARIABLES = REPERTOIRE_DATA / "classeur-variables.json"
CHEMIN_INBOX_MATRICE = REPERTOIRE_MATRICE / "intercom" / "matrice" / "inbox.jsonl"
CHEMIN_BOITE_CAMELEON = REPERTOIRE_MATRICE / "intercom" / "cameleon" / "inbox.jsonl"
CHEMIN_ALERTES = REPERTOIRE_MATRICE / "routines" / "veille-flux" / "alertes-emises.json"
CHEMIN_BDD_ACTIVITES = REPERTOIRE_DATA / "activites-recentes.json"
CHEMIN_BDD_USAGES = REPERTOIRE_DATA / "usages-outils-combos.jsonl"
CHEMIN_BDD_MODIFICATIONS = REPERTOIRE_DATA / "modifications-par-fichier.json"
CHEMIN_BDD_LECONS = REPERTOIRE_DATA / "lecons.json"
CHEMIN_BDD_VARIABLES = REPERTOIRE_DATA / "classeur-variables.json"

# Encarts fermes (decision createur) : ordre d'affichage, jamais en vrac.
ENCARTS = (
    "matrice",
    "missions",
    "routines",
    "alertes",
    "cameleon",
    "usages",
    "modifications",
    "lecons",
    "variables",
)

# FLUX de chaque encart (demande createur M-080) : d'ou viennent les
# informations, vers ou elles vont. Affiche en tete de chaque encart.
FLUX = {
    "matrice": (
        "classeur-variables.json + fichiers PID des boucles -> VUE lecture seule"
    ),
    "missions": (
        "pilote/file-missions.json + pilote/entonnoir-files.json -> VUE lecture seule"
    ),
    "routines": (
        "routines/veille-flux/journal-veille.txt -> VUE lecture seule"
    ),
    "alertes": (
        "veille-flux/alertes-emises.json + intercom/matrice/inbox.jsonl -> VUE lecture seule"
    ),
    "cameleon": (
        "intercom/cameleon/inbox.jsonl (ecrit par pause-session) -> VUE lecture seule"
    ),
    "usages": (
        "sac-a-dos (chaque outil) -> bdd-usages -> usages-outils-combos.jsonl -> VUE"
    ),
    "modifications": (
        "notes de mission -> bdd-modifications -> modifications-par-fichier.json -> VUE"
    ),
    "lecons": (
        "lecons gravees -> bdd-lecons -> lecons.json -> VUE (relues a chaque injection)"
    ),
    "variables": (
        "machine-defcon / pause-session / bdd-variables -> classeur-variables.json -> VUE"
    ),
}

ENCODAGE = "utf-8"