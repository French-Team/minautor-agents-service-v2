"""Constantes de l'activateur de vie de la Matrice.

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
"""
import sys
from pathlib import Path

from constants_suivi_sync import BOUCLES_SUIVI_SYNC
from constants_vigie_portes import BOUCLES_VIGIE_PORTES

REPERTOIRE_ACTIVATEUR = Path(__file__).resolve().parent
REPERTOIRE_ROUTINES = REPERTOIRE_ACTIVATEUR.parent
if REPERTOIRE_ROUTINES.name != "routines" or REPERTOIRE_ROUTINES.parent.name != "matrice":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_ACTIVATEUR) + " n'est pas dans matrice/routines/"
    )

# data/commun (motif unique M-076) : installe le dossier partage dans sys.path
# (lancement.py : lancement detache invisible du server et de l'activateur).
# vie/ est sous matrice/routines/ : data/commun se rejoint via matrice/data/commun.
CHEMIN_COMMUN = REPERTOIRE_ROUTINES.parent / "data" / "commun"
if not (CHEMIN_COMMUN / "racine.py").is_file():
    raise RuntimeError(
        "data/commun introuvable : " + str(CHEMIN_COMMUN) + " n'est pas le dossier partage attendu"
    )
sys.path.insert(0, str(CHEMIN_COMMUN))

# Les routines historiques du fond (nom lisible -> dossier de la routine).
BOUCLES_FOND = (
    ("veille-flux", REPERTOIRE_ROUTINES / "veille-flux"),
    ("espion-integrite", REPERTOIRE_ROUTINES / "espion-integrite"),
    ("vigie-profil", REPERTOIRE_ROUTINES / "vigie-profil"),
)

# Le routeur de maintenance : c'est le GARDE-FOU qui porte les signalements
# jusqu'a Optimus. Il n'etait PAS supervise -- donc mort depuis le 2026-09-12
# sans que personne ne le sache -- et 18 alertes (dont 10 graves) sont restees
# bloquees dans l'inbox. Un garde-fou qui ne tourne pas est un garde-fou absent.
BOUCLES_ROUTEUR = (("routeur-maintenance", REPERTOIRE_ROUTINES / "routeur-maintenance"),)

# LA liste des routines supervisees : assemblee ICI et NULLE PART ailleurs.
# Le server et l'etat l'IMPORTENT -- ils ne la reassemblent jamais (deux listes
# = deux verites : c'est ainsi que l'etat et le server ont pu diverger).
BOUCLES = tuple(
    list(BOUCLES_FOND) + list(BOUCLES_SUIVI_SYNC) + list(BOUCLES_VIGIE_PORTES) + list(BOUCLES_ROUTEUR)
)

# ORDRE DE LANCEMENT DE CHAQUE ROUTINE : UNE SEULE TABLE.
# Le server IMPORTE ces ordres, il ne les recopie plus (doctrine : deux tables
# = deux verites). Chaque entree = (script, arguments, option_intervalle) :
#   - script : le fichier a lancer (les routines historiques = main.py, le
#     routeur de maintenance = routeur.py -- c'est CE detail qui l'excluait de
#     la supervision quand le lanceur supposait main.py) ;
#   - option_intervalle : nom de l'option de cadence ; None = la routine ne
#     prend pas d'option, elle garde SON temps.
# ATTENTION : la CADENCE n'est PAS ici. Chaque routine declare SON temps dans
# ses propres constantes (voix unique) ; le server ne l'ecrase plus.
COMMANDE_PAR_NOM = {
    "veille-flux": ("main.py", ("veille", "--boucle"), "--intervalle"),
    "espion-integrite": ("main.py", ("boucle",), "--interval"),
    "vigie-profil": ("main.py", ("boucle",), "--interval"),
    "vigie-portes": ("main.py", ("boucle",), "--interval"),
    "suivi-sync": ("main.py", ("--boucle",), None),
    "routeur-maintenance": ("routeur.py", ("boucle",), None),
}

