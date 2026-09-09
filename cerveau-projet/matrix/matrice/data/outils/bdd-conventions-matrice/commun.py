"""Fonctions communes a toutes les categories : charger, enregistrer, empreinte, options.

Chaque fonction fait UNE chose (convention-architecture-outils).
"""
import hashlib
import json
import os

from constants import (
    CHEMIN_BDD,
    CHEMIN_EMPREINTE,
    ENCODAGE,
    INDENTATION_JSON,
    NOM_BDD_TMP,
    TAILLE_BLOC_LECTURE,
)


def charger_bdd():
    """Retourne le contenu de la BDD, ou une structure vide si elle n'existe pas encore."""
    if not CHEMIN_BDD.exists():
        return {"identite": {"type": "conventions-matrice.json", "version": 1}, "conventions": []}
    with open(CHEMIN_BDD, "r", encoding=ENCODAGE) as flux:
        return json.load(flux)


def enregistrer_bdd(donnees):
    """Ecrit la BDD de facon atomique puis enregistre son empreinte SHA-256.

    Protections : tmp + remplacement d'un coup, fins de ligne LF forcees
    (determinisme : meme donnee = memes octets = empreinte stable).
    """
    chemin_temporaire = CHEMIN_BDD.with_name(NOM_BDD_TMP)
    with open(chemin_temporaire, "w", encoding=ENCODAGE, newline="\n") as flux:
        json.dump(donnees, flux, indent=INDENTATION_JSON, ensure_ascii=True)
        flux.write("\n")
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
