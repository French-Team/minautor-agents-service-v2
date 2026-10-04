"""Constantes de l'espion-integrite : registre des BDD et valeurs de la boucle.

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
"""
import sys
from pathlib import Path

REPERTOIRE_ESPION = Path(__file__).resolve().parent
# L'espion vit dans routines/espion-integrite/ ; les BDD vivent dans data/.
REPERTOIRE_DATA = REPERTOIRE_ESPION.parent.parent / "data"
if REPERTOIRE_DATA.name != "data":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_DATA) + " n'est pas le dossier data/"
    )

# data/commun (motif unique M-076) : l'attente cooperative est PARTAGEE, jamais
# recopiee. Sans ce chemin, l'espion retombait sur `time.sleep(intervalle)` en
# un seul bloc : un arret demande attendait la cadence entiere (jusqu'a 900 s).
REPERTOIRE_COMMUN = REPERTOIRE_DATA / "commun"
if not (REPERTOIRE_COMMUN / "attente.py").is_file():
    raise RuntimeError(
        "Motif attente introuvable : " + str(REPERTOIRE_COMMUN / "attente.py")
    )
sys.path.insert(0, str(REPERTOIRE_COMMUN))

# Registre des BDD de la Matrice : nom -> faite (True) ou a construire (False).
BDDS = {
    "modifications-par-fichier.json": True,
    "historiques-missions.jsonl": True,
    "lecons.json": True,
    "classeur-variables.json": True,
    "usages-outils-combos.jsonl": True,
    "activites-recentes.json": True,
    "historique-bdd.jsonl": True,
    "vivier-themes.json": True,
    "defcon-historique.jsonl": True,
    "pauses-session-matrix.jsonl": True,
    "suivi-optimus.jsonl": True,
    "regles-matrice.json": True,
    "conventions-matrice.json": True,
    "protocoles-matrice.json": True,
    "sessions.json": True,
    "conservation.json": True,
    # LA BDD DES CORVEES (MO-416, 2026-09-25) : la phase < si j etais user >
    # consigne les taches ingrates, leur cout mesure et leur automatisation ;
    # elle s ecrit par la porte `bdd-corvees`, qui repose son empreinte etalon.
    "corvees.json": True,
    # LE REGISTRE DES OUTILS (EO-314, MO-316) : une BDD REGENEREE par
    # `registre-outils rafraichir`, qui repose son empreinte etalon a chaque
    # publication -- sans ce geste, l espion crierait a chaque rafraichissement.
    "registre-outils.json": True,
}
# NOTA (M-080) : session-matrix-etat.json n'est PAS surveillee -- c'est un
# fichier EPHEMERE qui n'existe QUE pendant une pause (pose par pause-session,
# supprime a la reprise). Sa presence variable serait un faux ECART permanent.

NOM_JOURNAL = "espion-log.jsonl"
CHEMIN_JOURNAL = REPERTOIRE_ESPION / NOM_JOURNAL
# FIN DE PASSE (maillon 3 de la non-regression du flux, MO-478) : le marqueur
# ecrit a CHAQUE passe. Le maillon lit ce fait ICI, chez la routine (M-076).
EVENEMENT_FIN_PASSE = "passe"
# TEMOIN DE CADENCE (MO-479) : le fait que `verifier-cadence` lit pour mesurer le
# BATTEMENT REEL, declare ICI (M-076) au lieu d etre recopie dans la table du garde.
# (genre, fichier, marqueur) : le fichier DESIGNE une constante du dossier (pas une
# valeur en double). Aucun temoin = la routine n est PAS mesuree, et le garde le DIT.
TEMOIN_CADENCE = ("journal", NOM_JOURNAL, "passe")
NOM_PID = "espion.pid"
CHEMIN_PID = REPERTOIRE_ESPION / NOM_PID
NOM_DRAPEAU_ARRET = "boucle-arret.txt"
CHEMIN_DRAPEAU_ARRET = REPERTOIRE_ESPION / NOM_DRAPEAU_ARRET

# Etat COURT de la routine (une ligne, ecrasee a chaque demarrage). La cadence
# EFFECTIVE vit ici, pas seulement dans le journal : une rotation deplace les
# evenements anciens du journal (dont le `demarrage`), et un controle qui lit la
# cadence dans le journal deviendrait AVEUGLE apres une rotation -- c'est-a-dire
# neutralise par le nettoyage qu'il surveille (lecon L-040). Un etat se lit dans
# un FICHIER D'ETAT, une histoire se lit dans un JOURNAL.
NOM_ETAT = "espion-etat.json"
CHEMIN_ETAT = REPERTOIRE_ESPION / NOM_ETAT

