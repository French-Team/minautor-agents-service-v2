"""Domicile unique de la ZONE DES SOURCES du createur (MO-377).

UNE zone, UNE declaration, TROIS consommateurs (M-076) : la porte `ecrire`
(passage oblige de toute ecriture), le garde `garde-ascii` et le scan de
maintenance `corriger-ascii`. Avant ce module, la MEME decision vivait dans deux
fichiers -- et PAS dans la porte : deux instruments de la meme maison disaient
deux choses differentes sur la meme zone (mesure MO-377 du 2026-09-24 : la porte
REFUSAIT un document de docs/ en proposant un remede qui MUTILERAIT la source,
pendant que le garde l exemptait en mode dossier et l accusait en mode fichier).

LA DECISION EST DEJA ECRITE, a son domicile -- c est elle qui fait foi :
`_operateur/optimus-prime/regles-immuables/ascii-strict.md` :
    EXCEPTION (decision createur) : `docs/` est la zone des SOURCES (vision,
    transcriptions, notes) -- LECTURE SEULE. Elle est EXEMPTEE : accents, degres
    et emojis y sont legitimes, et aucun scan ne doit y lever d alerte.
et `docs/docs-readme.md` declare les banks de lecture externe INTACTES, jamais
modifiees, jamais traduites.

ARBITRAGE MO-377 (mesure du 2026-09-24) : des trois issues proposees, la seule
coherente avec cette regle est (c) -- la Matrice n ECRIT JAMAIS dans `docs/`, et
le passage oblige le REFUSE en le DISANT. Les deux autres sont ECARTEES :
  (a) faire de `docs/` une exemption ASCII de la PORTE aurait ouvert l ecriture
      dans une zone que la regle declare LECTURE SEULE ;
  (b) laisser la porte telle quelle laissait son remede (< ajouter la conversion
      a carte_ascii.py >) CONTREDIRE docs-readme.md : le suivre aurait mutile la
      source.
Le refus ne remplace AUCUN chemin de recouvrement : un source suivie par git se
recouvre par git (git checkout HEAD -- <chemin>), une source VIVANTE appartient au
createur. Un document NET que la Matrice doit produire se produit A COTE (ou dans
une zone declaree), jamais par-dessus la source.

La zone est designee par sa POSITION : le PREMIER segment du chemin, relatif a la
racine de la Matrice. C est ce qui distingue `docs/` (les sources du createur) de
`matrice/docs/` (les documents INTERNES de la Matrice, ecrivables par elle).
"""
from cible import forme_canonique

NOM_ZONE_SOURCES = "docs"
MOTIF_ZONE_SOURCES = ("zone des SOURCES du createur (vision, transcriptions, notes) -- "
                      "LECTURE SEULE, decision createur")


def chemin_canonique(chemin):
    """La forme canonique (relative a la racine de la Matrice), en forme POSIX.

    Le domicile de FORME est CONSOMME (cible.forme_canonique), jamais recopie :
    une forme qui depend de qui l ecrit ne se compare ni ne se mesure (EO-363).
    """
    return forme_canonique(chemin).replace("\\", "/")


def est_zone_sources(chemin):
    """True si <chemin> designe la zone des sources (PREMIER segment = docs)."""
    canonique = chemin_canonique(chemin)
    if not canonique:
        return False
    return canonique.split("/", 1)[0] == NOM_ZONE_SOURCES


def refus_zone_sources(chemin):
    """Le refus NOMME la zone, sa raison et les REMEDES -- None si hors zone.

    Trois sorties, jamais une quatrieme : hors zone (None), dans la zone (le
    refus). Le refus est ecrit en ASCII strict et il est COMPLET : il dit ce qui
    n a PAS ete fait (rien n a ete ecrit), POURQUOI, et les trois remedes reels.
    """
    if not est_zone_sources(chemin):
        return None
    return ("REFUS (code 2) : " + str(chemin) + " est dans " + NOM_ZONE_SOURCES + "/ -- "
            + MOTIF_ZONE_SOURCES + ". RIEN n a ete ecrit.\n"
            "  La porte ECRIRE ne publie JAMAIS dans cette zone : un source n est ni recree "
            "ni corrige par la Matrice.\n"
            "  Le remede n est PAS d ajouter le caractere a la carte ASCII "
            "(matrice/data/commun/carte_ascii.py) : cela mutilerait la source.\n"
            "  REMEDE 1 (source suivie par git) : la recouvrer par git -- "
            "git checkout HEAD -- " + str(chemin) + "\n"
            "  REMEDE 2 (source VIVANTE, ex. IMPERATIF.md) : elle appartient au createur.\n"
            "  REMEDE 3 (document NET a produire) : l ecrire A COTE, ou dans une zone "
            "declaree, jamais par-dessus la source.\n"
            "  Regle qui fait foi : _operateur/optimus-prime/regles-immuables/ascii-strict.md "
            "(EXCEPTION docs/) + docs/docs-readme.md (banks intactes).")
