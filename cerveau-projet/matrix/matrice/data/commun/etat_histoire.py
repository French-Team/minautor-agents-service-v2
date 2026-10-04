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

# --- LE RECUL D UN TEMOIN : la fenetre d absorption (MO-097, MO-494) ----------
# LA QUESTION : un temoin qui porte `0 passe absorbe` est-il en DEFAUT, ou
# simplement dans une FENETRE ou il n a pas encore eu l OCCASION d absorber ?
#
# Ce que la mesure a montre (2026-09-27, MO-494) : le lanceur de non-regression a
# rendu KO sur `passe-absorbee-sur-le-service : 0 passe(s) sans fait absorbee(s)`
# alors que le service etait SAINT -- replay direct deux minutes plus tard :
# VERDICT OK (1 passe absorbe), l etat ayant ete ECRIT a 07:52:22 pour une cadence
# declaree d environ 60 s. La suite jugeait un ETAT AU MOMENT DU BALAYAGE : entre
# la ligne servie et la passe suivante, `0` est NORMAL. Accuser la fait crier sur
# un service sain, et un rouge faux coute plus cher qu aucun rouge (L-055).
#
# POURQUOI CETTE DECISION VIT ICI, ET PAS DANS UN GARDE (M-076, lecon L-211) :
# elle avait ete ecrite dans UN SEUL des deux gardes de la maison
# (`verifier-observations-non-redondantes.py`, MO-097) ; son voisin
# `verifier-historique-non-redondant.py`, qui juge la MEME propriete sur la MEME
# routine, l ignorait -- et accusait a tort. Une decision ecrite dans l instrument
# qui la consomme n existe pas pour les autres : elle est ici, UNE fois, et les
# deux gardes la CONSOMMENT.
#
# JUGER SANS ATTENDRE (regle immuable : attente-ne-prouve-rien) : ce n est pas au
# garde d ATTENDRE une cadence -- c est a lui de LIRE l age de l etat et de le
# comparer a la cadence que la ROUTINE DECLARE (jamais recopiee ici : elle est
# passee en argument, son domicile est `constants.py` de la routine).
RECUL_INSUFFISANT = "recul-insuffisant"


def recul_insuffisant(passes_absorbes, age_etat_secondes, cadence_declaree_secondes,
                      battement_mesure_secondes=None):
    """(bool, motif) : la FENETRE d absorption est-elle encore ouverte ?

    Rend (True, motif) quand le temoin doit etre EPARGNE : aucune passe n a encore
    eu l occasion d absorber. Le motif DIT l age et la fenetre accordee -- un
    epargne muet se lirait comme un vert de complaisance (L-055).

    Rend (False, motif) quand l accusation tient : un recul SUFFISANT existe et
    rien n a ete absorbe. Le motif dit alors ce qui manque pour epargner quand
    l age ou la cadence n ont pas pu etre LUS : le critere n est pas prouve, donc
    le temoin n est PAS epargne -- un controle qui ne peut pas prouver se tait sur
    l epargne, jamais sur l ecart.

    LA FENETRE VALUT LE BATTEMENT MESURE (EO-559, 2026-10-02). Elle valait la seule
    cadence DECLAREE, qui est une cadence de SOMMEIL : le service dort entre deux
    passes de toute la duree de la passe. Mesure sur routeur-maintenance : 30 s
    declarees contre un battement median de 61 s (60, 60, 61, 71) -- le garde
    accusait donc une routine SAINE pendant environ 31 s sur 61, et le faux
    positif a ete observe en direct (lecon L-076 : un battement se resume par un
    ecart median, jamais par une cadence supposee).

    `battement_mesure_secondes` est donc consume par le moteur partage
    `battement.battement_median`, sur la serie que la routine publie deja. La
    cadence DECLAREE reste un PLANCHER : le battement peut l ouvrir, jamais la
    resserrer sous l intervalle reel. Quand le battement n est pas mesurable, la
    cadence declaree fait foi -- on ne COMPTE PAS les passes pour les attendre
    (doctrine `attente-ne-prouve-rien`, deja ecrite dans verifier-cadence.py).
    """
    if int(passes_absorbes or 0) >= 1:
        return False, ""
    age = age_etat_secondes
    cadence = cadence_declaree_secondes
    if age is None:
        return False, ("age de l etat ILLISIBLE : la fenetre ne peut pas etre mesuree,"
                       " donc elle n est pas accordee")
    if cadence is None or float(cadence) <= 0:
        return False, ("cadence declaree ILLISIBLE : la fenetre ne peut pas etre mesuree,"
                       " donc elle n est pas accordee")
    # LE BATTEMENT ELARGIT, IL NE RESSERRE PAS. Un battement nul ou negatif
    # (serie abitee) est sans valeur : il ne Decide de rien.
    fenetre = float(cadence)
    mesure = None
    try:
        candidat = float(battement_mesure_secondes)
    except (TypeError, ValueError):
        candidat = None
    if candidat is not None and candidat > fenetre:
        fenetre = candidat
        mesure = candidat
    if int(age) < fenetre:
        portee = ("un battement MESURE de " + str(mesure) + " s")
        if mesure is None:
            portee = "la cadence declaree de " + str(cadence) + " s"
        return True, (RECUL_INSUFFISANT + " : etat vieux de " + str(int(age))
                      + " s pour " + portee
                      + " -- l absorption vient SEULE, a la passe suivante"
                      " (aucune attente requise)")
    return False, ""

