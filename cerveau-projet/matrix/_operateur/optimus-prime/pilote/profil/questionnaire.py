#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Questionnaire du parcours USER-PROFIL : voie directe, une question a la fois.

Ecrit les reponses dans la VRAIE fiche (matrix/USER-PROFIL.md).

Trois regles tenues ici, chacune corrigeant un defaut de l'ancienne version
(fichier deplace depuis pilote/questionnaire.py, ou la porte ne le cherchait pas) :
  - le chemin de la fiche vient du motif PARTAGE `fiche_profil` (M-076).
    L'ancienne version remontait trois parents : elle pointait donc
    `_operateur/USER-PROFIL.md`, un fichier MYTHIQUE -- exactement la classe de
    bug que MO-043 avait deja corrigee ailleurs ;
  - une reponse vide (ou "passer") CONSERVE la valeur existante. L'ancienne
    version regenerait la fiche depuis un template, donc elle ecrasait tout
    (le parcours dit "ne jamais ecraser les reponses existantes") ;
  - le statut de la fiche ne passe a "rempli" que si TOUS les champs attendus
    sont remplis. L'ancien template stampait "rempli" sans jamais poser la
    question du fuseau horaire : la vigie-profil se serait taise a tort.

Usage : python questionnaire.py
"""
import sys
from pathlib import Path

REPERTOIRE_CATEGORIE = Path(__file__).resolve().parent
REPERTOIRE_PILOTE = REPERTOIRE_CATEGORIE.parent
sys.path.insert(0, str(REPERTOIRE_PILOTE))

import constants  # noqa: F401  (pose data/commun dans sys.path, motif M-076)

import fiche_profil as motif_profil

CHEMIN_FICHE = motif_profil.chemin_profil(REPERTOIRE_CATEGORIE)

REPONSE_IGNORER = "passer"
STATUT_A_REMPLIR = "a-remplir"
STATUT_REMPLI = "rempli"

# Champs demandes : (libelle dans la fiche, question posee, options ou None).
# Le libelle doit correspondre EXACTEMENT a une ligne de la fiche, sinon
# `ecrire_valeurs` le signale comme "sans ligne" au lieu de l'inventer.
QUESTIONS = (
    ("Pseudo", "Quel est ton pseudo ?", None),
    ("Age", "Quel est ton age ? (optionnel)", None),
    ("Fuseau horaire", "Quel est ton fuseau horaire ? (ex : Europe/Paris)", None),
    (
        "Style de conversation",
        "Quel style de conversation preferes-tu ?",
        ("Formel", "Decontracte", "Mixte"),
    ),
    ("Sujets d'interet", "Quels sont tes sujets d'interet ?", None),
    (
        "Mode d'apprentissage",
        "Comment preferes-tu apprendre ?",
        ("Visuel", "Texte", "Pratique"),
    ),
    (
        "Niveau technique",
        "Quel est ton niveau technique ?",
        ("Debutant", "Intermediaire", "Avance"),
    ),
)


def poser_question(intitule, options, valeur_actuelle):
    """Pose UNE question. Retourne la reponse ("" = conserver ce qui existe)."""
    print()
    print(intitule)
    if valeur_actuelle:
        print("  (valeur actuelle : " + valeur_actuelle + " -- entree vide, on la garde)")
    if options:
        for rang, option in enumerate(options, 1):
            print("  " + str(rang) + ". " + option)
    reponse = input("Votre reponse (ou '" + REPONSE_IGNORER + "' pour ignorer) : ").strip()
    if reponse.lower() == REPONSE_IGNORER:
        return ""
    if options and reponse.isdigit() and 1 <= int(reponse) <= len(options):
        return options[int(reponse) - 1]
    return reponse


def collecter(valeurs_existantes):
    """Pose toutes les questions du parcours et retourne {champ: reponse}."""
    reponses = {}
    for champ, intitule, options in QUESTIONS:
        reponses[champ] = poser_question(intitule, options, valeurs_existantes.get(champ, ""))
    return reponses


def changements(reponses, valeurs_existantes):
    """Reponses qui apportent vraiment quelque chose (le reste est conserve)."""
    return [
        (champ, reponse)
        for champ, reponse in reponses.items()
        if reponse and reponse != valeurs_existantes.get(champ, "")
    ]


def confirmer(changements_a_ecrire):
    """Resume ce qui va changer puis demande confirmation (refus = rien ecrit)."""
    print()
    print("=" * 60)
    if not changements_a_ecrire:
        print("Aucun changement : la fiche reste telle quelle.")
        return False
    print("Ce qui va etre ecrit dans " + str(CHEMIN_FICHE) + " :")
    for champ, reponse in changements_a_ecrire:
        print("  " + champ + " : " + reponse)
    reponse = input("Confirmer ? (oui/non) : ").strip().lower()
    return reponse in ("oui", "o", "yes", "y")


def ecrire(reponses, valeurs_existantes):
    """Ecrit les seules reponses nouvelles, puis aligne le statut sur l'etat reel."""
    a_ecrire = dict(changements(reponses, valeurs_existantes))
    if not a_ecrire:
        return 0
    etat_apres = dict(valeurs_existantes)
    etat_apres.update(a_ecrire)
    attendus_vides = [c for c in motif_profil.CHAMPS_ATTENDUS if not etat_apres.get(c, "")]
    statut = STATUT_REMPLI if not attendus_vides else STATUT_A_REMPLIR
    ecrits, sans_ligne = motif_profil.ecrire_valeurs(CHEMIN_FICHE, a_ecrire, statut)
    print()
    print("Fiche mise a jour : " + str(len(ecrits)) + " champ(s) ecrit(s).")
    for champ in ecrits:
        print("  ecrit   : " + champ)
    for champ in sans_ligne:
        print("  SANS LIGNE : " + champ + " (aucune ligne de ce nom dans la fiche : a corriger)")
    print("Statut de la fiche : " + statut)
    if attendus_vides:
        print("Champs attendus encore vides : " + ", ".join(attendus_vides))
    return 0


def main():
    print("=" * 60)
    print("QUESTIONNAIRE PROFIL UTILISATEUR")
    print("=" * 60)
    print("Fiche : " + str(CHEMIN_FICHE))
    print()
    print("Bienvenue ! Ces quelques questions servent a personnaliser nos echanges.")
    print("Une seule question a la fois : reponds, ou tape '" + REPONSE_IGNORER + "' pour ignorer.")
    valeurs_existantes = motif_profil.lire_valeurs(CHEMIN_FICHE)
    reponses = collecter(valeurs_existantes)
    if confirmer(changements(reponses, valeurs_existantes)):
        return ecrire(reponses, valeurs_existantes)
    print("Rien n'a ete ecrit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
