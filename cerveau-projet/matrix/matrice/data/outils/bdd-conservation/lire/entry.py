"""Porte de lecture du registre de conservation."""
import json

from commun import charger_bdd, extraire_options
from lire.fonctions import afficher, filtrer

NOMS_OPTIONS = ("tag", "categorie", "statut", "verdict", "id")


def manifeste(donnees):
    """Affiche un manifeste deterministe, sans ecrire sur le disque."""
    elements = donnees.get("elements", [])
    resultat = {
        "type": "manifeste-conservation",
        "version": donnees.get("identite", {}).get("version", 1),
        "bdd": "conservation.json",
        "compteur": donnees.get("compteur", 0),
        "nombre_elements": len(elements),
        "elements": [
            {
                "id": entree.get("id", ""),
                "source": entree.get("source", ""),
                "destination": entree.get("destination", ""),
                "categorie": entree.get("categorie", ""),
                "statut": entree.get("statut", ""),
                "verdict": entree.get("verdict", ""),
                "sha_avant": entree.get("sha_avant", ""),
                "sha_apres": entree.get("sha_apres", ""),
                "restaurable": entree.get("restaurable", False),
                "operation": entree.get("operation", ""),
            }
            for entree in elements
        ],
    }
    print(json.dumps(resultat, ensure_ascii=True, indent=2, sort_keys=True))
    return 0


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    donnees = charger_bdd()
    if arguments and arguments[0] == "manifeste":
        return manifeste(donnees)
    afficher(filtrer(donnees, options))
    return 0
