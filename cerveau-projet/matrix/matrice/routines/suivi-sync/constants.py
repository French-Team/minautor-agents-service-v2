"""Constantes de la routine de synchronisation du suivi-optimus.

Sync les missions terminees (inbox.jsonl) vers le suivi-optimus.
"""
import sys
from pathlib import Path

REPERTOIRE_ROUTINE = Path(__file__).resolve().parent

# data/commun (motif unique M-076) : l'insertion montait d'UN CRAN DE TROP
# (`matrice/routines/data/commun`, dossier inexistant) : elle etait MORTE depuis
# toujours. Rien ne le voyait parce que suivi-sync n'avait jamais eu besoin du
# module partage ; la premiere tentative d'import l'a revele.
REPERTOIRE_COMMUN = REPERTOIRE_ROUTINE.parent.parent / "data" / "commun"
if not (REPERTOIRE_COMMUN / "attente.py").is_file():
    raise RuntimeError(
        "Motif attente introuvable : " + str(REPERTOIRE_COMMUN / "attente.py")
    )
sys.path.insert(0, str(REPERTOIRE_COMMUN))

# LA CADENCE VIT AU PLANNING (decision createur D1, 2026-09-26, MO-429) : ce
# fichier ne la CONTIENT plus, il la LIT a sa source partagee (motif unique
# M-076 : data/commun/planning_routines.py). Le nom CANONIQUE est conserve :
# vie etat, le serveur et les gardes lisent INTERVALLE_DECLARE_SECONDES.
from planning_routines import cadence_planning  # noqa: E402

INTERVALLE_SECONDS = cadence_planning('suivi-sync')
# Nom CANONIQUE de la cadence declaree, lu par `vie etat` : on LIT la cadence
# au lieu de l'attendre (attendre n'est pas verifier). Meme valeur, meme objet.
INTERVALLE_DECLARE_SECONDES = INTERVALLE_SECONDS
ENCODAGE = "utf-8"

# Sources et destination.
CHEMIN_INBOX = REPERTOIRE_ROUTINE.parent.parent / "intercom" / "matrice" / "inbox.jsonl"
REPERTOIRE_OUTIL_SUIVI = REPERTOIRE_ROUTINE.parent.parent / "data" / "outils" / "suivi-optimus"

# MO-563 : LE HEAD GENERE, ET LE PASSAIT QUI LE REGENERE.
#
# `suivi-optimus.md` est un VISUEL GENERE depuis ses BDD : il se le declare, et il
# donne son remede (`suivi-optimus vue`). Mais AUCUN appelant ne l appliquait. Mesure
# du 2026-10-03 : le maillon `head-coherent` a echoue CINQ fois d affilee sur cinq
# missions consecutives (MO-558 a MO-562), toujours avec le meme ecart d un
# evenement, toujours repare a la main par l agent. Cinq fois le meme rattrapage
# n est pas cinq incidents : c est une automatisation manquante.
#
# LE BON PROPRIETAIRE EST ICI, ET NULLE PART AILLEURS (M-076). Cette routine
# detient deja la donnee (elle synchronise `suivi-optimus.jsonl`) ; c est donc elle
# qui regenere son propre visuel. Le mettre dans `veille-flux` aurait cree un
# SECOND proprietaire du meme document -- deux verites pour un seul visuel, et le
# genre de trou que la tresse refuse deja de tolerer pour les items.
CHEMIN_HEAD_SUIVI = REPERTOIRE_ROUTINE.parent.parent.parent / "_operateur" / "optimus-prime" / "suivi-optimus.md"
CHEMIN_LANCEUR = REPERTOIRE_ROUTINE.parent.parent.parent / "lancer.py"
COMBO_HEAD = "vue"
CIBLE_HEAD = "_operateur/optimus-prime/suivi-optimus.md"
# Le journal des regenerations : une ligne par passe, avec le RETARD AVANT et la
# DUREE. Un geste qu on ne trace pas ne se mesure pas -- et c est le retard qu on
# veut voir, pas la presence du journal.
NOM_JOURNAL_HEAD = "journal-head.txt"
CHEMIN_JOURNAL_HEAD = REPERTOIRE_ROUTINE / NOM_JOURNAL_HEAD
NOM_PID = "suivi-sync.pid"
CHEMIN_PID = REPERTOIRE_ROUTINE / NOM_PID
NOM_DRAPEAU_ARRET = "suivi-sync.arret"
CHEMIN_DRAPEAU_ARRET = REPERTOIRE_ROUTINE / NOM_DRAPEAU_ARRET

