"""Categorie rotation : borne le journal des usages en ARCHIVANT ses anciens.

Interface entre main.py et le MOTEUR PARTAGE `data/commun/rotation_journal.py`
(motif unique M-076) : la surete (archiver d'abord, archive dans le "deja
connu", course refusee) vit a UN seul endroit. Ici, cet outil ne declare que SON
journal et SA capacite (constants.py) -- et la rotation y est LIEE, au lieu
d'etre un nettoyage ponctuel.

Pourquoi cette categorie (MO-101 / P3 de la revue MO-098) : le journal des
usages n'etait borne PAR PERSONNE. Sa capacite vivait chez l'observateur (le
cockpit, `usages_lignes = 50000`) alors que la seule rotation jamais faite etait
un nettoyage manuel (MO-093, 15/09 : 69519 evenements archives et 500 gardes).
Deux politiques sans lien. La borne vit maintenant chez le proprietaire, et le
cockpit la LIT (declare -> publie -> lire, motif MO-097/MO-100).
"""
from pathlib import Path

from constants import (
    CHEMIN_RELATIF_JOURNAL,
    ESSAIS_ROTATION,
    EVENEMENTS_GARDES_JOURNAL,
    NOM_ARCHIVE_PREFIXE,
    RACINE,
    SEUIL_OCTETS_JOURNAL,
)
from commun import tracer_rotation
from rotation_journal import cli
from rotation_journal import tourner_et_journaliser as _tourner_et_journaliser


def chemin_journal(racine=None):
    """Retourne le journal a traiter pour une racine donnee (defaut : le depot)."""
    return (Path(racine) if racine else RACINE) / CHEMIN_RELATIF_JOURNAL


def executer(arguments):
    """Verbe `rotation` : borne le journal des usages en archivant ses anciens."""
    return cli(
        arguments,
        chemin_journal,
        SEUIL_OCTETS_JOURNAL,
        EVENEMENTS_GARDES_JOURNAL,
        ESSAIS_ROTATION,
        NOM_ARCHIVE_PREFIXE,
        tracer_rotation,
    )


def tourner_et_journaliser(racine=None, verbeux=False, forcer=False):
    """Rotation silencieuse, verifiee a chaque ecriture depassee (voir commun).

    Rend (code, rapport) et ne leve jamais : une rotation refusee est un fait
    journalise, pas une note perdue (lecon L-026).
    """
    return _tourner_et_journaliser(
        chemin_journal(racine),
        SEUIL_OCTETS_JOURNAL,
        EVENEMENTS_GARDES_JOURNAL,
        ESSAIS_ROTATION,
        NOM_ARCHIVE_PREFIXE,
        tracer_rotation,
        verbeux=verbeux,
        forcer=forcer,
    )
