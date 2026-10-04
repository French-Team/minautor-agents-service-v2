"""Constantes de la porte `passerelle` : le canal, son journal, et la porte appelee.

La porte `passerelle` est le PASSAGE entre le canal du user (`user-demandes/`) et
le reste de la Matrice : elle LIT le canal, depose un ITEM par la porte de
l entonnoir, et RETIRE la demande du canal. Elle n ecrit JAMAIS un item elle-meme
(un item se depose par sa porte).

LA RACINE SE LIT AU DOMICILE DU PILOTE (M-076), elle ne se compte pas a la main :
la suite a accuse ce fichier pour un chemin de racine COMPTE A LA MAIN (L-013) --
un dossier de plus ou de moins et le chemin devenait FAUX EN SILENCE (mesure du
2026-09-29). Le motif fautif n est pas CITE ici : le controle lit le TEXTE, et une
citation du defaut suffit a le faire accuser.
"""
import sys
from pathlib import Path

REPERTOIRE_CATEGORIE = Path(__file__).resolve().parent
REPERTOIRE_PILOTE = REPERTOIRE_CATEGORIE.parent

# Le dossier du pilote est sur sys.path quand la porte est lancee par main.py ; il
# ne l est PAS quand elle est chargee par CHEMIN (suite, outils). On l ajoute donc
# nous-memes : le domicile du pilote porte alors la racine DETECTEE par le marqueur
# partage (matrice/data/commun/racine.py) et le dossier COMMUN deja installe.
if str(REPERTOIRE_PILOTE) not in sys.path:
    sys.path.insert(0, str(REPERTOIRE_PILOTE))
from constants import (  # noqa: E402
    REPERTOIRE_COMMUN,
    REPERTOIRE_MATRIX,
    CHEMIN_ENTONNOIR,
)

# LES NOMS DE CE FICHIER : la racine du workspace (celle que le pilote DETECTE) et
# le dossier PARTAGE, ou vivent le FORMAT du canal (`passerelle_user`) et la carte
# ASCII (`carte_ascii`) -- deux domiciles qui se LISENT, jamais ne se recopient.
REPERTOIRE_MATRICE = REPERTOIRE_MATRIX
COMMUN = REPERTOIRE_COMMUN
if not (COMMUN / "passerelle_user.py").is_file():
    raise RuntimeError("Structure inattendue : " + str(COMMUN)
                       + " ne porte pas le domicile du canal du user (passerelle_user.py)")
if str(COMMUN) not in sys.path:
    sys.path.insert(0, str(COMMUN))

from carte_ascii import convertir_texte  # noqa: E402,F401  (re-export)
from passerelle_user import NOM_PASSERELLE_USER  # noqa: E402

NOM_FICHIER_CANAL = "user-demandes.md"
REPERTOIRE_CANAL = REPERTOIRE_MATRICE / NOM_PASSERELLE_USER
CHEMIN_CANAL = REPERTOIRE_CANAL / NOM_FICHIER_CANAL
CHEMIN_JOURNAL = REPERTOIRE_CANAL / "archives" / "demandes-extraites.md"
CHEMIN_ENTONNOIR_MAIN = REPERTOIRE_PILOTE / "entonnoir" / "main.py"

# L ETAT qui veut dire < a extraire > : le user l a declare en phase 1 de son
# en-tete. Les autres etats ne s extraient pas -- ils se SUIVENT.
ETAT_SERVABLE = "A-FAIRE"
# Le prefixe de la trace : d OU vient l item. La trace est lue par le pilote.
MARQUE_SOURCE = "passerelle"
LARGEUR_TITRE = 90
