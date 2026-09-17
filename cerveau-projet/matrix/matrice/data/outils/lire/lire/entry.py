"""Categorie lire : orchestre la lecture d'un ou plusieurs fichiers.

Interface entre main.py et les fonctions simples (lire/fonctions.py).
"""
from commun import extraire_options
from lire.fonctions import lire_dossier, lire_fichier, lire_fichiers

# CONTRAT DE TRANSPORT (friction 72, MO-149) : une liste --fichiers arrive JOINte
# par son appelant. Le caractere qui la separe vit dans SON domicile
# data/commun/transport_listes.py (M-076), importe ici comme les autres moteurs
# partages : cette porte est le COUPANT, elle ne redevine jamais la forme
# (L-100/L-102 : une forme recopiee derive en silence).
from transport_listes import decouper_liste  # noqa: E402

# --prive : la TRAPPE d ouverture des zones invisibles L-016, reservee a la
# Matrice (mesure MO-151 : cette porte n avait aucune garde d invisibilite ;
# reparation MO-152, meme contrat que rechercher --prive).
NOMS_OPTIONS = ("fichier", "fichiers", "dossier", "lignes", "hash", "filtre",
                "recursif", "prive")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    fichier = options.get("fichier", "")
    fichiers = options.get("fichiers", "")
    dossier = options.get("dossier", "")
    lignes = options.get("lignes", "")
    avec_hash = "hash" in options
    filtre = options.get("filtre", "")
    recursif = "recursif" in options
    inclure_prive = "prive" in options

    cibles = sum(1 for v in (fichier, fichiers, dossier) if v)
    if cibles == 0:
        print("Usage : python main.py lire --fichier <chemin> [--lignes debut:fin] [--hash]")
        print("       python main.py lire --fichiers <c1,c2> [--lignes debut:fin] [--hash]")
        print("       python main.py lire --dossier <chemin> [--filtre *.py] [--recursif] [--hash]")
        print("       --prive : ouvre les zones invisibles L-016 (Matrice seule)")
        return 2
    if cibles > 1:
        print("REFUS : une seule cible a la fois (--fichier OU --fichiers OU --dossier).")
        return 2

    if fichier:
        return lire_fichier(fichier, lignes, avec_hash, inclure_prive)
    if fichiers:
        chemins = decouper_liste(fichiers)
        if not chemins:
            print("REFUS : --fichiers vide.")
            return 2
        return lire_fichiers(chemins, lignes, avec_hash, inclure_prive)
    return lire_dossier(dossier, lignes, avec_hash, filtre, recursif, inclure_prive)
