"""Categorie lire : orchestre la consultation de la BDD.

Interface entre main.py et les fonctions simples (lire/fonctions.py).
"""
from commun import canoniser_cle, charger_bdd, extraire_options
from lire.fonctions import afficher, filtrer

NOMS_OPTIONS = ("fichier", "tag")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    donnees = charger_bdd()
    # EO-363 : lire sous la MEME cle canonique que l ecriture -- les deux formes
    # d un meme fichier ne peuvent plus rendre deux lectures differentes.
    fichier = options.get("fichier")
    resultats = filtrer(donnees, canoniser_cle(fichier) if fichier else fichier,
                        options.get("tag"))
    afficher(resultats)
    return 0
