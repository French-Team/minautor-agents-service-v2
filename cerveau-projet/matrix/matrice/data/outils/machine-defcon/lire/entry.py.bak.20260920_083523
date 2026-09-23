"""Categorie lire : etat courant + echelle fermee + dernieres transitions."""
from commun import lire_journal, lire_niveau
from lire.fonctions import composer_echelle, composer_etat


def executer(arguments):
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
