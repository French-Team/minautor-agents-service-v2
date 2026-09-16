"""Categorie lire : orchestre la lecture d'un ou plusieurs fichiers.

Interface entre main.py et les fonctions simples (lire/fonctions.py).
"""
from commun import extraire_options
from lire.fonctions import lire_dossier, lire_fichier, lire_fichiers

NOMS_OPTIONS = ("fichier", "fichiers", "dossier", "lignes", "hash", "filtre", "recursif")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    fichier = options.get("fichier", "")
    fichiers = options.get("fichiers", "")
    dossier = options.get("dossier", "")
    lignes = options.get("lignes", "")
    avec_hash = "hash" in options
    filtre = options.get("filtre", "")
    recursif = "recursif" in options

    cibles = sum(1 for v in (fichier, fichiers, dossier) if v)
    if cibles == 0:
        print("Usage : python main.py lire --fichier <chemin> [--lignes debut:fin] [--hash]")
        print("       python main.py lire --fichiers <c1,c2> [--lignes debut:fin] [--hash]")
        print("       python main.py lire --dossier <chemin> [--filtre *.py] [--recursif] [--hash]")
        return 2
    if cibles > 1:
        print("REFUS : une seule cible a la fois (--fichier OU --fichiers OU --dossier).")
        return 2

    if fichier:
        return lire_fichier(fichier, lignes, avec_hash)
    if fichiers:
        chemins = [c.strip() for c in fichiers.split(",") if c.strip()]
        if not chemins:
            print("REFUS : --fichiers vide.")
            return 2
        return lire_fichiers(chemins, lignes, avec_hash)
    return lire_dossier(dossier, lignes, avec_hash, filtre, recursif)
