"""Roles d'Optimus : la table FERMEE type de mission -> PERSONNALITE du vivier.

POURQUOI CE MODULE (revision du 2026-09-14, chantier MAILLON 2/5) : le cameleon a
UNE personnalite par mission, choisie par la Matrice dans le VIVIER (categorie
PERSONNALITE), jamais par lui. Optimus n'en avait AUCUNE : ses missions ne
portaient qu'un theme de CHANTIER (REPARATION, OUTIL, PILOTE...) -- le QUOI
toucher, jamais le QUI JE SUIS. Une mission commencee sans posture laisse l'agent
improviser sa conduite : c'est exactement ce que le pilote doit fournir AVANT la
mission, et non noye au demarrage dans une fiche entiere.

La table est COMPLETE sur les types de l'entonnoir (`listes.TYPES`) et verifiee AU
CHARGEMENT : une table trouee est un blocage en puissance, jamais une commodite
(lecon L-037 -- un garde-fou qui peut etre vide est un garde-fou absent).

Le mappage est PORTE PAR LE PILOTE, jamais par l'agent (doctrine cameleon : la
personnalite est donnee, jamais choisie). Ni la fiche ni un theme ne le
declarent : il ne peut donc pas deriver.

La fermeture du champ est celle du PILOTE (`commun.valider_theme`) : UNE SEULE
lecture du vivier dans tout le flux (M-042). Ce module ne relit jamais le vivier,
il interroge la porte -- et il exige que la personnalite soit de categorie
PERSONNALITE : un theme de chantier ne peut pas se faire passer pour une posture.
"""
import sys
from pathlib import Path

try:
    from entonnoir.listes import TYPES
except ImportError:  # importe depuis l'entonnoir : chemins locaux
    from listes import TYPES

REPERTOIRE_PILOTE = Path(__file__).resolve().parent
if REPERTOIRE_PILOTE.name != "pilote":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_PILOTE) + " n'est pas le dossier pilote/"
    )

# `append` (jamais `insert(0)`) : les modules LOCAUX de l'entonnoir restent
# prioritaires, sinon `listes` resoudrait le paquet checklist du pilote.
if str(REPERTOIRE_PILOTE) not in sys.path:
    sys.path.append(str(REPERTOIRE_PILOTE))
try:
    from commun import valider_theme
except ImportError:  # degradation AVOUEE : la porte le dira au premier usage
    valider_theme = None

# Le NOM de la categorie et le nom du champ viennent des constantes du PILOTE
# (proprietaire du contrat) : une seule declaration pour tout le flux (L-035).
from constants import CATEGORIE_POSTURE, CHAMP_POSTURE_MISSION  # noqa: E402

# Correspondance EXPLICITE type -> personnalite du vivier. Toute valeur est un
# theme REELLEMENT present au vivier (verifie par le cobaye et le garde) : une
# posture inventee serait refusee par la porte et laisserait la mission sans
# conduite. Meme mappage que le cameleon (fiche agents/cameleon/cameleon.md) :
# une seule doctrine de posture pour tout le cerveau-projet.
POSTURE_PAR_TYPE = {
    "dev": "CONSTRUCTEUR",
    "reparation": "REPARATEUR",
    "doc": "REDACTEUR",
    "audit": "AUDITEUR",
    "revision": "REVISEUR",
}


def verifier_table():
    """CRIE si un type n'a pas de posture (jamais de defaut muet, L-037).

    Retourne la liste des types sans posture (vide = table complete) ; le
    chargement du module echoue si elle n'est pas vide : une mission d'un type
    connu commencerait sans conduite, et rien ne le dirait.
    """
    manquants = [type_cible for type_cible in TYPES if type_cible not in POSTURE_PAR_TYPE]
    inconnus = [type_cible for type_cible in POSTURE_PAR_TYPE if type_cible not in TYPES]
    if manquants:
        raise RuntimeError(
            "Table des roles INCOMPLETE : "
            + ", ".join(manquants)
            + " -- une mission de ce type commencerait SANS posture."
        )
    if inconnus:
        raise RuntimeError(
            "Table des roles HORS LISTE : "
            + ", ".join(inconnus)
            + " -- type inconnu de l'entonnoir (listes.TYPES)."
        )
    return manquants


verifier_table()


def posture_du_type(type_cible):
    """Retourne la posture PROPOSEE pour ce type de mission, jamais devinee."""
    return POSTURE_PAR_TYPE.get((type_cible or "").strip().lower(), "")


def valider_posture(nom):
    """Valide une posture contre le VIVIER (porte unique du pilote).

    Retourne (code, nom_canonique, message_ecart). Code 2 = refuse (la porte a
    deja dit pourquoi + la liste) ; la degradation -- porte injoignable -- est
    AVOUEE dans message_ecart, jamais silencieuse. Exige en plus la CATEGORIE
    PERSONNALITE : un theme de chantier (REPARATION, OUTIL...) n'est pas une
    conduite, et l'accepter ferait passer un QUOI pour un QUI.
    """
    if valider_theme is None:
        return 0, nom, (
            "ECART : porte du vivier injoignable (commun.valider_theme) -- posture "
            + repr(nom) + " acceptee SANS verification (a reparer)."
        )
    code, canonique = valider_theme(nom)
    if code != 0:
        return code, canonique, ""
    categorie = categorie_du_vivier(canonique)
    if categorie and categorie != CATEGORIE_POSTURE:
        return 2, canonique, (
            "REFUS : " + canonique + " est un theme de categorie " + categorie
            + ", pas une PERSONNALITE -- une posture dit QUI, pas QUOI."
        )
    return 0, canonique, ""


def categorie_du_vivier(nom):
    """Categorie d'un theme du vivier ("" si introuvable : jamais inventee)."""
    try:
        from commun import item_du_vivier
    except ImportError:
        return ""
    item = item_du_vivier(nom)
    return (item or {}).get("categorie", "")


def role_de_mission(mission):
    """Compose le ROLE d'une mission : posture (type) + chantier (theme).

    Retourne (code, role, ecarts). `role` porte DEUX choses distinctes, et
    chacune dit ce qu'elle est :
      - `posture` : QUI conduit la mission (PERSONNALITE du vivier), deduite du
        TYPE par la table fermee -- si le type manque, la posture manque et
        l'ecart est DIT (c'est la carte d'identite de mission qui doit le poser) ;
      - `theme`   : le chantier de la mission (champ `theme` deja FERME).
    Code 2 = la posture proposee n'existe pas au vivier : l'injection est refusee
    plutot que de laisser la mission partir sans conduite.
    """
    ecarts = []
    theme = mission.get("theme", "") or ""
    type_cible = (mission.get("type") or "").strip().lower()
    posture = posture_du_type(type_cible)
    if not posture:
        ecarts.append(
            "mission " + str(mission.get("id", "?")) + " sans type ferme : POSTURE ABSENTE "
            "(le role ne porte que le chantier " + repr(theme) + ")."
        )
        return 0, {"posture": "", "theme": theme, "type": ""}, ecarts
    code, canonique, ecart = valider_posture(posture)
    if ecart:
        ecarts.append(ecart)
    if code != 0:
        return code, {"posture": "", "theme": theme, "type": type_cible}, ecarts
    return 0, {"posture": canonique, "theme": theme, "type": type_cible}, ecarts


CHAMP_ROLE = CHAMP_POSTURE_MISSION
