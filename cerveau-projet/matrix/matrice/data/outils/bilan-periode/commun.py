"""Fonctions communes de bilan-periode : periode, lecture securisee, filtrage.

Chaque fonction fait UNE chose (convention-architecture-outils).
Tout est tolerant : une source absente ou cassee est juste vide (jamais bloquant).
Lecture optimisee (M-130) : les journaux JSONL append-only sont tries par date
-> parcours inverse avec break precoce (TH-023, 4.4x sur 6h).
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


def lire_jsonl_depuis(chemin, borne, cle_date="date"):
    """Retourne les entrees dont cle_date >= borne (optimise, M-130).

    Le journal est append-only et trie par date croissante : on parcourt
    en sens INVERSE et on s'arrete a la premiere entree trop ancienne.
    Lignes cassees ou dates malformees = ignorees (jamais bloquant).
    Resultat garde l'ordre chronologique (ancien -> recent).
    """
    if not chemin.exists():
        return []
    try:
        lignes = chemin.read_text(encoding=ENCODAGE).splitlines()
    except OSError:
        return []
    entrees = []
    for ligne in reversed(lignes):
        brute = ligne.strip()
        if not brute:
            continue
        try:
            entree = json.loads(brute)
        except json.JSONDecodeError:
            continue
        chaine = entree.get(cle_date)
        if not chaine:
            continue
        try:
            moment = datetime.strptime(chaine, FORMAT_DATE)
        except ValueError:
            continue
        if moment >= borne:
            entrees.append(entree)
        else:
            break
    entrees.reverse()
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
