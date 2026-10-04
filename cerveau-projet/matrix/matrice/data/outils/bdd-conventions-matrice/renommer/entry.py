"""Categorie renommer : renomme l'IDENTIFIANT d'une convention (jamais son contenu).

Interface entre main.py et les fonctions simples (renommer/fonctions.py).
C'est la PORTE qui renomme (ecriture atomique + empreinte recalculee), jamais
la main : un id est une cle, il ne se change pas dans un editeur.

Refus (code 1 ou 2, aucune ecriture) :
    - id source ou cible de forme invalide (attendu <PREFIXE>-<NNN>) ;
    - id source identique a la cible ;
    - id source inconnu dans la BDD ;
    - id cible deja porte par une autre entree (jamais d'ecrasement).
"""
from commun import charger_bdd, enregistrer_bdd, extraire_options
from renommer.fonctions import id_deja_pris, id_valide, renommer_entree, trouver_entree

NOMS_OPTIONS = ("id", "vers")

MOTIF_USAGE = 'Usage : python main.py renommer --id <ancien> --vers <nouveau> (ex : --id CV-011 --vers CV-012)'


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    ancien = options.get("id", "")
    nouveau = options.get("vers", "")

    if not ancien or not nouveau:
        print(MOTIF_USAGE)
        return 2
    if ancien == nouveau:
        print("REFUS : l'id est deja " + nouveau + " (rien a renommer).")
        return 1
    if not id_valide(ancien) or not id_valide(nouveau):
        print("REFUS : la forme attendue est <PREFIXE>-<NNN> (ex : CV-007).")
        return 2

    donnees = charger_bdd()
    if trouver_entree(donnees, ancien) is None:
        print("REFUS : id inconnu dans la BDD : " + ancien)
        return 1
    if id_deja_pris(donnees, nouveau):
        print("REFUS : l'id " + nouveau + " est deja porte par une entree (aucun ecrasement).")
        return 1

    renommer_entree(donnees, ancien, nouveau)
    empreinte = enregistrer_bdd(donnees)
    print(
        "Convention " + nouveau + " renommee (etait " + ancien + ") -- empreinte : "
        + empreinte[:16] + "..."
    )
    return 0
