"""Constantes de l'activateur de vie de la Matrice.

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
"""
import sys
from pathlib import Path

from constants_suivi_sync import BOUCLES_SUIVI_SYNC
from constants_verifier_liens_cartes import BOUCLES_VERIFIER_LIENS_CARTES
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
    # LE CHIEN (MO-564, demande createur du 2026-10-03) : le declencheur sur
    # changement. Il est en BOUCLE et non en `passe` pour une raison mesuree : sa
    # cadence est de 20 s, donc un mode `passe` demarrerait un processus 4 320 fois
    # par jour pour regarder 990 fichiers. Une seule boucle qui dort -- en tranches
    # de 2 s, drapeau d arret vu en 2 s -- fait le meme travail dans un processus.
    ("chien", REPERTOIRE_ROUTINES / "chien"),
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
    + list(BOUCLES_VERIFIER_LIENS_CARTES)
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
    "verifier-liens-cartes": ("main.py", ("--boucle",), None),
    # LE CHIEN (MO-564) : mode BOUCLE, donc COMMANDE_PAR_NOM le lance en boucle
    # comme les autres. Mesure du 2026-10-03 : sans cette entree, la boucle de
    # relance du serveur tape une KeyError sur COMMANDE_PAR_NOM["chien"] et le
    # chien reste ARRET pour toujours -- c'est ce que la non-regression accusait
    # (< aucun PID >). Mesure aussi : la cadence est ILLISIBLE parce que
    # CADENCE_PAR_NOM ne le declarait pas non plus. Une routine declaree a moitie
    # (BOUCLES + PID) n'est pas une routine declaree.
    "chien": ("main.py", ("--boucle",), None),
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
    "routeur-maintenance": ("constants.py", "INTERVALLE_DECLARE_SECONDES"),
    "verifier-liens-cartes": ("constants.py", "INTERVALLE_DECLARE_SECONDES"),
    "chien": ("constants.py", "INTERVALLE_DECLARE_SECONDES"),
}

NOM_PID_VEILLE = "veille-flux.pid"
NOM_PID_ESPION = "espion.pid"
NOM_PID_SUIVI_SYNC = "suivi-sync.pid"
NOM_PID_VIGIE_PROFIL = "vigie-profil.pid"
NOM_PID_VIGIE_PORTES = "vigie-portes.pid"
NOM_PID_ROUTEUR = "routeur.pid"
NOM_PID_VERIFIER_LIENS_CARTES = "verifier-liens-cartes.pid"
NOM_PID_CHIEN = "chien.pid"
NOMS_PID = (
    NOM_PID_VEILLE, NOM_PID_ESPION, NOM_PID_SUIVI_SYNC, NOM_PID_VIGIE_PROFIL, NOM_PID_VIGIE_PORTES,
    NOM_PID_ROUTEUR,
    NOM_PID_VERIFIER_LIENS_CARTES,
    NOM_PID_CHIEN,
)

NOM_DRAPEAU_VEILLE = "veille-flux.arret"
NOM_DRAPEAU_ESPION = "boucle-arret.txt"
NOM_DRAPEAU_SUIVI_SYNC = "suivi-sync.arret"
NOM_DRAPEAU_VIGIE_PROFIL = "vigie-profil.arret"
NOM_DRAPEAU_VIGIE_PORTES = "vigie-portes.arret"
# Le drapeau du routeur porte l'extension `.flag` (choix de sa propre boucle,
# dans routeur.py) : la table unique doit dire la VERITE sur son nom reel.
NOM_DRAPEAU_ROUTEUR = "routeur-arret.flag"
NOM_DRAPEAU_VERIFIER_LIENS_CARTES = "verifier-liens-cartes.arret"
NOM_DRAPEAU_CHIEN = "chien.arret"
NOMS_DRAPEAUX = (
    NOM_DRAPEAU_VEILLE,
    NOM_DRAPEAU_ESPION,
    NOM_DRAPEAU_SUIVI_SYNC,
    NOM_DRAPEAU_VIGIE_PROFIL,
    NOM_DRAPEAU_VIGIE_PORTES,
    NOM_DRAPEAU_ROUTEUR,
    NOM_DRAPEAU_VERIFIER_LIENS_CARTES,
    NOM_DRAPEAU_CHIEN,
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
    "verifier-liens-cartes": NOM_PID_VERIFIER_LIENS_CARTES,
    "chien": NOM_PID_CHIEN,
}
DRAPEAU_PAR_NOM = {
    "veille-flux": NOM_DRAPEAU_VEILLE,
    "espion-integrite": NOM_DRAPEAU_ESPION,
    "suivi-sync": NOM_DRAPEAU_SUIVI_SYNC,
    "vigie-profil": NOM_DRAPEAU_VIGIE_PROFIL,
    "vigie-portes": NOM_DRAPEAU_VIGIE_PORTES,
    "routeur-maintenance": NOM_DRAPEAU_ROUTEUR,
    "verifier-liens-cartes": NOM_DRAPEAU_VERIFIER_LIENS_CARTES,
    "chien": NOM_DRAPEAU_CHIEN,
}

