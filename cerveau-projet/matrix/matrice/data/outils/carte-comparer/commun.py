"""Fonctions communes de carte-comparer : resolution, lecture, parseur.

Chaque fonction fait UNE chose (convention-architecture-outils). L outil est en
LECTURE seule : il n ecrit rien, il n a donc ni porte, ni fragments -- la seule
ecriture qui le concerne est celle de l agent qui agit sur SON rapport.
"""

import subprocess
import sys
from pathlib import Path

# --- DOMICILE DU LANCEMENT (EO-430 / MO-416, bloc autosuffisant) -------------
# La racine se DETECTE par marqueur (MO-088 : aucun parents[N] nu), refus sinon.
_RACINE_LANCEMENT = Path(__file__).resolve().parent
while _RACINE_LANCEMENT.name != "matrix":
    if _RACINE_LANCEMENT.parent == _RACINE_LANCEMENT:
        raise RuntimeError("racine `matrix` introuvable en remontant depuis " + __file__)
    _RACINE_LANCEMENT = _RACINE_LANCEMENT.parent
_REPERTOIRE_COMMUN_LANCEMENT = _RACINE_LANCEMENT / "matrice" / "data" / "commun"
if not (_REPERTOIRE_COMMUN_LANCEMENT / "lancement.py").is_file():
    raise RuntimeError("Structure inattendue : " + str(_REPERTOIRE_COMMUN_LANCEMENT)
                       + " ne porte pas le domicile du lancement")
if str(_REPERTOIRE_COMMUN_LANCEMENT) not in sys.path:
    sys.path.insert(0, str(_REPERTOIRE_COMMUN_LANCEMENT))
from lancement import drapeaux_popen  # noqa: E402

# Le parseur d options EST le domicile partage (EO-158), jamais recopie.
from options import CLE_SANS_VALEUR, extraire_options  # noqa: E402

from constants import ENCODAGE, RACINE  # noqa: E402


def lancer_enfant(*arguments, **options):
    """Le SEUL lancement de processus de cet outil : jamais de fenetre."""
    return subprocess.run(*arguments, **options, **drapeaux_popen())


def relatif(chemin):
    """Chemin du workspace, racine-relative (la forme canonique des documents)."""
    try:
        return Path(chemin).resolve().relative_to(RACINE).as_posix()
    except (OSError, ValueError):
        return Path(chemin).name


def lire_texte(chemin):
    """Texte UTF-8 d un fichier, ou chaine vide s il est illisible."""
    try:
        return Path(chemin).read_text(encoding=ENCODAGE)
    except (OSError, UnicodeDecodeError):
        return ""
