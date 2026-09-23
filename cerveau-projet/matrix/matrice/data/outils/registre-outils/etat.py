"""Etat du REGISTRE DES OUTILS : charger, enregistrer, empreindre.

Une seule responsabilite par fonction (convention-architecture-outils). L ECRITURE
est atomique (tmp + os.replace, LF forces) : la lecon M-018 vaut pour toute BDD.
"""
import hashlib
import json
import os
from datetime import datetime

from constants import (CHEMIN_BDD, CHEMIN_EMPREINTE, CLE_OUTILS, ENCODAGE, IDENTITE,
                       INDENTATION, TAILLE_BLOC_LECTURE)


def horodater():
    """La date-heure locale, au format des journaux."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def empreinte_texte(texte):
    """L empreinte sha256 d un TEXTE (le document lu, pas le fichier).

    C est elle qui est rangee dans la BDD : quand le texte source change, l empreinte
    change, et `verifier` peut alors DIRE que la copie du registre a perime -- au lieu
    de laisser une description morte servir de base a une proposition.
    """
    return hashlib.sha256((texte or "").encode(ENCODAGE)).hexdigest()


def charger():
    """La BDD du registre, ou None si elle n existe pas encore.

    None n est pas une erreur : c est l etat AVANT le premier rafraichissement, et
    chaque verbe le DIT a sa facon (lire et verifier refusent en nommant le geste).
    """
    if not CHEMIN_BDD.is_file():
        return None
    with open(CHEMIN_BDD, "r", encoding=ENCODAGE) as flux:
        return json.load(flux)


def enregistrer(entrees, perimetre, homonymes):
    """Ecrit la BDD de facon ATOMIQUE (tmp + remplacement, LF forces).

    Rend le nombre d entrees ecrites : un compte, pas une impression.
    """
    donnees = {
        "identite": dict(IDENTITE),
        "genere_le": horodater(),
        "perimetre": perimetre,
        "homonymes": homonymes,
        CLE_OUTILS: entrees,
    }
    chemin_tmp = CHEMIN_BDD.with_name(CHEMIN_BDD.name + ".tmp")
    CHEMIN_BDD.parent.mkdir(parents=True, exist_ok=True)
    with open(chemin_tmp, "w", encoding=ENCODAGE, newline="\n") as flux:
        json.dump(donnees, flux, indent=INDENTATION, ensure_ascii=True)
        flux.write("\n")
    os.replace(chemin_tmp, CHEMIN_BDD)
    ecrire_empreinte(CHEMIN_BDD)
    return len(entrees)


def ecrire_empreinte(chemin):
    """Pose l EMPREINTE ETALON de la BDD (fichier voisin `.sha256`).

    Une BDD REGENEREE doit reposer son etalon a chaque publication : l espion
    d integrite de la Matrice la surveille par cette empreinte, et sans ce geste
    la BDD crierait un ecart a CHAQUE `rafraichir` -- un faux ecart par
    construction, qui apprend a ne plus croire l espion (patron de
    bdd-conservation, meme geste).
    """
    hacheur = hashlib.sha256()
    with open(chemin, "rb") as flux:
        for bloc in iter(lambda: flux.read(TAILLE_BLOC_LECTURE), b""):
            hacheur.update(bloc)
    with open(CHEMIN_EMPREINTE, "w", encoding=ENCODAGE, newline="\n") as flux:
        flux.write(hacheur.hexdigest() + "\n")
