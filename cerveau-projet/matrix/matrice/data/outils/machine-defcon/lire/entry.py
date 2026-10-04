"""Categorie lire : etat courant + echelle fermee + dernieres transitions."""
from commun import lire_journal, lire_niveau
from lire.fonctions import composer_echelle, composer_etat

USAGE = "Usage : python main.py lire"
# Ce VERBE ne declare AUCUNE option : le DOMICILE refuse donc tout --xxx en le
# NOMMANT (T3 de PB-002, MO-302). MESURE : `lire --option-bidon-mo202 1` rendait
# code 0 -- l option etait avalee et l etat du defcon partait comme si de rien
# n etait (EO-179, L-055). Trouve par l AXE 2 de la sonde, qui n existait pas avant
# ce round.
OPTIONS = ()


def executer(arguments):
    from options import extraire_options
    extraire_options(arguments, OPTIONS, outil="machine-defcon", usage=USAGE)
    niveau, message = lire_niveau()
    if niveau is None:
        print(message)
        return 1
    print(composer_etat(niveau))
    print("Echelle fermee (5 = max) :")
    for ligne in composer_echelle():
        print(ligne)
    transitions = lire_journal()
    if transitions:
        print("Dernieres transitions :")
        for t in transitions:
            print(
                "  " + t["quand"] + "  "
                + str(t["de"]) + " -> " + str(t["vers"])
                + "  (" + t["raison"] + ")"
            )
    else:
        print("Aucune transition journalisee.")
    return 0
