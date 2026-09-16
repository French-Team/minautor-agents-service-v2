"""Roles d'item d'entonnoir : la table (type, categorie) -> THEME du vivier.

POURQUOI CE MODULE (L-061, MO-076) : un item d'entonnoir transportait son TITRE
en texte libre dans le champ `theme` ; a la relance automatique, l'injection
refusait ce titre (le champ `theme` d'une MISSION est FERME, c'est le vivier) et
la mission restait en attente jusqu'a un retiquetage a la main. Le role de la
mission n'existait NULLE PART dans l'entonnoir (4 blocages mesures : MO-070,
MO-071, MO-072, MO-075).

L'item porte desormais DEUX champs distincts, et chacun dit ce qu'il est :
  - `theme` : le TITRE de la demande (texte libre, inchange) ;
  - `role`  : le ROLE de la mission, choisi dans le VIVIER (champ ferme).

La table est COMPLETE sur toutes les combinaisons (type, categorie) des listes
fermees : elle est verifiee AU CHARGEMENT et CRIE si un trou apparait (jamais un
defaut muet, lecon L-037 : un garde-fou qui peut etre vide est un garde-fou
absent). Le role propose n'est jamais devine : il vient d'une correspondance
explicite, et il est IMPRIME pour etre confirme ou corrige (`--role`).

La fermeture du champ est celle du PILOTE (`commun.valider_theme`) : UNE SEULE
lecture du vivier dans tout le flux (M-042) -- ce module ne relit jamais le
vivier, il interroge la porte.
"""
import sys
from pathlib import Path

try:
    from listes import CATEGORIES, TYPES
except ImportError:  # importe comme paquet (depuis le pilote) : chemins complets
    from entonnoir.listes import CATEGORIES, TYPES

REPERTOIRE_PILOTE = Path(__file__).resolve().parent.parent
if REPERTOIRE_PILOTE.name != "pilote":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_PILOTE) + " n'est pas le dossier pilote/"
    )

# La porte du champ ferme vit dans le pilote. `append` (jamais `insert(0)`) : les
# modules LOCAUX de l'entonnoir (listes, mots, stockage) restent prioritaires,
# sinon `listes` resoudrait le paquet checklist du pilote et l'entonnoir mourrait.
if str(REPERTOIRE_PILOTE) not in sys.path:
    sys.path.append(str(REPERTOIRE_PILOTE))
try:
    from commun import valider_theme
except ImportError:  # degradation AVOUEE : la porte le dira au premier usage
    valider_theme = None

# Le NOM du champ vient des constantes du PILOTE (proprietaire du contrat) : une
# seule declaration pour tout le flux (deux copies = deux verites, L-035). Le
# titre de l'item reste son champ `theme` historique (inchange).
from constants import CHAMP_ROLE_ITEM as CHAMP_ROLE  # noqa: E402  (apres le sys.path)
CHAMP_TITRE = "theme"

# Correspondance EXPLICITE (type, categorie) -> theme du vivier. Toute valeur est
# un theme REELLEMENT present au vivier (verifie par le cobaye et le garde) : un
# role invente serait refuse par la porte et recreerait le blocage qu'on ferme.
# Les roles suivent l'usage MESURE des missions deja menees (20 REPARATION,
# 5 PILOTE, 5 ROUTINE, 4 CONSTRUCTEUR, 2 OUTIL, 3 CONTRATS, 1 REDACTEUR, 1 AUDITEUR).
ROLE_PAR_TYPE_CATEGORIE = {
    # dev : le role dit CE QUI EST CONSTRUIT.
    ("dev", "outil"): "OUTIL",
    ("dev", "routine"): "ROUTINE",
    ("dev", "bdd"): "BDD",
    ("dev", "pilote"): "PILOTE",
    ("dev", "matrice"): "CONSTRUCTEUR",
    ("dev", "autre"): "CONSTRUCTEUR",
    # reparation : le role dit la NATURE (reparer), quelle que soit la cible.
    ("reparation", "outil"): "REPARATION",
    ("reparation", "routine"): "REPARATION",
    ("reparation", "bdd"): "REPARATION",
    ("reparation", "pilote"): "REPARATION",
    ("reparation", "marbre"): "REPARATION",
    ("reparation", "autre"): "REPARATION",
    # doc : le redacteur (un contrat se range dans CONTRATS).
    ("doc", "manuel"): "REDACTEUR",
    ("doc", "contrat"): "CONTRATS",
    ("doc", "lecon"): "REDACTEUR",
    ("doc", "autre"): "REDACTEUR",
    # audit : AUDITEUR ('AUDIT-NEMESIS' n'est PAS au vivier -- mesure du 2026-09-13).
    ("audit", "marbre"): "AUDITEUR",
    ("audit", "flux"): "AUDITEUR",
    ("audit", "file"): "AUDITEUR",
    ("audit", "autre"): "AUDITEUR",
    # revision : reviser le marbre = CONTRATS ; reviser une regle isolee = REVISEUR.
    ("revision", "marbre"): "CONTRATS",
    ("revision", "contrat"): "CONTRATS",
    ("revision", "regle"): "CONTRATS",
    ("revision", "protocole"): "CONTRATS",
    ("revision", "autre"): "REVISEUR",
}


def combinaisons_attendues():
    """Retourne toutes les combinaisons (type, categorie) des listes fermees."""
    return [(type_cible, categorie) for type_cible in TYPES
            for categorie in CATEGORIES.get(type_cible, ())]


def verifier_table():
    """CRIE si la table n'est pas complete (jamais de defaut muet, L-037).

    Retourne la liste des combinaisons manquantes (vide = table complete) ; le
    chargement du module echoue si elle n'est pas vide : une table trouee est un
    blocage en puissance, pas une commodite.
    """
    manquants = [paire for paire in combinaisons_attendues()
                 if paire not in ROLE_PAR_TYPE_CATEGORIE]
    if manquants:
        raise RuntimeError(
            "Table des roles INCOMPLETE : "
            + ", ".join(type_cible + "/" + categorie for type_cible, categorie in manquants)
            + " -- un role manquant ferait retomber l'item sur un theme invente."
        )
    return manquants


verifier_table()


def proposer_role(type_cible, categorie_cible):
    """Retourne le role PROPOSE pour ce couple (type, categorie), jamais devine."""
    return ROLE_PAR_TYPE_CATEGORIE.get((type_cible, categorie_cible), "")


def valider_role(role):
    """Valide un role contre le VIVIER (porte unique du pilote).

    Retourne (code, role_canonique, message_ecart). Code 2 = refuse (la porte a
    deja dit pourquoi + la liste) ; la degradation -- porte injoignable -- est
    AVOUEE dans message_ecart, jamais silencieuse (Vivier absent : on n'invente
    pas une fermeture qui bloquerait une reparation du vivier lui-meme).
    """
    if valider_theme is None:
        return 0, role, (
            "ECART : porte du vivier injoignable (commun.valider_theme) -- role "
            + repr(role) + " accepte SANS verification (a reparer)."
        )
    code, canonique = valider_theme(role)
    return code, canonique, ""
