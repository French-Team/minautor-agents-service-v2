"""Fonctions de la categorie verifier : une seule tache chacune."""
from commun import (
    detecter_non_ascii,
    lister_fichiers_conventions,
    lire_lignes,
    verifier_frontmatter,
    verifier_index,
)
from constants import NOM_INDEX, NOM_ZONE_SOURCES, REPERTOIRE_CONVENTIONS

# L'affichage DIT et sa FORMULATION vivent au domicile du jugement (M-076 /
# EO-479) : les trois verificateurs les consomment, aucun ne les porte.
from jugement_citations import afficher_dit, decrire_hors_champ


def afficher_groupe(titre, ecarts):
    """Affiche un groupe d'ecarts sous son titre. Retourne leur nombre."""
    if not ecarts:
        print("OK    " + titre)
        return 0
    print("ECART " + titre)
    for ecart in ecarts:
        print("  - " + ecart)
    return len(ecarts)


def executer_verification():
    """Effectue les 3 controles. Retourne le nombre d'ecarts (0 = conforme)."""
    fichiers = lister_fichiers_conventions()
    total = 0

    total += afficher_groupe(
        "ASCII strict",
        [ecart for chemin in fichiers for ecart in detecter_non_ascii(chemin)],
    )
    total += afficher_groupe(
        "front-matter identite (type + appartient_a)",
        [
            str(chemin) + " -- " + ecart
            for chemin in fichiers
            for ecart in verifier_frontmatter(chemin)
        ],
    )

    chemin_index = REPERTOIRE_CONVENTIONS / NOM_INDEX
    if chemin_index.exists():
        manquants, morts, hors_champ = verifier_index(lire_lignes(chemin_index), fichiers)
        total += afficher_groupe(
            "fichiers absents de l'index",
            [chemin.name for chemin in fichiers if chemin.name in manquants],
        )
        total += afficher_groupe("lignes mortes de l'index", morts)
        afficher_dit(
            "citations HORS CHAMP (zone des SOURCES du createur : "
            + NOM_ZONE_SOURCES + "/)",
            decrire_hors_champ(hors_champ),
        )
    else:
        total += afficher_groupe("index", ["index absent : " + str(chemin_index)])
    return total
