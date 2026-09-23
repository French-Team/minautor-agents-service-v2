"""Constantes de la porte chaine-pense-bete (EO-215, MO-224).

LA CHAINE (arbitrages createur du 2026-09-19) : un seul document a NOM STABLE,
un STATUT dans la carte d'identite, TROIS familles d'ids (PB- / SP- / TD-), et
un AVANCEMENT pose par la PORTE des que les conditions sont reunies -- le
NEMESIS est une CONDITION LUE, jamais une promesse (arbitrage D).

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs.
"""
import sys
from pathlib import Path

REPERTOIRE_OUTIL = Path(__file__).resolve().parent
if REPERTOIRE_OUTIL.parent.name != "outils" or REPERTOIRE_OUTIL.parent.parent.name != "data":
    raise RuntimeError("Structure inattendue : " + str(REPERTOIRE_OUTIL))
REPERTOIRE_MATRICE = REPERTOIRE_OUTIL.parent.parent.parent
if REPERTOIRE_MATRICE.name != "matrice":
    raise RuntimeError("Structure inattendue : " + str(REPERTOIRE_MATRICE))
REPERTOIRE_MATRIX = REPERTOIRE_MATRICE.parent
if REPERTOIRE_MATRIX.name != "matrix":
    raise RuntimeError("Structure inattendue : " + str(REPERTOIRE_MATRIX))

# data/commun (motif unique M-076) : le dossier PARTAGE est installe dans
# sys.path. C'est lui qui porte le parseur d'options (jamais recopie) et
# sac_a_dos (l'enveloppe qui note l'usage) -- sans cette ligne, l'outil
# s'importe dans un cobaye mais ECHOUE au lancement reel (defaut trouve par
# la preuve d'integration de MO-224).
sys.path.insert(0, str(REPERTOIRE_MATRICE / "data" / "commun"))

ENCODAGE = "utf-8"

# DOMICILE (arbitrage A1) : l'espace PREPARATION -- INVISIBLE du cameleon (L-016),
# car un pense-bete porte les mots du createur et ses arbitrages.
DOMICILE_RELATIF = "_operateur/optimus-prime/preparation"
REPERTOIRE_DOMICILE = REPERTOIRE_MATRIX / DOMICILE_RELATIF

# La PORTE unique d'ecriture : cette porte ne fabrique JAMAIS un fichier
# elle-meme, elle CONSOMME le passage oblige (regle du cerveau).
# EO-287 : le NOM suffit -- la resolution (et son refus nomme) est PARTAGEE
# (data/commun/resolution_outils.py), jamais recopiee ici.
NOM_PORTE_ECRIRE = "ecrire"

# LES TROIS ETAPES et les TROIS familles d'ids (arbitrage C).
ETAPE_PENSE_BETE = "pense-bete"
ETAPE_SPEC = "spec"
ETAPE_TODO = "todo"
ETAPES = (ETAPE_PENSE_BETE, ETAPE_SPEC, ETAPE_TODO)
PREFIXES = {ETAPE_PENSE_BETE: "PB", ETAPE_SPEC: "SP", ETAPE_TODO: "TD"}
CHAMPS_ETAPE = {ETAPE_PENSE_BETE: "pense-bete:", ETAPE_SPEC: "spec:", ETAPE_TODO: "todo:"}

# LA CARTE D'IDENTITE : les champs lus et poses (arbitrage B : nom STABLE, statut
# et ids DANS la carte).
CHAMP_STATUT = "statut:"
CHAMP_TITRE = "titre:"
CHAMP_NEMESIS = "nemesis:"
MARQUEURS_NEMESIS = ("NEMESIS", "CONTRE-ANALYSE")
SEPARATEUR_CARTE = "---"

# CONDITIONS DE L'AVANCEMENT (arbitrage D) : la porte avance QUAND elles tiennent.
MIN_LIGNES_CORPS = 5
NEMESIS_EXIGE_A_PARTIR_DE = ETAPE_SPEC
STATUT_INITIAL = ETAPE_PENSE_BETE

# FICHIERS du domicile.
NOM_INDEX = "index-chaine.md"
NOM_COMPTEURS = "chaine-compteurs.json"
EXTENSION = ".md"
FORMAT_NUMERO = "{:03d}"

# MESSAGES DITS (jamais un silence).
MESSAGE_NAISSANCE = "PENSE-BETE cree : "
MESSAGE_AVANCE = "ETAPE FRANCHIE : "
MESSAGE_INDEX = "index mis a jour : "
REFUS_NEMESIS = "REFUS : la trace NEMESIS manque (champ nemesis: ET marqueur dans le corps) -- le nemesis est une CONDITION, pas une promesse"
REFUS_STRUCTURE = "REFUS : structure insuffisante : il faut au moins " + str(MIN_LIGNES_CORPS) + " lignes de corps"
REFUS_DERNIERE = "REFUS : l'objet est deja au dernier etat (todo-list)"
REFUS_INTROUVABLE = "REFUS : aucun document de la chaine pour cet id : "
REFUS_HORS_PERIMETRE = "REFUS : le domicile de la chaine est introuvable : "
