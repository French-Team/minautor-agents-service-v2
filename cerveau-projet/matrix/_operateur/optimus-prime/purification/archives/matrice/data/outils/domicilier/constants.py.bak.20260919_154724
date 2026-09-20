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

RACINE = detecter_racine(REPERTOIRE_OUTIL)
PERIMETRE = RACINE / "cerveau-projet"

# La PORTE d'ecriture : la remorque n'ecrit JAMAIS elle-meme. Toute ecriture
# passe par elle (garde, validation, .bak, SHA) -- mesure MO-171 : une passe
# d'alignement qui ecrit en direct n'a AUCUNE de ces garanties.
PORTE_ECRIRE = REPERTOIRE_DATA / "outils" / "ecrire" / "main.py"
ZONE_FRAGMENTS = REPERTOIRE_DATA.parent / "tmp-optimus"

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