# ETAT COURT DE LA PASSE (friction 28, 2026-09-14) : le BATTEMENT d'une routine
# est un ETAT, pas une histoire -- il s'ecrit ICI, a chaque passe et ECRASE.
# Sans ce temoin, suivi-sync etait la SEULE routine dont le rythme reel n'etait
# mesurable nulle part : ni journal, ni etat de passe (elle n'ecrit que son PID,
# une fois). `verifier-cadence` le lit et le compare a la cadence DECLAREE
# ci-dessus -- c'est la troisieme jambe : declarer, publier, MESURER.
NOM_ETAT = "suivi-sync-etat.json"
CHEMIN_ETAT = REPERTOIRE_ROUTINE / NOM_ETAT
# FIN DE PASSE (maillon 3 de la non-regression du flux, MO-478) : cette routine
# n'ecrit aucun journal (elle ne publie que son PID et son etat). Le fait est
# DECLARE `None` -- le maillon le DIT, il n'invente pas une fin a lire.
EVENEMENT_FIN_PASSE = None
# Combien de dernieres passes l'etat garde : assez pour un ecart MEDIAN (une
# passe en retard ou un redemarrage ne doivent pas faire croire a une derive),
# et borne pour que l'etat reste un etat (une poignee d'horodatages).
# La FABRIQUE de l'anneau (ajout + borne) et sa LECTURE (ecart median) sont le
# moteur PARTAGE `data/commun/battement.py` : la routine ne declare QUE sa
# longueur, elle ne recopie pas le decoupage (L-029 : un moteur recopie quatre
# fois diverge quatre fois).
PASSES_GARDEES_ETAT = 5
# Clef de l'anneau DANS l'etat : un seul nom, ecrit ET relu par sa constante.
CLE_ANNEAU_PASSES = "dernieres_passes"
# TEMOIN DE CADENCE (MO-479) : le fait que `verifier-cadence` lit pour mesurer le
# BATTEMENT REEL, declare ICI (M-076) au lieu d etre recopie dans la table du garde.
# (genre, fichier, clef) : fichier et clef DESIGNENT des constantes du dossier (jamais
# une valeur en double). Aucun temoin = la routine n est PAS mesuree, et le garde le DIT.
TEMOIN_CADENCE = ("anneau", NOM_ETAT, CLE_ANNEAU_PASSES)
# Format UNIQUE des horodatages (journal + etat) : le temps s'ecrit a un seul
# endroit, le meme des deux cotes (ecriture et relecture du battement).
FORMAT_HORODATAGE = "%Y-%m-%d %H:%M:%S"
ENCODAGE_ETAT = "utf-8"

# Actions a synchroniser (ce qui interesse optimus-prime).
TYPES_INTERESSANTS = ("fin-mission", "retour-lot")

# La synchronisation evite les doublons en comparant les dates.
# Si la date de l'evenement inbox est <= la date du dernier evenement
# dans le suivi-optimus, on considere que c'est deja synchronise.
# On utilise une comparaison lexicographique (format ISO 8601).
# Note : les dates dans l'inbox sont au format "AAAA-MM-JJ HH:MM:SS".
# On les compare en tant que chaines (ordre chronologique preserve).
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
