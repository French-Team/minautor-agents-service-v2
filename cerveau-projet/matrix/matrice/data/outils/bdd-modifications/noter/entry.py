"""Categorie noter : orchestre l'enregistrement d'une modification.

Interface entre main.py et les fonctions simples (noter/fonctions.py).
"""
from commun import (calculer_empreinte_si_existe, canoniser_cle, charger_bdd,
                    chemin_de_cle, enregistrer_bdd, extraire_options)
from constants import ACTIONS_PERMISES, CHEMIN_BDD
from cible import est_dans_perimetre
from noter.fonctions import ajouter_modification, separer_tags, valider_action

NOMS_OPTIONS = ("fichier", "action", "detail", "tags")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    chemin_fichier = options.get("fichier", "")
    action = options.get("action", "modifie")
    detail = options.get("detail", "")
    tags = separer_tags(options.get("tags", ""))

    if not chemin_fichier or not detail:
        print('Usage : python main.py noter --fichier <chemin> --action <action> --detail "..." --tags "a,b"')
        return 2
    if not valider_action(action, ACTIONS_PERMISES):
        print("Action inconnue : " + action + " (permises : " + ", ".join(ACTIONS_PERMISES) + ")")
        return 2

    # EO-363 : la cle s ECRIT dans SA forme canonique. Une forme NON canonique se
    # DIT (elle ne se refuse pas : c est la MEME cible, dite autrement) -- et deux
    # histoires pour un seul fichier ne peuvent plus naitre.
    cle = canoniser_cle(chemin_fichier)
    if cle != chemin_fichier:
        print("CLE CANONISEE (EO-363) : " + chemin_fichier + " -> " + cle
              + " (forme relative a la racine de la Matrice)")
    chemin_fichier = cle

    # L'EMPREINTE DU CONTENU (friction du 2026-09-23) : la note ATTESTE le fichier
    # tel qu'il est MAINTENANT. Sans elle, une note ne disait qu'une DATE -- et une
    # note ecrite pour une autre ecriture blanchissait n'importe quel changement
    # posterieur (mesure : le controle IMPRIMAIT les deux empreintes sans comparer).
    # On ne l'invente JAMAIS : une cible absente, illisible ou HORS PERIMETRE
    # rend une empreinte ABSENTE, et la porte le DIT tout de suite. MO-411 : le
    # PERIMETRE, pas seulement la Matrice -- un fichier ALLOWLISTE de la racine
    # (demarrer-*.md, AGENTS.md) est attestable comme les autres, sans quoi il
    # etait MODIFIABLE mais jamais PROUVABLE.
    chemin_cible = chemin_de_cle(chemin_fichier)
    empreinte_cible = ""
    if est_dans_perimetre(chemin_cible, CHEMIN_BDD):
        empreinte_cible = calculer_empreinte_si_existe(chemin_cible) or ""
    if empreinte_cible:
        print("Contenu atteste : " + empreinte_cible[:16] + "... (l'empreinte de la cible au moment de la note)")
    else:
        print("EMPREINTE ABSENTE pour " + chemin_fichier
              + " (cible absente, illisible ou hors du perimetre) : la note ne pourra rien attester.")

    donnees = charger_bdd()
    ajouter_modification(donnees, chemin_fichier, action, detail, tags, empreinte_cible)
    empreinte = enregistrer_bdd(donnees)
    print("Note enregistree pour " + chemin_fichier + " (empreinte BDD : " + empreinte[:16] + "...)")
    return 0
