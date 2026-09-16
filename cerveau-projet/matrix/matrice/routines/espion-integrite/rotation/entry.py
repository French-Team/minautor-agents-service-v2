"""Categorie rotation : borne le journal en ARCHIVANT ses evenements anciens.

Interface entre main.py et le MOTEUR PARTAGE `data/commun/rotation_journal.py`
(motif unique M-076) : la surete (archiver d'abord, archive dans le "deja
connu", course refusee) vit a UN seul endroit, l'espion ne fait que declarer
SON journal et SES constantes.

Ordre de securite, borne par le moteur : 1) archiver (append, jumeaux ignores) ;
2) reecrire le journal actif (tmp + remplacement atomique) ; 3) controler que
tout ce qui a quitte le journal est dans l'archive.
"""
from pathlib import Path

from constants import (
    CHEMIN_RELATIF_JOURNAL,
    ESSAIS_ROTATION,
    EVENEMENTS_GARDES_JOURNAL,
    NOM_ARCHIVE_PREFIXE,
    REPERTOIRE_MATRIX,
    SEUIL_OCTETS_JOURNAL,
)
from commun import journaliser
from rotation_journal import cli
from rotation_journal import tourner_et_journaliser as _tourner_et_journaliser


def chemin_journal(racine=None):
    """Retourne le journal a traiter pour une racine donnee (defaut : le depot)."""
    return (Path(racine) if racine else REPERTOIRE_MATRIX) / CHEMIN_RELATIF_JOURNAL


def executer(arguments):
    """Verbe `rotation` : borne le journal en archivant ses evenements anciens."""
    return cli(
        arguments,
        chemin_journal,
        SEUIL_OCTETS_JOURNAL,
        EVENEMENTS_GARDES_JOURNAL,
        ESSAIS_ROTATION,
        NOM_ARCHIVE_PREFIXE,
        journaliser,
    )


def tourner_et_journaliser(racine=None, verbeux=False, forcer=False):
    """Rotation silencieuse (verifiee AVANT chaque passe de la boucle).

    Rend (code, rapport) et ne leve jamais : une rotation refusee est un fait
    journalise, pas une passe morte (lecon L-026).
    """
    return _tourner_et_journaliser(
        chemin_journal(racine),
        SEUIL_OCTETS_JOURNAL,
        EVENEMENTS_GARDES_JOURNAL,
        ESSAIS_ROTATION,
        NOM_ARCHIVE_PREFIXE,
        journaliser,
        verbeux=verbeux,
        forcer=forcer,
    )
