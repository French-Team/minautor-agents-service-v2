"""Fonctions communes a toutes les categories : lire, ajouter, empreinte, options.

Chaque fonction fait UNE chose (convention-architecture-outils).
La BDD est un journal EN AJOUT SEUL (append-only) : une ligne JSON par
evenement, jamais de reecriture du passe.
"""
import hashlib
import json
import os

from constants import (
    CHEMIN_BDD,
    CHEMIN_EMPREINTE,
    CHEMIN_INBOX,
    ENCODAGE,
    NOM_BDD_TMP,
    TAILLE_BLOC_LECTURE,
)


def lire_evenements():
    """Retourne la liste des evenements du journal (vide si absent)."""
    if not CHEMIN_BDD.exists():
        return []
    evenements = []
    with open(CHEMIN_BDD, "r", encoding=ENCODAGE) as flux:
        for ligne in flux:
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                evenements.append(json.loads(ligne))
            except ValueError:
                continue
    return evenements


def lire_inbox():
    """Retourne la liste des evenements de l'inbox (vide si absent)."""
    if not CHEMIN_INBOX.exists():
        return []
    evenements = []
    with open(CHEMIN_INBOX, "r", encoding=ENCODAGE) as flux:
        for ligne in flux:
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                evenements.append(json.loads(ligne))
            except json.JSONDecodeError:
                continue
    return evenements


def ajouter_ligne(evenement):
    """Ajoute UNE ligne au journal de facon atomique puis enregistre l'empreinte.

    Protections : tmp + remplacement d'un coup (lecon M-018, jamais de
    journal a moitie ecrit), fins de ligne LF forcees (determinisme),
    empreinte SHA-256 recalculee A CHAQUE ajout (etalon-or C-003).
    """
    ancien = b""
    if CHEMIN_BDD.exists():
        with open(CHEMIN_BDD, "rb") as flux:
            ancien = flux.read()
    nouvelle_ligne = json.dumps(evenement, ensure_ascii=True).encode(ENCODAGE) + b"\n"
    chemin_temporaire = CHEMIN_BDD.with_name(NOM_BDD_TMP)
    with open(chemin_temporaire, "wb") as flux:
        flux.write(ancien)
        flux.write(nouvelle_ligne)
    os.replace(chemin_temporaire, CHEMIN_BDD)

    empreinte = calculer_empreinte(CHEMIN_BDD)
    with open(CHEMIN_EMPREINTE, "w", encoding=ENCODAGE, newline="\n") as flux:
        flux.write(empreinte + "\n")
    return empreinte


def calculer_empreinte(chemin):
    """Calcule l'empreinte SHA-256 d'un fichier (convention-integrite-sha256)."""
    hacheur = hashlib.sha256()
    with open(chemin, "rb") as flux:
        for bloc in iter(lambda: flux.read(TAILLE_BLOC_LECTURE), b""):
            hacheur.update(bloc)
    return hacheur.hexdigest()


def calculer_empreinte_si_existe(chemin):
    """Retourne l'empreinte du fichier, ou None s'il est absent (jamais de crash)."""
    if not chemin.exists():
        return None
    return calculer_empreinte(chemin)


def lire_empreinte():
    """Retourne l'empreinte enregistree, ou None si elle n'existe pas."""
    if not CHEMIN_EMPREINTE.exists():
        return None
    return CHEMIN_EMPREINTE.read_text(encoding=ENCODAGE).strip()


def extraire_options(arguments, noms_connus):
    """Extrait les options --nom valeur d'une liste d'arguments (forme seulement)."""
    options = {}
    index = 0
    while index < len(arguments):
        morceau = arguments[index]
        if morceau.startswith("--") and morceau[2:] in noms_connus:
            if index + 1 < len(arguments):
                options[morceau[2:]] = arguments[index + 1]
            index += 2
        else:
            index += 1
    return options