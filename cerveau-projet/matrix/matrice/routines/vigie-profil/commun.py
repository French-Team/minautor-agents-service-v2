"""Fonctions communes de la vigie-profil : journal, etat, PID.

Chaque fonction fait UNE chose (convention-architecture-outils).
La lecture de la fiche elle-meme vit dans le motif partage
`matrice/data/commun/fiche_profil.py` : ce module ne la recopie pas.
"""
import json
import os
import tempfile
from datetime import datetime

from constants import (
    CHEMIN_CADENCE,
    CHEMIN_ETAT,
    CHEMIN_ETAT_PASSES,
    CHEMIN_JOURNAL,
    CHEMIN_PID,
    ENCODAGE,
    FORMAT_HORODATAGE,
    INDENTATION_JSON,
)


def horodater(maintenant=None):
    """Retourne la date-heure locale au format UNIQUE du journal.

    `maintenant` (datetime) est injectable : le cobaye de l'anti-spam rejoue une
    passe a une heure choisie sans toucher a l'horloge du systeme.
    """
    return (maintenant or datetime.now()).strftime(FORMAT_HORODATAGE)


def journaliser(entree):
    """Ajoute UNE ligne au journal (en ajout seul, jamais modifie a posteriori)."""
    entree = dict(entree)
    entree["date"] = horodater()
    with open(CHEMIN_JOURNAL, "a", encoding=ENCODAGE, newline="\n") as flux:
        flux.write(json.dumps(entree, ensure_ascii=True) + "\n")


def publier_cadence(intervalle):
    """Publie la cadence EFFECTIVE dans un etat COURT (vigie-profil-cadence.json).

    Le journal est ROTATIONNE (MO-078) : un jour, l'evenement de demarrage quitte
    le journal actif pour l'archive, et un controle qui cherche la cadence DANS
    LE JOURNAL devient AVEUGLE -- neutralise par le nettoyage qu'il surveille
    (lecon L-040). Un etat se lit dans un fichier d'etat, une histoire dans un
    journal.
    """
    donnees = {"type": "demarrage", "intervalle": intervalle, "pid": os.getpid(), "date": horodater()}
    # UNE SEULE LIGNE : un etat lu par un lecteur de journal se lit ligne par
    # ligne -- un JSON indente (plusieurs lignes) serait illisible pour lui, et
    # le controle retomberait en silence sur "sans trace" (le piege qu'on
    # repare). Ecriture atomique quand meme (tmp + remplacement, LF forces).
    temporaire = CHEMIN_CADENCE.with_name(CHEMIN_CADENCE.name + ".tmp")
    with open(str(temporaire), "w", encoding=ENCODAGE, newline="\n") as flux:
        flux.write(json.dumps(donnees, ensure_ascii=True, sort_keys=True) + "\n")
    os.replace(str(temporaire), str(CHEMIN_CADENCE))
    return CHEMIN_CADENCE


def lire_json(chemin, defaut):
    """Lit un JSON ; retourne le defaut si absent ou illisible (jamais de crash)."""
    if not chemin.exists():
        return defaut
    try:
        return json.loads(chemin.read_text(encoding=ENCODAGE))
    except (OSError, ValueError):
        return defaut


def ecrire_json_atomique(chemin, donnees):
    """Ecrit un JSON par tmp + remplacement (jamais de fichier tronque), LF forces."""
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding=ENCODAGE, newline="\n",
        dir=str(chemin.parent), delete=False, suffix=".tmp",
    ) as temporaire:
        json.dump(donnees, temporaire, indent=INDENTATION_JSON, ensure_ascii=True)
        temporaire.write("\n")
        nom_tmp = temporaire.name
    os.replace(nom_tmp, chemin)


def lire_etat_passes():
    """Etat COURT de la passe : {signature, passes_absorbes, ...} ou {}.

    Un ETAT se lit dans un fichier d'etat, une histoire se lit dans un journal
    (lecon L-071). Cet etat porte ce que la passe a vu, ce qu'elle a decide, et
    le nombre de passes ABSORBEES depuis la derniere ligne ecrite : la
    redondance supprimee est TRACEE, jamais silencieuse.
    """
    return lire_json(CHEMIN_ETAT_PASSES, {})


def ecrire_etat_passes(donnees):
    """Ecrit l'etat court de la passe (atomique : jamais de fichier tronque)."""
    ecrire_json_atomique(CHEMIN_ETAT_PASSES, donnees)
    return CHEMIN_ETAT_PASSES


def ecrire_pid(pid):
    """Note le PID de la boucle."""
    CHEMIN_PID.write_text(str(pid) + "\n", encoding=ENCODAGE)


def lire_pid():
    """Retourne le PID de la boucle, ou None si absent."""
    if not CHEMIN_PID.exists():
        return None
    contenu = CHEMIN_PID.read_text(encoding=ENCODAGE).strip()
    return int(contenu) if contenu else None


def supprimer_pid():
    """Retire le PID (arret propre)."""
    if CHEMIN_PID.exists():
        os.remove(CHEMIN_PID)
