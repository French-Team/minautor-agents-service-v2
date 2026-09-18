"""Persistance commune du registre de conservation."""
import hashlib
import json
import os

from constants import (
    CHEMIN_BDD, CHEMIN_EMPREINTE, ENCODAGE, INDENTATION_JSON,
    NOM_BDD_TMP, TAILLE_BLOC_LECTURE,
)


def structure_initiale():
    return {
        "identite": {"type": "bdd-conservation", "version": 1},
        "compteur": 0,
        "elements": [],
    }


def charger_bdd():
    if not CHEMIN_BDD.exists():
        return structure_initiale()
    with open(CHEMIN_BDD, "r", encoding=ENCODAGE) as flux:
        donnees = json.load(flux)
    donnees.setdefault("compteur", 0)
    donnees.setdefault("elements", [])
    donnees.setdefault("identite", {"type": "bdd-conservation", "version": 1})
    return donnees


def enregistrer_bdd(donnees):
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
    hacheur = hashlib.sha256()
    with open(chemin, "rb") as flux:
        for bloc in iter(lambda: flux.read(TAILLE_BLOC_LECTURE), b""):
            hacheur.update(bloc)
    return hacheur.hexdigest()


def calculer_empreinte_si_existe(chemin):
    if not chemin.exists():
        return None
    return calculer_empreinte(chemin)


def lire_empreinte():
    if not CHEMIN_EMPREINTE.exists():
        return None
    return CHEMIN_EMPREINTE.read_text(encoding=ENCODAGE).strip()


def extraire_options(arguments, noms_connus):
    """Voir le CONTRAT du domicile partage (EO-158) : options CONSOMMEES ici."""
    from options import extraire_options as repartir  # domicile partage (EO-158)
    return repartir(arguments, noms_connus)
