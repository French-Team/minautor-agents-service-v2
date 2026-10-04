#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""invisibilite.py -- le DOMICILE du contrat d invisibilite L-016/CV-006 (MO-152).

La LISTE des zones que le cameleon ne doit JAMAIS lire vit ICI, et nulle part
ailleurs : les quatre outils de LECTURE (rechercher, lister, benchmark, lire)
la CONSOMMENT au lieu de la recopier (M-076 : une valeur recopiee derive en
silence ; L-100/L-102).

Deux sources, une seule verite :
  1. le PLANCHER (dur, historique) : _operateur, tmp-optimus, suivi-optimus ;
  2. le PERIMETRE DECLARE : V-003 `perimetre-cameleon` du classeur
     (data/classeur-variables.json), pose par la porte pause-session -- c est la
     Matrice SEULE qui reduit le perimetre de lecture du cameleon
     (regles-matrice : PERIMETRE CAMELEON REDUCTIBLE).

MESURE DU 2026-09-17 (EO-134, audit MO-151) : la V-003 etait lue par
pause-session UNIQUEMENT (affichage), par AUCUN outil de lecture. Resultat :
92 fichiers / 39 218 lignes nommant l invisible restaient atteignables, dont des
zones DEJA declarees exclues (matrice-readme.md, data/manuel-outils.md,
journal-multi-encarts.md, routines/routines-readme.md). Une protection declaree
et jamais posee est une protection absente (L-037).

FORMES couvertes -- les trois defauts mesures :
  - dossier exclu      : _operateur/..., routines/espion-integrite/... ;
  - chemin declare     : matrice-readme.md, data/manuel-outils.md (V-003),
                         et leurs sauvegardes .bak. / .old / -archive ;
  - fichier NOMME comme une zone (defaut de FORME, l exclusion M-084 ratait) :
    suivi-optimus.md, suivi-optimus-fins-orphaned.jsonl -- un morceau du chemin
    COMMENCE par la zone (suivie de '.', '-' ou fin).

Ferme par defaut, ouvert par le drapeau `--prive` de chaque outil : c est la
Matrice qui ouvre ; le cameleon n ouvre jamais (regle 9 de sa fiche : une zone
exclue reste INTERDITE, meme pendant une mission qui toucherait data/).
"""
import json
from pathlib import Path

REPERTOIRE_COMMUN = Path(__file__).resolve().parent     # data/commun
REPERTOIRE_DATA = REPERTOIRE_COMMUN.parent              # data/
FICHIER_CLASSEUR = REPERTOIRE_DATA / "classeur-variables.json"
CLE_PERIMETRE = "perimetre-cameleon"

# Le plancher : les trois zones historiques, invisibles quoi qu il arrive --
# meme si le classeur est absent, vide ou illisible.
ZONES_PLANCHER = ("_operateur", "tmp-optimus", "suivi-optimus")

# Un chemin peut arriver absolu (scan), relatif a la RACINE du workspace
# (argument d une porte) ou relatif a la MATRICE : les trois formes doivent
# matcher les zones DECLAREES, qui sont relatives a la Matrice.
# PIEGE MESURE (MO-152) : un marqueur "matrice" nu tronquait les chemins qui
# contiennent le mot sans etre prefixes (intercom/matrice/inbox.jsonl devenait
# inbox.jsonl) -- la zone declaree etait RATEE. On ne coupe donc que sur la
# forme NON AMBIGUE du chemin de la Matrice.
MARQUEUR_MATRICE = "/matrix/matrice/"
PREFIXES_MATRICE = ("matrix/matrice/", "matrice/", "matrix/")

_cache_declarees = None


def chemin_relatif(chemin):
    """Ramene un chemin (absolu ou non) a sa forme RELATIVE sous la Matrice."""
    s = str(chemin).replace("\\", "/")
    i = s.find(MARQUEUR_MATRICE)
    if i != -1:
        s = s[i + len(MARQUEUR_MATRICE):]
    else:
        for prefixe in PREFIXES_MATRICE:
            while s.startswith(prefixe):
                s = s[len(prefixe):]
    while s.startswith("./"):
        s = s[2:]
    return s.strip("/")


def base_declaree(zone):
    """La base d une zone DECLAREE qui est un FICHIER (avant son extension).

    Un fichier declare couvre ses derives : `data/usages-outils-combos.jsonl`
    doit emporter `data/usages-outils-combos-archive-20260915.jsonl` (mesure du
    meme jour : 1 455 lignes restaient atteignables par cette seule marche).
    """
    dernier = zone.rsplit("/", 1)[-1]
    if "." not in dernier:
        return None
    return zone.rsplit(".", 1)[0]


def zones_declarees():
    """Les zones exclues par la Matrice (V-003 du classeur). Jamais d exception."""
    global _cache_declarees
    if _cache_declarees is not None:
        return _cache_declarees
    zones = ()
    try:
        donnees = json.loads(FICHIER_CLASSEUR.read_text(encoding="utf-8"))
        entrees = donnees if isinstance(donnees, list) else donnees.get("variables", [])
        for entree in entrees:
            if isinstance(entree, dict) and entree.get("cle") == CLE_PERIMETRE:
                valeur = entree.get("valeur") or ""
                zones = tuple(z.strip().strip("/") for z in valeur.split(",") if z.strip())
                break
    except (OSError, ValueError, TypeError, AttributeError):
        zones = ()
    _cache_declarees = zones
    return zones


def zones_exclues():
    """Le plancher + les zones declarees (dedoublonnees, ordre stable)."""
    vues = []
    for zone in ZONES_PLANCHER + zones_declarees():
        if zone and zone not in vues:
            vues.append(zone)
    return tuple(vues)


def zones_texte(zones=None):
    """La liste des zones en une ligne (pour les messages des portes)."""
    return ", ".join(zones if zones is not None else zones_exclues())


def est_invisible(chemin, zones=None):
    """True si le chemin tombe dans une zone interdite a la lecture cameleon.

    Un chemin VIDE n est jamais invisible : une porte sans cible ne doit pas
    etre refusee pour une zone qu elle ne vise pas.
    """
    zones = zones_exclues() if zones is None else tuple(zones)
    rel = chemin_relatif(chemin)
    if not rel:
        return False
    morceaux = rel.split("/")
    for zone in zones:
        zone = zone.strip().strip("/")
        if not zone:
            continue
        if zone in morceaux:                          # dossier/fichier du meme nom
            return True
        if rel == zone or rel.startswith(zone + "/") \
                or rel.startswith(zone + ".") or rel.startswith(zone + "-"):
            return True                               # chemin declare (+ ses derives)
        base = base_declaree(zone)
        if base and (rel.startswith(base + "-") or rel.startswith(base + ".")):
            return True                               # derives du FICHIER declare
        if "/" not in zone:                           # fichier NOMME comme une zone
            for morceau in morceaux:
                if morceau.startswith(zone + ".") or morceau.startswith(zone + "-"):
                    return True
    return False


def refus_invisible(chemin, zones=None):
    """Message de refus si le chemin est invisible, sinon None (les portes le lisent)."""
    if not est_invisible(chemin, zones):
        return None
    return ("REFUS : zone invisible L-016 (" + chemin_relatif(chemin)
            + "). Lecture cameleon interdite -- une zone exclue reste INTERDITE. "
            + "Matrice seule : `--prive`.")
