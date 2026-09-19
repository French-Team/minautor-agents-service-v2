#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
garde-tmp.py -- Garde perimetre des fichiers temporaires (M-100, MO-104)

Regle immuable defendue : `regles-immuables/perimetre-tmp.md`.
Quatre controles :
1. zero residu temporaire HORS des zones tmp-*/ ;
2. toute zone tmp-*/ PRESENTE porte son README (la zone est permanente :
   un tmp-* sans README est une zone privee de son contrat) ;
3. toute zone tmp-*/ vit a SON DOMICILE DECLARE (point 1) : le domicile est LU
   au moteur partage (`data/commun/zone_tmp.py`) et COMPARE, il n est plus
   suppose etre la racine -- MO-236 a deplace `tmp-optimus` sous
   `_operateur/optimus-prime/`, et exiger la racine aurait accuse ce deplacement a
   tort. Une zone dont le nom n est pas un domicile declare n a PAS de
   proprietaire (point 1) ;
4. la regle est LUE a l allumage : elle figure a ses 4 points de relecture
   (controle `regle-lue-a-l-allumage` -- une regle que personne ne relit ne
   protege rien).

Mesure du 2026-09-18 (EO-173, MO-180) : les controles ne regardaient que
`racine / <nom>`, si bien qu une zone ecrite dans `matrice/` etait INVISIBLE --
`matrice/tmp-optimus/`, six fichiers de MO-172, n a jamais ete vue, ni par ce
garde ni par le purgeur de cloture (qui ne connait que la zone de son flux).
Le controle 3 est la FERMETURE de ce trou.

Il INFORME du nombre de fichiers presents dans chaque zone, sans accuser :
pendant une mission, des cobayes y vivent legitimement. Le CONTENU vide en
fin de mission n est PAS verifiable par une garde : c est une discipline,
et la regle le dit elle-meme.

