"""Constantes de la routine veille-flux : chemins, etats, combos.

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
Racine (pattern v1) : DETECTEE en remontant jusqu'au dossier contenant AGENTS.md.
"""
import os
import sys
from pathlib import Path

REPERTOIRE_ROUTINE = Path(__file__).resolve().parent
REPERTOIRE_PARENT = REPERTOIRE_ROUTINE.parent
if REPERTOIRE_PARENT.name != "routines" or REPERTOIRE_PARENT.parent.name != "matrice":
    raise RuntimeError(
        "Structure inattendue : "
        + str(REPERTOIRE_ROUTINE)
        + " n'est pas dans matrice/routines/"
    )


# data/commun (motif unique M-076) : le motif racine est PARTAGE, jamais recopie.
sys.path.insert(0, str(REPERTOIRE_PARENT.parent / "data" / "commun"))
from lancement import delai_sous_processus  # noqa: E402
from racine import detecter_racine  # noqa: E402

RACINE = detecter_racine(REPERTOIRE_ROUTINE)
REPERTOIRE_MATRIX = RACINE / "cerveau-projet" / "matrix"

# Les combos de la veille (chemins des outils Python de la Matrice).
CHEMIN_CORRIGER_ASCII = REPERTOIRE_MATRIX / "matrice" / "data" / "outils" / "corriger-ascii"
CHEMIN_VERIFIER_CONVENTIONS = (
    REPERTOIRE_MATRIX / "matrice" / "data" / "outils" / "verifier-conventions"
)
CHEMIN_VERIFIER_REGLES = REPERTOIRE_MATRIX / "matrice" / "data" / "outils" / "verifier-regles"
CHEMIN_VERIFIER_PROTOCOLES = (
    REPERTOIRE_MATRIX / "matrice" / "data" / "outils" / "verifier-protocoles"
)
CHEMIN_ESPION = REPERTOIRE_MATRIX / "matrice" / "routines" / "espion-integrite"

# Les 3 verifiers du marbre (nom lisible -> chemin de l'outil).
VERIFIERS_MARBRE = (
    ("conventions", CHEMIN_VERIFIER_CONVENTIONS),
    ("regles", CHEMIN_VERIFIER_REGLES),
    ("protocoles", CHEMIN_VERIFIER_PROTOCOLES),
)

# Base des caracteres acceptes (decision du createur) : derives du scan
# corriger-ascii, pre-graves a la construction (voir base-acceptee.json).
CHEMIN_BASE = REPERTOIRE_ROUTINE / "base-acceptee.json"

# Boite intercom pour les alertes graves.
CHEMIN_BOITE_MATRICE_IN = REPERTOIRE_MATRIX / "matrice" / "intercom" / "matrice" / "inbox.jsonl"

# Boucle : PID, drapeau d'arret, intervalle, journal, etat des alertes.
NOM_PID = "veille-flux.pid"
NOM_DRAPEAU_ARRET = "veille-flux.arret"
NOM_JOURNAL = "journal-veille.txt"
# Rotation du journal (MO-078) : le PLUS GROS des quatre journaux de la Matrice
# (mesure 2026-09-13 : 3,85 Mo / 44 050 lignes, croissant d'environ 0,5 Mo par
# jour, aucune borne). Le moteur est PARTAGE (data/commun/rotation_journal.py),
# la veille ne declare que SES valeurs. Les seuils sont en CONSTANTES : le
# declenchement se LIT (une taille), jamais une valeur en dur dans la logique.
NOM_ARCHIVE_PREFIXE = "journal-veille-archive"
SEUIL_OCTETS_JOURNAL = 2 * 1024 * 1024
EVENEMENTS_GARDES_JOURNAL = 5000
ESSAIS_ROTATION = 3
CHEMIN_RELATIF_JOURNAL = Path("matrice") / "routines" / "veille-flux" / NOM_JOURNAL
NOM_ETAT_ALERTES = "alertes-emises.json"
INTERVALLE_SECONDES = 300
# Nom CANONIQUE de la cadence declaree, lu par `vie etat` : on LIT la cadence
# au lieu de l'attendre (attendre n'est pas verifier). Meme valeur, meme objet.
INTERVALLE_DECLARE_SECONDES = INTERVALLE_SECONDES
PAUSE_REPRISE_SECONDES = 2

