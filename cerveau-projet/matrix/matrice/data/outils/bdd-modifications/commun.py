"""Fonctions communes a toutes les categories : charger, enregistrer, empreinte, options.

Chaque fonction fait UNE chose (convention-architecture-outils).
"""
import hashlib
import json
import os
from pathlib import Path

from constants import (
    CHEMIN_BDD,
    CHEMIN_EMPREINTE,
    ENCODAGE,
    INDENTATION_JSON,
    NOM_BDD_TMP,
    TAILLE_BLOC_LECTURE,
)

# Le DOMICILE des formes de la Matrice (cible.NOMS_MATRICE) : cette fonction le
# CONSOMME, elle ne le recopie pas (M-076 ; L-029) -- une forme recopiee derive
# en silence, et c est exactement le defaut repare ici. L import vient APRES
# `constants`, qui installe data/commun dans sys.path (motif unique M-076).
from cible import (NOMS_MATRICE, chemin_de_cle as chemin_de_cle_du_domicile,  # noqa: E402, F401
                   forme_canonique, niveau_de_chemin, racine_matrice)


def canoniser_cle(chemin):
    """La CLE canonique d'un fichier : RELATIVE A LA RACINE DE LA MATRICE (EO-363).

    LA REGLE N'EST PLUS ICI. Mesure du 2026-09-22 : la BDD portait 935 cles = 232
    prefixees < cerveau-projet/matrix/ > + 703 relatives, et 158 fichiers sous les
    DEUX formes -- donc DEUX HISTOIRES pour un seul fichier, et la vue pouvait
    lister le meme fichier DEUX FOIS. La cause : la porte enregistrait la cle TELLE
    QU'ON LA LUI DONNAIT, donc la forme dependait du repertoire courant de
    l'appelant.

    La FORME a UN SEUL DOMICILE : `cible.forme_canonique` (data/commun/). Elle y a
    ete portee le 2026-09-22 quand un SECOND consommateur a eu besoin d'elle -- les
    LIENS d'une carte d'identite (EO-347). Deux copies d'une meme regle divergent
    toujours en silence (L-029/M-076) : ici on ne la recopie pas, on l'appelle.

    L ESCALIER, lui aussi (demande createur du 2026-10-04). Mesure : 208 cles sur
    1184 ne s'ancraient sur AUCUN fichier, dont 11 qui portaient un NIVEAU EN
    TROP en tete -- `matrice/matrice/data/data-readme.md` pour
    `matrice/data/data-readme.md`. La FORME etait correcte, l ANCRAGE non : une
    forme juste ne garantit pas qu elle DESIGNE un fichier, et une cle ossuaire
    entrait alors dans la BDD aussi tranquillement qu une cle vivante. La regle
    est celle de `cible.niveau_de_chemin`, chez le meme domicile : on retire un
    segment de tete a la fois jusqu a ce que la forme designe un fichier REEL.
    Une forme qu aucune marche ne retrouve est rendue TELLE : la porte ne devine
    pas un fichier, elle rend la main.
    """
    forme = forme_canonique(chemin, CHEMIN_BDD)
    if not forme:
        return forme
    reparee = niveau_de_chemin(forme, CHEMIN_BDD)[0]
    # Introuvable : la forme reste ce qu elle etait. Deviner un niveau ecrirait
    # une preuve qui n existe pas, et le vice se reproduirait en silence.
    return reparee if reparee else forme


def chemin_de_cle(cle):
    """Le CHEMIN ABSOLU d'une cle canonique -- l'INVERSE de `canoniser_cle`.

    La cle est ecrite RELATIVE a la racine de la Matrice (EO-363) : pour LIRE le
    fichier qu'elle designe, il faut la RE-ANCRER sur cette meme racine. La racine
    vient de son domicile (`cible.racine_matrice`, L-013), jamais d'un chemin
    compte a la main. Sert a LIRE (mesurer un contenu) : ce module n'ecrit rien.
    """
    # MO-411 : la regle a UN SEUL DOMICILE (cible.chemin_de_cle) -- une cle
    # ALLOWLISTEE (nom nu) se re-ancre sur la RACINE DU WORKSPACE, une cle de la
    # Matrice sur la racine de la Matrice (M-076).
    return chemin_de_cle_du_domicile(cle, CHEMIN_BDD)


def charger_bdd():
    """Retourne le contenu de la BDD, ou une structure vide si elle n'existe pas encore."""
    if not CHEMIN_BDD.exists():
        return {"identite": {"type": "bdd-modifications", "version": 1}, "fichiers": {}}
    with open(CHEMIN_BDD, "r", encoding=ENCODAGE) as flux:
        return json.load(flux)


def enregistrer_bdd(donnees):
    """Ecrit la BDD de facon atomique puis enregistre son empreinte SHA-256.

    Protections : ecriture dans un fichier temporaire, remplacement d'un seul
    coup (jamais de BDD a moitie ecrite), empreinte mise a jour a chaque fois.
    Retourne l'empreinte enregistree.
    """
    chemin_temporaire = CHEMIN_BDD.with_name(NOM_BDD_TMP)
    # newline="\n" : fins de ligne deterministes (LF) -- la meme donnee donne
    # les memes octets partout, donc une empreinte stable et comparable.
    with open(chemin_temporaire, "w", encoding=ENCODAGE, newline="\n") as flux:
        json.dump(donnees, flux, indent=INDENTATION_JSON, ensure_ascii=True)
        flux.write("\n")
    os.replace(chemin_temporaire, CHEMIN_BDD)

    empreinte = calculer_empreinte(CHEMIN_BDD)
    with open(CHEMIN_EMPREINTE, "w", encoding=ENCODAGE) as flux:
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
    """Voir le CONTRAT du domicile partage (EO-158) : options CONSOMMEES ici."""
    from options import extraire_options as repartir  # domicile partage (EO-158)
    return repartir(arguments, noms_connus)
