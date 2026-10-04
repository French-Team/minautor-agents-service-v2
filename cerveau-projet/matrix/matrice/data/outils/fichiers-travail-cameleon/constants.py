"""Constantes de l outil fichiers-travail-cameleon (MO-378).

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
"""

import re
import sys
from pathlib import Path

REPERTOIRE_OUTIL = Path(__file__).resolve().parent
REPERTOIRE_DATA = REPERTOIRE_OUTIL.parent.parent
if REPERTOIRE_DATA.name != "data":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_DATA) + " n est pas le dossier data/"
    )

# data/commun (motif unique M-076) : les motifs partages se CONSOMMENT, jamais recopies.
sys.path.insert(0, str(REPERTOIRE_DATA / "commun"))
from racine import detecter_racine  # noqa: E402
from zone_tmp import NOM_ZONE_CAMELEON, chemin_zone_cameleon  # noqa: E402

# LA RACINE DU WORKSPACE (celle qui porte AGENTS.md) : la zone du cameleon se resout
# depuis ELLE (son domicile est declare dans zone_tmp.py, racine par racine).
RACINE = detecter_racine(REPERTOIRE_OUTIL)

# LA ZONE : elle est CONSOMMEE de son domicile unique (M-076). Ce flux ne cree JAMAIS
# la zone d un autre (regle R-005) : elle est PREPAREE par le pilote du cameleon. La
# porte, elle, la LIT et la VIDE -- et elle DIT quand elle est absente.
ZONE = chemin_zone_cameleon(RACINE)
NOM_ZONE = NOM_ZONE_CAMELEON

# LE JOURNAL DU FLUX : une ligne par acte (pose, purge), en ajout seul. Il vit a cote
# de l outil : c est la MEMOIRE de ce qui a ete pose et de ce qui a ete solde -- sans
# lui, la zone vide ne dit plus rien de ce qu elle a porte (demande createur : je ne
# vois pas ce que tu fais).
JOURNAL = REPERTOIRE_OUTIL / "fichiers-travail-cameleon-journal.jsonl"

# LE NOM CANONIQUE : <mission minuscule>-<libelle>.<extension>. Le nom PORTE la
# mission, donc la lecture et la purge n ont plus besoin d une liste tenue a la main.
# La forme du cameleon est M- (son pilote) : mo- est celle d Optimus, et un nom
# etranger doit etre VU comme un residu, jamais adopte.
MOTIF_MISSION = re.compile(r"^m-([0-9]+)$")
MOTIF_CANONIQUE = re.compile(r"^m-([0-9]+)-([a-z0-9][a-z0-9-]*)\.([a-z0-9]+)$")
MOTIF_LIBELLE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
MISSION_HISTORIQUE = re.compile(r"^(m|mo)-([0-9]+)$")

# LES EXTENSIONS admises pour un fichier de travail : au-dela, le fichier n est pas
# un travail de mission mais un artefact -- il sera VU et NOMME comme residu.
EXTENSIONS = ("txt", "md", "json", "py", "log", "base64")

# Les deux ACTES que le journal distingue.
ACTION_CREE = "cree"
ACTION_PURGE = "purge"

# Bornes d affichage et d identite.
LIGNES_MONTREES = 200
PAR_DEFAUT = "cameleon"
