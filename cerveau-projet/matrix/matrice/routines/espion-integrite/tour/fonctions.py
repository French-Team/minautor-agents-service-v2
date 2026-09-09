"""Fonctions simples de la categorie tour : une seule tache chacune."""
from commun import (
    calculer_empreinte_si_existe,
    chemin_bdd,
    journaliser,
    lire_empreinte_enregistree,
)


def surveiller_bdd(nom_bdd, faite, chapitre_integrite, chapitre_presence):
    """Surveille UNE BDD : Chapitre 1 integrite, Chapitre 2 presence.

    BDD faite : ECART si empreinte fausse ou BDD absente.
    BDD a-construire : INFO (presente ou pas), jamais une fausse alerte.
    Retourne le constat {bdd, etat, detail}.
    """
    chemin = chemin_bdd(nom_bdd)
    if not faite:
        constat = {
            "bdd": nom_bdd,
            "etat": "INFO",
            "detail": "BDD a construire (absente du disque : " + str(not chemin.exists()) + ")",
        }
        journaliser({"type": "observation", "chapitre": chapitre_presence, **constat})
        return constat

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

    journaliser({"type": "observation", "chapitre": chapitre_integrite, **constat})
    return constat
