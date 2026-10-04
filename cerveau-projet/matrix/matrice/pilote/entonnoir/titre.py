"""Le TITRE d'un item n'est pas une ETIQUETTE -- garde de l'entonnoir de la MATRICE.

POURQUOI CE MODULE (mesure 2026-09-23, cote operateur) : DEUX items reels ont ete
deposes avec un nom du VIVIER la ou le champ attend le TITRE de la demande
(`--theme "OUTIL"`) ; la file affichait l'etiquette a la place de la phrase. Le
`theme` d'un ITEM est le TITRE (texte libre) ; le ROLE de la mission a son propre
champ (`role`, champ ferme = le vivier) -- un champ, un sens.

CE MODULE EST LE JUMEAU de `roles.est_theme_du_vivier` cote operateur : les deux
entonnoirs sont DEUX ARBRES (heritage v1/v2, chacun a SES fichiers). La lecture du
vivier passe par la PORTE du pilote de CET arbre (`commun.charger_themes_autorises`),
jamais une seconde lecture (M-042, mesure : deux copies d'une meme regle divergent
toujours en silence). Porte injoignable ou liste vide -> False : on n'invente pas
une fermeture (doctrine du vivier : jamais bloquant, une reparation du vivier
lui-meme doit rester possible).
"""
import sys
from pathlib import Path

REPERTOIRE_ENTONNOIR = Path(__file__).resolve().parent
REPERTOIRE_PILOTE = REPERTOIRE_ENTONNOIR.parent
if REPERTOIRE_PILOTE.name != "pilote":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_ENTONNOIR) + " n'est pas dans pilote/"
    )

# `append` (jamais `insert(0)`) : les modules LOCAUX de l'entonnoir (listes, mots,
# stockage, titre) restent prioritaires, sinon un module homonyme du pilote les
# masquerait et l'entonnoir mourrait.
if str(REPERTOIRE_PILOTE) not in sys.path:
    sys.path.append(str(REPERTOIRE_PILOTE))

try:
    from commun import charger_themes_autorises
except ImportError:  # degradation AVOUEE : le garde se tait, la porte le dira a l'usage
    charger_themes_autorises = None


def est_theme_du_vivier(texte):
    """Vrai si ce texte EST un nom du vivier -- donc une ETIQUETTE, jamais un titre.

    Sert au depot : un `--theme` qui est un nom du vivier est une CONFUSION DE
    CHAMPS, refusee AVANT toute ecriture (le titre de la demande serait perdu et la
    file afficherait une etiquette).
    """
    if charger_themes_autorises is None:
        return False
    cible = " ".join(str(texte).split()).lower()
    if not cible:
        return False
    try:
        noms = charger_themes_autorises()
    except Exception:  # une porte qui tombe ne bloque pas un depot : elle le DIT
        return False
    return any(str(nom).strip().lower() == cible for nom in noms)
