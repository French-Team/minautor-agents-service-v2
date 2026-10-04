"""Constantes de l'outil domicilier.

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
# MO-236 : le domicile de la zone jetable d'Optimus se LIT au moteur partage
# (`data/commun/zone_tmp.py`), jamais recopie (M-076).
from zone_tmp import chemin_zone_optimus  # noqa: E402

RACINE = detecter_racine(REPERTOIRE_OUTIL)
PERIMETRE = RACINE / "cerveau-projet"

# La PORTE d'ecriture : la remorque n'ecrit JAMAIS elle-meme. Toute ecriture
# passe par elle (garde, validation, .bak, SHA) -- mesure MO-171 : une passe
# d'alignement qui ecrit en direct n'a AUCUNE de ces garanties.
# EO-287 : on declare le NOM, jamais le chemin -- la resolution (et son
# refus nomme) vit dans data/commun/resolution_outils.py, ou on LA LIT.
NOM_PORTE_ECRIRE = "ecrire"
# MO-236 : la RACINE MATRICE se derive du PERIMETRE deja declare -- `REPERTOIRE_DATA`
# est `matrice/data`, donc son parent est `matrice/` et NON `matrix/`. L'ancienne
# forme (`REPERTOIRE_DATA.parent / "tmp-optimus"`) visait `matrice/tmp-optimus`,
# qui n'a jamais existe : un defaut PRE-EXISTANT, mesure en deplacant la zone.
ZONE_FRAGMENTS = chemin_zone_optimus(PERIMETRE / "matrix")

REPERTOIRE_PLANS = REPERTOIRE_OUTIL / "plans"
NOM_PLAN_DEFAUT = "parseur-options.json"

ENCODAGE = "utf-8"
INDENTATION = "    "

# Filtres TECHNIQUES : un point de restauration ou une archive ne sont pas des
# copies d'une classe (un balayage qui les compte crie dans le vide).
DOSSIERS_IGNORES = ("__pycache__", "purification", "tmp-optimus", ".git")
# Un perimetre NOMME est fouille en entier (hors ces caches) : celui qui le
# nomme sait ce qu'il regarde -- c'est ce qui rend l'epreuve possible dans un
# bac a sable, sans jamais toucher la classe reelle.
DOSSIERS_TECHNIQUES = ("__pycache__", ".git")
MOTIF_POINT_RESTAURATION = ".bak"
EXTENSIONS_CLASSE = (".py", ".moule")

# Champs FERMES d'un plan : un plan qui ne dit pas tout ne peut pas tout aligner.
CHAMPS_PLAN = ("classe", "fonction", "domicile", "marqueur", "docstring", "import", "appel")
CHAMPS_PLAN_OPTIONNELS = ("exclus", "extras", "derive", "attendu")
PLACEHOLDER_EXTRAS = "{extras}"

# Codes retour
CODE_OK = 0
CODE_ECART = 1
CODE_REFUS = 2