NOM_SERVER = "server_matrice.py"
NOM_PID_SERVER = "server-matrice.pid"
NOM_DRAPEAU_SERVER = "server-matrice-arret.txt"

ENCODAGE = "utf-8"


# --- SERVICE DU PLANNING (MO-429, decisions createur D1 a D5, 2026-09-26) ----
# Le service est le SEUL resident : il ALLUME les routines de mode passe (leur
# commande vient du planning), il RECOIT leur resultat (code retour, trace de
# lancement, passe publiee), il TRANSFORME un ecart en MESSAGE (porte signaler)
# -- niveaux DECLARES ici, jamais dans la logique (zero valeur en dur).
REPERTOIRE_MATRICE = REPERTOIRE_ROUTINES.parent
REPERTOIRE_MATRIX = REPERTOIRE_MATRICE.parent

# L ETAT du service (forme d etat de routine : <nom>-etat*.json, MOTIF_ETAT du
# controle d attribution). ECRITURE ATOMIQUE : tmp puis remplacement, LF.
NOM_ETAT_SERVICE = 'vie-service-etat.json'
CHEMIN_ETAT_SERVICE = REPERTOIRE_ACTIVATEUR / NOM_ETAT_SERVICE
SUFFIXE_TMP_SERVICE = '.tmp'

# POLITIQUE D ALLUMAGE (declarations, pas des caches) :
#   - plafond d une passe : au-dela, l allumage est juge sans attendre (jamais
#     de pendaison du tour de service) ;
#   - plafond du tour : au plus MAX_ALLUMAGES_PAR_TOUR allumages par tour, dans
#     l ordre du planning (priorite decroissante) -- le pic des 7 reste evite.
#     La COUVERTURE est mesuree : la demande en regime etabli vaut ~3,6
#     allumages/min (routeur 30 s = 2, suivi-sync 60 s = 1, veille et espion
#     300 s = 0,4, deux vigies 900 s = 0,13, liens 3600 s = 0,02), soit un
#     plafond de 4 par tour (4/min). Avec 1, routeur (position 1) repoussait
#     TOUTES les autres a chaque tour : suivi-sync n etait plus servie au-dela
#     de sa tolerance de 3 cadences (famine accusee par le maillon 7).
#   - anti-spam : le meme probleme n est pas redit avant ce delai (en secondes
#     MURALES, comme les autres planchers -- la cadence reelle est decidee ici).
PLAFOND_PASSE_SECONDES = 120
MAX_ALLUMAGES_PAR_TOUR = 4
ANTI_SPAM_SERVICE_SECONDES = 900

# NIVEAUX DES MESSAGES (decision D4) : un fait, un niveau, declare une fois.
NIVEAU_PLANTAGE = 'critique'   # plantage a l allumage / traceback
NIVEAU_ECHEC = 'haute'         # code retour non nul : la passe a rate
NIVEAU_RETARD = 'haute'        # due mais aucune passe publiee, ou passe suspendue
# Sur le niveau CRITIQUE seul : montee defcon par la porte machine-defcon
# monter (D4b) -- niveau 4 = suivi des problemes a resoudre. Le nombre est
# DECLARE ici : il change a UN endroit.
NIVEAU_DEFCON_CRITIQUE = 4

