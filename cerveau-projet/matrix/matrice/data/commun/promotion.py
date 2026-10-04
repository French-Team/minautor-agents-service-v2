"""DOMICILE de la PROMOTION AUTOMATIQUE (EO-457, demande createur 2026-09-27).

POURQUOI CE FICHIER EXISTE : le createur a demande que < un item plus important
que la mission en cours se reclasse seul > et que les CARTES D IDENTITE portent
DEUX champs d importance (`gravite` puis `niveau`, domicile carte_identite.py).
La REGLE de comparaison et de reclassement vit ICI, une seule fois (M-076) :
l entonnoir, le pilote et les cobayes la CONSOMMENT, ils ne la recopient pas.

CE QUE LA REGLE DIT, ET RIEN DE PLUS :
  - < plus important > = la cle d importance du DOMICILE de la carte d identite :
    GRAVITE (la bande) d abord, puis NIVEAU (le raffinement DANS la bande) ;
  - STRICTEMENT plus important : une importance EGALE ne reclasse RIEN -- c est le
    contre-temoin, et la stabilite est une GARANTIE, pas un hasard ;
  - le reclassement ne touche JAMAIS ce qui PRECEDE la position demandee : la
    mission EN COURS est menee a son TERME (serie stricte), seul l ORDRE des
    SUIVANTS change.

Ce module ne lit AUCUN fichier : il ne juge et n ordonne que des dicts.
"""
from carte_identite import importance_de_carte, plus_important


def cle_importance(entree):
    """La cle d importance d un item ou d une MISSION (dict), par le DOMICILE."""
    return importance_de_carte(entree)


def promotion_requise(entree, reference):
    """Vrai si `entree` est STRICTEMENT plus importante que `reference`.

    Une importance EGALE rend False : rien ne bouge (contre-temoin).
    """
    return plus_important(cle_importance(entree), cle_importance(reference))


def reclasser_par_importance(entrees):
    """Copie des entrees triee par importance (la plus importante en tete).

    Tri STABLE : a importance EGALE, l ordre d arrivee est CONSERVE -- une
    promotion ne bouscule jamais ce qui n a pas a bouger.
    """
    return sorted(entrees, key=cle_importance)


def reclasser_apres(entrees, position):
    """La sequence : INCHANGEE jusqu a `position` incluse, RECLASSEE au-dela.

    `position` est l INDEX de la PREMIERE entree a reclasser -- dans un lot ordonne
    (L-151/MO-470), c est l index de la mission EN COURS plus un : < on reclasse a
    partir de la position suivant la mission en cours > (decision du createur).
    Une position <= 0 reclasse TOUT ; une position au-dela rend la sequence telle
    quelle.
    """
    if position <= 0:
        return reclasser_par_importance(entrees)
    if position >= len(entrees):
        return list(entrees)
    return list(entrees[:position]) + reclasser_par_importance(entrees[position:])
