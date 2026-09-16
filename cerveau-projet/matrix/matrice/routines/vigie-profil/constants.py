"""Constantes de la routine vigie-profil (Flux 1, famille orchestration).

Role : verifier si la fiche USER-PROFIL.md est remplie et, sinon, declencher
une ALERTE dans l'inbox de la Matrice (porte officielle : outil signaler).
La Matrice route ensuite l'alerte vers la maintenance -> le pilote guide
l'agent sur le parcours USER-PROFIL (theme dedie) pour remplir la fiche
avec l'utilisateur.

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs.
Les CHAMPS du profil ne sont PAS ici : ils vivent dans le motif unique
partage `matrice/data/commun/fiche_profil.py` (jamais recopie, M-076).
ATTENTION au NOM : le module partage ne doit JAMAIS s'appeler comme une
categorie importable d'un pilote (`profil/` existe : un `profil.py` pose
dans sys.path le masquerait et tuerait le pilote -- regression 2026-09-13).
"""
import sys
from pathlib import Path

REPERTOIRE_ROUTINE = Path(__file__).resolve().parent
REPERTOIRE_ROUTINES = REPERTOIRE_ROUTINE.parent
if REPERTOIRE_ROUTINES.name != "routines" or REPERTOIRE_ROUTINES.parent.name != "matrice":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_ROUTINE) + " n'est pas dans matrice/routines/"
    )

REPERTOIRE_MATRICE = REPERTOIRE_ROUTINES.parent
if REPERTOIRE_MATRICE.name != "matrice":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_MATRICE) + " n'est pas le dossier matrice/"
    )

# matrix/ : un cran au-dessus de matrice/ (la fiche profil y vit).
REPERTOIRE_MATRIX = REPERTOIRE_ROUTINES.parent.parent
if REPERTOIRE_MATRIX.name != "matrix":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_MATRIX) + " n'est pas le dossier matrix/"
    )

REPERTOIRE_OUTILS = REPERTOIRE_MATRICE / "data" / "outils"

# Motif UNIQUE de lecture de la fiche profil (data/commun, partage M-076).
# Le nom est `fiche_profil.py` (jamais `profil.py`) : les pilotes posent
# data/commun dans sys.path et ont une categorie `profil/` a proteger.
REPERTOIRE_COMMUN = REPERTOIRE_MATRICE / "data" / "commun"
NOM_MODULE_PARTAGE = "fiche_profil.py"
if not (REPERTOIRE_COMMUN / NOM_MODULE_PARTAGE).is_file():
    raise RuntimeError(
        "Motif profil introuvable : " + str(REPERTOIRE_COMMUN / NOM_MODULE_PARTAGE)
    )
sys.path.insert(0, str(REPERTOIRE_COMMUN))

# Porte officielle d'alerte (unique voie d'ecriture dans l'inbox Matrice).
OUTIL_SIGNALER = REPERTOIRE_OUTILS / "signaler" / "main.py"

