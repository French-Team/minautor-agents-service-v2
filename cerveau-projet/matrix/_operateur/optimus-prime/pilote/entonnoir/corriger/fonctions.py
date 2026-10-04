"""Fonctions simples de la categorie corriger : une seule tache chacune.

POURQUOI CE VERBE (EO-175, mesure du 2026-09-18) : l'entonnoir n'avait aucun
moyen de CORRIGER le theme ou l'objectif d'un item -- `retiqueter` repose les
ETIQUETTES (la CATEGORIE et le ROLE, MO-213), `urgencer` ne change que l'URGENCE. La seule sortie officielle etait
`retirer` puis re-deposer, ce qui PERD l'id : EO-174 portait un objectif errone
(il affirmait qu'un item du vrac serait tisse en tete du brin, alors que le
tissage ne lit que les FILES) et il a fallu le retirer pour laisser naitre
EO-175 ; la trace gardait un id mort et le lecteur devait croiser deux items
pour comprendre l'erreur.

Ce verbe rectifie EN PLACE et CONSERVE l'id, la date de depot, l'urgence, le
role, le type et l'auto-validation. Il n'efface RIEN : la valeur precedente
voyage dans une entree `corrections` portee PAR l'item, donc la trace vit avec
ce qu'elle explique -- jamais un journal parallele a croiser.
"""
from stockage import horodater

CHAMP_CORRECTIONS = "corrections"
CHAMPS_CORRIGEABLES = ("theme", "objectif")


def trouver_item(etat, identifiant):
    """Retourne l'item EO-XXX, au vrac (echelon 0) ou dans sa file (echelons 1-2).

    Un seul parcours pour une seule tache : un item se corrige OU IL VIT. Le
    vrac et les files sont deux domiciles du meme objet, jamais deux objets.
    """
    for mission in etat.get("vrac", []):
        if mission.get("id") == identifiant:
            return mission
    for file_missions in etat.get("files", {}).values():
        for mission in file_missions:
            if mission.get("id") == identifiant:
                return mission
    return None


def champs_demandes(options):
    """Retourne [(champ, valeur)] des champs REELLEMENT demandes, ordre du contrat.

    La PRESENCE de l'option fait foi (EO-156) : un champ absent de la commande
    n'est JAMAIS corrige, et un champ non corrigeable est ignore -- un verbe ne
    touche que ce qu'il declare corriger.
    """
    return [(champ, options[champ]) for champ in CHAMPS_CORRIGEABLES if champ in options]


def options_sans_valeur(options, noms_options):
    """Retourne les options du contrat PRESENTES mais PRIVEES de valeur (EO-156).

    LE PARSEUR PARTAGE NE POSE JAMAIS UNE CHAINE VIDE (contrat de options.py) : il
    range le NOM de l'option dans une LISTE placee sous sa sentinelle
    (CLE_SANS_VALEUR). Cette garde lit donc LA LISTE. La premiere version lisait
    options[nom] == sentinelle -- une forme que le parseur ne produit JAMAIS : la
    garde etait MUETTE et une option avalee serait passee pour une correction
    valide. Defaut trouve en relisant le cobaye, qui avait lui aussi FABRIQUE la
    forme au lieu de la produire (L-060 : un cobaye qui invente la forme ne
    prouve rien sur le code qui la consomme).
    """
    from options import CLE_SANS_VALEUR  # domicile partage (EO-158, MO-171)
    rangees = options.get(CLE_SANS_VALEUR) or []
    if not isinstance(rangees, list):
        return []
    return [nom for nom in rangees if nom in noms_options]


def valeur_vide(champs):
    """Retourne les champs dont la valeur demandee est VIDE (ou blanche)."""
    return [champ for champ, valeur in champs if not valeur.strip()]


def corriger_item(mission, champs, motif=""):
    """Corrige les champs demandes d'UNE mission, en CONSERVANT son id.

    Retourne (code, message) : 0 succes, 1 rien a corriger (les valeurs
    demandees sont DEJA celles portees). Le refus de "rien a corriger" est
    VOLONTAIRE : une correction qui ne change rien se lirait comme une
    reussite, et une commande mal ciblee passerait pour un travail fait.

    L'historique est porte PAR l'item (champ `corrections`, AJOUT SEUL) : la
    valeur precedente n'est jamais perdue, et corriger deux fois laisse deux
    entrees. Les champs NON demandes ne sont jamais touches.
    """
    changements = [(champ, mission.get(champ, ""), valeur) for champ, valeur in champs
                   if mission.get(champ, "") != valeur]
    if not changements:
        return 1, ("Rien a corriger : les champs demandes portent DEJA ces valeurs ("
                   + ", ".join(champ for champ, _ in champs) + ") -- aucune ecriture.")
    for champ, _, valeur in changements:
        mission[champ] = valeur
    mission.setdefault(CHAMP_CORRECTIONS, []).append({
        "date": horodater(),
        "motif": motif,
        "champs": [{"champ": champ, "avant": avant, "apres": apres}
                   for champ, avant, apres in changements],
    })
    return 0, ("Mission " + str(mission.get("id", "?")) + " corrigee : "
               + ", ".join(champ for champ, _, _ in changements)
               + " -- id CONSERVE, date de depot et urgence intactes, "
               + str(len(mission[CHAMP_CORRECTIONS])) + " correction(s) tracee(s)"
               + (" ; motif : " + motif if motif else "") + ".")
