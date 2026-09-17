"""Fonctions simples de la categorie noter : une seule tache chacune."""
from datetime import datetime


def valider_action(action, actions_permises):
    """Retourne True si l'action fait partie des actions permises."""
    return action in actions_permises


# CONTRAT DE TRANSPORT des listes (frictions 72 et 73) : les tags voyagent joints
# par un caractere qui vit dans son DOMICILE (data/commun/transport_listes.py) --
# cette fonction le CONSOMME au lieu de le recopier, comme les dix autres portes de
# BDD (M-076 ; L-100/L-102 : une forme recopiee derive en silence).
from transport_listes import decouper_liste  # noqa: E402


def separer_tags(chaine_tags):
    """Transforme "a, b" en ["a", "b"] -- le separateur vient de son domicile."""
    return decouper_liste(chaine_tags)


def ajouter_modification(donnees, chemin_fichier, action, detail, tags):
    """Ajoute UNE modification a la fiche du fichier et met a jour ses tags.

    Ne touche a rien d'autre : l'enregistrement est fait par commun.enregistrer_bdd.
    """
    entree = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
        "detail": detail,
        "tags": tags,
    }
    fiche = donnees.setdefault("fichiers", {}).setdefault(
        chemin_fichier, {"modifications": [], "tags": []}
    )
    # Resilience : anciens fichiers sans cle tags (avant migration).
    fiche.setdefault("tags", [])
    fiche.setdefault("modifications", [])
    fiche["modifications"].append(entree)
    for tag in tags:
        if tag not in fiche["tags"]:
            fiche["tags"].append(tag)
    return entree
