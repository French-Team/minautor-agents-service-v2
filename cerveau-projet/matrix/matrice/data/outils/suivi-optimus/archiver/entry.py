"""Categorie archiver : sort du journal actif les evenements qui ne doivent pas y etre.

Interface entre main.py et les fonctions simples (archiver/fonctions.py).

Deux sorties possibles, meme discipline et meme ordre de securite :
  - HORS PERIMETRE (defaut) : evenements dont la mission n'est pas MO- ;
  - DOUBLONS (--doublons)   : 2e debut ou 2e fin pour la meme mission.

Ordre de securite : on ARCHIVE D'ABORD, on reecrit le journal ENSUITE, on
recalcule l'empreinte EN DERNIER. Si l'archive echoue, le journal n'a pas ete
touche ; si la reecriture echoue, l'archive contient deja tout.
"""
import argparse
from pathlib import Path

from archiver.fonctions import ajouter_archive, indexer_doublons, reecrire, separer
from commun import calculer_empreinte_si_existe, lire_evenements
from constants import (
    ACTIONS_SINGULIERES,
    CHEMIN_RELATIF_ARCHIVE_DOUBLONS,
    CHEMIN_RELATIF_ARCHIVE_HORS_PERIMETRE,
    CHEMIN_RELATIF_BDD,
    CHEMIN_RELATIF_EMPREINTE,
    ENCODAGE,
    PREFIXE_MISSION,
    REPERTOIRE_MATRIX,
)


def ecrire_empreinte(chemin, journal):
    """Recalcule et ecrit l'empreinte du journal. Retourne la valeur (ou None)."""
    nouvelle = calculer_empreinte_si_existe(journal)
    if nouvelle and chemin.parent.is_dir():
        with open(str(chemin), "w", encoding=ENCODAGE, newline="\n") as flux:
            flux.write(nouvelle + "\n")
    return nouvelle


def archiver_hors_perimetre(matrice, journal, empreinte, evenements):
    """Sort du journal les evenements dont la mission n'est pas du perimetre."""
    archive = matrice / CHEMIN_RELATIF_ARCHIVE_HORS_PERIMETRE
    dedans, dehors = separer(evenements, PREFIXE_MISSION)
    if not dehors:
        print(
            "Rien a archiver : les " + str(len(evenements)) + " evenement(s) sont tous"
            " dans le perimetre (" + PREFIXE_MISSION + ")."
        )
        return 0

    ecrits = ajouter_archive(archive, dehors)
    reecrire(journal, dedans)
    nouvelle = ecrire_empreinte(empreinte, journal)

    print("Archive  : " + str(ecrits) + " ecrit(s) / " + str(len(dehors))
          + " hors perimetre (jumeaux deja archives ignores) -> " + str(archive))
    print("Journal  : " + str(len(evenements)) + " -> " + str(len(dedans))
          + " evenement(s) dans le perimetre (" + PREFIXE_MISSION + ")")
    print("Empreinte recalculee : " + (nouvelle[:16] + "..." if nouvelle else "(aucune)"))
    return 0


def archiver_doublons(matrice, journal, empreinte, evenements):
    """Sort du journal les 2e debut / 2e fin de la MEME mission (doublons).

    Le controle `verifier` remonte ces doublons en ECART : le journal doit
    repasser a UN debut + UNE fin par mission. Le premier evenement fait foi.
    """
    archive = matrice / CHEMIN_RELATIF_ARCHIVE_DOUBLONS
    gardes, doublons = indexer_doublons(evenements, ACTIONS_SINGULIERES)
    if not doublons:
        print(
            "Rien a dedoublonner : les " + str(len(evenements)) + " evenement(s) sont"
            " a UN seul " + " / ".join(ACTIONS_SINGULIERES) + " par mission."
        )
        return 0

    ecrits = ajouter_archive(archive, doublons)
    reecrire(journal, gardes)
    nouvelle = ecrire_empreinte(empreinte, journal)

    for evenement in doublons:
        print("Doublon  : " + str(evenement.get("mission")) + " "
              + str(evenement.get("action")) + " du " + str(evenement.get("date"))
              + " (le premier evenement fait foi)")
    print("Archive  : " + str(ecrits) + " ecrit(s) / " + str(len(doublons))
          + " doublon(s) -> " + str(archive))
    print("Journal  : " + str(len(evenements)) + " -> " + str(len(gardes))
          + " evenement(s) (UN debut + UNE fin par mission)")
    print("Empreinte recalculee : " + (nouvelle[:16] + "..." if nouvelle else "(aucune)"))
    return 0


def executer(arguments):
    """Archive les evenements hors perimetre (ou les doublons) et reecrit le journal."""
    analyseur = argparse.ArgumentParser(
        description="Sort du journal suivi-optimus les evenements hors perimetre OPTIMUS"
                    " ou les doublons debut/fin"
    )
    analyseur.add_argument(
        "--racine", default=None,
        help="Racine matrix/ a traiter (defaut : celle du depot ; sert aux cobayes)",
    )
    analyseur.add_argument(
        "--doublons", action="store_true",
        help="Dedoublonner : sortir les 2e debut / 2e fin d'une meme mission"
             " (l'ECART que le verbe `verifier` remonte)",
    )
    options = analyseur.parse_args(arguments)

    matrice = Path(options.racine).resolve() if options.racine else REPERTOIRE_MATRIX
    journal = matrice / CHEMIN_RELATIF_BDD
    empreinte = matrice / CHEMIN_RELATIF_EMPREINTE

    if not journal.is_file():
        print("Journal introuvable : " + str(journal))
        return 2

    evenements = lire_evenements(journal)
    if options.doublons:
        return archiver_doublons(matrice, journal, empreinte, evenements)
    return archiver_hors_perimetre(matrice, journal, empreinte, evenements)
