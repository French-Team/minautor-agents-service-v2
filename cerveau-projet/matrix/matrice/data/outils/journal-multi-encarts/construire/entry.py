"""Categorie construire : regenere le journal multi-encarts depuis les BDD (jamais a la main)."""
from constants import CHEMIN_JOURNAL, ENCARTS, ENCODAGE, FLUX
from commun import (
    composer_encart,
    entrees_alertes,
    entrees_cameleon,
    entrees_lecons,
    entrees_matrice,
    entrees_missions,
    entrees_modifications,
    entrees_routines,
    entrees_usages,
    entrees_variables,
)

FONCTIONS_ENCARTS = {
    "matrice": entrees_matrice,
    "missions": entrees_missions,
    "routines": entrees_routines,
    "alertes": entrees_alertes,
    "cameleon": entrees_cameleon,
    "usages": entrees_usages,
    "modifications": entrees_modifications,
    "lecons": entrees_lecons,
    "variables": entrees_variables,
}


def executer(arguments):
    """Regenere le journal complet (ordre ferme des encarts). Retourne 0."""
    blocs = [
        "# Journal multi-encarts de la Matrice (v3)",
        "",
        "> VISUEL GENERE depuis les BDD -- jamais edite a la main (E-049).",
        "> Regenerer : python main.py construire",
        "",
    ]
    for encart in ENCARTS:
        lignes = FONCTIONS_ENCARTS[encart]()
        blocs.extend(composer_encart(encart, FLUX[encart], lignes))
    contenu = "\n".join(blocs).rstrip() + "\n"
    CHEMIN_JOURNAL.write_text(contenu, encoding=ENCODAGE)
    print("Journal regenere : " + str(CHEMIN_JOURNAL))
    print("Encarts : " + ", ".join(ENCARTS))
    return 0