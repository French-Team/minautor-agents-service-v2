"""Fonctions simples de la categorie perimetre : mise a jour du classeur.

PORTE UNIQUE (MO-093) : le classeur-variables s'ecrit PAR LA PORTE
bdd-variables (verbe definir), jamais par une reecriture locale -- une
ecriture hors porte est ce qui a malforme V-003 (entree creee sans id,
sans statut, sans tags, le 2026-09-09). Les lecteurs du classeur
(commun.lire_perimetre, commun.lire_niveau_defcon) restent en lecture
directe : lire n'est pas ecrire.
"""
import subprocess
import sys

from constants import (
    CHEMIN_OUTIL_BDD_VARIABLES,
    CLE_PERIMETRE,
    ENCODAGE,
    RAISON_PERIMETRE,
    TAGS_PERIMETRE,
)


def normaliser_zones(brut):
    """Retourne la liste des zones exclues (separees par des virgules), nettoyee."""
    zones = []
    for morceau in str(brut).split(","):
        zone = morceau.strip().strip("/")
        if zone and zone not in zones:
            zones.append(zone)
    return zones


def deleguer_definir(cle, valeur, source, tags):
    """Ecrit la variable PAR LA PORTE bdd-variables (verbe definir).

    Retourne la sortie de la porte (sa ligne d'empreinte). En cas d'echec
    de la porte, une erreur est levee : la porte est unique, un echec
    d'ecriture ne reste jamais muet.
    """
    commande = [
        sys.executable, "main.py", "definir",
        "--cle", cle,
        "--valeur", valeur,
        "--source", source,
        "--tags", tags,
    ]
    resultat = subprocess.run(
        commande, cwd=str(CHEMIN_OUTIL_BDD_VARIABLES), capture_output=True,
        encoding=ENCODAGE, errors="replace",
    )
    if resultat.returncode != 0:
        raise RuntimeError(
            "porte bdd-variables en echec (code " + str(resultat.returncode)
            + ") : " + (resultat.stdout or "") + (resultat.stderr or "")
        )
    return (resultat.stdout or "").strip()


def ecrire_perimetre(zones):
    """Met a jour la cle perimetre-cameleon PAR LA PORTE bdd-variables.

    Liste vide = perimetre complet (aucune zone exclue) : la valeur passee
    a la porte est la chaine vide, que la porte accepte pour la mise a
    jour d'une cle existante (decision MO-093).
    """
    valeur = ",".join(zones)
    return deleguer_definir(CLE_PERIMETRE, valeur, RAISON_PERIMETRE, TAGS_PERIMETRE)
