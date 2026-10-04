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

# LES ETAPES et les FAMILLES d'ids (arbitrage C, etat d execution ajoute en MO-577
# sur decision createur : la chaine suivait la PRODUCTION d un document, jamais
# l ACCOMPLISSEMENT d un travail).
ETAPE_PENSE_BETE = "pense-bete"
ETAPE_SPEC = "spec"
ETAPE_TODO = "todo"
# L ETAT D EXECUTION (MO-577, decision createur : un 4e etat, mais CONDITIONNE A UNE
# PREUVE). Mesure de MO-538 : les trois etapes modelisent la PRODUCTION d un document,
# pas l ACCOMPLISSEMENT d un travail. Les quatre objets de la chaine sont tous bloques
# a `todo` alors que leurs quatre taches sont livrees sur le disque -- PB-003 en
# particulier, dont la todo-list porte T1..T4, toutes presentes.
#
# LA PREUVE EST LA CONDITION (arbitrage createur). Un `execute` pose sans fait atteste
# serait une DECLARATION : c est exactement le vice que le controle d attribution
# accuse, et que la famille des vues vient d interdire. Donc `executer` refuse tant
# que la preuve n est pas NOMMEE et VERIFIEE sur le disque -- fichier existant et non
# vide. La porte CONSTATE un fait ; elle ne juge pas l accomplissement.
#
# LA FAMILLE `EX` EST REELLE, pas cosmetique : `verifier-chaines.py` lit le champ
# d une etape comme un IDENTIFIANT et verifie qu il commence par le prefixe de sa
# famille et que son numero ne depasse pas son compteur. Un `execute:` sans famille
# ni compteur ferait passer chaque objet de la chaine en ecart.
ETAPE_EXECUTE = "execute"
PREFIXE_EXECUTE = "EX"
# CE QUE `avancer` PARCOURT. Les trois premieres etapes sont une PRODUCTION de
# documents ; l execution a son propre verbe et sa propre condition. `avancer` ne
# franchit donc JAMAIS `todo` : un raccourci sans preuve serait l exact defaut qu on
# repare.
ETAPES_AVANCEMENT = (ETAPE_PENSE_BETE, ETAPE_SPEC, ETAPE_TODO)
# LA PREUVE : un chemin de fichier, constate sur le disque au moment du verbe.
CHAMP_PREUVE = "preuve:"
# LA DATE : prise par la PORTE, jamais demandee a l appelant (une date ecrite par
# l appelant est une affirmation, pas une mesure).
CHAMP_EXECUTE_LE = "execute le:"

ETAPES = (ETAPE_PENSE_BETE, ETAPE_SPEC, ETAPE_TODO, ETAPE_EXECUTE)

PREFIXES = {ETAPE_PENSE_BETE: "PB", ETAPE_SPEC: "SP", ETAPE_TODO: "TD",
            ETAPE_EXECUTE: PREFIXE_EXECUTE}
CHAMPS_ETAPE = {ETAPE_PENSE_BETE: "pense-bete:", ETAPE_SPEC: "spec:",
               ETAPE_TODO: "todo:", ETAPE_EXECUTE: ETAPE_EXECUTE + ":"}

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

# LES MESSAGES DU VERBE D EXECUTION (MO-577). Un refus nomme ce qui MANQUE : une preuve
# non nommee et une preuve introuvable ne sont pas le meme refus, et le second se
# distingue du troisieme (un fichier la, mais vide).
REFUS_PREUVE_NON_NOMMEE = "REFUS : une preuve est requise -- un execute sans fait atteste est une DECLARATION ; nomme le fichier qui prouve le travail (--preuve <chemin>)"
REFUS_PREUVE_INTROUVABLE = "REFUS : la preuve nommee est introuvable sur le disque : "
REFUS_PREUVE_VIDE = "REFUS : la preuve nommee existe mais est VIDE -- un fichier sans contenu ne prouve rien : "
REFUS_PAS_TODO = "REFUS : l objet n est pas au statut todo : il est a \""
REFUS_TODO_ABSENT = "REFUS : l objet n porte aucun id de todo-list : rien n a ete produit, donc rien n peut etre execute"
REFUS_PAS_EXECUTE = "REFUS : l objet n est pas execute : il est a \""
# LE REFUS DE `revenir` DIT LE SENS DU VERBE. Mesure du 2026-10-04 : il
# empruntait celui de `executer` -- qui annoncait 'il est a todo' sur un verbe
# dont la condition est l INVERSE. Un refus juste ici et faux la-bas.
REFUS_DEJA_EXECUTE = "REFUS : l objet est deja execute (le "
MESSAGE_EXECUTE = "TRAVAIL CONSTATE : "
MESSAGE_RETOUR = "RETOUR A TODO : "

# MESSAGES DITS (jamais un silence).
MESSAGE_NAISSANCE = "PENSE-BETE cree : "
MESSAGE_AVANCE = "ETAPE FRANCHIE : "
MESSAGE_INDEX = "index mis a jour : "
REFUS_NEMESIS = "REFUS : la trace NEMESIS manque (champ nemesis: ET marqueur dans le corps) -- le nemesis est une CONDITION, pas une promesse"
REFUS_STRUCTURE = "REFUS : structure insuffisante : il faut au moins " + str(MIN_LIGNES_CORPS) + " lignes de corps"
REFUS_DERNIERE = "REFUS : l'objet est deja au dernier etat (todo-list)"
REFUS_INTROUVABLE = "REFUS : aucun document de la chaine pour cet id : "
REFUS_HORS_PERIMETRE = "REFUS : le domicile de la chaine est introuvable : "