# --- Etat COURT du CONTROLE (MO-081) ----------------------------------------
# Le TABLEAU DES BDD SURVEILLEES tel que la derniere passe l'a vu (chapitre,
# etat, detail). Mesure du 2026-09-14 : la passe journalisait 14 observations --
# une par BDD -- MEME quand rien n'avait bouge : 504 134 observations pour
# 36 000 passes, 93 % du journal, et il fallait lire 14 lignes pour trouver la
# seule qui dise quelque chose.
# Or l'integrite d'une BDD est un ETAT : elle ne change pas entre deux passes.
# Le tableau part donc dans l'ETAT (ecrit a chaque passe, ECRASE) ; l'HISTOIRE ne
# recoit les observations que si le tableau CHANGE (un fait).
NOM_ETAT_BDDS = "espion-etat-bdds.json"
CHEMIN_ETAT_BDDS = REPERTOIRE_ESPION / NOM_ETAT_BDDS

# --- Rotation du journal (MO-077) -------------------------------------------
# Le journal est en AJOUT SEUL : rien ne s'y supprime jamais. Le borner, c'est
# DEPLACER ses evenements les plus anciens dans une archive DATEE.
# Mesure du 2026-09-13 : 87,7 Mo / 540 608 lignes en 8 jours (~11 Mo par jour,
# croissance lineaire, aucune rotation), et les suites qui le lisent balayaient
# tout l'historique a chaque execution.
REPERTOIRE_MATRIX = REPERTOIRE_ESPION.parent.parent.parent
if not (REPERTOIRE_MATRIX / "matrice").is_dir():
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_MATRIX) + " n'est pas la racine matrix/"
    )
NOM_REPERTOIRE = "espion-integrite"
CHEMIN_RELATIF_JOURNAL = Path("matrice") / "routines" / NOM_REPERTOIRE / NOM_JOURNAL
NOM_ARCHIVE_PREFIXE = "espion-log-archive"
# Seuil de declenchement : une TAILLE (le declenchement se lit d'un stat, sans
# ouvrir le fichier). Au-dela, on archive tout sauf les N derniers evenements.
SEUIL_OCTETS_JOURNAL = 8 * 1024 * 1024
EVENEMENTS_GARDES_JOURNAL = 5000
# Essais bornes de la rotation : la boucle et les appels a la demande ecrivent
# dans ce journal, donc une rotation peut etre prise de vitesse. On recommence
# (le journal n'a pas ete touche), et on REFUSE en le nommant si ca bouge encore.
ESSAIS_ROTATION = 3

# LA CADENCE VIT AU PLANNING (decision createur D1, 2026-09-26, MO-429) : ce
# fichier ne la CONTIENT plus, il la LIT a sa source partagee (motif unique
# M-076 : data/commun/planning_routines.py). Le nom CANONIQUE est conserve :
# vie etat, le serveur et les gardes lisent INTERVALLE_DECLARE_SECONDES.
from planning_routines import cadence_planning  # noqa: E402

INTERVALLE_DEFAUT_SECONDES = cadence_planning('espion-integrite')
# Lecture BORNEE d'un journal : les suites lisent la QUEUE, jamais 87 Mo (mesure
# avant/apres en mission MO-077). 256 Ko couvrent largement les derniers
# evenements d'une passe et l'evenement de demarrage. La FENETRE ne se declare
# plus ici (MO-099) : le moteur PARTAGE (data/commun/rotation_journal.py) la
# deduit de SEUIL_OCTETS_JOURNAL ci-dessus -- cette copie n'avait AUCUN lecteur.
# Nom CANONIQUE de la cadence declaree, lu par `vie etat` : on LIT la cadence
# au lieu de l'attendre (attendre n'est pas verifier). Meme valeur, meme objet.
INTERVALLE_DECLARE_SECONDES = INTERVALLE_DEFAUT_SECONDES
SECONDES_PAR_TICK = 1.0
ENCODAGE = "utf-8"
# LES PRODUCTIONS DE LA ROUTINE (MO-534) : les fichiers qu elle ECRIT et qui ne
# sont NI ses etats courts de forme CONVENTIONNELLE (PID, drapeau d arret,
# etat, journal, cadence : le controle d attribution les reconnait a leur
# FORME), ni un fichier ecrit a la main. Cette case est VIDE PARCE QUE C EST
# VRAI : mesure du 2026-10-03 sur cette routine, la seule chose qu elle ecrit
# est son PID, son drapeau et son etat court -- tous deja hors jugement par
# leur forme. Elle ne produit ni rapport, ni inventaire, ni memoria de passe.
# Elle ne DISAIT rien jusqu ici : une case ABSENTE et une case VIDE ne se
# distinguent pas pour le controle, qui pouvait donc prendre le silence pour
# une declaration oubliee. Le jour ou cette routine ecrira une production,
# c est ICI qu elle se declare, et le controle la lira sans qu une liste soit
# retouchee -- la regle est celle de `selecteur-flux`, dont la case vide
# porte deja cette meme justification.
PRODUCTIONS = ()
