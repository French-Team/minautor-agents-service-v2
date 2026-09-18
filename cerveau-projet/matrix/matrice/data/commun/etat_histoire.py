"""MOTIF UNIQUE : separer l'ETAT de l'HISTOIRE dans un journal (M-076, jamais recopie).

Un journal en AJOUT SEUL est une HISTOIRE : il ne recoit que des FAITS. Un etat
qui se repete a chaque passe n'est PAS un fait -- c'est un etat, et un etat se lit
dans un fichier d'etat (lecon L-071).

Le meme defaut a ete trouve QUATRE fois, chaque fois sur un journal different :
  - le routeur de maintenance recopiait le tableau des anomalies a chaque passe
    (510 lignes identiques a la date pres sur 512 : 99,4 %, MO-080) ;
  - l'espion-integrite journalisait ses 14 observations a chaque tour
    (504 134 observations pour 36 000 passes : 93,2 % du journal, MO-081) ;
  - les deux vigies ecrivent la meme ligne `passe` a chaque tour
    (vigie-profil 194 fois la meme ligne sur 330 ; vigie-portes 105 sur 204).

Ce module est le moteur PARTAGE (data/commun, comme rotation_journal.py) : les
routines l'utilisent avec LEURS donnees, elles ne le recopient pas (lecon L-029 :
un moteur recopie quatre fois diverge quatre fois).

Trois choses s'y trouvent, et rien d'autre :

  1. UNE SIGNATURE COMPARABLE d'un fait (`signature_fait`) : la donnee dont les
     champs VOLATILS ont ete retires. Un champ volatil ne fait pas un fait -- la
     date de la passe, le motif de decision, un compteur qui repart a zero : les
     inclure ferait changer la signature a chaque tour et l'absorption ne se
     ferait jamais (c'est exactement la faute attrapee par le cobaye de MO-080,
     ou le RETOUR du compteur de routage a zero passait pour un fait).

  2. UNE DECISION PURE (`decision_fait`) : un fait s'ecrit si la signature a
     change. Fonction pure -- meme reponse pour memes donnees, donc testable sans
     disque ni horloge, et donc PIEGEABLE par un cobaye (lecon L-032).

  3. LES DEUX MOTIFS de cette decision, journalises : la redondance supprimee est
     TRACEE, jamais silencieuse.

Ce module ne connait AUCUN format de journal : il rend une chaine comparable et
un couple (notable, motif). L'ecriture reste dans la routine (son `commun.py`),
parce que c'est elle qui connait son etat court et son journal.

ATTENTION (lecon L-029) : le nom de ce module ne doit jamais etre celui d'une
categorie importable d'un pilote ou d'une routine (`commun.py`, `constants.py`,
`tour/`...). `etat_histoire.py` est unique et non ambigu.
"""
import json

# L IDENTITE D UN FAIT : ce qui DIT ce qui s est passe (le fait lui-meme), par
# opposition aux champs d ETAT (la date de la passe, le tableau courant, le compteur
# absorbe). Un fait SANS identite est INDISTINGUABLE de la recopie du meme etat :
# le garde de non-redondance l accuse alors a juste titre, et l histoire ne peut plus
# repondre "que s est-il passe ?" (EO-163, decision du createur 2026-09-18 : le fait
# PORTE l identite de l evenement -- le garde, lui, ne s affaiblit pas).
CHAMP_IDENTITE = "identite"

# Motifs de la DECISION (journalises, jamais recopies dans la logique).
MOTIF_CHANGEMENT = "changement"
MOTIF_ABSORBEE = "absorbee"


def sans_volatils(donnees, volatils=()):
    """Copie de `donnees` sans les champs VOLATILS (une donnee brute est rendue telle quelle).

    Les volatils sont ceux qui bougent a chaque passe SANS rien dire : la date de
    la passe, le motif de decision, le nombre de passes absorbees. Les laisser
    dans la signature rendrait chaque passe "nouvelle" -- et le journal
    redeviendrait le battement de coeur qu'on vient de supprimer.
    """
    if not isinstance(donnees, dict):
        return donnees
    ecartes = {str(volatil) for volatil in volatils}
    return {cle: valeur for cle, valeur in donnees.items() if cle not in ecartes}


def signature_fait(donnees, volatils=()):
    """Signature COMPARABLE d'un fait : la donnee sans ses champs volatils.

    `sort_keys=True` rend la signature insensible a l'ORDRE des clefs (un
    dictionnaire reordonne n'est pas un fait nouveau) ; pour une liste, c'est
    l'ordre de la liste qui compte, et c'est a l'appelant de la trier s'il veut
    ignorer cet ordre.
    """
    return json.dumps(sans_volatils(donnees, volatils), sort_keys=True, ensure_ascii=True)


def decision_fait(signature_actuelle, signature_memoire):
    """(notable, motif) : DECISION PURE -- cette passe laisse-t-elle un fait ?

    Vrai si la signature a change (une premiere passe est un fait : il n'y a rien
    a comparer). Faux = la passe a vu exactement la meme chose : c'est un ETAT,
    il part dans l'etat court, et l'histoire n'y gagnerait qu'une ligne de plus a
    lire pour retrouver la seule qui dise quelque chose.
    """
    if signature_actuelle != signature_memoire:
        return True, MOTIF_CHANGEMENT
    return False, MOTIF_ABSORBEE
