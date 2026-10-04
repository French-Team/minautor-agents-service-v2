"""Constantes de l'outil rendre-graphe : les sources, la sortie, et le rendu.

CE QUE L OUTIL FAIT (demande du createur 2026-09-26, item EO-449, mission MO-493) :
transformer N IMPORTE QUOI en MERMAID, puis en SVG -- pour que l agent lise le
MERMAID et que le createur lise le SVG, et que les INCOHERENCES cachees dans les
parcours d Optimus et dans le vivier deviennent VISIBLES.

LA MEMOIRE DE LA v1 EST CONSULTEE, PAS DEVINEE (bank de ressources, LECTURE SEULE) :
`cerveau-projet/agents/tools/consulter/convertir-carte-mermaid/convertir-carte-mermaid.py`
  - l. 526-598 : le parseur .mmd (id, forme, etiquette, aretes) ;
  - l. 620-649 : les RANGS (BFS puis plus long chemin, cycles casses) ;
  - l. 651-681 : la mise en page (rangs centres, ordre stable) ;
  - l. 683-807 : le rendu SVG (formes, aretes, etiquettes, en-tete, defs).
Le moteur est PORTE ici (ASCII, valeurs au domicile), jamais importe : la bank v1
vit hors de mon perimetre d ecriture, et un outil de la Matrice ne depend pas d un
fichier qu il ne possede pas.

ZERO VALEUR EN DUR : ma place se DEDUIT de ma place dans la Matrice (motif M-076 :
le module unique `data/commun/racine.py`), et le vivier se LIT a son domicile.
"""
import sys
from pathlib import Path

# --- MA PLACE (deduite ET verifiee : jamais un parents[N] a l aveugle) ----------
REPERTOIRE_OUTIL = Path(__file__).resolve().parent
REPERTOIRE_OUTILS = REPERTOIRE_OUTIL.parent
REPERTOIRE_DATA = REPERTOIRE_OUTILS.parent
if REPERTOIRE_DATA.name != "data":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_DATA) + " n est pas le dossier data/"
    )
REPERTOIRE_MATRICE = REPERTOIRE_DATA.parent
REPERTOIRE_MATRIX = REPERTOIRE_MATRICE.parent
if not (REPERTOIRE_MATRIX / "_operateur").is_dir():
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_MATRIX) + " ne porte pas _operateur/"
    )

# LE DOSSIER PARTAGE data/commun (motif unique M-076) : installe dans sys.path ICI,
# une fois. C est lui qui porte la racine (racine.py), le lancement sans fenetre
# (lancement.py) et les options (options.py).
REPERTOIRE_COMMUN = REPERTOIRE_MATRICE / "data" / "commun"
if not (REPERTOIRE_COMMUN / "racine.py").is_file():
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_COMMUN) + " ne porte pas data/commun"
    )
if str(REPERTOIRE_COMMUN) not in sys.path:
    sys.path.insert(0, str(REPERTOIRE_COMMUN))

from racine import detecter_racine  # noqa: E402  (le domicile, pas une copie)

RACINE = detecter_racine(REPERTOIRE_OUTIL)

REPERTOIRE_OPERATEUR = REPERTOIRE_MATRIX / "_operateur" / "optimus-prime"
REPERTOIRE_PARCOURS = REPERTOIRE_OPERATEUR / "parcours"
CHEMIN_INDEX_PARCOURS = REPERTOIRE_PARCOURS / "index-parcours.json"
REPERTOIRE_THEMES = REPERTOIRE_PARCOURS / "themes"
CHEMIN_FINS = REPERTOIRE_PARCOURS / "fins.json"
# LA ZONE JETABLE : les textes passent par des FICHIERS quand ils vont a la porte
# (un argument traverserait le shell, ou un accent grave est EXECUTE -- MO-142).
REPERTOIRE_JETABLE = REPERTOIRE_OPERATEUR / "tmp-optimus"
# LE LANCEUR unique de la Matrice : il resout une brique par son NOM, et c est par
# lui que passe TOUTE ecriture (la porte `ecrire`). Il vit a la RACINE de la
# Matrice (`matrix/lancer.py`) -- mesure du 2026-09-29 : le chercher sous
# `matrice/lancer.py` faisait REFUSER chaque depot, et le refus disait `can't open
# file` (un chemin faux se voit, un chemin devine en silence ne se verrait pas).
CHEMIN_LANCEUR = REPERTOIRE_MATRIX / "lancer.py"
if not CHEMIN_LANCEUR.is_file():
    raise RuntimeError("Structure inattendue : " + str(CHEMIN_LANCEUR)
                       + " n est pas le lanceur de la Matrice")