# Garde anti-blocage des sous-processus (E-045) : un combo qui depasse ce
# delai est tue et l'incident est journalise -- la boucle ne pend jamais.
# MO-102 (P5 de la revue MO-098) : la valeur n'est plus ecrite ici -- elle est
# LUE chez son proprietaire (data/commun/lancement.py, le module qui lance les
# sous-processus). Une seule source pour toute la Matrice.
TIMEOUT_COMBO_SECONDES = delai_sous_processus()

# Garde Windows (MO-035) : la ligne de commande Windows est plafonnee (~32767
# caracteres). Compiler les 352 .py de matrix/ en UNE commande depassait la
# limite (WinError 206) : l'exception tuait la passe entre passe-debut et
# passe-fin, le serveur relancait la routine chaque minute et la veille est
# restee MORTE du 2026-09-12 22:23:39 au 2026-09-13 09:2x sans le dire.
# Donc compilation par LOTS (le contrat d'extraction des fichiers en erreur
# ne change pas : les sorties de lots sont concatenees).
# MO-097 : le lot n'est plus un NOMBRE de fichiers mais un budget de LONGUEUR de
# ligne de commande -- la contrainte REELLE. 40 etait un plancher tres prudent :
# 435 .py donnaient 11 lots, donc 11 demarrages d'interpreteur (~460 ms de pure
# tare sur une passe mesuree a 1739 ms, pour 1406 ms de py_compile). Le budget
# reste TRES en dessous du plafond Windows, avec un plafond de securite en
# nombre (un chemin anormalement long ne part jamais seul au-dela du budget).
LONGUEUR_MAX_COMMANDE = 20000
LOT_PY_COMPILE_MAX = 250

# Budget DECLARE d'une passe, en millisecondes (MO-097) : la routine reste la
# SEULE voix de son budget, et elle le PUBLIE dans son etat court
# (veille-cadence.json) pour que le cockpit le LISE au lieu de comparer a un
# seuil en dur. Mesures du 2026-09-15 : passe relax 1739 ms AVANT optimisation
# (corriger-ascii 341 ms + py_compile 1406 ms), ~1,2 s APRES ; budget declare
# avec marge, pour crier sur une DERIVE et non sur le cout normal du contrat
# (compilation GLOBALE des .py, cf. DESCRIPTION de la routine).
BUDGET_PASSE_MS = 2000

# Notation de chaque passe dans la BDD usages-outils-combos (outil bdd-usages).
CHEMIN_BDD_USAGES = REPERTOIRE_MATRIX / "matrice" / "data" / "outils" / "bdd-usages"
TAGS_PASSE = "veille-flux,passe,auto"

# Depot de chaque passe dans la section passes des activites-recentes (bdd-activites).
CHEMIN_BDD_ACTIVITES = REPERTOIRE_MATRIX / "matrice" / "data" / "outils" / "bdd-activites"
SECTION_PASSES = "passes"

# Depot d'une mission-reparation au VRAC de l'entonnoir d'OPTIMUS (M-020) : une
# alerte y verse automatiquement sa mission (urgence bloquante -- aligne sur
# entonnoir/listes.py).
# PERIMETRE : la veille est une routine de la MATRICE ; ses alertes partent deja
# vers la maintenance (porte `signaler` -> routeur-maintenance -> maintien par
# Optimus). Son entonnoir est donc celui d'OPTIMUS.
# Corrige : elle visait `matrice/pilote/entonnoir`, c'est-a-dire l'entonnoir du
# CAMELEON. Preuve : E-090 (source `veille`, deposee le 2026-09-13 14:32:04) a
# ete retrouvee dans le vrac du cameleon, alors que le vrac d'Optimus est reste
# VIDE (0 item) -- l'automate nourrissait le mauvais flux.
CHEMIN_ENTONNOIR = REPERTOIRE_MATRIX / "_operateur" / "optimus-prime" / "pilote" / "entonnoir"
URGENCE_VEILLE = "bloquante"
THEME_REPARATION = "reparer"

