"""Fonctions simples de la categorie profil : une seule tache chacune.

Le guidage suit le PARCOURS dedie : theme USER-PROFIL (parcours/themes/
theme-user-profil.json). L'etat de la fiche n'est jamais recalcule ici : il
vient du motif PARTAGE `matrice/data/commun/fiche_profil.py` (jamais recopie,
M-076) -- c'est la meme verite que celle de la routine vigie-profil.

Garde-fou du guidage : le parcours est la CONSIGNE que l'agent suit pour poser
les questions, donc un champ attendu qu'aucune etape ne nomme est un champ que
l'agent ne demandera jamais. `guider` refuse alors de charger la mission au lieu
d'exiger un travail qui ne peut pas aboutir (cas reel : le FUSEAU HORAIRE,
absent du parcours alors que le motif le compte parmi ses 8 champs attendus).
"""
import json
import subprocess
import sys
import unicodedata
from pathlib import Path

import fiche_profil as motif_profil

from commun import charger_file
from constants import (
    CHEMIN_FILE,
    CHEMIN_THEME_PROFIL,
    STATUT_EN_ATTENTE,
    THEME_PROFIL,
)
from file.fonctions import afficher_file, charger_mission

REPERTOIRE_CATEGORIE = Path(__file__).resolve().parent
BESOIN_QUESTIONS = "Poser"

# Mots de liaison ignores quand on lit un libelle de champ ("Style de conversation").
MOTS_VIDES = frozenset(("de", "du", "des", "la", "le", "les", "un", "une", "et", "en", "au", "aux"))
LONGUEUR_MOT_MIN = 3


def mots_cles(libelle):
    """Mots significatifs d'un libelle : minuscules, sans accent, sans elision.

    Comparaison MOT A MOT, jamais par sous-chaine : "age" est une sous-chaine
    de "apprentissage", et le garde-fou serait aveugle. Le pluriel final est
    ramene au singulier ("sujets" == "sujet") : le parcours ecrit l'etape comme
    il veut, tant qu'il NOMME le champ.
    """
    sans_accent = unicodedata.normalize("NFKD", libelle)
    sans_accent = "".join(c for c in sans_accent if not unicodedata.combining(c))
    mots = []
    for mot in "".join(c if c.isalnum() else " " for c in sans_accent.lower()).split():
        if mot in MOTS_VIDES or len(mot) < LONGUEUR_MOT_MIN:
            continue
        if len(mot) > 4 and mot.endswith("s"):
            mot = mot[:-1]
        mots.append(mot)
    return mots


def vocabulaire_parcours(parcours):
    """Mots nommes par les etapes du parcours (et par ses regles)."""
    morceaux = []
    for redirect in (parcours or {}).get("redirects", []):
        morceaux.extend(redirect.get("etapes", []))
        if redirect.get("regle"):
            morceaux.append(redirect["regle"])
    return set(mots_cles(" ".join(morceaux)))


def champs_non_poses(etat, parcours):
    """Champs ATTENDUS encore vides qu'AUCUNE etape du parcours ne nomme.

    Un champ deja rempli (la LANGUE, pourvue d'une valeur par defaut) n'est
    jamais reclame : inutile de le nommer dans le parcours.
    """
    vocabulaire = vocabulaire_parcours(parcours)
    return [champ for champ in etat["attendus_vides"] if not set(mots_cles(champ)) <= vocabulaire]


def etat_fiche():
    """Etat de remplissage de la fiche utilisateur (motif partage)."""
    etat = motif_profil.etat(REPERTOIRE_CATEGORIE)
    etat["description"] = motif_profil.description(etat)
    return etat


def afficher_etat(etat):
    """Affiche l'etat de la fiche (jamais de guidage ici)."""
    if not etat["attendus_vides"]:
        print("PROFIL UTILISATEUR : REMPLI (" + str(etat["pourcentage"]) + "%)")
        return 0
    print("PROFIL UTILISATEUR : NON REMPLI (" + str(etat["pourcentage"]) + "%)")
    print("Champs restants : " + ", ".join(etat["attendus_vides"]))
    print("Action : python main.py profil --guider   (guidage sur le parcours)")
    print("         python main.py profil --remplir   (questionnaire direct)")
    return 0


def lire_parcours():
    """Theme USER-PROFIL lu sur le disque (but + questions), ou None."""
    if not CHEMIN_THEME_PROFIL.is_file():
        return None
    try:
        theme = json.loads(CHEMIN_THEME_PROFIL.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return theme.get("theme", {})


def mission_en_attente():
    """Vrai si une mission USER-PROFIL attend deja dans la file (anti-doublon)."""
    if not CHEMIN_FILE.is_file():
        return False
    try:
        file_missions = json.loads(CHEMIN_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    for mission in file_missions.get("missions", []):
        if mission.get("theme") == THEME_PROFIL and mission.get("statut") == STATUT_EN_ATTENTE:
            return True
    return False


def objectif_mission(etat):
    """Objectif de la mission de remplissage, construit sur les champs vides."""
    return (
        "Remplir la fiche USER-PROFIL.md avec l'utilisateur ("
        + str(len(etat["attendus_vides"])) + " champ(s) restant(s) : "
        + ", ".join(etat["attendus_vides"]) + "). Une question a la fois."
    )


def guider(etat):
    """Guide l'agent sur le parcours USER-PROFIL et charge la mission si besoin.

    Silence quand la fiche est complete (anti-bruit). Jamais de mission en
    double : une mission USER-PROFIL deja en attente suffit.
    """
    if not etat["attendus_vides"]:
        print("PROFIL UTILISATEUR : REMPLI -- rien a guider.")
        return 0
    parcours = lire_parcours()
    if parcours is None:
        print("REFUS : parcours " + THEME_PROFIL + " introuvable (" + str(CHEMIN_THEME_PROFIL) + ")")
        return 1
    print("PARCOURS " + THEME_PROFIL + " -- a remplir AVEC l'utilisateur")
    print("Fiche : " + etat["chemin"])
    print("Etat  : " + str(etat["pourcentage"]) + "% -- " + etat["description"])
    if parcours:
        print("But : " + parcours.get("but", ""))
        for redirect in parcours.get("redirects", []):
            if redirect.get("besoin", "").startswith(BESOIN_QUESTIONS):
                print("Questions (une seule a la fois) :")
                for etape in redirect.get("etapes", []):
                    print("  - " + etape)
                print("Regle : " + redirect.get("regle", ""))
    non_poses = champs_non_poses(etat, parcours)
    if non_poses:
        print("ECART PARCOURS : champ(s) attendu(s) jamais nomme(s) dans les questions -- "
              + ", ".join(non_poses))
        print("  La fiche resterait plafonnee : le parcours doit demander ce champ ("
              + CHEMIN_THEME_PROFIL.name + ").")
        print("  Mission NON chargee : un travail qui ne peut pas aboutir ne se charge pas.")
        return 1
    if mission_en_attente():
        print("Mission " + THEME_PROFIL + " deja en attente : pas de doublon charge.")
        return 0
    return charger_mission(
        ["--theme", THEME_PROFIL, "--objectif", objectif_mission(etat)],
        charger_file,
        afficher_file,
    )


def remplir():
    """Lance le questionnaire interactif de remplissage (voie directe)."""
    questionnaire = REPERTOIRE_CATEGORIE / "questionnaire.py"
    if not questionnaire.is_file():
        print("Questionnaire absent : " + str(questionnaire))
        return 1
    return subprocess.run([sys.executable, str(questionnaire)]).returncode
