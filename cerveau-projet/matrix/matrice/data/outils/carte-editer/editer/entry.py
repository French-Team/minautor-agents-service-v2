"""Entree du verbe editer : options -> premesses -> remplacement par la porte.

Role : ORCHESTRER. Les regles de forme ne vivent pas ici : elles viennent du
domicile partage (carte_identite.py).
"""
# commun D ABORD : son bloc de lancement pose data/commun sur le chemin avant
# tout import du domicile partage (l ordre des imports tue en silence).
from commun import CLE_SANS_VALEUR, extraire_options
from constants import CODE_REFUS

from editer.fonctions import editer

NOMS_CONNUS = ("fichier", "nouveau-fichier")


def executer_verbe(arguments):
    """Parse, refuse ce qui manque, puis remplace (la logique est en fonctions)."""
    options = extraire_options(arguments, NOMS_CONNUS, outil="carte-editer")
    sans_valeur = options.get(CLE_SANS_VALEUR)
    if sans_valeur:
        print("REFUS : option privee de valeur : "
              + ", ".join("--" + nom for nom in sans_valeur))
        return CODE_REFUS
    if not options.get("fichier"):
        print("REFUS : --fichier est obligatoire (le document dont la carte change)")
        return CODE_REFUS
    if not options.get("nouveau-fichier"):
        print("REFUS : --nouveau-fichier est obligatoire (le NOUVEAU front-matter,"
              " un fichier qui porte deja la carte validee)")
        return CODE_REFUS
    return editer(options)
