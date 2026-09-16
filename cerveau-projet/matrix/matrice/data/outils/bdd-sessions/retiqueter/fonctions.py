"""Categorie retiqueter : CORRIGE les tags d'une entree EXISTANTE (MO-122).

Pourquoi cette porte existe (friction 40, mesuree le 2026-09-16) : une
entree notee avec un tag HORS du vocabulaire declare est INVISIBLE du
lecteur qui ne lit que ce vocabulaire (la porte de reprise ne retient que
les entrees portant un tag de session) et la BDD n'offrait AUCUNE facon de
la reparer -- l'ecriture a la main du JSON etant interdite par le marbre
(porte unique). Mesure d'origine : 34 entrees sur 51 sans tag de session,
la derniere entree taguee etant vieille de 19 missions.

Le pilote a recu `retiqueter` en MO-112 pour la meme raison : un fait
historique se CORRIGE par la porte, avec sa trace, jamais par reecriture
manuelle. Regle CV-010 : un id ne change que par la porte.

La correction CONSERVE la trace : tags_avant, retiquete_le et
motif_retiquetage restent dans l'entree. Le TEXTE n'est JAMAIS touche :
corriger un tag ne reecrit pas un fait, et corriger une DATE ne reecrit pas un
fait non plus : le texte reste intact et l'ancienne date reste dans l'entree
(horodatage_avant).

MO-124 -- RE-DATAGE : une entree peut etre RE-DATEE (`--horodatage`), car une
collision a la SECONDE n'est departageable par rien (accident S-052/S-053 de
MO-119 : une cloture et une ouverture a la meme seconde, la reprise tranchait
au hasard de la lecture). La seule reparation honnete est de REDONNER une
seconde propre a l'une des deux. Le re-datage est REFUSE si la seconde visee
est deja occupee : il CREERAIT la collision qu'il sert a reparer.
"""
from datetime import datetime

# Le FORMAT appartient au contrat de trace (MO-121/MO-124) : la porte VALIDE
# avec la meme constante que celle qui ecrit et que celle qui lit.
from trace_session import FORMAT_HORODATAGE  # noqa: E402


def trouver(donnees, identifiant):
    """Retourne l'entree portant cet id, ou None (jamais d'exception)."""
    for entree in donnees.get("sessions", []):
        if entree.get("id") == identifiant:
            return entree
    return None


def retiqueter_entree(entree, tags, motif):
    """Corrige les tags d'une entree en CONSERVANT la trace de l'ancien etat."""
    entree["tags_avant"] = list(entree.get("tags", []))
    entree["tags"] = list(tags)
    entree["retiquete_le"] = datetime.now().strftime(FORMAT_HORODATAGE)
    entree["motif_retiquetage"] = motif
    return entree


def valider_horodatage(texte):
    """Retourne l'horodatage NORMALISE, ou None si la forme est illisible.

    Un re-datage est une ECRITURE de temps : la porte ne devine pas, elle
    refuse ce qu'elle ne comprend pas (et rien n'est ecrit). Les espaces
    autour sont toleres, la forme rendue est celle du contrat.
    """
    if not texte:
        return None
    try:
        moment = datetime.strptime(texte.strip(), FORMAT_HORODATAGE)
    except ValueError:
        return None
    return moment.strftime(FORMAT_HORODATAGE)


def occupants(donnees, horodatage, sauf_id):
    """Les entrees qui OCCUPENT deja cette seconde (garde de collision).

    L'entree visee est exclue : se re-dater sur SA propre seconde n'est pas
    une collision (sinon la porte refuserait un geste sans effet).
    """
    return [
        entree
        for entree in donnees.get("sessions", [])
        if entree.get("id") != sauf_id and entree.get("date") == horodatage
    ]


def re_dater_entree(entree, horodatage, motif):
    """Re-date une entree en CONSERVANT la trace de l'ancienne date."""
    entree["horodatage_avant"] = entree.get("date")
    entree["date"] = horodatage
    entree["re_date_le"] = datetime.now().strftime(FORMAT_HORODATAGE)
    entree["motif_retiquetage"] = motif
    return entree
