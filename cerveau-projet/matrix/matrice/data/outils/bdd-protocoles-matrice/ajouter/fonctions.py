"""Fonctions simples de la categorie ajouter : une seule tache chacune."""
from datetime import datetime

from constants import PREFIXE_ID


# CONTRAT DE TRANSPORT des listes (frictions 72 et 73) : les tags voyagent joints
# par un caractere qui vit dans son DOMICILE (data/commun/transport_listes.py) --
# cette fonction le CONSOMME au lieu de le recopier, comme les dix autres portes de
# BDD (M-076 ; L-100/L-102 : une forme recopiee derive en silence).
from transport_listes import decouper_liste  # noqa: E402


def separer_tags(chaine_tags):
    """Transforme "a, b" en ["a", "b"] -- le separateur vient de son domicile."""
    return decouper_liste(chaine_tags)


def prochain_id(donnees):
    """Calcule l'identifiant de la prochaine entree (compteur incremente)."""
    donnees["compteur"] = donnees.get("compteur", 0) + 1
    return PREFIXE_ID + str(donnees["compteur"]).zfill(3)


def ajouter_entree(donnees, contenu, tags, source):
    """Ajoute UNE entree taguee a la liste. Ne touche a rien d'autre."""
    entree = {
        "id": prochain_id(donnees),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "protocole": contenu,
        "tags": tags,
        "source": source,
    }
    donnees.setdefault("protocoles", []).append(entree)
    return entree
