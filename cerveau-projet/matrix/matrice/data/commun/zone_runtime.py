"""zone_runtime -- le DOMICILE de la ZONE RUNTIME (le Python embarque).

POURQUOI CE FICHIER EXISTE. Le runtime Python est un ARTEFACT que la Matrice
PRODUIT ELLE-MEME : `runtime/installer.py` le telecharge, l extrait, le corrige
et le prouve. Ce n est donc pas une source, ni un fichier pose a la main, ni un
artefact d un outil etranger (comme `.kilo`, qui a son propre domicile
`artefacts_externes.py`) -- c est une zone produite par UNE porte.

Mesure du 2026-10-04 : sans declaration, le controle d attribution reportait
ses 37 fichiers un par un (`runtime/_asyncio.pyd source NEUVE, absente de la
pose`), et le garde ASCII-allait lui aussi les juger fichier par fichier. Un
artefact de 23 Mo juge comme 37 sources orphelines, c est un garde qu on
apprend a ignorer -- exactement le rouge permanent que R-008 fait inverser.

La regle est donc la meme que les trois zones voisines (MO-377, MO-492,
MO-497) : un PREDICAT, un NOM et un MOTIF, tous trois dans CE fichier, et les
consommateurs les LISEENT (M-076 : une zone reecrite dans chaque garde
divergerait au premier ajout). Une exemption muette serait un angle mort --
donc le motif est dit, jamais applique en silence.

CE QUE LA ZONE DIT, ET CE QU ELLE NE FAIT PAS. Elle ne dispense d AUCUNE
verification : le runtime reste compile, demarre et prouve a chaque installation
(c'est `installer.py` qui le prouve, jamais une declaration). Elle dit
seulement QUELS fichiers sont produits par une porte, pour que le controle les
compte au lieu de les accuser.
"""
import sys
from pathlib import Path

# `racine.py` est un VOISIN de ce module (data/commun) : le chemin est pose pour
# que l import marche meme quand le module est charge seul.
_DOSSIER_COMMUN = Path(__file__).resolve().parent
if str(_DOSSIER_COMMUN) not in sys.path:
    sys.path.insert(0, str(_DOSSIER_COMMUN))

# Le segment qui PORTE la zone : `runtime/`, a la racine de la Matrice.
SEGMENT_RUNTIME = "runtime"

NOM_ZONE_RUNTIME = "runtime-python-embarque"
MOTIF_ZONE_RUNTIME = (
    "le runtime Python EMBARQUE (artefact officiel python.org) : produit par la "
    "porte `runtime/installer.py`, qui telecharge, VERIFIE l empreinte, extrait, "
    "corrige et PROUVE par l usage -- donc jamais pose a la main et jamais "
    "accusable comme ecriture non attribuee"
)


def est_zone_runtime(chemin):
    """True si <chemin> est dans la zone du runtime embarque.

    Le predicat est le PREMIER segment : il reconnait la zone a son Ancre
    (la racine de la Matrice), pas a une liste de fichiers -- une liste
    divergerait des que le runtime gagne un fichier.
    """
    morceaux = Path(str(chemin)).as_posix().strip("/").split("/")
    for index, morceau in enumerate(morceaux):
        if morceau != SEGMENT_RUNTIME:
            continue
        # A la racine de la Matrice (`.../matrix/runtime/...`) ou plus profond.
        # Le segment doit etre celui du runtime, pas un homonyme ailleurs.
        if index == 0 or index == 1 or morceaux[index - 1] == "matrix":
            return True
    return False