"""Categorie tour : orchestre UNE passe de la vigie-portes.

Interface entre main.py et les fonctions simples (tour/fonctions.py).
"""
from datetime import datetime
from pathlib import Path

from commun import lire_etat_passes
from constants import INTERVALLE_DECLARE_SECONDES, REPERTOIRE_MATRIX
from tour.fonctions import derniere_passe, executer_tour, passe_due

# `--sans-signal` = passe a BLANC (rapport et journal, aucun depot).
# `--si-due` = la passe n'est jouee QUE si la cadence declaree est echue.
OPTION_SANS_SIGNAL = "--sans-signal"
OPTION_SI_DUE = "--si-due"


def extraire_racine(arguments):
    """Racine matrix/ a controler (--racine <chemin>) ; defaut : celle du depot.

    --racine existe pour pouvoir PIEUGER le controle (lecon L-032 : un controle
    qu'on ne peut pas pieger ne prouve rien). C'est aussi ce qui permet de faire
    tourner la vigie sur un arbre cobaye sans toucher aux vraies donnees.
    """
    for index, morceau in enumerate(arguments):
        if morceau == "--racine" and index + 1 < len(arguments):
            return Path(arguments[index + 1]).resolve()
    return REPERTOIRE_MATRIX


def executer_si_due(racine, signaler_actif=True):
    """Joue la passe SEULEMENT si la cadence declaree est echue.

    LA CADENCE EST UN CONTRAT : la roue publie son battement (l'anneau de passes)
    et le garde de cadence le MESURE. Une passe A LA DEMANDE qui tombe avant
    l'echeance fait battre la routine plus vite qu'elle ne le declare, et le garde
    accuse alors un battement REEL -- la vigie se contredit elle-meme (mesure du
    2026-09-20 pendant MO-292 a MO-295 : 5 passes de round en 29 min, median 261 s
    pour 900 s declarees). Ici une passe fraiche n'est PAS rejouee : l'age de la
    derniere passe est DIT, la derniere photo de la vigie est rappelee, et le code
    rendu est 0 (rien a faire, le verdict tient jusqu'a l'echeance).
    """
    etat_passes = lire_etat_passes()
    due, age = passe_due(derniere_passe(etat_passes), INTERVALLE_DECLARE_SECONDES, datetime.now())
    if due:
        return executer_tour(racine, signaler_actif=signaler_actif)
    print("VIGIE-PORTES -- passe NON DUE : derniere passe il y a " + str(int(age)) + " s"
          " pour une cadence declaree de " + str(INTERVALLE_DECLARE_SECONDES) + " s.")
    print("  derniere photo : " + str(etat_passes.get("portes", "?")) + " porte(s), "
          + str(etat_passes.get("alertes", "?")) + " alerte(s), "
          + str(etat_passes.get("date", "date inconnue")))
    return 0


def executer(arguments):
    """Lance la passe. --sans-signal = passe a BLANC ; --si-due = si cadence echue.

    Une vigie doit pouvoir etre REGARDEE avant de tirer (premier lancement,
    diagnostic, essai sur un cobaye) : dans ce mode elle affiche et journalise
    mais ne depose RIEN dans l'inbox de la Matrice.
    """
    racine = extraire_racine(arguments)
    signaler_actif = OPTION_SANS_SIGNAL not in arguments
    if OPTION_SI_DUE in arguments:
        return executer_si_due(racine, signaler_actif)
    return executer_tour(racine, signaler_actif=signaler_actif)
