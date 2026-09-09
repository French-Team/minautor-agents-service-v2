"""Categorie valider : clot def3 (defcon 3 -> 2, periode de validation definitive)."""
from commun import (
    appliquer_transition,
    charger_classeur,
    extraire_options,
    journaliser_transition,
    lire_niveau,
    trouver_defcon,
)
from constants import NOMS_NIVEAUX
from valider.fonctions import verifier_validation

NOMS_OPTIONS = ("--raison",)


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    if not options.get("--raison"):
        print("Usage : python main.py valider --raison \"...\"")
        return 2
    raison = options["--raison"]

    niveau_avant, message = lire_niveau()
    if niveau_avant is None:
        print(message)
        return 1
    donnees = charger_classeur()
    courant, entree = trouver_defcon(donnees)
    code, message_garde = verifier_validation(courant)
    if code != 0:
        print(message_garde)
        return code

    source = "machine-defcon valider"
    appliquer_transition(donnees, entree, 2, source)
    journaliser_transition(courant, 2, raison, source)
    print(
        "defcon " + str(courant) + " -> 2 (" + NOMS_NIVEAUX[2]
        + ") -- periode de surveillance validee, def3 clot : " + raison
    )
    return 0
