"""Constantes de l'outil carte-editer (MO-430).

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les
contient pas.
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

# La PORTE d'ecriture : ce noutil n'ecrit JAMAIS lui-meme (decision createur
# MO-430 : editer passe par la porte ecrire -- fragments et cible, garde de
# provenance compris : le controle attribution jauge chaque carte remplacee).
NOM_PORTE_ECRIRE = "ecrire"

# Fragments d'ecriture : la zone jetable du flux (le pilote la vide a la cloture).
ZONE_FRAGMENTS = chemin_zone_optimus(RACINE_MATRICE)

# Codes retour (contrat des outils : 0 sain, 1 ecart, 2 refus d'usage).
CODE_OK = 0
CODE_ECHEC = 1
CODE_REFUS = 2

ENCODAGE = "utf-8"