# Etat de la routine : empreinte de l'episode incomplet OUVERT (anti-spam).
# `signature` non vide = une alerte est ouverte : on ne repose pas tant que la
# fiche n'est pas redevenue COMPLETE (borne par mission).
NOM_ETAT = "vigie-profil-etat.json"
CHEMIN_ETAT = REPERTOIRE_ROUTINE / NOM_ETAT
# Etat COURT de la PASSE (correction MO-082) : ce que la passe a VU. Le journal
# ne recoit plus la meme ligne `passe` a chaque tour -- mesure du 2026-09-14 :
# 194 lignes identiques sur 330 (58,8 %), une par tour. Une passe est un ETAT
# (le remplissage de la fiche), il s'ecrit ICI, a CHAQUE passe et ECRASE ;
# l'HISTOIRE (le journal) ne la recoit que si ce qu'elle a vu a CHANGE (moteur
# PARTAGE data/commun/etat_histoire.py, motif unique M-076).
NOM_ETAT_PASSES = "vigie-profil-etat-passes.json"
CHEMIN_ETAT_PASSES = REPERTOIRE_ROUTINE / NOM_ETAT_PASSES
# Combien de dernieres passes l'etat court garde : assez pour un ecart MEDIAN
# (un redemarrage ou une passe A LA DEMANDE ne doivent pas faire croire a une
# derive), et BORNE pour que l'etat reste un etat.
# La FABRIQUE de l'anneau (ajout + borne) et sa LECTURE (ecart median) sont le
# moteur PARTAGE `data/commun/battement.py` : la vigie ne declare QUE sa
# longueur, elle ne recopie pas le decoupage (L-029).
# POURQUOI LA MEDIANE, PAS UNE MOYENNE (mesure du 2026-09-14) : le premier
# temoin de cadence calculait (date - derniere_ecriture) / passes_absorbes. Pour
# cette vigie, dont le journal prouve la cadence a 900 s, il a lu 450,5 s puis
# 600,3 s -- une moyenne ne decrit aucun intervalle reel des qu'une passe n'est
# pas a l'heure. Une valeur fausse mais DANS la tolerance ne crie pas.
PASSES_GARDEES_ETAT = 5
# Clef de l'anneau DANS l'etat : un seul nom, ecrit ET relu par sa constante.
CLE_ANNEAU_PASSES = "dernieres_passes"
# Etat COURT de la cadence EFFECTIVE (le journal est rotationne : l'evenement de
# demarrage peut partir dans l'archive, un controle qui le chercherait la serait
# aveugle -- lecon L-040).
NOM_CADENCE = "vigie-profil-cadence.json"
CHEMIN_CADENCE = REPERTOIRE_ROUTINE / NOM_CADENCE
NOM_JOURNAL = "vigie-profil-log.jsonl"
CHEMIN_JOURNAL = REPERTOIRE_ROUTINE / NOM_JOURNAL
# Rotation du journal (MO-078) : le moteur est PARTAGE (data/commun/
# rotation_journal.py), la vigie ne declare que SES valeurs. Le declenchement
# se LIT (une taille) et la boucle le verifie AVANT chaque passe.
NOM_ARCHIVE_PREFIXE = "vigie-profil-archive"
SEUIL_OCTETS_JOURNAL = 512 * 1024
EVENEMENTS_GARDES_JOURNAL = 500
ESSAIS_ROTATION = 3
CHEMIN_RELATIF_JOURNAL = Path("matrice") / "routines" / "vigie-profil" / NOM_JOURNAL
NOM_PID = "vigie-profil.pid"
CHEMIN_PID = REPERTOIRE_ROUTINE / NOM_PID
NOM_DRAPEAU_ARRET = "vigie-profil.arret"
CHEMIN_DRAPEAU_ARRET = REPERTOIRE_ROUTINE / NOM_DRAPEAU_ARRET

INTERVALLE_DEFAUT_SECONDES = 900
# Nom CANONIQUE de la cadence declaree, lu par `vie etat` : on LIT la cadence
# au lieu de l'attendre (attendre n'est pas verifier). Meme valeur, meme objet.
INTERVALLE_DECLARE_SECONDES = INTERVALLE_DEFAUT_SECONDES
ENCODAGE = "utf-8"
INDENTATION_JSON = 2
# Lecture BORNEE de la queue d'un journal (MO-078) : une surveillance se lit
# dans les DERNIERS evenements, jamais dans tout l'historique. La FENETRE ne se
# declare plus ici (MO-099) : le moteur PARTAGE (data/commun/rotation_journal.py)
# la deduit de SEUIL_OCTETS_JOURNAL ci-dessus -- cette copie n'avait AUCUN lecteur.
# Format UNIQUE des horodatages (journal + etat) : le temps s'ecrit a un seul
# endroit, le meme des deux cotes (ecriture et relecture de l'anti-spam).
FORMAT_HORODATAGE = "%Y-%m-%d %H:%M:%S"

# ANTI-SPAM (correction MO-070, 2026-09-13) : plancher de temps a l'OUVERTURE
# d'un episode incomplet. Le depot est borne par MISSION (un seul depot tant que
# la fiche reste incomplete -- cf. tour/fonctions.py decision_depot) ; ce
# plancher ne fait qu'empecher une fiche qui CLIGNOTE (complete -> incomplete)
# de reposer une alerte aussitot. Il est en SECONDES MURALES, jamais en tours de
# boucle : la cadence REELLE est decidee par le serveur (mesure de l'incident :
# 60 s, 4 depots en 3 min), donc la routine ne peut pas s'y fier. Meme valeur
# que la cadence par defaut, mais c'est une AUTRE notion : la cadence dit quand
# on REGARDE, ce plancher dit quand on REPOSE.
ANTI_SPAM_SECONDES = 900

# Motifs de la DECISION de depot (anti-spam) : ils sont JOURNALISES par la
# passe, jamais recopies dans la logique (tour/fonctions.py les CONSOMME).
MOTIF_DEPOT = "depot"
MOTIF_EPISODE_OUVERT = "episode-ouvert"
MOTIF_PLANCHER = "plancher"
MOTIF_COMPLET = "profil-complet"

# Identite du signal (le signal doit dire la VERITE sur qui parle).
EXPEDITEUR_SIGNAL = "routine"
OUTIL_SIGNAL = "user-profil"
NIVEAU_SIGNAL = "moyenne"
MISSION_SIGNAL = "USER-PROFIL"
