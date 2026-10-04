"""Categorie ajouter : orchestre l'enregistrement d'une segment taguee.

Interface entre main.py et les fonctions simples (ajouter/fonctions.py).

LE DOUBLON EST REFUSE AVANT TOUTE ECRITURE (EO-537, mesure du 2026-09-30) : un
segment identique a une entree ACTIVE, de la MEME source, est refuse en
nommant l id deja present. La porte refuse donc AVANT de toucher au compteur :
un depot refuse ne laisse pas de trou dans la numerotation, parce qu il ne
consomme aucun id.
"""
from commun import charger_bdd, enregistrer_bdd, extraire_options
from ajouter.fonctions import ajouter_entree, separer_tags, trouver_doublon

NOMS_OPTIONS = ("segment", "tags", "source")

USAGE = ('Usage : python main.py ajouter --segment "..." --tags "a,b"'
         ' [--source "..."]')


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    contenu = options.get("segment", "")
    tags = separer_tags(options.get("tags", ""))
    source = options.get("source", "")

    if not contenu or not tags:
        print(USAGE)
        return 2

    donnees = charger_bdd()
    # LE REFUS, avec l id qu il faut corriger. Le meme TEXTE sous une autre
    # source est ACCEPTEE : deux missions peuvent Legitimement produire le meme
    # raisonnement, et c est la source qui les distingue.
    deja = trouver_doublon(donnees, contenu, source)
    if deja is not None:
        print("REFUS : DOUBLON -- " + str(deja.get("id")) + " porte DEJA ce segment"
              " pour la source " + repr(str(deja.get("source", "")))
              + " (depose le " + str(deja.get("date", "?"))
              + "). Rien n est ecrit, aucun id n est consomme"
              " -- un depot refuse ne doit pas laisser de trou dans la"
              " numerotation. Deux segments de MEME TEXTE mais de sources"
              " DIFFERENTES restent acceptes : c est la source qui distingue les"
              " deux, jamais le texte.")
        return 2
    entree = ajouter_entree(donnees, contenu, tags, source)
    empreinte = enregistrer_bdd(donnees)
    print(
        "Segment " + entree["id"] + " enregistree (tags : " + ", ".join(entree["tags"])
        + ") -- empreinte : " + empreinte[:16] + "..."
    )
    return 0
