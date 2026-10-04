"""MOTIF UNIQUE : mesurer le BATTEMENT d'une routine sans le MOYENNER (M-076).

Pourquoi ce module existe (friction 28, 2026-09-14) : `veille-flux` a tourne a
6,0 s d'ecart median contre 300 s declarees, les 09-11 (10 494 passes) et 09-12
(8 960) -- 20 219 passes en trop, ~5,6 h de CPU, ~39 000 lignes de journal. La
routine DECLARAIT sa cadence et la PUBLIAIT, mais RIEN ne MESURAIT son battement
reel : le seul temoin fut la TAILLE du journal, trois jours plus tard.

LA PREMIERE REPONSE S'EST TROMPEE, et c'est la lecon de ce module. Le garde de
cadence a d'abord lu le battement comme

    (date - derniere_ecriture) / passes_absorbes

C'est une MOYENNE. Elle ne decrit donc AUCUN intervalle reel des qu'une passe
n'est pas a l'heure (redemarrage, passe A LA DEMANDE, serveur qui relance) :
mesure du 2026-09-14 sur `vigie-profil`, dont le journal prouve la cadence a
900 s et dont le compteur est juste (3 -> 4 en une passe), la MEME cadence a ete
lue 450,5 s puis 600,3 s. Une valeur fausse mais DANS la tolerance ne crie pas :
c'est le pire des temoins -- il rassure.

La reponse juste est une SERIE d'horodatages et un ecart MEDIAN : un
redemarrage ou une passe en retard deplacent la mediane d'un cran, ils ne
divisent plus le resultat par deux.

Ce module est le moteur PARTAGE (data/commun, comme `rotation_journal.py` et
`etat_histoire.py`) : la fabrique de l'anneau (`ajouter_passe`) et la lecture
(`battement_median`) vivent a UN seul endroit. Les routines l'utilisent avec
LEURS donnees, elles ne le recopient pas (L-029 : un moteur recopie quatre fois
diverge quatre fois).

Ce que ce module NE fait PAS : il ne connait AUCUNE cadence, AUCune tolerance et
AUCun fichier. Il rend des secondes et des instants ; c'est le garde qui juge.
"""
import json
from datetime import datetime

# Assez de passes pour un ecart MEDIAN, et BORNE pour que l'etat reste un etat :
# une poignee d'horodatages, jamais un journal.
LONGUEUR_ANNEAU_DEFAUT = 8
# Combien d'ecarts la lecture retient (les derniers) : la cadence courante se
# juge sur les dernieres passes, pas sur toute la vie de l'anneau.
PASSES_MESUREES_DEFAUT = 12
# Horodatages necessaires pour qu'un ecart median existe (2 ecarts).
RECUL_MINIMUM = 3


def ajouter_passe(anneau, horodatage, longueur=LONGUEUR_ANNEAU_DEFAUT):
    """Nouvel ANNEAU borne : l'horodatage ajoute, les plus vieux oublies.

    Un ETAT ne grandit pas -- c'est ce qui le distingue d'un journal. Cette
    fonction est la seule fabrique de l'anneau : une routine qui recopierait le
    decoupage `[-longueur:]` finirait par oublier la borne d'un cote seulement
    (L-029).
    """
    suite = list(anneau or [])
    suite.append(horodatage)
    return suite[-longueur:]


def instants(horodatages, format_horodatage):
    """Horodatages lisibles, convertis en instants ; les illisibles sont ECARTES.

    Un horodatage casse ne doit pas faire tomber un controle : il est ignore, et
    c'est le RECUL qui dira si la serie reste mesurable.
    """
    resultat = []
    for brut in horodatages or []:
        try:
            resultat.append(datetime.strptime(str(brut), format_horodatage))
        except (TypeError, ValueError):
            continue
    return resultat


def battement_median(horodatages, format_horodatage,
                     passes_mesurees=PASSES_MESUREES_DEFAUT,
                     recul_minimum=RECUL_MINIMUM):
    """(battement, dernier) : ecart MEDIAN en secondes, et le dernier instant.

    `battement` vaut None quand le recul est insuffisant (< `recul_minimum`
    horodatages lisibles) : un manque de recul est DIT, jamais comble par une
    valeur inventee.

    La MEDIANE est prise sur les ecarts des `passes_mesurees` derniers instants,
    tries : un redemarrage qui creuse un trou, ou une passe a la demande qui
    serre un intervalle, deplacent la mediane d'un cran -- ils ne la faussent pas
    d'un facteur deux comme le faisait la moyenne.
    """
    moments = instants(horodatages, format_horodatage)
    if len(moments) < recul_minimum:
        return None, (moments[-1] if moments else None)
    moments = sorted(moments)[-passes_mesurees:]
    ecarts = sorted(
        (moments[index + 1] - moments[index]).total_seconds()
        for index in range(len(moments) - 1)
    )
    return ecarts[len(ecarts) // 2], moments[-1]


def lire_anneau(chemin, clef):
    """Anneau garde dans un etat court (liste d'horodatages), ou [] si illisible.

    Un etat illisible rend une serie VIDE, donc un manque de recul DIT -- jamais
    une exception dans un controle (lecon L-026).
    """
    try:
        with open(str(chemin), "r", encoding="utf-8") as flux:
            return json.load(flux).get(clef) or []
    except (OSError, ValueError):
        return []
