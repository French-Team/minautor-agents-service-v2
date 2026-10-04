"""Fonctions simples de la categorie ajouter : une seule tache chacune.

LE DOUBLON (EO-537, mesure du 2026-09-30) : `ajouter` acceptait un segment
IDENTIQUE a une entree deja presente, et le double depot de la MEME source
passait sans un mot. Mesure reelle : cinq segments deposes deux fois par un
script de depot relance (RS-033 a RS-037, puis RS-038 a RS-042, contenu
identique). Ce n'est pas qu une gene esthetique -- la BDD de raisonnement est
la MEMOIRE du raisonnement reutilisable, donc un doublon y fait lire deux fois
le meme segment comme s il en etait deux, et le compteur que la cloture MO-500
mesure gonfle d autant.

La REGLE : un doublon ACTIF, c'est le meme CONTENU et la meme SOURCE. Les deux
conditions sont exigees, parce que deux missions peuvent produire le meme
raisonnement : c'est la source qui distingue les deux, jamais le texte.
"""
from datetime import datetime

from constants import PREFIXE_ID


def separer_tags(chaine_tags):
    """Transforme "a, b" en ["a", "b"] (chaine vide -> liste vide)."""
    if not chaine_tags:
        return []
    return [morceau.strip() for morceau in chaine_tags.split(",") if morceau.strip()]


def prochain_id(donnees):
    """Calcule l'identifiant de la prochaine entree (compteur incremente)."""
    donnees["compteur"] = donnees.get("compteur", 0) + 1
    return PREFIXE_ID + "-" + str(donnees["compteur"]).zfill(3)


def trouver_doublon(donnees, contenu, source):
    """L entree ACTIVE identique (meme contenu ET meme source), ou None.

    Le retour est l ENTREE, pas un booleen : le refus doit NOMMER l id que
    l appelant vient de dupliquer, sinon l appelant ne sait pas quoi corriger.
    Les entrees retirees ne sont pas dans la liste -- donc jamais accusees a
    tort d etre actives.
    """
    for entree in donnees.get("segments", []):
        if entree.get("segment") == contenu and str(entree.get("source", "")) == str(source):
            return entree
    return None


def ajouter_entree(donnees, contenu, tags, source):
    """Ajoute UNE entree taguee a la liste. Ne touche a rien d'autre."""
    entree = {
        "id": prochain_id(donnees),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "segment": contenu,
        "tags": tags,
        "source": source,
    }
    donnees.setdefault("segments", []).append(entree)
    return entree


def separer_tags(chaine_tags):
    """Transforme "a, b" en ["a", "b"] (chaine vide -> liste vide)."""
    if not chaine_tags:
        return []
    return [morceau.strip() for morceau in chaine_tags.split(",") if morceau.strip()]


def prochain_id(donnees):
    """Calcule l'identifiant de la prochaine entree (compteur incremente)."""
    donnees["compteur"] = donnees.get("compteur", 0) + 1
    return PREFIXE_ID + "-" + str(donnees["compteur"]).zfill(3)


def ajouter_entree(donnees, contenu, tags, source):
    """Ajoute UNE entree taguee a la liste. Ne touche a rien d'autre."""
    entree = {
        "id": prochain_id(donnees),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "segment": contenu,
        "tags": tags,
        "source": source,
    }
    donnees.setdefault("segments", []).append(entree)
    return entree
