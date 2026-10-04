"""Constantes de l'outil signaler : cameleon signale un probleme outil.

Le cameleon utilise cet outil quand un outil est en panne, buggy,
ou amelioration manquante. La Matrice route le message vers
intercom maintenance (Optimus).
"""
import sys
from pathlib import Path

REPERTOIRE_OUTIL = Path(__file__).resolve().parent
REPERTOIRE_DATA = REPERTOIRE_OUTIL.parent.parent
if REPERTOIRE_DATA.name != "data":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_DATA) + " n'est pas le dossier data/"
    )

sys.path.insert(0, str(REPERTOIRE_DATA / "commun"))
from racine import detecter_racine  # noqa: E402

RACINE = detecter_racine(REPERTOIRE_OUTIL)
# Detection robuste : remonter jusqu'a cerveau-projet/matrix/
REPERTOIRE_MATRIX = None
for p in [REPERTOIRE_OUTIL, *REPERTOIRE_OUTIL.parents]:
    if p.name == "matrix" and (p / "matrice" / "data").is_dir():
        REPERTOIRE_MATRIX = p
        break
if REPERTOIRE_MATRIX is None:
    REPERTOIRE_MATRIX = RACINE / "cerveau-projet" / "matrix"
REPERTOIRE_MATRICE = REPERTOIRE_MATRIX / "matrice"

ENCODAGE = "utf-8"

# LES VERBES (MO-244) : l aide annoncait le verbe signal alors que le dispatch n acceptait
# que signaler -- DEUX sources pour un seul mot, donc une porte qui MENTAIT sur son propre
# contrat (mesure du 2026-09-19 : le verbe annonce rendait verbe inconnu signal, et l agent
# qui suivait l aide etait bloque). Une seule source desormais : le canonique, et l alias
# que l aide a annonce -- il est ACCEPTE, sinon on punit celui qui a suivi l aide. L aide
# ET le message d erreur lisent tous les deux CETTE liste.
VERBE = "signaler"
VERBES_ACCEPTES = (VERBE, "signal")

# Boite d'entree Matrice (le cameleon y depose ses signalements)
BOITE_MATRICE_INBOX = REPERTOIRE_MATRICE / "intercom" / "matrice" / "inbox.jsonl"

# Niveaux d'importance
NIVEAUX = {
    "critique": {"ordre": 1, "desc": "Outil en panne totale, mission impossible sans reparation"},
    "haute": {"ordre": 2, "desc": "Bug bloquant, mission ralentie mais contournable"},
    "moyenne": {"ordre": 3, "desc": "Amelioration manquante, mission possible mais defaillante"},
    "basse": {"ordre": 4, "desc": "Souhait d'amelioration, pas bloquant"},
}

# Expediteurs autorises (liste FERMEE) : qui signe le signal.
# "cameleon" = defaut historique (compatibilite) ; "routine" = une routine de
# vie de la Matrice (ex : vigie-profil) ; "matrice" = la Matrice elle-meme.
EXPEDITEUR_DEFAUT = "cameleon"
EXPEDITEURS = ("cameleon", "routine", "matrice")

NOMS_OPTIONS = ("outil", "niveau", "description", "mission", "erreur", "expediteur", "json")
