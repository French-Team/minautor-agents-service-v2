"""Categorie corriger : reattribuer UNE entree, puis laisser la porte recalculer.

Interface entre main.py et les fonctions simples (corriger/fonctions.py).
"""
from commun import charger_bdd, enregistrer_bdd, extraire_options
from corriger.fonctions import (choisir_position, corriger_entree,
                                positions_correspondantes, reattribuer_tags_fiche,
                                trouver_fiche)

# CONTRAT DE TRANSPORT des listes (frictions 72 et 73) : le separateur vit dans
# son DOMICILE partage (data/commun/transport_listes.py) -- cette porte le
# CONSOMME au lieu de le recopier (M-076 ; L-100/L-102).
from transport_listes import decouper_liste  # noqa: E402

NOMS_OPTIONS = ("fichier", "extrait", "tags", "motif", "index")

USAGE = ('Usage : python main.py corriger --fichier <chemin> '
         '--extrait "<texte du detail>" --tags "a,b" [--motif "..."] [--index N]')


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    chemin_fichier = options.get("fichier", "")
    extrait = options.get("extrait", "")
    tags = decouper_liste(options.get("tags", ""))
    if not chemin_fichier or not extrait or not tags:
        print(USAGE)
        return 2

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

    code, message = corriger_entree(fiche, position, tags, options.get("motif", ""))
    if code != 0:
        print(message)
        return code

    ajoutes, retires = reattribuer_tags_fiche(fiche)
    # enregistrer_bdd recalcule ET ecrit l'empreinte : c'est le SECOND defaut
    # d'EO-155 ferme ici -- reparee par la porte generique, l'empreinte cassait
    # et le verifier criait, a juste titre (il ne pouvait pas deviner l'intention).
    empreinte = enregistrer_bdd(donnees)
    print(message)
    print("Tags de la fiche recalcules : "
          + ("ajout " + ", ".join(ajoutes) if ajoutes else "aucun ajout")
          + " ; " + ("retrait " + ", ".join(retires) if retires else "aucun retrait") + ".")
    print("Empreinte recalculee par la porte : " + empreinte[:16] + "...")
    return 0
