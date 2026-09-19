"""Constantes de l'outil pause-session : chemins et valeurs.

Protocole de pause session-matrix (M-080, decisions createur) :
sauvegarde SEULEMENT a la pause, perimetre cameleon reducible, cycle
pause -> maintenance -> reprise a l'identique, raison jamais divulguee.

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
"""
import sys
from pathlib import Path

REPERTOIRE_OUTIL = Path(__file__).resolve().parent
REPERTOIRE_DATA = REPERTOIRE_OUTIL.parent.parent
if REPERTOIRE_DATA.name != "data":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_OUTIL) + " n'est pas dans data/outils/"
    )
REPERTOIRE_MATRICE = REPERTOIRE_DATA.parent

# Etat serialise de la session-matrix (pose a la pause, supprime a la reprise).
NOM_ETAT = "session-matrix-etat.json"
NOM_ETAT_TMP = "session-matrix-etat.tmp"
CHEMIN_ETAT = REPERTOIRE_DATA / NOM_ETAT

# File du pilote : la mission en pause en SORT (la reprise la remet a l'identique).
CHEMIN_FILE_PILOTE = REPERTOIRE_MATRICE / "pilote" / "file-missions.json"

# Notification au cameleon (intercom) : raison "maintenance", JAMAIS plus.
CHEMIN_BOITE_CAMELEON = REPERTOIRE_MATRICE / "intercom" / "cameleon" / "inbox.jsonl"
RAISON_NOTIFIEE = "maintenance"
MESSAGE_PAUSE = (
    "Ta mission est mise en pause pour MAINTENANCE. "
    "Tu seras prevu quand la maintenance sera terminee."
)
MESSAGE_REPRISE = "Maintenance terminee : ta mission reprend ou elle avait ete laissee."

# Journal append-only de toutes les pauses/reprises (une ligne JSON par evenement).
NOM_JOURNAL = "pauses-session-matrix.jsonl"
CHEMIN_JOURNAL = REPERTOIRE_DATA / NOM_JOURNAL

# Porte d'ecriture du classeur-variables (MO-093 : PORTE UNIQUE bdd-variables).
CHEMIN_OUTIL_BDD_VARIABLES = REPERTOIRE_DATA / "outils" / "bdd-variables"
RAISON_PERIMETRE = "pause-session perimetre"
TAGS_PERIMETRE = "cameleon,perimetre"

# Perimetre du cameleon (cle du classeur-variables, zones exclues de SA lecture).
# Regle matrice-utilise-cameleon : la Matrice seule reduit ce perimetre.
CLE_PERIMETRE = "perimetre-cameleon"
CHEMIN_CLASSEUR = REPERTOIRE_DATA / "classeur-variables.json"
CHEMIN_EMPREINTE_CLASSEUR = REPERTOIRE_DATA / "classeur-variables.json.sha256"
NOM_CLASSEUR_TMP = "classeur-variables.tmp"

# Zone neutre "maintenance" (decision createur, audit protections 2026-09-09) :
# le classeur ne revele JAMAIS le nom reel de l'entite interne. La zone cachee
# dans le classeur est "maintenance" ; cette table RESOUT la zone vers les
# chemins reels a exclure de la lecture cameleon (appliquee a la lecture).
ZONE_MAINTENANCE = "maintenance"
CHEMINS_MAINTENANCE = (
    "data/outils/suivi-optimus",
    "data/suivi-optimus.jsonl",
    "data/suivi-optimus.jsonl.sha256",
    "_operateur/optimus-prime/suivi-optimus.md",
    "docs/suivi-optimus-conception.md",
)

# Niveau defcon qui declenche la pause automatique (lecture seule ici).
CLE_DEFCON = "defcon"
NIVEAU_PAUSE_AUTO = 5

STATUT_EN_COURS = "en-cours"
ENCODAGE = "utf-8"
INDENTATION_JSON = 2
TAILLE_BLOC_LECTURE = 65536  # lecture seule du classeur (empreinte lecture)

# data/commun (motif unique M-076) : installe le dossier partage dans sys.path.
_courant = REPERTOIRE_OUTIL
for _ in range(30):
    if (_courant / "commun" / "racine.py").is_file():
        sys.path.insert(0, str(_courant / "commun"))
        break
    _courant = _courant.parent
else:
    raise RuntimeError("data/commun introuvable en remontant.")

from racine import detecter_racine  # noqa: E402

RACINE = detecter_racine(REPERTOIRE_OUTIL)
