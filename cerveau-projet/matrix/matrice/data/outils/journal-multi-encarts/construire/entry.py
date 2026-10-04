"""Categorie construire : regenere le journal multi-encarts depuis les BDD (jamais a la main).

DEPUIS EO-394, LE VISUEL PORTE SA CARTE D'IDENTITE, ET C'EST LE GENERATEUR QUI
L'EMET. Le fichier est reecrit a chaque `construire` : une carte posee a la main
aurait ete effacee a la regeneration suivante, et le rouge du garde `cartes` serait
revenu tout seul. Le generateur emet donc la carte ET la verifie avec la grammaire
de son domicile (`matrice/data/commun/carte_identite.py`, M-076) : un visuel qui
naitrait sans ses trois cles obligatoires n'est PAS publie (code 1, le visuel
precedent reste intact).
"""
from constants import CARTE, CHEMIN_JOURNAL, ENCARTS, ENCODAGE, FLUX
from carte_identite import CLE_IDENTITE, CLES_OBLIGATOIRES, MARQUEUR_FRONT, lire_carte
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


USAGE = "Usage : python main.py construire"


def carte_du_visuel():
    """Les lignes de la carte d'identite EMISE en tete du visuel (EO-394).

    La carte est un front-matter (`---` / `identite:`) EN TETE de fichier : elle
    precede donc le titre, sans quoi la grammaire ne la lit pas (elle exige que la
    PREMIERE ligne du document soit le marqueur). Les valeurs viennent de
    constants.py ; les trois cles obligatoires viennent du DOMICILE de la grammaire.
    """
    lignes = [MARQUEUR_FRONT, CLE_IDENTITE]
    for ligne in CARTE:
        lignes.append("  " + ligne)
    lignes.append(MARQUEUR_FRONT)
    return lignes


def verifier_carte(lignes):
    """(vrai, "") si la carte emise porte les trois cles obligatoires, sinon (faux, motif).

    Un generateur qui publierait une carte INCOMPLETE rendrait le rouge au lieu de
    le fermer : la verification passe donc AVANT l'ecriture, et son echec REFUSE --
    le visuel precedent reste en place, intact.
    """
    carte = lire_carte("\n".join(lignes) + "\n")
    if carte is None:
        return False, "la carte emise n'est pas lisible par la grammaire de la carte"
    manquantes = [cle for cle in CLES_OBLIGATOIRES if cle not in carte]
    if manquantes:
        return False, "cles obligatoires absentes : " + ", ".join(manquantes)
    return True, ""


def executer(arguments):
    """Regenere le journal complet (ordre ferme des encarts). Retourne 0."""
    from options import extraire_options
    # Ce VERBE ne declare AUCUNE option : le domicile refuse tout --xxx (T2 de PB-002).
    extraire_options(arguments, (), outil="journal-multi-encarts", usage=USAGE)
    carte = carte_du_visuel()
    valide, motif = verifier_carte(carte)
    if not valide:
        print("REFUS : le visuel n'est PAS regenere -- carte d'identite : " + motif)
        return 1
    blocs = carte + [
        "",
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