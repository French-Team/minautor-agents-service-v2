"""Constantes du REGISTRE DES OUTILS (EO-314) -- perimetre, cible, empreinte.

ZERO VALEUR EN DUR : la logique CONSOMME ces valeurs, elle ne les contient pas.
Trois choses sont declarees ici, et une seule fois :
  1. LE PERIMETRE -- quels domiciles de briques sont inventories, et a qui ils
     appartiennent. Le PROPRIETAIRE n est jamais devine : il se DEDUIT du domicile,
     et cette table est la SEULE source de la correspondance.
  2. LA CIBLE -- ou vit la BDD (matrice/data/, le domicile des BDD de la Matrice).
  3. LA FORME DE L EMPREINTE -- sha256 du TEXTE SOURCE lu, jamais du fichier entier :
     c est le texte qui est RANGE dans la BDD, donc c est lui qui perime.

POURQUOI UNE BDD UNIQUE ET PAS TROIS (decision createur 2026-09-20) : l injection
croise DEJA les flux pour une seule mission (une mission dev recoit des outils
d Optimus ET de la Matrice). Trois domiciles = trois lectures a chaque proposition,
et deux endroits ou le meme outil peut etre declare. Une BDD, une colonne
`proprietaire`, trois VUES.

LES RACINES SERVIES NE SONT PAS RECOPIEES : elles sont LUES dans l extracteur
(injection/modes_emploi.py RACINES), qui est le domicile de ce que l INJECTION
sait servir. Cette table n ajoute que les domiciles SUPPLEMENTAIRES (inventories,
non servis) -- deux verites pour un meme perimetre divergeraient.
"""
import sys
from pathlib import Path

REPERTOIRE_OUTIL = Path(__file__).resolve().parent
# L outil vit dans outils/registre-outils/ ; la BDD vit deux niveaux au-dessus (data/).
REPERTOIRE_DATA = REPERTOIRE_OUTIL.parent.parent
if REPERTOIRE_DATA.name != "data":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_DATA) + " n est pas le dossier data/"
    )
NOM_BDD = "registre-outils.json"

# data/commun (motif unique M-076) : installe le dossier partage dans sys.path en
# REMONTANT jusqu a lui -- jamais un `parents[N]` nu : le nombre d etages n est pas une
# adresse stable (L-013 / MO-088, et le controle `chemins` le refuse, a raison).
_courant = REPERTOIRE_OUTIL
for _ in range(30):
    if (_courant / "commun" / "racine.py").is_file():
        sys.path.insert(0, str(_courant / "commun"))
        break
    _courant = _courant.parent
else:
    raise RuntimeError("data/commun introuvable en remontant.")

from cible import racine_matrice  # noqa: E402

RACINE_MATRIX = racine_matrice(REPERTOIRE_OUTIL)  # matrix/ (base des chemins relatifs)
RACINE_MATRICE = RACINE_MATRIX / "matrice"        # matrix/matrice/
CHEMIN_BDD = REPERTOIRE_DATA / NOM_BDD
# L EMPREINTE ETALON, voisine de la BDD : la forme attendue par l espion d integrite
# de la Matrice (nom + ".sha256", motif de bdd-conservation) -- le registre est une
# BDD REGENEREE, donc il doit reposer son etalon a chaque publication.
CHEMIN_EMPREINTE = CHEMIN_BDD.with_name(CHEMIN_BDD.name + ".sha256")
TAILLE_BLOC_LECTURE = 65536

# L EXTRACTEUR : ce que l injection SAIT SERVIR (racines + lecture de brique).
PILOTE = RACINE_MATRIX / "_operateur" / "optimus-prime" / "pilote"
CHEMIN_EXTRACTEUR = PILOTE / "injection" / "modes_emploi.py"
# Le PLAFOND de la proposition est celui de l INJECTION : lu a SON domicile, jamais recopie.
CHEMIN_PLAFOND = PILOTE / "constants.py"
NOM_CONSTANTE_PLAFOND = "PLAFOND_OUTILS_MODE_EMPLOI"

# LE PROPRIETAIRE de chaque racine SERVIE (l ordre suit celui de l extracteur).
PROPRIETAIRES_RACINES = {
    "outils": "optimus",          # les outils de l operateur
    "combos": "optimus",          # les combos de l operateur
    "super-combos": "optimus",    # les super-combos de l operateur
    "outils-matrice": "matrice",  # les outils de la Matrice
}
# LES DOMICILES SUPPLEMENTAIRES : inventories, NON servis a l injection (l extracteur
# ne les connait pas). Le troisieme proprietaire est le CAMELEON -- mesure du
# 2026-09-20 : il n a PAS de domicile de briques distinct des outils de la Matrice ;
# ses propres briques sont son pilote (matrice/pilote/). C est cette mesure, et pas
# un choix, qui separe `matrice` (les outils servis) de `cameleon` (son pilote).
DOMICILES_SUPPLEMENTAIRES = (
    ("optimus", "_operateur/optimus-prime/pilote"),
    ("matrice", "matrice/routines"),
    ("cameleon", "matrice/pilote"),
)

# LES CHAMPS de la BDD : un nom, une declaration (la logique les consomme).
CLES = {
    "nom": "nom",
    "proprietaire": "proprietaire",
    "domicile": "domicile",
    "chemin": "chemin",
    "servi": "servi_a_l_injection",
    "origine": "origine",
    "but": "but",
    "snippet": "snippet",
    "empreinte": "empreinte_texte",
    "statut": "statut",
}
# LA BORNE des mots de la DEMANDE dans une proposition : plus large que celle d une
# question (NOMBRE_MOTS_QUESTION, EO-131) -- un objectif de mission est long -- mais
# bornee quand meme : chaque mot partage suffit a faire entrer une brique, donc une
# demande SANS borne ratisserait tout le parc et ne proposerait plus rien.
NOMBRE_MOTS_PROPOSITION = 24
CLE_OUTILS = "outils"
CLE_PERIMETRE = "perimetre"
CLE_HOMONYMES = "homonymes"
CLE_GENERE = "genere_le"
IDENTITE = {"type": "registre-outils", "version": 1}

# LE STATUT d une brique : VIVANTE (elle dit son usage) ou MUETTE (elle ne dit rien --
# enregistree QUAND MEME, et ACCUSEE : un silence enregistre se repare, un silence
# absent ne se voit pas). Jamais de troisieme statut devine.
STATUT_VIVANT = "vivant"
STATUT_MUET = "muet"
STATUTS = (STATUT_VIVANT, STATUT_MUET)

ENCODAGE = "utf-8"
INDENTATION = 1
SUFFIXE_BRIQUE = ".py"
NOM_ENTREE = "main.py"
