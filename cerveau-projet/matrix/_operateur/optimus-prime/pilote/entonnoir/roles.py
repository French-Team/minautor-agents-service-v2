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
    # Les quatre types du CANAL USER (decision createur 2026-09-30). Chaque role
    # existe REELLEMENT au vivier -- aucun n est invente ici, et c est la
    # regle que `verifier_table` puis la porte du champ ferme verifient.
    #   question -> ANALYSE : le vivier le definit "Part 1 d une [question]".
    #   cadrage  -> CADRAGE  : "Constituer la CHAINE de missions avant de
    #               resoudre une demande (crochet ???)". C est exactement [???].
    #   cablage  -> CONTRATS : un controle de CABLAGE relit un contrat.
    #   preparer -> CADRAGE  : preparer une demande, c est la poser en chaine.
    ("question", "reponse"): "ANALYSE",
    ("question", "explication"): "ANALYSE",
    ("question", "autre"): "ANALYSE",
    ("cadrage", "plan"): "CADRAGE",
    ("cadrage", "exploration"): "CADRAGE",
    ("cadrage", "autre"): "CADRAGE",
    ("cablage", "cablage"): "CONTRATS",
    ("cablage", "contrat"): "CONTRATS",
    ("cablage", "autre"): "CONTRATS",
    ("preparer", "plan"): "CADRAGE",
    ("preparer", "cadrage"): "CADRAGE",
    ("preparer", "autre"): "CADRAGE",
    # investigation -> AUDITEUR (MO-525) : verifier qu une ancienne demande a
    # ete menee a son terme, qu elle est FONCTIONNELLE, puis la valider et la
    # certifier, c est un constat factuel LECTURE SEULE -- exactement le
    # metier de la personnalite AUDITEUR, deja au vivier. Le createur a oppose
    # les deux mots : [cablage] regarde le BRANCHEMENT (CONTRATS relit un
    # contrat), [investigation] regarde l EFFET (AUDITEUR constate).
    ("investigation", "controle"): "AUDITEUR",
    ("investigation", "certification"): "AUDITEUR",
    ("investigation", "autre"): "AUDITEUR",
    # tache -> OUTIL (demande createur 2026-10-02) : une COMMANDE d execution.
    # La posture est celle de l operateur qui FAIT et qui livre, pas de celui qui
    # constate (AUDITEUR) ni de celui qui redige un plan (CADRAGE). Une tache qui
    # constate se dit [investigation] ; une tache qui planifie se dit [preparer].
    # tache -> CADREUR (demande createur 2026-10-02, MO-543) : une COMMANDE
    # se DECORTIQUE avant d etre dirigee -- nommer le bon choix, dire le vrai
    # besoin. C est le metier de CADREUR (vivier TH-029). ARBITRAGE DIT : le
    # livrable d une [tache] est un PLAN d execution ; qui conduit la tache ne
    # l execute pas d office. Meme valeur que personnalites.POSTURE_PAR_TYPE.
    ("tache", "execution"): "CADREUR",
    ("tache", "production"): "CADREUR",
    ("tache", "autre"): "CADREUR",
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


def est_theme_du_vivier(texte):
    """Vrai si ce texte EST un nom du vivier -- donc une ETIQUETTE, jamais un titre.

    POURQUOI (mesure 2026-09-23) : deux items reels ont ete deposes avec un nom du
    vivier LA OU le champ attend le TITRE (`--theme "OUTIL"`), et la file a affiche
    cette etiquette a la place de la phrase. Le champ a UN sens : il ne se devine
    pas. La lecture passe par la PORTE du pilote (M-042, jamais une seconde lecture
    du vivier) ; porte injoignable ou liste vide -> False : on n'invente pas une
    fermeture (doctrine du vivier : jamais bloquant).
    """
    if valider_theme is None:
        return False
    try:
        from commun import charger_themes_autorises
    except ImportError:
        return False
    cible = " ".join(str(texte).split()).lower()
    if not cible:
        return False
    return any(str(nom).strip().lower() == cible
               for nom in charger_themes_autorises())
