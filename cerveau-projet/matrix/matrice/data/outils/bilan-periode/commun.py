"""Fonctions communes de bilan-periode : periode, lecture securisee, filtrage.

Chaque fonction fait UNE chose (convention-architecture-outils).
Tout est tolerant : une source absente ou cassee est juste vide (jamais bloquant).
"""
import json
from datetime import datetime, timedelta

from constants import ENCODAGE, FORMAT_DATE


def analyser_periode(nom):
    """Retourne (heures, "") pour une periode fermee connue, (None, message) sinon."""
    from constants import PERIODES_HEURES

    heures = PERIODES_HEURES.get(nom)
    if heures is None:
        return None, "Periode inconnue : " + repr(nom) + ". Periodes fermees : " + ", ".join(sorted(PERIODES_HEURES))
    return heures, ""


def horodatage():
    """Retourne la date-heure locale au format de la Matrice."""
    return datetime.now().strftime(FORMAT_DATE)


def borne_periode(heures):
    """Retourne la borne inferieure de la periode (maintenant - heures)."""
    return datetime.now() - timedelta(hours=heures)


def dans_periode(chaine_date, borne):
    """True si la date (format Matrice) est dans la periode. Malformee -> False."""
    if not chaine_date:
        return False
    try:
        return datetime.strptime(chaine_date, FORMAT_DATE) >= borne
    except ValueError:
        return False


def lire_jsonl(chemin):
    """Retourne la liste des lignes JSON d'un journal (lignes cassees ignorees)."""
    if not chemin.exists():
        return []
    entrees = []
    for ligne in chemin.read_text(encoding=ENCODAGE).splitlines():
        try:
            entrees.append(json.loads(ligne))
        except json.JSONDecodeError:
            continue
    return entrees


def lire_json(chemin, cle_defaut=None):
    """Retourne le JSON du fichier (fichier absent ou casse -> cle_defaut)."""
    if not chemin.exists():
        return cle_defaut if cle_defaut is not None else {}
    try:
        with open(chemin, "r", encoding=ENCODAGE) as flux:
            return json.load(flux)
    except (json.JSONDecodeError, OSError):
        return cle_defaut if cle_defaut is not None else {}