code 0 = sain, code 1 = ecart detecte.
Usage: python garde-tmp.py [--racine <path>]
"""

import sys
import argparse
import fnmatch
from pathlib import Path


# Les domiciles DECLARES par la regle (point 1) : une zone tmp-* qui porte un
# autre nom n a aucun proprietaire -- la regle n en nomme que deux.
# Les NOMS viennent du moteur PARTAGE des zones (data/commun/zone_tmp.py) :
# une valeur, une maison (M-076). Depuis R-005 (MO-189), la zone du cameleon ne
# vit plus a la racine de la MATRICE mais dans SON perimetre d ecriture
# (workspace/tmp-cameleon) : elle se controle a son DOMICILE DECLARE, sinon le
# rglob ci-dessous -- qui ne balaie que matrix/ -- en ferait un angle mort.
import sys as _sys

_MATRICE = Path(__file__).resolve()
while _MATRICE.name != 'matrix' and _MATRICE.parent != _MATRICE:
    _MATRICE = _MATRICE.parent
_sys.path.insert(0, str(_MATRICE / 'matrice' / 'data' / 'commun'))
from racine import detecter_racine  # noqa: E402
from zone_tmp import (NOM_ZONE_CAMELEON, NOM_ZONE_OPTIMUS, DOMICILE_ZONE_OPTIMUS,
                      DOMICILE_ZONE_CAMELEON, chemin_zone_cameleon)  # noqa: E402

TMP_DIRS = {NOM_ZONE_OPTIMUS, NOM_ZONE_CAMELEON}
# MO-236 : le DOMICILE d'une zone se LIT au moteur partage, il ne se suppose plus.
# Avant, le controle exigeait `chemin.parent == racine` -- une zone deplacee par
# une decision restait donc accusee a tort. Ici : le domicile declare SOUS la
# Matrice ; la zone du cameleon, elle, est jugee a part (racine differente).
DOMICILES_SOUS_MATRICE = {NOM_ZONE_OPTIMUS: tuple(DOMICILE_ZONE_OPTIMUS)}
# Le prefixe d une zone jetable vient du moteur PARTAGE (data/commun/zone_tmp.py,
# PREFIXE_ZONE) : le garde ne recopie pas une seconde definition du meme fait.
PREFIXE_ZONE = "tmp-"
# Le fichier qui fait d une zone une zone (point 3 de la regle).
NOM_README_ZONE = "README.md"
PATTERNS = ("_cobaye*", "*.tmp", "_*.txt", ".tmp-*", ".zz-*")
EXCLUS_DIRS = {".git", "__pycache__"}
# Un dossier d ARCHIVE n est pas un lieu d ecriture : il garde l etat d une
# Matrice PASSEE (mesure du 2026-09-18 : `purification/archives/` est le seul du
# depot, et il contient l instantane d une matrice ancienne, avec une zone
# tmp-optimus dedans). Ses zones sont SPAREES -- et RENDUES, jamais tues : une
# exemption muette serait un angle mort (doctrine MO-075).
DOSSIERS_ARCHIVE = {"archive", "archives"}

# Domicile de l operateur : sa presence distingue une vraie racine matrix/
# d une racine de cobaye (ou les points de relecture n existent pas).
DOSSIER_OPERATEUR = Path("_operateur") / "optimus-prime"
MARQUEUR_REGLE = "perimetre-tmp.md"
POINTS_LECTURE = (
    DOSSIER_OPERATEUR / "regles-immuables" / MARQUEUR_REGLE,
    DOSSIER_OPERATEUR / "regles-immuables" / "regles-immuables-readme.md",
    DOSSIER_OPERATEUR / "optimus-prime.md",
    DOSSIER_OPERATEUR / "protocoles" / "proto-1-reprise-mission.md",
)


def trouver_racine(depart: Path) -> Path:
    """Localise le dossier matrix/ a partir du chemin demande."""
    racine = depart.resolve()
    if racine.name == "matrix":
        return racine
    cand = racine / "matrix"
    if cand.is_dir():
        return cand
    cand = racine / "cerveau-projet" / "matrix"
    if cand.is_dir():
        return cand
    return racine


def controler_residus(racine: Path) -> list:
    """Fichiers temporaires presents HORS des zones tmp-*/."""
    residus = []
    for p in racine.rglob("*"):
        if not p.is_file():
            continue
        try:
            rel = p.relative_to(racine)
        except ValueError:
            continue
        if any(part in EXCLUS_DIRS for part in rel.parts):
            continue
        # Un fichier DANS une zone tmp-* est l affaire du controle des ZONES :
        # c est la ZONE qui est jugee (son domicile, son README), pas chacun de
        # ses fichiers. Le prefixe juge est celui du moteur partage.
        if any(partie.startswith(PREFIXE_ZONE) for partie in rel.parts):
            continue
        if any(fnmatch.fnmatch(p.name, pat) for pat in PATTERNS):
            residus.append(str(rel))
    return residus


def zones_du_depot(racine: Path) -> list:
    """TOUTES les zones `tmp-*` du depot, a quelque profondeur.

    Une zone ne se cherche plus a un chemin SUPPOSE (`racine / <nom>`) : elle se
    TROUVE, ou qu elle soit. C est ce qui rend VISIBLE une zone ecrite la ou la
    regle l interdit (point 2) -- le trou mesure le 2026-09-18.
    """
    zones = []
    for chemin in sorted(racine.rglob(PREFIXE_ZONE + "*")):
        if not chemin.is_dir():
            continue
        try:
            rel = chemin.relative_to(racine)
        except ValueError:
            continue
        if any(partie in EXCLUS_DIRS for partie in rel.parts):
            continue
        zones.append((chemin, rel))
    return zones


def juger_zone(chemin: Path, rel: Path, racine: Path) -> tuple:
    """Juge UNE zone : rend (ecart, exemption), l un des deux valant None.

    Trois causes d ecart, DANS CET ORDRE : le DOMICILE (points 1 et 2 -- une zone
    hors de la racine, `matrice/` compris, est un ecart quel que soit son nom),
    le PROPRIETAIRE (le nom doit etre un de ceux que la regle nomme), le CONTRAT
    (le README). Une zone d ARCHIVE est SPAREE avant tout examen : elle n est pas
    un lieu d ecriture, et l exemption est RENDUE a l appelant, jamais tue.
    """
    if any(partie in DOSSIERS_ARCHIVE for partie in rel.parts):
        return None, (str(rel) + " : zone d ARCHIVE (etat d une Matrice passee, pas"
                      " un lieu d ecriture) -- SPAREE, et ce fait est DIT")
    if chemin.name not in TMP_DIRS:
        return ("zone jetable SANS DOMICILE DECLARE : " + str(rel)
                + " -- la regle (point 1) n en nomme que deux : "
                + ", ".join(sorted(TMP_DIRS))), None
    # MO-236 : le domicile est COMPARE au DOMICILE DECLARE (moteur partage). Une
    # zone deplacee par une decision est donc acceptee a sa nouvelle place, et une
    # zone declassee est dite AVEC son domicile reel -- jamais un simple "hors
    # perimetre" qui ne dit pas ou aller.
    domicile = DOMICILES_SOUS_MATRICE.get(chemin.name)
    if domicile is None:
        return ("zone jetable HORS DE SON DOMICILE DECLARE : " + str(rel)
                + " -- la zone " + chemin.name + " vit HORS de la Matrice, a "
                + str(DOMICILE_ZONE_CAMELEON)), None
    if tuple(rel.parts) != domicile:
        return ("zone jetable HORS DE SON DOMICILE DECLARE : " + str(rel)
                + " -- attendu " + "/".join(domicile)), None
    if not (chemin / NOM_README_ZONE).is_file():
        return (str(rel) + " present SANS son README (zone privee de son contrat)"), None
    return None, None


def controler_zones(racine: Path) -> tuple:
    """Chaque zone tmp-*/ du depot : ecarts, informations, exemptions.

    L INFORMATION n est pas un verdict : pendant une mission, des cobayes vivent
    legitimement dans la zone -- c est le PILOTE qui la vide a la cloture
    (point 4). Le garde compte, il ne juge pas le contenu.
    """
    ecarts = []
    infos = []
    exemptions = []
    for chemin, rel in zones_du_depot(racine):
        ecart, exemption = juger_zone(chemin, rel, racine)
        if ecart:
            ecarts.append(ecart)
        if exemption:
            exemptions.append(exemption)
        fichiers = [
            p for p in chemin.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts
        ]
        infos.append(str(rel) + " : " + str(len(fichiers)) + " fichier(s) present(s)")
    return ecarts, infos, exemptions


def controler_zone_declaree(racine: Path) -> tuple:
    '''Controle la zone du cameleon a son DOMICILE DECLARE (R-005, MO-189).

    Elle vit HORS de matrix/ (workspace/tmp-cameleon) : le rglob de zones_du_depot
    ne peut pas la voir, et sans ce controle elle serait un ANGLE MORT -- une zone
    privee de son contrat que personne ne verifierait. Le domicile est CITE (moteur
    partage des zones), jamais recopie (M-076).

    Une zone ABSENTE n'est pas un ecart : elle est creee par le pilote de son flux
    a l'injection (regle R-005), donc son absence est un fait a DIRE, pas a juger.
    '''
    zone = chemin_zone_cameleon(detecter_racine(racine))
    if not zone.is_dir():
        return ([], [str(zone) + ' : zone DECLAREE du cameleon ABSENTE -- elle est'
                     ' creee par le pilote de son flux (R-005)'])
    ecarts = []
    if not (zone / NOM_README_ZONE).is_file():
        ecarts.append(str(zone) + ' : zone DECLAREE du cameleon SANS son README'
                      ' (zone privee de son contrat)')
    fichiers = [p for p in zone.rglob('*') if p.is_file()]
    infos = ['workspace/' + NOM_ZONE_CAMELEON + ' (declaree, hors Matrice) : '
             + str(len(fichiers)) + ' fichier(s) present(s)']
    return ecarts, infos


def controler_regle(racine: Path) -> list:
    """Controle `regle-lue-a-l-allumage` : la regle figure a ses 4 points.

    Ignore quand le domicile de l operateur est absent : la racine controlee
    n est alors pas une racine matrix/ (cas des racines de cobaye).
    """
    if not (racine / DOSSIER_OPERATEUR).is_dir():
        return []
    ecarts = []
    for point in POINTS_LECTURE:
        chemin = racine / point
        if not chemin.is_file():
            ecarts.append(str(point) + " : la regle a disparu de ce point")
            continue
        if point.name == MARQUEUR_REGLE and point.parent.name == "regles-immuables":
            continue
        try:
            texte = chemin.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as erreur:
            ecarts.append(str(point) + " : illisible (" + str(erreur) + ")")
            continue
        if MARQUEUR_REGLE not in texte:
            ecarts.append(str(point) + " : ne cite plus " + MARQUEUR_REGLE)
    return ecarts


def main():
    parser = argparse.ArgumentParser(
        description="Garde perimetre des fichiers temporaires (tmp-*/)"
    )
    parser.add_argument("--racine", default=".", help="Dossier matrix/ (defaut: cwd)")
    args = parser.parse_args()

    racine = trouver_racine(Path(args.racine))
    if racine.name != "matrix" or not racine.is_dir():
        print("Dossier matrix/ introuvable depuis " + str(args.racine))
        return 2

    ecarts = controler_residus(racine)
    ecarts_zones, infos, exemptions = controler_zones(racine)
    ecarts.extend(ecarts_zones)
    ecarts_declaree, infos_declaree = controler_zone_declaree(racine)
    ecarts.extend(ecarts_declaree)
    infos.extend(infos_declaree)
    ecarts.extend(controler_regle(racine))

    for info in infos:
        print("INFO zone : " + info)
    for exemption in exemptions:
        print("EXEMPTE   : " + exemption)

    if ecarts:
        print("ECARTS : " + str(len(ecarts)) + " ecart(s) de perimetre temporaire :")
        for ecart in ecarts:
            print("  - " + ecart)
        return 1

    print("Tmp sain : aucune zone hors de son DOMICILE DECLARE, tout tmp-* a son README,"
          " aucun residu hors des zones, regle perimetre-tmp lue a ses 4 points.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