# OU LIRE la cadence declaree de chaque routine : la table ne RECOPIE aucune
# valeur, elle dit SEULEMENT ou elle est declaree (voix unique : la cadence vit
# chez la routine). `vie etat` s'en sert pour AFFICHER la cadence reelle -- on
# la LIT, on ne l'attend pas (attendre n'est pas verifier, 2026-09-13).
CADENCE_PAR_NOM = {
    "veille-flux": ("constants.py", "INTERVALLE_DECLARE_SECONDES"),
    "espion-integrite": ("constants.py", "INTERVALLE_DECLARE_SECONDES"),
    "vigie-profil": ("constants.py", "INTERVALLE_DECLARE_SECONDES"),
    "vigie-portes": ("constants.py", "INTERVALLE_DECLARE_SECONDES"),
    "suivi-sync": ("constants.py", "INTERVALLE_DECLARE_SECONDES"),
    "routeur-maintenance": ("routeur.py", "INTERVALLE_DECLARE_SECONDES"),
}

NOM_PID_VEILLE = "veille-flux.pid"
NOM_PID_ESPION = "espion.pid"
NOM_PID_SUIVI_SYNC = "suivi-sync.pid"
NOM_PID_VIGIE_PROFIL = "vigie-profil.pid"
NOM_PID_VIGIE_PORTES = "vigie-portes.pid"
NOM_PID_ROUTEUR = "routeur.pid"
NOMS_PID = (
    NOM_PID_VEILLE, NOM_PID_ESPION, NOM_PID_SUIVI_SYNC, NOM_PID_VIGIE_PROFIL, NOM_PID_VIGIE_PORTES,
    NOM_PID_ROUTEUR,
)

NOM_DRAPEAU_VEILLE = "veille-flux.arret"
NOM_DRAPEAU_ESPION = "boucle-arret.txt"
NOM_DRAPEAU_SUIVI_SYNC = "suivi-sync.arret"
NOM_DRAPEAU_VIGIE_PROFIL = "vigie-profil.arret"
NOM_DRAPEAU_VIGIE_PORTES = "vigie-portes.arret"
# Le drapeau du routeur porte l'extension `.flag` (choix de sa propre boucle,
# dans routeur.py) : la table unique doit dire la VERITE sur son nom reel.
NOM_DRAPEAU_ROUTEUR = "routeur-arret.flag"
NOMS_DRAPEAUX = (
    NOM_DRAPEAU_VEILLE,
    NOM_DRAPEAU_ESPION,
    NOM_DRAPEAU_SUIVI_SYNC,
    NOM_DRAPEAU_VIGIE_PROFIL,
    NOM_DRAPEAU_VIGIE_PORTES,
    NOM_DRAPEAU_ROUTEUR,
)

# UNE SEULE table nom -> PID / nom -> drapeau pour tout le monde (l'etat et le
# serveur l'IMPORTENT ; ils ne la recopient jamais : deux tables = deux verites).
PID_PAR_NOM = {
    "veille-flux": NOM_PID_VEILLE,
    "espion-integrite": NOM_PID_ESPION,
    "suivi-sync": NOM_PID_SUIVI_SYNC,
    "vigie-profil": NOM_PID_VIGIE_PROFIL,
    "vigie-portes": NOM_PID_VIGIE_PORTES,
    "routeur-maintenance": NOM_PID_ROUTEUR,
}
DRAPEAU_PAR_NOM = {
    "veille-flux": NOM_DRAPEAU_VEILLE,
    "espion-integrite": NOM_DRAPEAU_ESPION,
    "suivi-sync": NOM_DRAPEAU_SUIVI_SYNC,
    "vigie-profil": NOM_DRAPEAU_VIGIE_PROFIL,
    "vigie-portes": NOM_DRAPEAU_VIGIE_PORTES,
    "routeur-maintenance": NOM_DRAPEAU_ROUTEUR,
}

NOM_SERVER = "server_matrice.py"
NOM_PID_SERVER = "server-matrice.pid"
NOM_DRAPEAU_SERVER = "server-matrice-arret.txt"

ENCODAGE = "utf-8"
