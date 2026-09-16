"""Fonctions simples de la categorie tour : une seule tache chacune.

Separation stricte entre OBSERVER (calculer un constat) et JOURNALISER (l'ecrire).
C'est cette separation qui rend possible le mode `verifier` -- un diagnostic qui
constate sans rien ecrire dans le journal (lecon L-041 : un mode diagnostic ne
laisse pas de trace dans l'etat du service qu'il observe ; ici, une route qui
declare `ecriture: false` ne doit pas faire grossir un journal en ajout seul).

Depuis MO-081, OBSERVER ne journalise JAMAIS de lui-meme : la decision d'ecrire
appartient au CONTROLE ENTIER (le tableau des 14 BDD), pas a une observation
isolee. Une observation seule ne peut pas savoir si le tableau a change -- et
c'est le tableau, pas la ligne, qui est le fait.
"""
from commun import (
    calculer_empreinte_si_existe,
    chemin_bdd,
    journaliser,
    lire_empreinte_enregistree,
)


def observer_bdd(nom_bdd, faite, chapitre_integrite, chapitre_presence):
    """Observe UNE BDD : rend (constat, chapitre). AUCUNE ecriture.

    BDD faite : ECART si empreinte fausse ou BDD absente.
    BDD a-construire : INFO (presente ou pas), jamais une fausse alerte.
    """
    chemin = chemin_bdd(nom_bdd)
    if not faite:
        constat = {
            "bdd": nom_bdd,
            "etat": "INFO",
            "detail": "BDD a construire (absente du disque : " + str(not chemin.exists()) + ")",
        }
        return constat, chapitre_presence

    # Chapitre 1 : integrite (empreinte reelle vs etalon)
    empreinte_reelle = calculer_empreinte_si_existe(chemin)
    empreinte_etalon = lire_empreinte_enregistree(nom_bdd)
    if empreinte_reelle is None:
        constat = {"bdd": nom_bdd, "etat": "ECART", "detail": "BDD faite mais absente du disque"}
    elif empreinte_etalon is None:
        constat = {
            "bdd": nom_bdd,
            "etat": "INFO",
            "detail": "pas d'etalon pose pour cette BDD (journal en ajout seul, sans empreinte)",
        }
    elif empreinte_reelle != empreinte_etalon:
        constat = {"bdd": nom_bdd, "etat": "ECART", "detail": "empreinte reelle != etalon (BDD modifiee hors outil)"}
    else:
        constat = {"bdd": nom_bdd, "etat": "ok", "detail": "integrite verifiee"}
    return constat, chapitre_integrite


def journaliser_observation(constat):
    """Journalise UNE observation (elle porte deja son chapitre, MO-081).

    Appelee par le CONTROLE quand le tableau a change -- jamais observation par
    observation : le fait est le tableau, pas la ligne (et l'etat court le porte
    a chaque passe sans rien ecrire).
    """
    journaliser({"type": "observation", **constat})
