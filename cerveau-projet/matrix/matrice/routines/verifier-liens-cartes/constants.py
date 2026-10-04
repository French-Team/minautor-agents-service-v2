"""Constantes de la routine verifier-liens-cartes -- squelette du moule routine.

Mesure le graphe des liens des cartes d identite : liens morts, liens non reciproques, couverture des liens dans le corpus
"""
import sys
from pathlib import Path

REPERTOIRE_ROUTINE = Path(__file__).resolve().parent

# data/commun (motif unique M-076) : l'insertion montait d'UN CRAN DE TROP
# (`matrice/routines/data/commun`, dossier inexistant) : elle etait MORTE depuis
# toujours. Rien ne le voyait parce que verifier-liens-cartes n'avait jamais eu besoin du
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

INTERVALLE_SECONDS = cadence_planning('verifier-liens-cartes')
# Nom CANONIQUE de la cadence declaree, lu par `vie etat` : on LIT la cadence
# au lieu de l'attendre (attendre n'est pas verifier). Meme valeur, meme objet.
INTERVALLE_DECLARE_SECONDES = INTERVALLE_SECONDS
ENCODAGE = "utf-8"

# LA RACINE DES DOCUMENTS : `matrix/` -- la Matrice est `matrice/`, la zone de l
# operateur est son VOISIN `_operateur/`. Les liens des cartes sont canoniques
# depuis CETTE racine : c est celle du garde des cartes (une seule forme, un seul
# jugement), et cette routine la CONSOMME au lieu de la redeviner (M-076).
RACINE_DOCUMENTS = REPERTOIRE_ROUTINE.parent.parent.parent
EXTENSION_DOCUMENT = ".md"
# Zones IGNOREES : du provisoire et des archives. Un lien qui y pointe ne
# disparait pas pour autant -- mais l inventaire ne s y egare pas.
ZONES_IGNOREES = ("/tmp-optimus/", "/tmp-cameleon/", "/tmp-test/", "/__pycache__/",
                  "/purification/", "/archives/", "/.git/")
NOM_RAPPORT = "rapport-liens.json"
CHEMIN_RAPPORT = REPERTOIRE_ROUTINE / NOM_RAPPORT

# LES PRODUCTIONS DE LA ROUTINE : ce qu'elle ECRIT elle-meme et qui n'est PAS un
# etat court (etat, journal, cadence, PID). Un RAPPORT est la MEMOIRE LONGUE d'une
# passe : il se REEcrit a chaque tour, personne ne l'ecrit a la main, sa porte est
# CETTE routine -- ce n'est donc PAS une source.
# Le controle d'attribution LIT cette declaration : il CONSOMME le domicile, il ne
# recopie aucun nom (M-076). Mesure du 2026-09-23 : sans elle, `rapport-liens.json`
# etait accuse comme une source des sa premiere reecriture -- a CHAQUE passe, sans fin.
PRODUCTIONS = (CHEMIN_RAPPORT,)

NOM_PID = "verifier-liens-cartes.pid"
CHEMIN_PID = REPERTOIRE_ROUTINE / NOM_PID
# FIN DE PASSE (maillon 3 de la non-regression du flux, MO-478) : cette routine
# n'ecrit aucun journal (elle publie son PID et son RAPPORT de passe). Le fait est
# DECLARE `None` -- le maillon le DIT, il n'invente pas une fin a lire.
EVENEMENT_FIN_PASSE = None
NOM_DRAPEAU_ARRET = "verifier-liens-cartes.arret"
CHEMIN_DRAPEAU_ARRET = REPERTOIRE_ROUTINE / NOM_DRAPEAU_ARRET

# ETAT COURT DE LA PASSE (friction 28, 2026-09-14) : le BATTEMENT d'une routine
# est un ETAT, pas une histoire -- il s'ecrit ICI, a chaque passe et ECRASE.
# Sans ce temoin, verifier-liens-cartes etait la SEULE routine dont le rythme reel n'etait
# mesurable nulle part : ni journal, ni etat de passe (elle n'ecrit que son PID,
# une fois). `verifier-cadence` le lit et le compare a la cadence DECLAREE
# ci-dessus -- c'est la troisieme jambe : declarer, publier, MESURER.
NOM_ETAT = "verifier-liens-cartes-etat.json"
CHEMIN_ETAT = REPERTOIRE_ROUTINE / NOM_ETAT
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

