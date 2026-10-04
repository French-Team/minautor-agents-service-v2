"""Constantes de l'outil ecrire.

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

# Perimetre ecriture : matrix/ seul, sauf allowlist racine (2 demarrages).
REPERTOIRE_MATRIX = RACINE / "matrix"
REPERTOIRE_MATRICE = RACINE / "cerveau-projet" / "matrix" / "matrice"
if not REPERTOIRE_MATRIX.is_dir():
    REPERTOIRE_MATRIX = RACINE / "matrix"
# Fallback detection si structure cerveau-projet/
ALT_MATRIX = RACINE / "cerveau-projet" / "matrix"
if ALT_MATRIX.is_dir():
    REPERTOIRE_MATRIX_ALT = ALT_MATRIX
else:
    REPERTOIRE_MATRIX_ALT = REPERTOIRE_MATRIX
ALLOWLIST_RACINE = ("AGENTS.md",)
ALLOWLIST_PREFIXES = ("demarrer-",)

# LE MOULE EST LE SEUL CHEMIN DE NAISSANCE D'UNE ROUTINE (EO-389) : toute
# ecriture sous `matrice/routines/<nom>/` exige le marqueur de provenance que
# pose le generateur (`dupliquer-template --moule routine`). Le garde vit ICI,
# dans le passage oblige de TOUTE ecriture -- jamais dans un outil qu'on peut
# oublier d'appeler : une regle que rien n'applique est une regle morte.
SEGMENT_ROUTINES = "routines"
RACINES_MATRICE = ("matrice", "matrix")
NOM_MARQUEUR_PROVENANCE = "provenance.json"
# Les deux origines ADMISES d'une routine : nee du moule, ou ANTERIEURE au moule
# (le passe se declare alors, par un motif -- une declaration muette ne declare rien).
ORIGINES_PROVENANCE = ("moule", "anterieure")


# LA RACINE DE LA MATRICE est CONSOMMEE chez son domicile partage (data/commun/
# cible.py) : le perimetre doit juger le chemin RESOLU, donc il a besoin de la
# racine REELLE de la Matrice. Deux installations existent (depot :
# cerveau-projet/matrix ; deploiement : matrix) -- rejouer cette detection ici en
# ferait un SECOND domicile (M-076, EO-154). `racine_matrice_stricte` est
# SEPAREE de `racine_matrice` (MO-184) : celle-ci a un repli sur la racine du
# WORKSPACE (juste pour ANCRER une destination, FAUX pour JUGER un perimetre),
# celle-la n en a AUCUN -- None veut dire aucune Matrice, et le perimetre REFUSE
# alors NOMMEMENT (jamais en silence -- MO-183 / EO-177).
from cible import racine_matrice_stricte  # noqa: E402
RACINE_MATRICE = racine_matrice_stricte(REPERTOIRE_OUTIL)

# LA ZONE DES SOURCES DU CREATEUR (docs/) a SON DOMICILE PARTAGE : la porte le
# CONSOMME, elle ne le recopie pas (M-076). Ce n est pas une convention ASCII de
# plus : la zone est LECTURE SEULE (regle `ascii-strict.md`), donc le passage
# oblige de toute ecriture la REFUSE -- la ou le garde ASCII l exempte, les deux
# instruments disent enfin la MEME chose sur la MEME zone (MO-377).
from zone_sources import (  # noqa: E402,F401  (re-export pour commun.py)
    MOTIF_ZONE_SOURCES,
    NOM_ZONE_SOURCES,
    refus_zone_sources,
)

ENCODAGE = "utf-8"
ENCODAGE_ERREUR = "strict"
TAILLE_BLOC_LECTURE = 65536
INDENTATION_JSON = 2

# Suffixes
SUFFIXE_TMP = ".tmp"
SUFFIXE_BAK = ".bak"

# FORME du point de restauration (friction 42, arbitrage createur 2026-09-16) :
# la forme est PRODUITE par cette porte (commun.chemin_bak) et nulle part
# ailleurs -- elle se declare donc ICI, une seule fois. Tout consommateur qui
# doit RECONNAITRE un point de restauration (contrat fondamental, espion
# d'integrite, remorque Optimus) compile CE motif au lieu de le redeviner :
# une forme redevinee par un consommateur derive en silence (L-100/L-102).
FORMAT_HORODATE_BAK = "%Y%m%d_%H%M%S"
MOTIF_BAK_HORODATE = r"\.bak\.\d{8}_\d{6}(-\d+)?$"

# EO-191 (MO-223) : une RAFALE d'editions du meme fichier dans la MEME SECONDE
# ne doit plus ECRASER le point pristine. Le nom canonique reste celui declare
# juste au-dessus ; quand il est DEJA pris par un AUTRE etat, la porte ouvre un
# point DISTINCT en suffixant un compteur -- et le motif DECLARE le couvre, donc
# les consommateurs (espion d'integrite, remorque, contrat fondamental) le
# recoivent par le domicile, sans avoir une seule ligne a changer.
MARQUEUR_POINT_EN_PLUS = "-"
RANG_POINT_EN_PLUS_MIN = 2
RANG_POINT_EN_PLUS_MAX = 99
MESSAGE_POINT_DISTINCT = "[BAK] nom canonique deja pris : point de restauration DISTINCT "

# Modes
MODES_PERMIS = ("creer", "remplacer", "ajouter")

# Options CLI
NOMS_OPTIONS_ECRIRE = ("fichier", "contenu", "contenu-fichier", "contenu-base64", "mode")
NOMS_OPTIONS_EDITER = ("fichier", "ancien", "nouveau", "ancien-fichier", "nouveau-fichier",
                        "ancien-base64", "nouveau-base64")

# Option SANS valeur : la sentinelle est CONSOMMEE du DOMICILE partage
# data/commun/options.py (EO-158) -- UN SEUL domicile par verite (lecon EO-154 :
# deux domiciles qui divergent font une trace muette). Le chemin data/commun est
# deja pose plus haut par le motif M-076, d ou l import APRES, jamais avant.
from options import CLE_SANS_VALEUR  # noqa: E402,F401
