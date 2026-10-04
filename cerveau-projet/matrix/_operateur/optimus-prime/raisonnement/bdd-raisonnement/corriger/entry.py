"""Categorie corriger : orchestre la correction des TAGS d une entree existante.

Interface entre main.py et les fonctions simples (corriger/fonctions.py).
"""
from commun import charger_bdd, enregistrer_bdd, extraire_options
from ajouter.fonctions import separer_tags
from corriger.fonctions import corriger_tags, trouver_entree

NOMS_OPTIONS = ("id", "tags", "motif")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    identifiant = (options.get("id") or "").strip()
    tags = separer_tags(options.get("tags", ""))
    motif = (options.get("motif") or "").strip()

    if not identifiant or not tags:
        print('Usage : python main.py corriger --id RS-XXX --tags "a,b" [--motif "..."]')
        return 2

    donnees = charger_bdd()
    entree = trouver_entree(donnees, identifiant)
    if entree is None:
        connus = ", ".join(str(lue.get("id", "?")) for lue in donnees.get("segments", []))
        print("REFUS : aucun segment " + identifiant + " dans la BDD -- elle porte : "
              + (connus if connus else "(rien, elle est VIDE)")
              + " (une correction vise une entree EXISTANTE : c est le verbe ajouter qui"
              " en cree une).")
        return 2
    if list(entree.get("tags", [])) == tags:
        print("REFUS : " + identifiant + " porte DEJA ces tags (rien a corriger -- rien"
              " n est ecrit, aucune trace n est posee).")
        return 2

    anciens = corriger_tags(entree, tags, motif)
    empreinte = enregistrer_bdd(donnees)
    print("Segment " + identifiant + " corrige (tags : " + ", ".join(tags)
          + ") -- anciens tags TRACES : " + (", ".join(anciens) if anciens else "(aucun)")
          + " -- empreinte : " + empreinte[:16] + "...")
    return 0
