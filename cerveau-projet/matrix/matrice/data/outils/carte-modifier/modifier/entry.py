"""Entree du verbe modifier : options -> premesses -> changement par la porte.

Role : ORCHESTRER. Les regles de forme ne vivent pas ici : elles viennent du
domicile partage (carte_identite.py).
"""
# commun D ABORD : son bloc de lancement pose data/commun sur le chemin avant
# tout import du domicile partage (l ordre des imports tue en silence).
from commun import CLE_SANS_VALEUR, extraire_options
from constants import CODE_REFUS

from modifier.fonctions import changer

NOMS_CONNUS = ("fichier", "cle", "valeur")
DRAPEAUX = ("supprimer",)


def executer_verbe(arguments):
    """Parse, refuse ce qui manque, puis change (la logique est en fonctions)."""
    options = extraire_options(arguments, NOMS_CONNUS, drapeaux=DRAPEAUX,
                               outil="carte-modifier")
    sans_valeur = options.get(CLE_SANS_VALEUR)
    if sans_valeur:
        print("REFUS : option privee de valeur : "
              + ", ".join("--" + nom for nom in sans_valeur))
        return CODE_REFUS
    if not options.get("fichier"):
        print("REFUS : --fichier est obligatoire (le document dont la carte change)")
        return CODE_REFUS
    if not options.get("cle"):
        print("REFUS : --cle est obligatoire (le champ a changer)")
        return CODE_REFUS
    a_valeur = "valeur" in options
    a_supprimer = "supprimer" in options
    if a_valeur and a_supprimer:
        print("REFUS : --valeur et --supprimer sont EXCLUSIFS :"
              " un seul geste par appel.")
        return CODE_REFUS
    if not a_valeur and not a_supprimer:
        print("REFUS : il manque le geste : --valeur <valeur> (changer)"
              " ou --supprimer (retirer le champ)")
        return CODE_REFUS
    return changer(options)