# Porte OFFICIELLE d'alerte : l'UNIQUE voie d'ecriture dans l'inbox Matrice.
# Deux consommateurs lisent cette boite et ne routent QUE `type == "signaler"` :
# routeur-maintenance (vers la maintenance) puis maintenir (vers Optimus).
# Une ecriture directe d'un autre type est une PORTE PIRATE : elle finit en
# `ignores` anonymes et n'atteint jamais personne.
CHEMIN_SIGNALER = REPERTOIRE_MATRIX / "matrice" / "data" / "outils" / "signaler"

# Identite du signal : le signal doit dire la VERITE sur qui parle.
EXPEDITEUR_SIGNAL = "routine"
OUTIL_SIGNAL = "veille-flux"
MISSION_SIGNAL = "VEILLE-FLUX"

# Niveau d'un etat. Un incident de l'OUTILLAGE passe avant un fichier qui ne
# compile pas : quand l'outil est aveugle, on ne voit plus rien du tout.
NIVEAU_PAR_ETAT = {
    "incident-combo": "critique",
    "incident-py-compile": "critique",
    "python-compile": "haute",
    "ascii-non-convertible": "haute",
    "marbre": "haute",
}
NIVEAU_DEFAUT = "haute"

# Etats REELLEMENT re-testes par une passe : une signature dont l'etat est
# re-teste et qui n'est PAS re-detectee est RESOLUE (on la purge).
# Sans cela le garde-fou d'anti-spam devient un piege : une signature
# `ascii-non-convertible:U+XXXX` dont le caractere a disparu du disque restait
# "vivante" POUR TOUJOURS (5 des 9 signatures de l'etat) et bloquait
# silencieusement toute alerte future du meme caractere.
# ATTENTION : `marbre` n'est teste qu'en mode VIGILE. Le purger sur une passe
# RELAX relancerait l'alerte a chaque passe VIGILE (fausse boucle).
ETATS_TESTES = {
    "relax": ("ascii-non-convertible", "incident-combo", "incident-py-compile", "python-compile"),
    "vigile": ("ascii-non-convertible", "incident-combo", "incident-py-compile", "python-compile", "marbre"),
}

# Etat COURT : la cadence EFFECTIVE du demarrage en cours. Elle ne peut PAS vivre
# seulement dans le journal (le journal est rotationne : l'evenement de demarrage
# finit dans l'archive, et le controle de cadence deviendrait aveugle -- L-040).
NOM_CADENCE = "veille-cadence.json"
CHEMIN_CADENCE = REPERTOIRE_ROUTINE / NOM_CADENCE
CHEMIN_PID = REPERTOIRE_ROUTINE / NOM_PID
CHEMIN_DRAPEAU_ARRET = REPERTOIRE_ROUTINE / NOM_DRAPEAU_ARRET
CHEMIN_JOURNAL = REPERTOIRE_ROUTINE / NOM_JOURNAL
CHEMIN_ETAT_ALERTES = REPERTOIRE_ROUTINE / NOM_ETAT_ALERTES

# Lecture BORNEE de la queue d'un journal : une surveillance se lit dans les
# DERNIERS evenements, jamais dans tout l'historique (mesure MO-077 : 0,154 s
# de balayage complet contre 0,001 s bornes). La FENETRE ne se declare plus ici
# (MO-099) : elle vit dans le moteur PARTAGE (data/commun/rotation_journal.py),
# qui la DEDUIT de SEUIL_OCTETS_JOURNAL ci-dessus -- cette copie n'avait AUCUN
# lecteur (valeur morte, meme classe que le py_compile_ms de la revue MO-098).

ENCODAGE = "utf-8"


def chemin_python():
    """Retourne l'executable python du processus courant (pour les sous-processus)."""
    return sys.executable or "python"


def env_console_sure():
    """Retourne l'environnement console-sure pour les sous-processus (cp1252).

    PYTHONIOENCODING au format valide "encodage:erreurs" (un seul mot "replace"
    est un nom d'encodage invalide : le Python fils meurt a l'init_stdio_encoding).
    """
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8:replace"
    return env
