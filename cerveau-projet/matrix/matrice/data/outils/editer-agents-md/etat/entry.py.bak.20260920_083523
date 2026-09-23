"""Categorie etat : affiche l'encart session-matrix de AGENTS.md (lecture seule)."""
from commun import (
    charger_texte,
    lire_empreinte_enregistree,
    trouver_agents_md,
)
from constants import MARQUEUR_DEBUT, MARQUEUR_FIN


def executer(arguments):
    chemin = trouver_agents_md()
    texte = charger_texte(chemin)
    print("AGENTS.md : " + str(chemin))
    empreinte = lire_empreinte_enregistree()
    print(
        "Empreinte enregistree : "
        + (empreinte[:16] + "..." if empreinte else "aucune (jamais ecrit par l'outil)")
    )
    if MARQUEUR_DEBUT in texte and MARQUEUR_FIN in texte:
        debut = texte.index(MARQUEUR_DEBUT)
        fin = texte.index(MARQUEUR_FIN) + len(MARQUEUR_FIN)
        print("--- Encart session-matrix ---")
        print(texte[debut:fin])
    else:
        print("Encart session-matrix : ABSENT (jamais cree).")
    return 0
