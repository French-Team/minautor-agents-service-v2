"""Constantes de la routine vigie-portes (Flux 1, famille securite).

Role : surveiller les PORTES de la Matrice (les outils de matrice/data/outils/)
et CEUX QUI LES UTILISENT (le journal d'usages).

Pourquoi cette routine existe : cette session a trouve QUATRE pannes de porte,
toutes invisibles -- et aucune n'etait un crash :
  1. la porte INTROUVABLE     : le questionnaire du profil etait un cran trop haut,
                                la porte repondait "Questionnaire absent" depuis toujours ;
  2. la porte AVEUGLE         : le moteur de recherche scannait un dossier parasite
                                supprime la veille -> "0 resultat" sur TOUT ;
  3. la porte NEUTRALISEE     : suivi-sync reimportait ce que la porte `archiver`
                                venait de deplacer, a chaque passe ;
  4. la porte a MOITIE        : `enregistrer` ecrivait la file sans le journal.
Une porte qui ne dit rien et une porte qui va bien se ressemblent : il faut un
temoin qui les distingue.

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs.
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

# matrix/ : un cran au-dessus de matrice/.
REPERTOIRE_MATRIX = REPERTOIRE_ROUTINES.parent.parent
if REPERTOIRE_MATRIX.name != "matrix":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_MATRIX) + " n'est pas le dossier matrix/"
    )

# data/commun (motif unique M-076) : l'attente cooperative est PARTAGEE, jamais
# recopiee. Sans ce chemin, la vigie retombait sur `time.sleep(intervalle)` en un
# seul bloc : un arret demande attendait la cadence entiere (jusqu'a 900 s).
REPERTOIRE_COMMUN = REPERTOIRE_MATRICE / "data" / "commun"
if not (REPERTOIRE_COMMUN / "attente.py").is_file():
    raise RuntimeError(
        "Motif attente introuvable : " + str(REPERTOIRE_COMMUN / "attente.py")
    )
sys.path.insert(0, str(REPERTOIRE_COMMUN))

# Chemins RELATIFS a matrix/ : une seule source, reutilisable sur un cobaye
# (le tour accepte --racine : un controle qu'on ne peut pas pieger ne prouve rien).
CHEMIN_RELATIF_OUTILS = "matrice/data/outils"
CHEMIN_RELATIF_ROUTINES = "matrice/routines"
CHEMIN_RELATIF_USAGES = "matrice/data/usages-outils-combos.jsonl"
CHEMIN_RELATIF_RECHERCHER = "matrice/data/outils/rechercher/main.py"
CHEMIN_RELATIF_SIGNALER = "matrice/data/outils/signaler/main.py"

# La RECETTE d'une porte : ce qu'un outil doit avoir pour etre utilisable.
FICHIERS_RECETTE = ("main.py", "DESCRIPTION.md")
NOM_ENTREE = "entry.py"

# Seuils d'usage (fenetre glissante).
FENETRE_JOURS = 30
SEUIL_REFUS_MIN = 5
PART_REFUS_ALERTE = 0.5

# Un appel d'AIDE sort en code 2 comme un refus. Les compter comme de la
# mauvaise utilisation faisait crier la vigie sur des outils sains : tous les
# "refus" de `editer-agents-md` etaient des `--help`.
COMMANDES_AIDE = ("--help", "-h", "help", "aide")

# Une SONDE DECLAREE : un harnais qui appelle une porte FAUX VOLONTAIREMENT pour
# verifier que son refus fonctionne. Ces appels sortent en code 2, comme ceux d un
# appelant qui se trompe, donc la metrique les comptait comme une faute -- et le
# bruit noiait les vraies alertes (mesure : 35 alertes, dont 274/274 sur plusieurs
# portes).
#
# LE TAG, PAS LE TEXTE. La sonde se RECONNAIT a son tag `sonde`, pose par le
# harnais (canal MATRICE_SONDE, dans le sac-a-dos -- MO-555). Reconnaitre une sonde
# a son TEXTE (l option bidon) serait fragile : un appelant reel qui taperait la
# meme option serait innocente, et le filtre s elargirait a tout ce qui ressemble a
# un refus. Ici la declaration vient de celui qui APPELLE : c est lui qui sait.
#
# CE QUE LE TAG NE FAIT PAS. Il n exclut pas l usage : la ligne reste au journal,
# avec sa sortie et son code. Seule la lettre < mal utilisee > cesse de les compter.
TAGS_EXCLUS = ("sonde",)

# Requete TEMOIN du moteur de recherche : une chaine qui EXISTE forcement dans le
# perimetre. 0 resultat = le moteur est AVEUGLE (exactement le bug MO-055, ou il
# scannait un dossier disparu et repondait "0 resultat" a toutes les requetes).
REQUETE_TEMOIN = "main.py"
SEUIL_TEMOIN = 1

# Identite du signal (le signal doit dire la VERITE sur qui parle).
EXPEDITEUR_SIGNAL = "routine"
OUTIL_SIGNAL = "vigie-portes"
NIVEAU_SIGNAL = "moyenne"
MISSION_SIGNAL = "VIGIE-PORTES"
# Niveaux qui partent dans l'inbox ; "basse" reste au journal.
NIVEAUX_ALERTES = ("critique", "haute", "moyenne")

# Etat (anti-spam), journal, PID, drapeau.
NOM_ETAT = "vigie-portes-etat.json"
CHEMIN_ETAT = REPERTOIRE_ROUTINE / NOM_ETAT
# Etat COURT de la PASSE (correction MO-082) : ce que la passe a VU. Le journal
# ne recoit plus la meme ligne `passe` a chaque tour -- mesure du 2026-09-14 :
# 105 lignes identiques sur 204 (51,5 %), une par tour. Une passe est un ETAT
# (la photo des portes et de leurs alertes), il s'ecrit ICI, a CHAQUE passe et
# ECRASE ; l'HISTOIRE (le journal) ne la recoit que si ce qu'elle a vu a CHANGE
# (moteur PARTAGE data/commun/etat_histoire.py, motif unique M-076).
NOM_ETAT_PASSES = "vigie-portes-etat-passes.json"
CHEMIN_ETAT_PASSES = REPERTOIRE_ROUTINE / NOM_ETAT_PASSES
# Combien de dernieres passes l'etat court garde : assez pour un ecart MEDIAN
# (un redemarrage ou une passe A LA DEMANDE ne doivent pas faire croire a une
# derive), et BORNE pour que l'etat reste un etat.
# La FABRIQUE de l'anneau (ajout + borne) et sa LECTURE (ecart median) sont le
# moteur PARTAGE `data/commun/battement.py` : la vigie ne declare QUE sa
# longueur, elle ne recopie pas le decoupage (L-029).
# POURQUOI LA MEDIANE, PAS UNE MOYENNE (mesure du 2026-09-14) : jumelle de
# vigie-profil, elle a subi le meme temoin faux -- le premier temoin de cadence
# calculait (date - derniere_ecriture) / passes_absorbes, une MOYENNE qui ne
# decrit aucun intervalle reel des qu'une passe n'est pas a l'heure.
PASSES_GARDEES_ETAT = 5
# Clef de l'anneau DANS l'etat : un seul nom, ecrit ET relu par sa constante.
CLE_ANNEAU_PASSES = "dernieres_passes"
# Etat COURT de la cadence EFFECTIVE (le journal est rotationne : l'evenement de
# demarrage peut partir dans l'archive, un controle qui le chercherait la serait
# aveugle -- lecon L-040).
NOM_CADENCE = "vigie-portes-cadence.json"
CHEMIN_CADENCE = REPERTOIRE_ROUTINE / NOM_CADENCE
NOM_JOURNAL = "vigie-portes-log.jsonl"
CHEMIN_JOURNAL = REPERTOIRE_ROUTINE / NOM_JOURNAL
# FIN DE PASSE (maillon 3 de la non-regression du flux, MO-478) : cette vigie ne
# journalise PAS une fin a chaque passe -- `tour/fonctions.py` ne journalise la ligne
# `passe` que si ce qu'elle a vu a CHANGE (`if notable:`), et sa passe ordinaire va
# dans l'ANNEAU de `vigie-portes-etat-passes.json`. Le fait est DECLARE `None` : le
# maillon le DIT au lieu d'accuser une routine saine dont le journal est stable.
# Mesure du 2026-09-26 : journal fige a 11:19, anneau frais a 13:49 -- un `passe`
# declare ici aurait fait un FAUX KO. Sa VIE reste surveillee par le maillon 7.
EVENEMENT_FIN_PASSE = None
# TEMOIN DE CADENCE (MO-479) : le fait que `verifier-cadence` lit pour mesurer le
# BATTEMENT REEL, declare ICI (M-076) au lieu d etre recopie dans la table du garde.
# (genre, fichier, clef) : fichier et clef DESIGNENT des constantes du dossier (jamais
# une valeur en double). Aucun temoin = la routine n est PAS mesuree, et le garde le DIT.
TEMOIN_CADENCE = ("anneau", NOM_ETAT_PASSES, CLE_ANNEAU_PASSES)
# Rotation du journal (MO-078) : moteur PARTAGE (data/commun/rotation_journal.py),
# la vigie ne declare que SES valeurs ; le declenchement se LIT (une taille).
NOM_ARCHIVE_PREFIXE = "vigie-portes-archive"
SEUIL_OCTETS_JOURNAL = 512 * 1024
EVENEMENTS_GARDES_JOURNAL = 500
ESSAIS_ROTATION = 3
CHEMIN_RELATIF_JOURNAL = Path("matrice") / "routines" / "vigie-portes" / NOM_JOURNAL
NOM_PID = "vigie-portes.pid"
CHEMIN_PID = REPERTOIRE_ROUTINE / NOM_PID
NOM_DRAPEAU_ARRET = "vigie-portes.arret"
CHEMIN_DRAPEAU_ARRET = REPERTOIRE_ROUTINE / NOM_DRAPEAU_ARRET

# LA CADENCE VIT AU PLANNING (decision createur D1, 2026-09-26, MO-429) : ce
# fichier ne la CONTIENT plus, il la LIT a sa source partagee (motif unique
# M-076 : data/commun/planning_routines.py). Le nom CANONIQUE est conserve :
# vie etat, le serveur et les gardes lisent INTERVALLE_DECLARE_SECONDES.
from planning_routines import cadence_planning  # noqa: E402

INTERVALLE_DEFAUT_SECONDES = cadence_planning('vigie-portes')
# Nom CANONIQUE de la cadence declaree, lu par `vie etat` : on LIT la cadence
# au lieu de l'attendre (attendre n'est pas verifier). Meme valeur, meme objet.
INTERVALLE_DECLARE_SECONDES = INTERVALLE_DEFAUT_SECONDES
ENCODAGE = "utf-8"
INDENTATION_JSON = 2
TIMEOUT_PORTE_SECONDES = 60

# Format UNIQUE des horodatages (journal + etat) : le temps s'ecrit a un seul
# endroit, le meme des deux cotes (ecriture et relecture de l'anti-spam).
FORMAT_DATE = "%Y-%m-%d %H:%M:%S"

# Lecture BORNEE de la queue d'un journal (MO-078) : une surveillance se lit
# dans les DERNIERS evenements, jamais dans tout l'historique. La FENETRE ne se
# declare plus ici (MO-099) : le moteur PARTAGE (data/commun/rotation_journal.py)
# la deduit de SEUIL_OCTETS_JOURNAL ci-dessus -- cette copie n'avait AUCUN lecteur.

# ANTI-SPAM (correction MO-073, jumelle de MO-070) : le depot est borne par
# MISSION -- il porte sur les alertes NOTABLES (celles qui partent dans l'inbox),
# jamais sur n'importe quelle variation d'observation. Deux gardes :
#   1) une variation d'une alerte "basse" ne compte pas (elle n'a rien a dire
#      dans l'inbox, et son mouvement reposait un depot IDENTIQUE) ;
#   2) un vrai changement de jeu notable survenu moins de ANTI_SPAM_SECONDES
#      apres le dernier depot est RETENU (journalise) et repart a la passe
#      suivante -- jamais perdu. Secondes MURALES, jamais des tours de boucle :
#      la cadence reelle est decidee par le serveur, pas par la routine.
ANTI_SPAM_SECONDES = 900

# Motifs de la DECISION de depot (journalises, jamais recopies dans la logique).
MOTIF_DEPOT = "depot"
MOTIF_DEJA_SIGNALE = "deja-signale"
MOTIF_PLANCHER = "plancher"
MOTIF_VIDE = "aucune-alerte-notable"
MOTIF_RESOLU = "resolu"

# --- 7. NEMESIS (EO-219, regle createur du 2026-09-19) --------------------------
# La regle : apres la chaine pense-bete -> spec -> todo-list, TOUT process de
# construction de fichiers passe par un passage NEMESIS (3 axes du proto-4,
# forme Oui MAIS, en THEME jamais en agent). Ce controle permanent LIT la trace
# DECLAREE : il ne croit pas une promesse.
# Etats INITIAUX : un document qui n'a pas encore ete attaque porte ces statuts
# et n'exige AUCUN nemesis -- le premier etat n'est pas une livraison.
# MO-224 (2026-09-19) : le premier etat de la CHAINE est pense-bete. La porte
# chaine-pense-bete REFUSE deja, elle, la sortie du spec sans la trace ; mais le
# premier etat n'est pas une livraison -- il entre donc dans cette liste.
ETATS_INITIAUX_NEMESIS = ("pense-bete", "proposition", "ebauche", "constat", "brouillon")
# Trace = DECLAREE dans la carte d'identite (ce champ) ET ECRITE dans le corps
# (un de ces marqueurs). DEUX conditions : un champ seul serait une promesse.
CHAMP_STATUT_CARTE = "statut:"
CHAMP_TRACE_NEMESIS = "nemesis:"
MARQUEURS_PASSAGE_NEMESIS = ("NEMESIS", "CONTRE-ANALYSE")
SEPARATEUR_CARTE = "---"
# Domicile DECLARE du controle (decision A1 du 2026-09-19 : le domicile de la
# chaine), relatif a matrix/. Le controle ne balaie pas tout matrix/ : il lit le
# domicile ou les fichiers de la chaine se construisent.
CHEMIN_RELATIF_CONSTRUITS = "_operateur/optimus-prime/preparation"
# ANTERIEURS declares : construits AVANT la regle, avec leur RAISON. Une liste
# d'exemptions se DIT ici, elle ne se cache pas dans le corps du controle.
ANTERIEURS_NEMESIS = {
    "inventaire-types.md": "construit le 2026-09-17, avant la regle du 2026-09-19",
}
NIVEAU_NEMESIS = "haute"
PORTE_NEMESIS = "preparation"
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
