"""Fonctions simples de la categorie perimetre : mise a jour du classeur.

Motif repris de machine-defcon : ecriture atomique (tmp + remplacement,
LF forces) + empreinte SHA-256 recalculee. UNE source de verite : le
classeur-variables, cle CLE_PERIMETRE.
"""
import hashlib
import json
import os
from datetime import datetime

from constants import (
    CHEMIN_CLASSEUR,
    CHEMIN_EMPREINTE_CLASSEUR,
    CLE_PERIMETRE,
    ENCODAGE,
    INDENTATION_JSON,
    NOM_CLASSEUR_TMP,
    TAILLE_BLOC_LECTURE,
)


def normaliser_zones(brut):
    """Retourne la liste des zones exclues (separees par des virgules), nettoyee."""
    zones = []
    for morceau in str(brut).split(","):
        zone = morceau.strip().strip("/")
        if zone and zone not in zones:
            zones.append(zone)
    return zones


def ecrire_perimetre(zones):
    """Met a jour la cle perimetre-cameleon du classeur (atomique + empreinte).

    Liste vide = perimetre complet (aucune zone exclue).
    """
    with open(CHEMIN_CLASSEUR, "r", encoding=ENCODAGE) as flux:
        donnees = json.load(flux)
    entree = None
    for variable in donnees.get("variables", ()):
        if variable.get("cle") == CLE_PERIMETRE:
            entree = variable
            break
    valeur = ",".join(zones)
    if entree is None:
        entree = {"cle": CLE_PERIMETRE}
        donnees.setdefault("variables", []).append(entree)
    entree["valeur"] = valeur
    entree["source"] = "pause-session perimetre"
    entree["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    chemin_tmp = CHEMIN_CLASSEUR.with_name(NOM_CLASSEUR_TMP)
    with open(chemin_tmp, "w", encoding=ENCODAGE, newline="\n") as flux:
        json.dump(donnees, flux, indent=INDENTATION_JSON, ensure_ascii=True)
        flux.write("\n")
    os.replace(chemin_tmp, CHEMIN_CLASSEUR)

    hacheur = hashlib.sha256()
    with open(CHEMIN_CLASSEUR, "rb") as flux:
        for bloc in iter(lambda: flux.read(TAILLE_BLOC_LECTURE), b""):
            hacheur.update(bloc)
    empreinte = hacheur.hexdigest()
    with open(CHEMIN_EMPREINTE_CLASSEUR, "w", encoding=ENCODAGE, newline="\n") as flux:
        flux.write(empreinte + "\n")
    return empreinte
