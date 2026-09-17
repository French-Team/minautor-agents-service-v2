#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""vocabulaire_invisible.py -- le DOMICILE du VOCABULAIRE interdit L-016/CV-006 (MO-153).

Deuxieme moitie du contrat d invisibilite :
  - les ZONES interdites a la LECTURE vivent dans data/commun/invisibilite.py ;
  - le VOCABULAIRE interdit a la LIVRAISON vit ici.

Pourquoi un domicile : la liste etait RECOPIEE dans les deux pilotes
(`filtrer_pour_cameleon`, Flux 1 et Flux 2) et l audit d invisibilite en tenait
une troisieme version, plus courte. Une valeur ecrite trois fois derive en
silence (M-076 ; L-100/L-102).

Regle : un CONTENU qui nomme l invisible ne se LIVRE jamais a un agent qui ne
doit pas le connaitre (lecon gravee -> injection ; entree de BDD -> moteur de
recherche). Retirer l item ENTIER, jamais le caviarder : une phrase caviardee
laisse deviner qu il y avait un secret.

MESURE DU 2026-09-17 (MO-153) : la livraison par l injection etait PROPRE
(90 lecons livrees, 0 mot interdit) -- c est le MOTEUR qui servait la BDD brute
(101 entrees nommant l invisible, dont la BDD SUIVI-OPTIMUS declaree exclue).
"""

# Les mots qui trahissent l invisible. Union des trois listes qui existaient
# (deux pilotes + audit) : AUCUNE ne contenait les trois autres.
MOTS_INTERDITS = (
    "optimus-prime",
    "optimus",
    "_operateur",
    "tmp-optimus",
    "suivi-optimus",
    "espions-optimus",
    "remorque",
)


def contient_invisible(texte):
    """True si le texte nomme l invisible (case-insensitive)."""
    if not texte:
        return False
    minuscule = str(texte).lower()
    return any(mot in minuscule for mot in MOTS_INTERDITS)


def contient_invisible_item(item):
    """Meme regle, appliquee a un ITEM de BDD (dictionnaire, liste ou chaine).

    Les consommateurs n ont pas la meme forme d entree (lecon, entree de BDD,
    theme) : le domicile joint TOUT ce qui est textuel (valeurs et listes) et
    laisse le tri fin aux appelants qui ont une forme plus precise.
    """
    if isinstance(item, dict):
        morceaux = []
        for valeur in item.values():
            if isinstance(valeur, str):
                morceaux.append(valeur)
            elif isinstance(valeur, list):
                morceaux.append(" ".join(str(x) for x in valeur))
        return contient_invisible(" ".join(morceaux))
    return contient_invisible(item)
