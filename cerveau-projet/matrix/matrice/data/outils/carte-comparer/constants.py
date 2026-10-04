"""Constantes de l'outil carte-comparer (MO-430).

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les
contient pas. L outil est en LECTURE seule : il ne pose aucun fragment.
"""
import sys
from pathlib import Path

REPERTOIRE_OUTIL = Path(__file__).resolve().parent
REPERTOIRE_DATA = REPERTOIRE_OUTIL.parent.parent
if REPERTOIRE_DATA.name != "data":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_DATA) + " n'est pas le dossier data/"
    )

# data/commun (motif unique M-076) : racine detectee par marqueur, zone jetable.
sys.path.insert(0, str(REPERTOIRE_DATA / "commun"))
from racine import detecter_racine  # noqa: E402
from zone_tmp import chemin_zone_optimus  # noqa: E402

RACINE = detecter_racine(REPERTOIRE_OUTIL)
PERIMETRE = RACINE / "cerveau-projet"
# La racine des documents de la Matrice : la ou vivent les cartes et les modeles.
RACINE_MATRICE = PERIMETRE / "matrix"

# LA REFERENCE DE COMPARAISON (decision createur MO-430) : le modele de la
# carte TRES detaillee donne les CHAMPS a presence, le domicile partage donne
# la CONFORMITE (carte_identite valider_carte).
REPERTOIRE_MODELE = RACINE_MATRICE / "matrice" / "templates" / "carte-identite"
MODELE_COMPLET = REPERTOIRE_MODELE / "carte-complete.modele"
MODELE_MINIMAL = REPERTOIRE_MODELE / "carte.modele"
CHOIX_MODELE = ("complet", "minimal")
MODELE_DEFAUT = "complet"

# La zone jetable du flux : seule l auto-test s y pose (l outil est lecture).
ZONE_FRAGMENTS = chemin_zone_optimus(RACINE_MATRICE)

# Codes retour (contrat des outils : 0 sain, 1 ecart, 2 refus d'usage).
CODE_OK = 0
CODE_ECHEC = 1
CODE_REFUS = 2

# Filtres du scan corpus : memes exclusions que le garde (archives, caches,
# points de restauration -- un balayage qui les compte crie dans le vide).
DOSSIERS_IGNORES = ("__pycache__", ".git", "purification", "tmp-optimus")
MOTIF_POINT_RESTAURATION = ".bak"
EXTENSIONS_CORPUS = (".md",)
LIMITE_LIGNES = 8

ENCODAGE = "utf-8"
