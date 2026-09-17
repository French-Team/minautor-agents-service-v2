"""Fonctions simples de la categorie noter : une seule tache chacune."""
from datetime import datetime


# CONTRAT DE TRANSPORT des listes (frictions 72 et 73) : les tags voyagent joints
# par un caractere qui vit dans son DOMICILE (data/commun/transport_listes.py) --
# cette fonction le CONSOMME au lieu de le recopier, comme les dix autres portes de
# BDD (M-076 ; L-100/L-102 : une forme recopiee derive en silence).
from transport_listes import decouper_liste  # noqa: E402


def separer_tags(chaine_tags):
    """Transforme "a, b" en ["a", "b"] -- le separateur vient de son domicile."""
    return decouper_liste(chaine_tags)


def fabriquer_entree(outil, commande, code, duree, detail, tags, tokens_avant=None, tokens_apres=None):
    """Fabrique UNE entree d'usage {date, outil, commande, code, duree, tokens, detail, tags}.

    Espion tokens (E-097, imperatif 56) : le poids du contexte est porte par la
    ligne d'usage -- tokens_avant (l'ordre donne) et tokens_apres (la sortie).
    Champs OPTIONNELS : les lignes anciennes n'en ont pas (contrat per-ligne,
    L-010 : le verifier n'exige que les cles requises).
    """
    entree = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "outil": outil,
        "commande": commande,
        "code": code,
        "tags": tags,
    }
    if duree is not None:
        entree["duree_ms"] = duree
    if tokens_avant is not None:
        entree["tokens_avant"] = tokens_avant
    if tokens_apres is not None:
        entree["tokens_apres"] = tokens_apres
    if detail:
        entree["detail"] = detail
    return entree
