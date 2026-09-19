"""Fonctions simples de la categorie corriger : une seule tache chacune.

POURQUOI CE VERBE (EO-155, mesure du 2026-09-17) : la porte n'avait que noter /
lire / verifier. Or le rattachement d'une ligne a sa mission se fait par TAG ou
par mention en tete du detail -- et la republication de la ligne d'appui 41
(controler_borne_conservation, pilote/commun.py) a ete taggee MO-164 parce que
sa RAISON citait "mesure MO-164", alors qu'elle appartient a MO-165. Sans verbe
de correction, la faute a du etre reparee par la porte GENERIQUE d'ecriture :
l'empreinte a casse (le verifier a crie, correctement) et il a fallu la
recalculer a la main. Ce verbe fait les DEUX dans le meme geste : reattribuer
une entree ET laisser la porte recalculer l'empreinte.

LA LIGNE N'EST JAMAIS EFFACEE NI RECREEE : la correction est EN PLACE, donc la
date, la position, l'action et le detail SURVIVENT -- seuls les tags changent,
et l'ancienne valeur voyage dans `corrections`, portee par l'entree.
"""
from datetime import datetime

CHAMP_CORRECTIONS = "corrections"


def trouver_fiche(donnees, chemin):
    """Retourne la fiche du fichier, ou None (une seule tache : chercher)."""
    return donnees.get("fichiers", {}).get(chemin)


def positions_correspondantes(fiche, extrait):
    """Retourne les positions des entrees dont le DETAIL contient l'extrait."""
    return [position for position, entree in enumerate(fiche.get("modifications", []))
            if extrait in entree.get("detail", "")]


def choisir_position(positions, extrait, index_demande=""):
    """Retourne (code, position, message) : 0 = une seule position designee.

    L'AMBIGUITE EST REFUSEE, jamais tranchee : deux entrees qui contiennent le
    meme extrait ont la meme forme, et deviner laquelle corriger editerait la
    mauvaise ligne EN SILENCE. L'appelant desambigue avec --index.
    """
    if not positions:
        return 1, -1, "Aucune entree ne contient cet extrait : " + repr(extrait)
    if index_demande:
        try:
            numero = int(index_demande)
        except ValueError:
            return 2, -1, ("Indice illisible : " + repr(index_demande)
                           + " (attendu un entier de 1 a " + str(len(positions)) + ").")
        if numero < 1 or numero > len(positions):
            return 2, -1, ("Indice hors plage : " + str(numero) + " (candidats : "
                           + str(len(positions)) + ").")
        return 0, positions[numero - 1], ""
    if len(positions) > 1:
        return 2, -1, ("Extrait AMBIGU : " + str(len(positions)) + " entrees le contiennent"
                       " -- desambiguer avec --index <1.." + str(len(positions)) + ">.")
    return 0, positions[0], ""


def corriger_entree(fiche, position, tags, motif=""):
    """Reattribue les TAGS d'UNE entree, EN PLACE. Retourne (code, message).

    1 = rien a corriger (les tags demandes sont deja ceux de l'entree) : une
    reussite muette ferait passer une commande mal ciblee pour un travail fait.
    """
    entree = fiche.get("modifications", [])[position]
    avant = list(entree.get("tags", []))
    if avant == list(tags):
        return 1, ("Rien a corriger : cette entree porte DEJA les tags "
                   + ", ".join(avant) + " -- aucune ecriture.")
    entree["tags"] = list(tags)
    entree.setdefault(CHAMP_CORRECTIONS, []).append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "motif": motif,
        "tags_avant": avant,
        "tags_apres": list(tags),
    })
    return 0, ("Entree " + str(position + 1) + " du " + str(entree.get("date", "?"))
               + " corrigee : tags " + (", ".join(avant) if avant else "(aucun)")
               + " -> " + ", ".join(tags) + " -- date, action et detail CONSERVES"
               + (" ; motif : " + motif if motif else "") + ".")


def reattribuer_tags_fiche(fiche):
    """Recalcule les tags de la FICHE depuis ses entrees (valeur DERIVEE).

    La fiche porte la REUNION des tags de ses lignes : c'est une valeur derivee,
    donc elle se RECALCULE et ne s'entretient jamais a la main (M-076). Retourne
    (ajoutes, retires) pour que le geste soit DIT -- jamais silencieux.
    """
    avant = list(fiche.get("tags", []))
    reunion = []
    for entree in fiche.get("modifications", []):
        for tag in entree.get("tags", []):
            if tag not in reunion:
                reunion.append(tag)
    fiche["tags"] = reunion
    return [t for t in reunion if t not in avant], [t for t in avant if t not in reunion]
