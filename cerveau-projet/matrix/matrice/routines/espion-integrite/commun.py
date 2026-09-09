"""Fonctions communes de l'espion : empreinte, journal, PID.

Chaque fonction fait UNE chose (convention-architecture-outils).
"""
import hashlib
import json
import os
from datetime import datetime

from constants import (
    BDDS,
    CHEMIN_JOURNAL,
    CHEMIN_PID,
    ENCODAGE,
    REPERTOIRE_DATA,
)


def calculer_empreinte(chemin):
    """Calcule l'empreinte SHA-256 d'un fichier."""
    hacheur = hashlib.sha256()
    with open(chemin, "rb") as flux:
        for bloc in iter(lambda: flux.read(65536), b""):
            hacheur.update(bloc)
    return hacheur.hexdigest()


def calculer_empreinte_si_existe(chemin):
    """Retourne l'empreinte du fichier, ou None s'il est absent (jamais de crash)."""
    if not chemin.exists():
        return None
    return calculer_empreinte(chemin)


def lire_empreinte_enregistree(nom_bdd):
    """Retourne l'empreinte etalon d'une BDD, ou None si absente."""
    chemin = REPERTOIRE_DATA / (nom_bdd + ".sha256")
    if not chemin.exists():
        return None
    return chemin.read_text(encoding=ENCODAGE).strip()


def chemin_bdd(nom_bdd):
    """Retourne le chemin complet d'une BDD du registre."""
    return REPERTOIRE_DATA / nom_bdd


def nombre_bdds():
    """Retourne la taille du registre (pour la normalisation du taux)."""
    return len(BDDS)


def horodater():
    """Retourne la date-heure locale au format du journal."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def journaliser(entree):
    """Ajoute UNE ligne au journal (en ajout seul, jamais modifie a posteriori)."""
    entree = dict(entree)
    entree["date"] = horodater()
    with open(CHEMIN_JOURNAL, "a", encoding=ENCODAGE) as flux:
        flux.write(json.dumps(entree, ensure_ascii=True) + "\n")


def ecrire_pid(pid):
    """Note le PID de la boucle dans espion.pid."""
    CHEMIN_PID.write_text(str(pid) + "\n", encoding=ENCODAGE)


def lire_pid():
    """Retourne le PID de la boucle, ou None si absent."""
    if not CHEMIN_PID.exists():
        return None
    contenu = CHEMIN_PID.read_text(encoding=ENCODAGE).strip()
    return int(contenu) if contenu else None


def supprimer_pid():
    """Retire espion.pid (arret propre)."""
    if CHEMIN_PID.exists():
        os.remove(CHEMIN_PID)
