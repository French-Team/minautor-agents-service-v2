"""LA PROPOSITION : quels outils pour cette mission, chacun avec SON MOTIF.

REGLE : la proposition ne POSE rien (une proposition n ouvre rien -- meme doctrine que
le classement de l entonnoir). Elle est IMPRIMEE avec le geste exact qui la pose, et
c est l OPERATEUR qui decide.

COMMENT ELLE MATCHE, et pourquoi ainsi : les mots UTILES du theme et de l objectif
sont confrontes au NOM et au BUT de chaque brique SERVIE. Une brique NON SERVIE ne
peut pas etre proposee : la porte de preparation refuserait son nom, et deux avis
contradictoires pour la meme question seraient un piege. Une brique MUETTE non plus :
sans but, il n y a rien a matcher -- et `verifier` l accuse deja.

Le MOTIF est la liste des mots PARTAGES, jamais un score opaque : l operateur doit
pouvoir NE PAS etre d accord.

LA DERIVATION EST CONSOMMEE de son domicile partage (data/commun/
recherche_mission.py, `mots_utiles`, EO-131 + M-076) : deux decoupages du meme
francais divergeraient, et la question de recherche et la proposition parleraient
deux langues. La seule valeur d ici : LA BORNE DE LA DEMANDE, plus large que celle
d une question -- un objectif de mission est plus long qu un sujet de question.
"""
from constants import CLES, NOMBRE_MOTS_PROPOSITION, STATUT_VIVANT
from recherche_mission import mots_utiles


def mots_de_la_demande(theme, objectif, nombre=NOMBRE_MOTS_PROPOSITION):
    """Les mots UTILES de la demande, bornes -- par la derivation PARTAGEE.

    Rend une LISTE (l ordre et la deduplication viennent du domicile partage), vide
    si rien d utile : l appelant le DIT, il n invente pas des mots a la place.
    """
    return mots_utiles(str(theme or "") + " " + str(objectif or ""), nombre)


def proposer(entrees, mots, plafond):
    """(propositions, ecartees, nombre_de_candidates) -- bornees par le PLAFOND.

    Les ECARTEES par le plafond sont rendues AVEC leur motif : un plafond muet se
    lirait comme une liste complete (L-055). Une CIBLE se lit SANS borne (le nom et
    le but entiers) : la tronquer ferait manquer des mots en silence.
    """
    candidates = []
    for entree in entrees:
        if not entree.get(CLES["servi"]):
            continue
        if entree.get(CLES["statut"]) != STATUT_VIVANT:
            continue
        mots_du_but = mots_utiles(entree.get(CLES["but"], ""))
        mots_du_nom = mots_utiles(entree.get(CLES["nom"], ""))
        partages = [mot for mot in mots if mot in mots_du_but or mot in mots_du_nom]
        if not partages:
            continue
        candidates.append({
            "nom": entree.get(CLES["nom"], ""),
            "proprietaire": entree.get(CLES["proprietaire"], ""),
            "motif": partages,
            "score": len(partages),
        })
    candidates.sort(key=lambda item: (-item["score"], item["nom"]))
    return candidates[:plafond], candidates[plafond:], len(candidates)
