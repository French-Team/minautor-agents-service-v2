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
NOM_ETAT_ALERTES = "alertes-emises.json"
INTERVALLE_SECONDES = 300
PAUSE_REPRISE_SECONDES = 2

# Garde anti-blocage des sous-processus (E-045) : un combo qui depasse ce
# delai est tue et l'incident est journalise -- la boucle ne pend jamais.
TIMEOUT_COMBO_SECONDES = 120

# Notation de chaque passe dans la BDD usages-outils-combos (outil bdd-usages).
CHEMIN_BDD_USAGES = REPERTOIRE_MATRIX / "matrice" / "data" / "outils" / "bdd-usages"
TAGS_PASSE = "veille-flux,passe,auto"

# Depot de chaque passe dans la section passes des activites-recentes (bdd-activites).
CHEMIN_BDD_ACTIVITES = REPERTOIRE_MATRIX / "matrice" / "data" / "outils" / "bdd-activites"
SECTION_PASSES = "passes"

# Depot d'une mission-reparation au VRAC de l'entonnoir (M-020) : une alerte-grave
# y verse automatiquement sa mission (urgence bloquante -- aligne sur entonnoir/listes.py).
CHEMIN_ENTONNOIR = REPERTOIRE_MATRIX / "matrice" / "pilote" / "entonnoir"
URGENCE_VEILLE = "bloquante"
THEME_REPARATION = "reparer"

CHEMIN_PID = REPERTOIRE_ROUTINE / NOM_PID
CHEMIN_DRAPEAU_ARRET = REPERTOIRE_ROUTINE / NOM_DRAPEAU_ARRET
CHEMIN_JOURNAL = REPERTOIRE_ROUTINE / NOM_JOURNAL
CHEMIN_ETAT_ALERTES = REPERTOIRE_ROUTINE / NOM_ETAT_ALERTES

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
