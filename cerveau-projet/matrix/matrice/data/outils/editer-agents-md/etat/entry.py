"""Categorie etat : affiche l'encart session-matrix de AGENTS.md (lecture seule)."""
from commun import (
    charger_texte,
    lire_empreinte_enregistree,
    trouver_agents_md,
)
from constants import MARQUEUR_DEBUT, MARQUEUR_FIN

USAGE = "Usage : python main.py etat"
# Ce VERBE ne declare AUCUNE option (lecture seule) : le DOMICILE refuse donc tout
# --xxx en le NOMMANT (T3 de PB-002, MO-302). MESURE : `etat --option-bidon-mo202 1`
# rendait code 0 -- l option fautive etait ignoree, et l etat partait : le defaut se
# lisait comme le resultat demande (EO-179, L-055). Trouve par l AXE 2 de la sonde,
# qui n existait pas avant ce round.
OPTIONS = ()


def executer(arguments):
    from options import extraire_options
    extraire_options(arguments, OPTIONS, outil="editer-agents-md", usage=USAGE)
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
