"""Constantes de l outil bdd-conservation."""
import sys
from pathlib import Path

REPERTOIRE_OUTIL = Path(__file__).resolve().parent
REPERTOIRE_DATA = REPERTOIRE_OUTIL.parent.parent
if REPERTOIRE_DATA.name != "data":
    raise RuntimeError("Structure inattendue : " + str(REPERTOIRE_DATA))

NOM_BDD = "conservation.json"
NOM_BDD_TMP = NOM_BDD + ".tmp"
CHEMIN_BDD = REPERTOIRE_DATA / NOM_BDD
CHEMIN_EMPREINTE = REPERTOIRE_DATA / (NOM_BDD + ".sha256")

PREFIXE_ID = "K-"
CATEGORIES = (
    "VIVANT", "STRUCTUREL", "GENERE", "HISTORIQUE",
    "OBSOLETE", "COBAYE", "ORPHELIN", "HORS-PERIMETRE",
)
STATUTS = (
    "propose", "classe", "decide", "archive", "conserve",
    "repare", "dette", "signale", "restaure",
)
VERDICTS = ("conserver", "archiver", "reparer", "dette", "signaler")
OPERATIONS = ("proposer", "classer", "decider", "preciser", "rejuger", "manifester",
              "archiver", "restaurer")

ENCODAGE = "utf-8"
INDENTATION_JSON = 2
TAILLE_BLOC_LECTURE = 65536

sys.path.insert(0, str(REPERTOIRE_DATA / "commun"))
from racine import detecter_racine  # noqa: E402

RACINE = detecter_racine(REPERTOIRE_OUTIL)

# --- PORTE DE ROTATION (MO-160, cases 7 et 8 de la suite de purification) ---
# L'archive de la famille des points de restauration. La DESTINATION de chaque
# element vient de SA decision (colonne `destination`, posee par la case 6) : la
# porte ne la calcule pas, elle la RESOUT. Ce qui se declare ICI, c'est le
# DOMICILE de l'archive, le nom de son manifeste et celui de son temoin.
# Ce domicile vit sous `_operateur/` : c'est le PLANCHER du domicile
# d'invisibilite (data/commun/invisibilite.py), donc une zone que le cameleon ne
# lit jamais -- l'archive contient du CONTENU INTERNE (contre-analyse MO-156).
REPERTOIRE_ARCHIVES = "_operateur/optimus-prime/purification/archives"
NOM_MANIFESTE = "manifeste-archives.jsonl"
NOM_TEMOIN = "temoin-avant.json"
# La zone JETABLE du voisin (Flux 1) : un point qui s'y trouve est HORS
# PERIMETRE et se SIGNALE (regle immuable perimetre-tmp, point 1).
ZONES_CAMELEON = ("tmp-cameleon",)
# La FORME du point de restauration a UN domicile : la porte qui le PRODUIT
# (`data/outils/ecrire/constants.py`). Cette porte la CONSOMME -- elle ne la
# recopie jamais (M-076 ; friction 42).
CHEMIN_DOMICILE_FORME_BAK = REPERTOIRE_DATA / "outils" / "ecrire" / "constants.py"