# --- LA PRODUCTION DE L OUTIL -------------------------------------------------
# Une vue est un POINT DE VUE recalcule depuis la source : elle vit a cote de sa
# source (le parcours de l operateur), pas dans les donnees de la Matrice.
DOSSIER_VUES = REPERTOIRE_OPERATEUR / "vues"
DOSSIER_MERMAID = DOSSIER_VUES / "mermaid"
DOSSIER_SVG = DOSSIER_VUES / "svg"

# --- LE VOCABULAIRE DES SOURCES (liste FERMEE) --------------------------------
SOURCE_PARCOURS = "parcours"
SOURCE_VIVIER = "vivier"
SOURCE_ARBRE = "arbre"
SOURCES = (SOURCE_PARCOURS, SOURCE_VIVIER, SOURCE_ARBRE)
# La VUE du parcours : l INDEX (les themes dans leur ordre) ou UN theme (sa suite de
# cases). Sans --theme, c est l index.
VUE_INDEX = "index"

# --- LA MEMOIRE v1, CITEE PAR SA MESURE (fichier + ligne) ---------------------
CHEMIN_MEMOIRE_V1 = ("cerveau-projet/agents/tools/consulter/convertir-carte-mermaid"
                     "/convertir-carte-mermaid.py")
MEMOIRE_V1 = (
    (CHEMIN_MEMOIRE_V1, 526, "le parseur .mmd (id, forme, etiquette)"),
    (CHEMIN_MEMOIRE_V1, 620, "les rangs : BFS puis plus long chemin, cycles casses"),
    (CHEMIN_MEMOIRE_V1, 651, "la mise en page : rangs centres, ordre stable"),
    (CHEMIN_MEMOIRE_V1, 683, "l echappement XML et le rendu des formes"),
    (CHEMIN_MEMOIRE_V1, 743, "les aretes : droite, coudee, courbe, boucle"),
    (CHEMIN_MEMOIRE_V1, 776, "l en-tete SVG (defs, marqueur, fond)"),
)

# --- LES CONSTANTES DU RENDU (portees de la v1) -------------------------------
FONTE = "Arial, Helvetica, sans-serif"
TAILLE_TEXTE = 11.5
TAILLE_ETIQUETTE = 10.5
COULEUR_FOND = "#ffffff"
COULEUR_TEXTE = "#0f172a"
COULEUR_ARETE = "#64748b"
COULEUR_ETIQUETTE = "#1e293b"
# Les formes : le STYLE appartient au dessin, jamais a la source.
FORMES = {
    "rect": {"fond": "#f8fafc", "bord": "#334155"},
    "diamond": {"fond": "#fef3c7", "bord": "#b45309"},
    "stadium": {"fond": "#e0f2fe", "bord": "#1d4ed8"},
    "appelant": {"fond": "#fce7f3", "bord": "#be185d"},
    # LA FORME DE L INCOHERENCE : elle doit SAUTER AUX YEUX dans le SVG -- c est
    # elle qui rend visible ce que le parcours cache.
    "erreur": {"fond": "#fee2e2", "bord": "#b91c1c"},
}
FORME_DEFAUT = "rect"

# --- LA GEOMETRIE DU DESSIN (portee de la v1) ---------------------------------
LARGEUR_LIBELLE_MAX = 34
PLANCHE_MIN_NOEUD = 64
HAUTEUR_MIN_NOEUD = 36
MARGE_HORIZONTALE_RANG = 40
MARGE_VERTICALE_RANG = 90
MARGE_PAGE = 50
# LA LARGEUR DE PAGE : au-dela, un rang SE REPLIE sur une ligne de plus. La v1
# laissait UNE ligne par rang -- mesure du 2026-09-29 sur le vivier reel (12
# themes, 4 categories) : 6866 px de large, une image qu on ne lit pas d un coup
# d oeil. Le repli est DECLARE ici, jamais cache dans le code.
LARGEUR_PAGE_MAX = 1500
PAS_DE_LIGNE_TEXTE = 14.0
LARGEUR_CARACTERE = 6.4
LARGEUR_CARACTERE_ETIQUETTE = 5.6

# --- LE FORMAT MERMAID (ce que l agent lit) -----------------------------------
TETE_FLUX = "flowchart TD"
MARQUE_COMMENTAIRE = "%%"

VERSION = "1.0.0"
NOM_OUTIL = "rendre-graphe"