def battement_de_passes(dernieres_passes):
    """(battement, motif) : l ecart MEDIAN entre deux passes reelles.

    La MESURE de la fenetre, a cote de sa DECISION (`recul_insuffisant`), pour la
    meme raison que `age_secondes` : les deux gardes qui consomment la decision
    lisaient l un et l autre le meme etat de service, et l un des deux calculait
    son age pendant que l autre ignorait la serie. Le moteur de la mediane est le
    PARTAGE `battement.py` (lecon L-076) -- il ne se recopie pas.

    Rend (None, motif) quand le recul manque : une serie trop courte ne se comble
    JAMAIS par une valeur inventee. Les DEUX formes d horodatage sont essayees
    (celles que `FORMATS_HORODATAGE` declare deja dans ce module) : une forme
    fractionnaire qui ne se lirait pas ferait rendre None, donc une accusation
    sur un temoin frais -- c est exactement le defaut mesure le 2026-09-29.
    """
    try:
        import battement as moteur  # domicile partage, meme dossier
    except ImportError:  # pragma: no cover -- moteur absent : on le DIT
        return None, "moteur de battement absent : le repli est la cadence declaree"
    if not dernieres_passes:
        return None, "aucune passe publiee : le repli est la cadence declaree"
    for format_essaie in FORMATS_HORODATAGE:
        mesure, _dernier = moteur.battement_median(dernieres_passes, format_essaie)
        if mesure is not None:
            return mesure, ("battement median mesure sur "
                            + str(len(dernieres_passes)) + " passes publiees")
    return None, ("recul insuffisant pour mesurer un battement : le repli est la"
                  " cadence declaree, on ne compte PAS les passes pour les attendre")


# --- L AGE D UN TEMOIN (la mesure de la decision ci-dessus) --------------------

# Il vit ici, A COTE de `recul_insuffisant`, et pour la meme raison : la mesure et
# la decision qui la consomme sont UNE seule question -- < ce temoin a-t-il eu le
# TEMPS d absorber ? >. Mesure du 2026-09-29 : `age_secondes` existait en UN
# exemplaire, dans `verifier-observations-non-redondantes.py` ; son voisin, qui
# jugeait pourtant la meme propriete, ne pouvait donc pas mesurer la fenetre et
# accusait a tort. Deux gardes, une question : une seule definition.
FORMAT_HORODATAGE = "%Y-%m-%d %H:%M:%S"
# DEUX FORMES REelles, et la mesure les a separees (2026-09-29) : l ETAT du
# routeur ecrit `2026-09-29 09:40:03` (sans fraction), mais un `str(datetime.now())`
# ecrit `... 09:45:12.123456` -- et la forme fractionnaire rendait None, donc
# < fenetre non mesurable >, donc une ACCUSATION sur un temoin frais. Un
# horodatage illisible doit rester None ; un horodatage LISIBLE dans une AUTRE
# forme ne l est pas.
FORMATS_HORODATAGE = ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S.%f")


def age_secondes(horodatage, maintenant=None):
    """Age en secondes d un horodatage, ou None s il n est LISIBLE dans AUCUNE forme.

    Un horodatage ILLISIBLE rend None -- jamais 0, jamais une exception : 0 se
    lirait comme < tout frais > et epargnerait a tort, alors que None DIT que la
    fenetre ne peut pas etre mesuree (le domicile n accorde alors AUCUNE fenetre --
    voir `recul_insuffisant`).

    L import de `datetime` est LOCAL : ce module n importe que `json`, et il n a
    pas a s alourdir d une horloge pour ses trois fonctions de signature.
    """
    from datetime import datetime  # noqa: PLC0415 -- horloge locale a cette mesure
    reference = maintenant or datetime.now()
    texte = str(horodatage)
    for format_essaie in FORMATS_HORODATAGE:
        try:
            instant = datetime.strptime(texte, format_essaie)
        except (TypeError, ValueError):
            continue
        return int((reference - instant).total_seconds())
    return None
