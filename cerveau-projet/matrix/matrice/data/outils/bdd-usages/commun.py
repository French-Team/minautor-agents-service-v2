"""Fonctions communes a toutes les categories : ajouter une ligne, lire, options.

Chaque fonction fait UNE chose (convention-architecture-outils).
"""
import json
from datetime import datetime

from constants import (
    CHEMIN_BDD,
    ENCODAGE,
    ESSAIS_ROTATION,
    EVENEMENTS_GARDES_JOURNAL,
    NOM_ARCHIVE_PREFIXE,
    SEUIL_OCTETS_JOURNAL,
)

# Moteur PARTAGE de rotation (motif unique M-076) : la surete (archiver d'abord,
# archive dans le "deja connu", course refusee) vit a UN seul endroit. Ce journal
# ne fait que declarer SES bornes (constants.py) et les lui donner.
from rotation_journal import tourner_et_journaliser


def horodater():
    """Retourne la date-heure locale au format du journal."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ajouter_ligne(entree):
    """Ajoute UNE ligne a la BDD (ajout seul : l'histoire n'est jamais reecrite).

    Puis BORNE le journal si la capacite DECLAREE est depassee (MO-101/P3) :
    le proprietaire du journal est le seul endroit qui sait ce qu'il peut
    garder. La rotation est silencieuse et NE TUE JAMAIS la note qui l'appelle
    (lecon L-026) : un refus est un fait, pas une note perdue.
    """
    with open(CHEMIN_BDD, "a", encoding=ENCODAGE, newline="\n") as flux:
        flux.write(json.dumps(entree, ensure_ascii=True) + "\n")
    borner_si_necessaire()


def tracer_rotation(evenement):
    """Trace une rotation DANS LE JOURNAL MEME (l'histoire de ce journal).

    Meme forme que les autres lignes (cles requises respectees) : une rotation
    du journal des usages EST un usage du journal des usages.
    """
    with open(CHEMIN_BDD, "a", encoding=ENCODAGE, newline="\n") as flux:
        flux.write(
            json.dumps(
                {
                    "date": horodater(),
                    "outil": "bdd-usages",
                    "commande": "rotation",
                    "code": 0 if evenement.get("rotation") else 1,
                    "detail": str(evenement.get("motif", ""))[:400],
                    "tags": ["rotation", "archive"],
                },
                ensure_ascii=True,
            )
            + "\n"
        )


def borner_si_necessaire():
    """Borne le journal au-dela de SA capacite declaree ; ne leve JAMAIS.

    Le test est un `stat()` (cout constant) : le moteur partage n'est appele que
    si la capacite declaree est reellement depassee. Rend (code, rapport) pour
    que les cobayes puissent jouer la porte REELLE.
    """
    if not CHEMIN_BDD.exists() or CHEMIN_BDD.stat().st_size <= SEUIL_OCTETS_JOURNAL:
        return 0, None
    return tourner_et_journaliser(
        CHEMIN_BDD,
        SEUIL_OCTETS_JOURNAL,
        EVENEMENTS_GARDES_JOURNAL,
        ESSAIS_ROTATION,
        NOM_ARCHIVE_PREFIXE,
        tracer_rotation,
    )


def charger_lignes():
    """Retourne la liste des lignes valides de la BDD ([] si absente)."""
    if not CHEMIN_BDD.exists():
        return []
    lignes = []
    with open(CHEMIN_BDD, "r", encoding=ENCODAGE) as flux:
        for ligne in flux:
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                lignes.append(json.loads(ligne))
            except json.JSONDecodeError:
                continue
    return lignes


def extraire_options(arguments, noms_connus):
    """Voir le CONTRAT du domicile partage (EO-158) : options CONSOMMEES ici."""
    from options import extraire_options as repartir  # domicile partage (EO-158)
    return repartir(arguments, noms_connus)
