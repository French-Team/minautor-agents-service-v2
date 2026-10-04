"""Entree du verbe creer : options -> premesses -> pose par la porte.

Role : ORCHESTRER. Les regles de forme ne vivent pas ici : elles viennent du
domicile partage (carte_identite.py) et du modele de reference.
"""
# commun D ABORD : son bloc de lancement pose data/commun sur le chemin avant
# tout import du domicile partage (l ordre des imports tue en silence).
from commun import CLE_SANS_VALEUR, extraire_options
from constants import CHOIX_MODELE, CHOIX_MODELE_DEFAUT, CODE_REFUS

from creer.fonctions import poser

NOMS_CONNUS = ("fichier", "type", "appartient-a", "commun", "liens",
               "version", "date", "statut", "tags", "modele")


def executer_verbe(arguments):
    """Parse, refuse ce qui manque, puis pose (la logique est en fonctions)."""
    options = extraire_options(arguments, NOMS_CONNUS, outil="carte-creer")
    sans_valeur = options.get(CLE_SANS_VALEUR)
    if sans_valeur:
        print("REFUS : option privee de valeur : "
              + ", ".join("--" + nom for nom in sans_valeur))
        return CODE_REFUS
    if not options.get("fichier"):
        print("REFUS : --fichier est obligatoire (le document qui recoit la carte)")
        return CODE_REFUS
    if not options.get("type"):
        print("REFUS : --type est obligatoire (cle obligatoire, vocabulaire ferme)")
        return CODE_REFUS
    if not options.get("appartient-a"):
        print("REFUS : --appartient-a est obligatoire (un NOM, jamais un chemin)")
        return CODE_REFUS
    choix = (options.get("modele") or CHOIX_MODELE_DEFAUT).strip().lower()
    if choix not in CHOIX_MODELE:
        print("REFUS : --modele inconnu : " + choix
              + " (connus : " + ", ".join(CHOIX_MODELE) + ")")
        return CODE_REFUS
    return poser(options)