# Le depot passe par la PORTE UNIQUE signaler (jamais d ecriture directe dans
# l inbox) ; l expediteur dit la VERITE : c est la Matrice qui parle.
EXPEDITEUR_SIGNAL = 'matrice'
CHEMIN_OUTIL_SIGNALER = REPERTOIRE_MATRICE / 'data' / 'outils' / 'signaler' / 'main.py'
CHEMIN_OUTIL_DEFCON = REPERTOIRE_MATRICE / 'data' / 'outils' / 'machine-defcon' / 'main.py'
CAUSE_TRACEBACK = 'Traceback (most recent call last)'

# Format UNIQUE des horodatages (meme convention que les routines) : le temps
# s ecrit a UN endroit, le service et les etats lisent la meme chose.
FORMAT_HORODATAGE = '%Y-%m-%d %H:%M:%S'

# --- LE JOURNAL DE LANCEMENT : DECLARE ET BORNABLE (EO-486) -------------------
# Le lanceur (data/commun/lancement.py) envoie la sortie de l enfant DANS son
# journal de lancement, et il le REECRIT a chaque lancement. Ce contrat tient
# pour une passe courte ; il est FAUX pour le serveur, dont la sortie
# s accumule pendant toute sa vie : 1 884 278 o mesures en deux heures, et la
# porte /sante en ECHEC (un fichier de routines sans borne que RIEN ne mesure).
# Trois valeurs DECLAREES, lues par la porte /sante et par le serveur :
#   NOM_JOURNAL + SEUIL_OCTETS_JOURNAL : le journal devient JUGEABLE (il cesse
#   d etre un angle mort) ; NOM_ARCHIVE_PREFIXE : le prefixe de ses archives.
# GARDES_JOURNAL_LANCEMENT : combien d evenements restent lisibles dans le
# journal actif apres une borne.
# LA BORNE EST POSSIBLE ICI, CONTRAIREMENT aux journaux des autres routines :
# le serveur TIENT son descripteur, donc il ne peut pas remplacer le fichier
# (mesure : os.replace rend WinError 5 sur un fichier tenu, le temoin passe).
# Il borne donc par SON descripteur -- voir rotation_journal.borner_journal_tenu.
NOM_JOURNAL = 'journal-lancement.log'
SEUIL_OCTETS_JOURNAL = 512 * 1024
NOM_ARCHIVE_PREFIXE = 'vie-journal-lancement-archive'
GARDES_JOURNAL_LANCEMENT = 200
CHEMIN_JOURNAL = REPERTOIRE_ACTIVATEUR / NOM_JOURNAL
# LES PRODUCTIONS DE LA ROUTINE (MO-534) : les fichiers qu elle ECRIT et qui ne
# sont NI ses etats courts de forme CONVENTIONNELLE (PID, drapeau d arret,
# etat, journal, cadence, planning : le controle d attribution les reconnait a
# leur FORME), ni un fichier ecrit a la main. Cette case est VIDE PARCE QUE C
# EST VRAI : mesure du 2026-10-03 sur cette routine, la seule chose qu elle
# ecrit est son PID, ses drapeaux, son etat court, son journal de lancement et
# son planning -- tous deja hors jugement par leur forme. Elle ne produit ni
# rapport, ni inventaire, ni memoria de passe. Elle ne DISAIT rien jusqu ici :
# une case ABSENTE et une case VIDE ne se distinguent pas pour le controle, qui
# pouvait prendre le silence pour une declaration oubliee. Le jour ou cette
# routine ecrira une production, c est ICI qu elle se declare, et le controle la
# lira sans qu une liste soit retouchee -- meme regle que les huit autres
# routines, dont `selecteur-flux` porte deja cette justification.
PRODUCTIONS = ()
