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

# LE NOM DU CHAMP D'EMPREINTE vient de son DOMICILE (constants) : la note l'ECRIT
# ici, le controle d'attribution le RELIT -- une seule forme, ecrite et lue au meme
# endroit (M-076 ; L-029 : une forme recopiee derive en silence).
from constants import CHAMP_EMPREINTE  # noqa: E402

# LA REGLE ASCII VIT A SON DOMICILE (EO-365 / MO-466) : un TAG est une CLE, il se
# normalise a l ECRITURE comme a la RECHERCHE (M-076 ; L-029).
from texte_ascii import vers_ascii  # noqa: E402


def separer_tags(chaine_tags):
    """Transforme "a, b" en ["a", "b"] -- le separateur vient de son domicile."""
    return decouper_liste(chaine_tags)


def ajouter_modification(donnees, chemin_fichier, action, detail, tags, empreinte=""):
    """Ajoute UNE modification a la fiche du fichier et met a jour ses tags.

    Ne touche a rien d'autre : l'enregistrement est fait par commun.enregistrer_bdd.

    L'EMPREINTE DU CONTENU est posee AVEC la note (friction du 2026-09-23) : c'est
    elle qui permet au controle d'attribution de VERIFIER que la note parle de
    l'ecriture qu'il voit, au lieu de croire sa seule date. Une empreinte absente
    (cible illisible, hors Matrice, note anterieure a la mesure) est OMISE de la
    note : elle n'est jamais inventee, et le controle la COMPTE au lieu de la subir.
    """
    # UN TAG EST UNE CLE DE RECHERCHE, DONC IL SE NORMALISE (EO-365 / MO-466) :
    # ecrit avec un accent, il etait INTOUVRABLE (mesure du 2026-09-22 : 1 seul tag
    # non-ASCII dans toute la BDD, invisible a la recherche sur son propre nom). La
    # regle vit a son domicile (data/commun/texte_ascii.py) ; le DETAIL, lui, est du
    # TEXTE LIBRE et n est PAS retouche.
    tags = [vers_ascii(tag) for tag in (tags or [])]
    entree = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
        "detail": detail,
        "tags": tags,
    }
    if empreinte:
        entree[CHAMP_EMPREINTE] = empreinte
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
