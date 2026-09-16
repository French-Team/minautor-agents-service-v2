"""Fonctions simples de la categorie tour : une seule tache chacune.

La lecture de la fiche (etat, cle anti-spam, description) vient du motif
PARTAGE `matrice/data/commun/fiche_profil.py` : une seule verite sur ce qu'est
une fiche remplie, pour la routine comme pour le pilote.

La DECISION de depot (anti-spam) vit ici, en fonction PURE : elle se teste sans
disque ni horloge reelle (cobaye de MO-070).
"""
import subprocess
import sys
from datetime import datetime

import fiche_profil as motif_profil

from constants import (
    ANTI_SPAM_SECONDES,
    EXPEDITEUR_SIGNAL,
    FORMAT_HORODATAGE,
    MISSION_SIGNAL,
    MOTIF_COMPLET,
    MOTIF_DEPOT,
    MOTIF_EPISODE_OUVERT,
    MOTIF_PLANCHER,
    NIVEAU_SIGNAL,
    OUTIL_SIGNAL,
    OUTIL_SIGNALER,
    REPERTOIRE_ROUTINE,
)
from commun import horodater


def etat_profil():
    """Etat de remplissage de la fiche USER-PROFIL.md (motif partage)."""
    etat = motif_profil.etat(REPERTOIRE_ROUTINE)
    etat["cle"] = motif_profil.cle(etat)
    etat["description"] = motif_profil.description(etat)
    etat["verifie_le"] = horodater()
    return etat


def secondes_depuis(horodatage, maintenant):
    """Secondes ecoulees depuis un horodatage du journal (None si absent/illisible)."""
    if not horodatage:
        return None
    try:
        moment = datetime.strptime(horodatage, FORMAT_HORODATAGE)
    except ValueError:
        return None
    return (maintenant - moment).total_seconds()


def decision_depot(etat, memoire, maintenant):
    """(deposer, motif) : decision PURE du depot d'alerte -- BORNE PAR MISSION.

    La cause racine de l'incident MO-070 : l'ancienne regle comparait la
    SIGNATURE de l'etat (champs attendus vides) et re-alertait des qu'elle
    changeait -- or la fiche du createur se remplit UN CHAMP A LA FOIS, donc
    chaque champ rempli changeait la signature : 4 depots en 3 minutes.

    Ici le depot est borne par EPISODE INCOMPLET :
      - fiche complete            -> aucun depot (motif profil-complet) ;
      - episode incomplet OUVERT  -> aucun depot, quel que soit le nombre de
        champs remplis entre-temps (motif episode-ouvert) ;
      - sinon                     -> depot, sauf si le dernier depot est plus
        recent que ANTI_SPAM_SECONDES (motif plancher), qui RETARDE le depot
        d'ouverture sans jamais le supprimer.
    """
    if not etat["attendus_vides"]:
        return False, MOTIF_COMPLET
    if memoire.get("signature"):
        return False, MOTIF_EPISODE_OUVERT
    ecoule = secondes_depuis(memoire.get("alerte_le", ""), maintenant)
    if ecoule is not None and ecoule < ANTI_SPAM_SECONDES:
        return False, MOTIF_PLANCHER
    return True, MOTIF_DEPOT


def alerter(etat):
    """Depose l'alerte dans l'inbox de la Matrice par la PORTE OFFICIELLE.

    Le depot passe par l'outil `signaler` (jamais une ecriture directe) :
    c'est lui qui tient le format du message et la boite de destination.
    Retourne (code, sortie).
    """
    commande = [
        sys.executable,
        str(OUTIL_SIGNALER),
        "signaler",
        "--outil", OUTIL_SIGNAL,
        "--niveau", NIVEAU_SIGNAL,
        "--description", etat["description"],
        "--mission", MISSION_SIGNAL,
        "--expediteur", EXPEDITEUR_SIGNAL,
    ]
    try:
        resultat = subprocess.run(
            commande, capture_output=True, text=True, timeout=30,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
    except (OSError, subprocess.SubprocessError) as erreur:
        return 1, "porte signaler injoignable : " + str(erreur)
    return resultat.returncode, (resultat.stdout or resultat.stderr).strip()
