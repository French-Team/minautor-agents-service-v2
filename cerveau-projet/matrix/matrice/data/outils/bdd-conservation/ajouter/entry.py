"""Porte des propositions, classements et decisions de conservation."""
from commun import charger_bdd, enregistrer_bdd, extraire_options
from ajouter.fonctions import classer_entree, creer_entree, decider_entree, preciser_entree

NOMS_OPTIONS = (
    "source", "destination", "categorie", "raison", "lecteurs", "ecrivains",
    "index", "sha-avant", "sha-apres", "octets-avant", "octets-apres",
    "lignes-avant", "lignes-apres", "restaurable", "archive", "preuve",
    "tags", "mission", "id", "verdict",
)


def executer(arguments):
    verbe = arguments[0] if arguments else ""
    options = extraire_options(arguments[1:], NOMS_OPTIONS)
    donnees = charger_bdd()

    if verbe == "proposer":
        entree, message = creer_entree(donnees, options)
    elif verbe == "classer":
        entree, message = classer_entree(
            donnees, options.get("id", ""), options.get("categorie", ""), options.get("raison", "")
        )
    elif verbe == "decider":
        entree, message = decider_entree(
            donnees, options.get("id", ""), options.get("verdict", ""),
            options.get("destination", ""), options.get("preuve", "")
        )
    elif verbe == "preciser":
        entree, message = preciser_entree(
            donnees, options.get("id", ""), options.get("preuve", ""), options.get("raison", "")
        )
    else:
        print("Usage : proposer | classer | decider | preciser")
        return 2

    if entree is None:
        print("Refus : " + message)
        return 2
    empreinte = enregistrer_bdd(donnees)
    print(
        "Element " + entree["id"] + " " + entree["statut"]
        + " (operation " + entree["operation"] + ") -- empreinte : " + empreinte[:16] + "..."
    )
    return 0
