"""Categorie retirer : retirer UNE entree, puis laisser la porte recalculer.

Interface entre main.py et les fonctions simples (retirer/fonctions.py).

Le CHOIX de la position (extrait + --index, ambiguite refusee) et la
REATTRIBUTION des tags de la fiche sont les MEMES regles que `corriger` : elles
ont un seul domicile (corriger.fonctions) et elles sont CONSOMMEES ici, jamais
recopiees (M-076 ; L-029).
"""
from commun import canoniser_cle, charger_bdd, enregistrer_bdd, extraire_options
from corriger.fonctions import (choisir_position, positions_correspondantes,
                                reattribuer_tags_fiche, trouver_fiche)
from retirer.fonctions import retirer_entree

NOMS_OPTIONS = ("fichier", "extrait", "index", "motif")

USAGE = ('Usage : python main.py retirer --fichier <chemin> '
         '--extrait "<texte du detail>" [--index N] [--motif "..."]')


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    chemin_fichier = options.get("fichier", "")
    extrait = options.get("extrait", "")
    if not chemin_fichier or not extrait:
        print(USAGE)
        return 2

    # EO-363 : la MEME cle canonique qu a l ecriture (un seul domicile de cle).
    chemin_fichier = canoniser_cle(chemin_fichier)
    donnees = charger_bdd()
    fiche = trouver_fiche(donnees, chemin_fichier)
    if fiche is None:
        print("Fichier inconnu de la BDD : " + chemin_fichier)
        return 1

    positions = positions_correspondantes(fiche, extrait)
    code, position, message = choisir_position(positions, extrait, options.get("index", ""))
    if code != 0:
        print(message)
        return code

    code, message = retirer_entree(fiche, position, options.get("motif", ""))
    if code != 0:
        print(message)
        return code

    ajoutes, retires = reattribuer_tags_fiche(fiche)
    # enregistrer_bdd recalcule ET ecrit l'empreinte : le retrait d'une entree
    # change le contenu, donc l'empreinte doit etre reposee dans le MEME geste
    # (sinon `verifier` crierait, a juste titre, sur une BDD modifiee hors outil).
    empreinte = enregistrer_bdd(donnees)
    print(message)
    print("Tags de la fiche recalcules : "
          + ("ajout " + ", ".join(ajoutes) if ajoutes else "aucun ajout")
          + " ; " + ("retrait " + ", ".join(retires) if retires else "aucun retrait") + ".")
    print("Empreinte recalculee par la porte : " + empreinte[:16] + "...")
    return 0
