"""Domicile unique de la carte ASCII de la Matrice (MO-210).

Une seule carte, DEUX consommateurs : le scan de maintenance (outil
corriger-ascii, lance par la routine veille-flux) et la porte `ecrire`, passage
oblige de TOUTE ecriture. La carte vivait dans les constantes de l'outil : la
porte aurait alors lu un fichier d'outil, et une seconde copie aurait ete deux
verites -- l'une corrigeant ce que l'autre ignorait.

Les deux outils s'ajoutent deja data/commun a sys.path (motif M-076) : ce
domicile est importable tel quel, sans machinerie nouvelle.

Doctrine : tout caractere ABSENT de la carte est laisse tel quel et SIGNALE --
il n'est jamais devine. La porte `ecrire` en fait un REFUS (rien n'est ecrit).
"""
import re


CARTE_CONVERSION = {
    "\u00e0": "a", "\u00e2": "a", "\u00e4": "a",
    "\u00e9": "e", "\u00e8": "e", "\u00ea": "e", "\u00eb": "e",
    "\u00ee": "i", "\u00ef": "i",
    "\u00f4": "o", "\u00f6": "o",
    "\u00f9": "u", "\u00fb": "u", "\u00fc": "u",
    "\u00e7": "c",
    "\u00ff": "y",
    "\u00c0": "A", "\u00c2": "A", "\u00c4": "A",
    "\u00c9": "E", "\u00c8": "E", "\u00ca": "E",
    "\u00ce": "I",
    "\u00d4": "O",
    "\u00d9": "U", "\u00db": "U",
    "\u00c7": "C",
    "\u0153": "oe", "\u0152": "OE",
    "\u2018": "'", "\u2019": "'",
    "\u201c": '"', "\u201d": '"',
    "\u00ab": "<", "\u00bb": ">",
    "\u2013": "-", "\u2014": "-",
    "\u2026": "...",
    chr(0x00A0): " ",
    chr(0x2192): "->",
}

# L ORDINAL (2026-10-03, demande user-demandes l.205) : en francais, "le 1
# etage" -- le symbole de DEGRE (U+00B0) apres le 1 -- signifie "le PREMIER
# etage". NFKD ne decompose pas ce caractere : il disparaissait donc entier, et
# l ordinal perdu rendait la phrase fausse.
#
# BORNAGE (decision createur 2026-10-04). La premiere version mettait U+00B0
# DANS la carte -- donc partout, sans condition. Le controle de contrat l a vu
# tout de suite : "Temperature : 20 C" (vingt degres) devenait "20erC", et la
# porte ne REFUSAIT plus rien. Un caractere n a pas de sens ASCII unique : un
# remede trop large casse le sens au lieu de le preserver.
#
# DONC U+00B0 n EST PLUS dans la carte. Il obeit a une regle CONTEXTUELLE qui
# ne vaut que pour l ORDINAL : le couple "1 + degre" suivi d un ESPACE devient
# "1er". Tout le reste -- une temperature, un cap, un angle -- reste HORS
# CARTE, donc signale, donc REFUSE. Quand le sens n est pas sur, la porte dit
# non : c est sa doctrine, et elle vaut mieux qu une conversion qui invente.
#
# Les BORNES ne sont pas decoratives : ce sont elles, le bornage.
# A GAUCHE, un chiffre different : sans elle, "11 C" (onze degres) deviendrait
# "11er".
# A DROITE, un ESPACE ou la fin de ligne : sans elle, "un angle de 1."
# deviendrait "1er." -- et surtout "1 C" deviendrait "1erC", le cas qu on
# voulait justement epargner.
# Ces deux bornes rendent le cas SERRE impossible : seuls "le 1 etage",
# "le 1. etage" et un "1." en fin de ligne sont convertis. Tout le reste passe
# par la carte, qui ne sait pas U+00B0, donc le REFUSE. C est le compromis
# voulu : convertir moins, mais ne jamais deformer un sens.
#
# La regle vit ici, et nulle part ailleurs (M-076), et elle s applique AVANT la
# boucle caractere par caractere : ce n est pas une entree de carte, parce
# qu une carte ne voit qu UN caractere a la fois, alors qu ici le sens vient du
# VOISINAGE.
#
# CE QUE LES RAPPORTEURS VOIENT : les deux consommateurs qui interrogent
# CARTE_CONVERSION caractere par caractere (`fragment.py`, `corriger-ascii`)
# ne verront PLUS U+00B0 dans la carte : ils le diront "personne ne sait le
# convertir", meme dans le cas ordinal ou la porte, elle, le corrige. C est
# une SOUS declaration, donc le bon sens d erreur : on ne promet pas une
# conversion qu on ne peut pas decider seul. La porte, elle, applique la regle
# -- et c est elle qui autorise l ecriture.
MOTIF_ORDINAL = re.compile("(?<![0-9])1" + chr(0x00B0) + r"(?=[\s]|$)")
REMEDE_ORDINAL = "1er"


def convertir_texte(texte):
    """Retourne (texte_converti, caracteres_non_convertis) via la carte.

    L ORDINAL passe d ABORD (regle contextuelle, ci-dessus) : le reste suit la
    carte, caractere par caractere. Un caractere que personne ne sait convertir
    reste DANS le texte ET dans la liste des non convertis -- c est ce qui
    permet a la porte de REFUSER (rien n est ecrit) et a l outil de maintenance
    de nommer le point de code.
    """
    texte = MOTIF_ORDINAL.sub(REMEDE_ORDINAL, texte)
    non_convertis = []
    morceaux = []
    for caractere in texte:
        if ord(caractere) <= 127:
            morceaux.append(caractere)
            continue
        remplacement = CARTE_CONVERSION.get(caractere)
        if remplacement is None:
            non_convertis.append(caractere)
            morceaux.append(caractere)
        else:
            morceaux.append(remplacement)
    return "".join(morceaux), non_convertis
