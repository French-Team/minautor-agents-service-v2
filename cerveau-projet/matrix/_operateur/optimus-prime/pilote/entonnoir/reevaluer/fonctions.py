"""FONCTIONS DU VERBE `reevaluer` (EO-491).

POURQUOI CE VERBE (mesure du 2026-09-30) : les axes d auto-validation sont
poses A LA NAISSANCE et plus JAMAIS rejoues. Aucun des six verbes de
l entonnoir ne les reevalue -- `classer` CONSERVE meme l existant
(`mission_classee.get(CHAMP_AUTO_VALIDATION) or VERDICT_NON`). Un item corrige
peut donc porter un vote que son texte ne justifie plus, et RIEN ne permet de
le remettre a jour.

Deux conditions, non negociables :

1. LA PROVENANCE. Un rejeu n a de sens que si le TEXTE a bouge depuis le
   vote. Sans l empreinte du texte juge, un rejeu ne peut pas distinguer
   "rien n a change" de "le texte a change" -- et il fabriquerait du bruit a
   chaque passage, ce qui est exactement le defaut qu une reparation
   d auto-evaluation introduit.
2. LA TRACE D ECART. Le rejeu DIT quels axes ont bouge (N sur 5) et conserve
   le verdict d avant. Un rejeu sans trace d ecart serait invisible.

CONTRE-TEMPOIN A CONSERVER : le rejeu doit rejouer le meme item et dire
"0 axe bouge" quand rien n a change. C'est une condition de sortie, pas un
detail : un rejet qui exige une preuve peut etre reapplique par l item
lui-meme (le veto recopie dans l objectif), donc seul le rejeu sur un texte
qui a REELLEMENT bouge rend juste.
"""
from listes import (
    CHAMP_AUTO_AXES,
    CHAMP_AUTO_VALIDATION,
    CHAMP_AUTO_VALIDATION_TEXTE,
    CHAMP_REEVALUATIONS,
    CHAMP_TYPE_PROPOSE,
    PREFIXE_ITEM,
)
from roles import CHAMP_TITRE
from stockage import empreinte_texte, horodater, texte_juge, trouver_item

def _type_juge(mission):
    """Le type soumis au juge : celui PROPOSE a la naissance, sinon celui porte."""
    return mission.get(CHAMP_TYPE_PROPOSE) or mission.get("type") or ""


def _source_jugee(mission):
    """La provenance soumise au juge : la source de l item (jamais devinee)."""
    return mission.get("source") or ""


def _votes(axes):
    """{axe: vote} d une liste d axes -- lisible en un coup, pour comparer."""
    return {axe.get("axe"): axe.get("vote") for axe in (axes or [])}


def comparer_axes(avant, apres):
    """(bouges, disparus) : les axes dont le VOTE a change, et ceux qui ont disparu.

    PURE (deux listes d axes en, deux listes de noms hors) : c est elle que le
    cobaye rejoue sans disque. Un axe disparu est compte : perdre un axe sans
    le dire serait un ecart muet.
    """
    votes_avant = _votes(avant)
    votes_apres = _votes(apres)
    bougees = [nom for nom, vote in votes_apres.items() if votes_avant.get(nom) != vote]
    disparus = [nom for nom in votes_avant if nom not in votes_apres]
    return sorted(bougees), sorted(disparus)


def reevaluer_item(etat, identifiant, forcer=False):
    """Rejoue l evaluateur sur le TEXTE COURANT de l item.

    Rend (code, message, ecrit) : `ecrit` dit s il y a eu une ECRITURE dans
    l etat. Le caller l utilise pour ne pas enregistrer un etat inchange --
    une trace d acces a l entonnoir qui ne change rien Teachose de
    ("le rejeu s est produit") a "l etat a bouge".
    """
    mission, _type_file = trouver_item(etat, identifiant)
    if mission is None:
        return 2, ("Item introuvable : " + repr(identifiant)
                   + " -- l entonnoir ne le connait plus (il est consomme ou solde)."), False
    if not str(identifiant).startswith(PREFIXE_ITEM):
        return 2, ("Identifiant hors famille : " + repr(identifiant) + " (attendu "
                   + PREFIXE_ITEM + "-XXX)"), False
    objectif = mission.get("objectif") or ""
    # L empreinte porte le TEXTE JUGE (theme + objectif + type) : c est ce que
    # l evaluateur assemble, donc c est la seule empreinte qui dise si son
    # entree a change (correction du TITRE comprise -- mesure du 2026-10-01).
    empreinte_courante = empreinte_texte(texte_juge(
        mission.get(CHAMP_TITRE, ""), objectif, _type_juge(mission)))
    empreinte_stockee = mission.get(CHAMP_AUTO_VALIDATION_TEXTE, "")
    if not forcer and not empreinte_stockee:
        return 2, ("REFUS : item depose AVANT le marqueur de rejeu (EO-491) -- son vote"
                   " ne dit pas sur quel texte il a ete rendu. --forcer rejoue quand"
                   " meme, en le disant."), False
    if not forcer and empreinte_stockee == empreinte_courante:
        return 0, ("TEXTE INCHANGE depuis le vote (empreinte " + empreinte_courante[:12]
                   + "..., " + str(len(mission.get(CHAMP_AUTO_AXES) or []))
                   + " axe(s)) : 0 axe bouge, RIEN n est reecrit -- un rejeu sans"
                   " changement serait du bruit."), False
    from vrac.entry import avis_auto_validation
    verdict, axes = avis_auto_validation(mission.get(CHAMP_TITRE, ""), objectif,
                                         _type_juge(mission), _source_jugee(mission))
    avant_axes = mission.get(CHAMP_AUTO_AXES) or []
    avant_verdict = mission.get(CHAMP_AUTO_VALIDATION, "")
    bougees, disparus = comparer_axes(avant_axes, axes)
    mission[CHAMP_AUTO_VALIDATION] = verdict
    mission[CHAMP_AUTO_AXES] = axes
    mission[CHAMP_AUTO_VALIDATION_TEXTE] = empreinte_courante
    mission.setdefault(CHAMP_REEVALUATIONS, []).append({
        "le": horodater(),
        "verdict_avant": avant_verdict,
        "verdict_apres": verdict,
        "axes_bouges": bougees,
        "axes_disparus": disparus,
        "empreinte_texte": empreinte_courante,
    })
    lignes = ["Item " + identifiant + " : AUTO-VALIDATION REJOUEE sur le texte courant."]
    lignes.append("  texte     : " + str(len(objectif)) + " caractere(s), empreinte "
                  + empreinte_courante[:12] + "...")
    lignes.append("  verdict   : " + str(avant_verdict) + " -> " + str(verdict)
                  + " (" + str(len(bougees)) + " axe(s) bouge(s) sur "
                  + str(len(axes)) + ")")
    for axe in axes:
        marque = "*" if axe.get("axe") in bougees else " "
        lignes.append("   " + marque + str(axe.get("axe")) + " : "
                      + str(axe.get("vote")) + " -- " + str(axe.get("motif"))[:100])
    if disparus:
        lignes.append("  ATTENTION : " + str(len(disparus)) + " axe(s) disparu(s) : "
                      + ", ".join(disparus))
    lignes.append("  trace     : " + CHAMP_REEVALUATIONS + " de l item (rejoue auditable)")
    return 0, "\n".join(lignes), True
