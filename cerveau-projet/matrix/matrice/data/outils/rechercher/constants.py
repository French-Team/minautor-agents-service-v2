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

# --- LECTURE D UNE REQUETE : MOTIF OU LANGAGE NATUREL (MO-375) ---------------
# MESURE D ORIGINE (MO-368, audit-moteur-et-cartes.md) : la requete etait compilee
# comme UN SEUL motif regex, donc une phrase qui n existe pas LITTERALEMENT rendait
# 0 -- 5 zeros sur 12 requetes REELLES, et ces 5 zeros sont TOUS des requetes a
# plusieurs mots. Le moteur tolere desormais le langage naturel : les mots vides
# sont RETIRES (a leur domicile : data/commun/recherche_mission.py) et le PLURIEL
# est tolere ; les termes restants sont lies en ET.
#
# Un METACARACTERE de motif change le SENS de la requete : une requete qui porte
# la FORME d un motif reste un motif, employe TELLE QUELLE (le contrat historique
# < regex supportee >). Un texte ne se decoupe que s il n en porte pas la forme.
# Chaine BRUTE (prefixe r) : l antislash est un METACARACTERE, pas un echappement.
CARACTERES_MOTIF = r".^$*+?{}[]\|()"
# Le PLURIEL tolere : un s ou un x final est FACULTATIF dans le motif d un terme
# (un terme au singulier trouve le pluriel du corpus, et l inverse). La base du
# motif est le terme prive de ce s ou de ce x final.
FIN_PLURIEL = ("s", "x")
SUFFIXE_PLURIEL = "[sx]?"

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

# --- SOURCES JSON PRIVEES (L-016, MO-482) ------------------------------------
# DECLAREES une a une (jamais une liste ouverte) : nom de source -> chemin RELATIF
# a la racine `matrix/`, dans la ZONE INVISIBLE. Elles ne se servent QUE sous
# `--prive` (la fenetre privee d Optimus), JAMAIS au cameleon. La BDD de
# raisonnement d Optimus vit ici (une BDD par agent -- decision createur 2026-09-27).
BDD_SOURCES_PRIVEES = {
    "segments": "_operateur/optimus-prime/raisonnement/segments.json",
}

# --- SOURCES JSON PARTAGEES, HORS data/ (decision createur 2026-09-27) ------
# DECLAREES une a une (jamais une liste ouverte) : nom de source -> chemin RELATIF
# a la racine `matrix/`. Elles sont VISIBLES et servies SANS `--prive` : c est la
# BDD de raisonnement du CAMELEON, PARTAGEE entre les deux agents (elle vit dans
# le domicile du cameleon, mais aucun agent n est exclu de sa lecture -- decision
# createur 2026-09-27 : la BDD du cameleon est partagee dans la Matrice).
BDD_SOURCES_PARTAGEES = {
    "segments-cameleon": "agents/cameleon/raisonnement/segments-cameleon.json",
}

# --- BDD SQLite : DECOUVERTE AUTOMATIQUE (exception assumee, data-readme 2026-09-26) --
# Une BDD SQLite n est plus DECLAREE une a une : le moteur DECOUVRE les bases de
# DOSSIER_SQLITE, enumere leurs TABLES (sqlite_master) et les sert. Le NOM de la
# source est le STEM du fichier (frictions.db -> frictions). Le nom de la table
# n est donc plus un domicile a maintenir : il se LIT sur la base.
DOSSIER_SQLITE = REPERTOIRE_DATA
EXTENSIONS_SQLITE = (".db", ".sqlite", ".sqlite3")
# Un INDEX n est pas une BDD : ces fichiers sont ECARTES de la decouverte, sinon
# l index du moteur (palier 2) se servirait comme une source de hits.
FICHIERS_SQLITE_EXCLUS = ("index-recherche.sqlite",)
# POLITIQUE DE PUBLICATION (L-016) : une BDD SQLite DECOUVERTE est PRIVEE par
# DEFAUT -- le defaut ne s ouvre JAMAIS tout seul (meme doctrine que les zones
# invisibles). Un STEM liste ici est PUBLIC (servi sans --prive). Vide aujourd hui :
# frictions n appartient qu a l Operateur. Publier une base est donc un ACTE
# explicite, jamais une consequence automatique de sa decouverte.
SQLITE_PUBLIQUES = ()

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

# `--lien` : rendre les DOCUMENTS dont la carte DECLARE un chemin donne (le graphe
# des liens -- demande createur du 2026-09-23). `--champ` ne peut PAS le faire : il
# compare la VALEUR ENTIERE d un champ, or `liens: a, b` est une LISTE -- comparee
# a "a" elle ne correspond jamais (mesure du 2026-09-23 : 0 carte sur 113 ne
# declaraient un lien, et le moteur ne savait pas l interroger). La regle reste au
# DOMICILE de la grammaire (carte_identite.liens_de_carte) : cette porte la CONSOMME.
NOM_OPTION_LIEN = "lien"

NOMS_OPTIONS_RECHERCHER = ("requete", "dans", "tag", "mot-cle", "source", "periode",
                           NOM_OPTION_CHAMP, NOM_OPTION_LIEN, NOM_OPTION_JSON, NOM_OPTION_PRIVE, "limite")
NOMS_OPTIONS_INDEXER = ("forcer",)
