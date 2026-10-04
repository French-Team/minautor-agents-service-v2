#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
garde-ascii.py -- Garde ASCII strict matrice (M-099)

Verifie qu un fichier (ou dossier) ne contient que de l ASCII strict
(convention ASCII matrice). code 0 = sain, code 1 = non-ASCII detecte.
Usage: python garde-ascii.py <fichier|dossier> [--ext .py,.md,.json]

DEUX ZONES DECLAREES SONT HORS CHAMP, et chacune se declare a SON domicile :
  - `docs/` : la zone des SOURCES du createur (MO-377), declaree dans
    `matrice/data/commun/zone_sources.py` ;
  - `user-demandes/` : la PASSERELLE USER -- le user y ecrit ses demandes en clair,
    que la Matrice suit et extrait (MO-475), declaree dans
    `matrice/data/commun/passerelle_user.py` (MO-492).
Le garde CONSOMME ces declarations, il ne les recopie JAMAIS (M-076) : c est ce
qui fait dire la MEME chose a ce garde et au controle d attribution sur la MEME
zone. Une exclusion muette serait un angle mort qu aucune suite ne voit : les
zones mises de cote sont donc NOMMEES et COMPTEES a chaque passe (L-104).

LE DEFAUT REPARE (mesure MO-377 du 2026-09-24) : l exclusion ne s appliquait qu en
mode DOSSIER. Sur le MEME fichier (docs/conversation-unslot-gemma-4.md), ce garde
rendait 1 (violation) quand on lui donnait le FICHIER et 0 (hors champ) quand on
lui donnait son DOSSIER : deux verdicts pour une seule cible, donc un instrument
qui accuse ce que la decision du createur exempte. La cible est desormais jugee
ELLE-MEME, et la mise hors champ est DITE.

LE MEME DEFAUT, UNE AUTRE ZONE (mesure MO-492 du 2026-09-29) : la decision du
createur sur la passerelle user etait ecrite DANS `controle-attribution.py` -- un
SEUL instrument -- donc ce garde l ignorait et accusait `user-demandes/*.md`
(code 1, DEUX fichiers) alors que la zone est declaree hors jugement depuis
MO-475. Le fichier n etait pas fautif : c est la DECLARATION qui n avait pas de
domicile. Elle en a un, et les deux instruments la lisent au meme endroit.
"""

import sys
import argparse
from pathlib import Path

# data/commun (motif M-076) : les ZONES se LISENT chez leur domicile, elles ne se
# recopient pas. La racine `matrix/` est trouvee par son marqueur a partir de CE
# fichier (jamais de la cible) : le garde marche donc aussi sur une cible externe.
_RACINE_MATRICE = Path(__file__).resolve()
while _RACINE_MATRICE.name != "matrix" and _RACINE_MATRICE.parent != _RACINE_MATRICE:
    _RACINE_MATRICE = _RACINE_MATRICE.parent
sys.path.insert(0, str(_RACINE_MATRICE / "matrice" / "data" / "commun"))
from passerelle_user import (est_passerelle_user, MOTIF_PASSERELLE_USER,  # noqa: E402
                             NOM_PASSERELLE_USER)
from zone_sources import (est_zone_sources, MOTIF_ZONE_SOURCES,  # noqa: E402
                          NOM_ZONE_SOURCES)
from zone_banque import (est_zone_banque, MOTIF_ZONE_BANQUE,  # noqa: E402
                         NOM_ZONE_BANQUE)
from artefacts_externes import (est_artefact_externe,  # noqa: E402
                                MOTIF_ARTEFACTS_EXTERNES,
                                NOM_ARTEFACTS_EXTERNES)


# .git et __pycache__ sont exclus de PERIMETRE : techniques, ni juges ni nommes.
EXCLUS_DIRS = {".git", "__pycache__"}

# LES ZONES HORS CHAMP. Chacune DECLARE son nom, son motif et son PREDICAT a son
# domicile unique ; ce garde les CONSOMME (M-076). L ORDRE EST LA REGLE, il n est pas
# cosmetique : une zone PRECISE est lue AVANT la zone large, sinon la large absorbe la
# precise et le motif le plus exact disparait du rapport. La BANQUE (v1/v2) est donc
# declaree EN DERNIER : c'est la seule zone dont le motif est general.
ZONES_HORS_CHAMP = (
    (NOM_ZONE_SOURCES, MOTIF_ZONE_SOURCES, est_zone_sources),
    (NOM_PASSERELLE_USER, MOTIF_PASSERELLE_USER, est_passerelle_user),
    (NOM_ARTEFACTS_EXTERNES, MOTIF_ARTEFACTS_EXTERNES, est_artefact_externe),
    (NOM_ZONE_BANQUE, MOTIF_ZONE_BANQUE, est_zone_banque),
)


def motif_hors_champ(nom, motif):
    """Le message imprime quand la CIBLE elle-meme est hors champ (UNE seule forme)."""
    return "HORS CHAMP : " + nom + "/ -- " + motif + " -- aucun fichier controle"


def zone_hors_champ(chemin):
    """(nom, motif) de la zone declaree qui couvre <chemin>, ou None.

    Le PREDICAT vit au domicile de la zone : c est ce qui fait dire la MEME chose
    a ce garde et au controle d attribution sur la MEME zone (M-076).
    """
    for nom, motif, predicat in ZONES_HORS_CHAMP:
        if predicat(chemin):
            return nom, motif
    return None


def contient_le_perimetre(cible):
    """True si <cible> ENCONTRE le perimetre de la v3 (dossier parent, ou lui-meme).

    UNE ZONE NE CONTIENT PAS SON CONTENANT (MO-497). Un dossier qui RENFERME la
    Matrice n est pas lui-meme dans une zone declaree. Sans ce test, la declaration de
    la banque v1/v2 -- qui porte sur les FICHIERS hors perimetre -- faisait dire au
    garde que la RACINE DU WORKSPACE entierement hors champ : il rendait 0 SANS
    controler le moindre fichier, y compris ceux de la Matrice. C'est un vert obtenu
    par ABSENCE de controle, le pire des verdicts : il remplace 72 accusations par un
    silence total (lecon L-132, meme famille que le defaut que MO-377 avait paye).
    """
    try:
        resolu = Path(cible).resolve()
    except (OSError, RuntimeError):
        return False
    return _RACINE_MATRICE == resolu or _RACINE_MATRICE.is_relative_to(resolu)


def zone_hors_champ_entiere(cible):
    """La zone declaree qui COUVRE la cible ENTIEREMENT, ou None.

    C'est LA seule porte d'entree du jugement < cette cible est-elle hors champ >.
    Elle est donc ecrite UNE fois et consommee par les deux appelants (`est_hors_champ`
    et le routeur de `main`) : deux portes qui repondent differemment sur le meme
    chemin rendraient DEUX verdicts pour UNE cible (MO-377).
    """
    if contient_le_perimetre(cible):
        return None
    return zone_hors_champ(cible)


def est_hors_champ(cible):
    """True si la CIBLE elle-meme tombe dans un dossier technique ou une zone declaree.

    Sans ce controle, l exclusion ne jouait qu en mode DOSSIER : le MEME fichier
    rendait 1 isole et 0 dans son dossier (defaut mesure par MO-377).
    """
    if any(part in EXCLUS_DIRS for part in cible.parts):
        return True
    return zone_hors_champ_entiere(cible) is not None


def fichiers_a_controler(cible, exts, releve=None):
    """Les fichiers a controler, en RELEVANT les zones declarees traversees.

    Un fichier d une zone declaree n est ni juge ni perdu de vue : il est COMPTE
    par son nom de zone dans <releve>, et le verdict le DIT. Un angle mort muet
    est un angle mort qu aucune suite ne voit (L-104).
    """
    if est_hors_champ(cible):
        return
    if cible.is_file():
        yield cible
        return
    for p in cible.rglob("*"):
        if not p.is_file():
            continue
        if any(part in EXCLUS_DIRS for part in p.parts):
            continue
        zone = zone_hors_champ(p)
        if zone is not None:
            if releve is not None:
                releve[zone] = releve.get(zone, 0) + 1
            continue
        if exts and p.suffix not in exts:
            continue
        yield p


def dire_zones_hors_champ(releve):
    """DIT les zones declarees traversees, avec leur compte -- jamais en silence."""
    if not releve:
        return
    print("HORS CHAMP : " + str(sum(releve.values()))
          + " fichier(s) mis de cote, non juges :")
    for (nom, motif), nombre in sorted(releve.items()):
        print("  - " + nom + "/ : " + str(nombre) + " fichier(s) [" + motif + "]")


def main():
    parser = argparse.ArgumentParser(description="Garde ASCII strict")
    parser.add_argument("cible", help="Fichier ou dossier a controler")
    parser.add_argument("--ext", default=".py,.md,.json,.jsonl",
                        help="Extensions (dossier seulement, defaut: .py,.md,.json,.jsonl)")
    args = parser.parse_args()

    cible = Path(args.cible)
    if not cible.exists():
        print(f"Cible introuvable: {cible}")
        return 2

    # La cible ELLE-MEME est hors champ : on le DIT et on rend 0, exactement comme
    # pour son dossier -- deux verdicts pour une meme cible n ont pas de sens.
    if any(part in EXCLUS_DIRS for part in cible.parts):
        print("HORS CHAMP : dossier technique -- aucun fichier controle : " + str(cible))
        return 0
    zone = zone_hors_champ_entiere(cible)
    if zone is not None:
        print(motif_hors_champ(zone[0], zone[1]) + " : " + str(cible))
        return 0

    exts = {e.strip() for e in args.ext.split(",") if e.strip()}
    releve = {}
    violations = []
    total = 0
    for p in fichiers_a_controler(cible, exts if cible.is_dir() else None, releve):
        total += 1
        try:
            raw = p.read_bytes()
        except OSError as e:
            violations.append((str(p), f"illisible: {e}"))
            continue
        lignes_fautives = set()
        try:
            raw.decode("ascii")
        except UnicodeDecodeError:
            for i, ligne in enumerate(raw.split(b"\n"), 1):
                try:
                    ligne.decode("ascii")
                except UnicodeDecodeError:
                    lignes_fautives.add(i)
            violations.append((str(p), f"lignes non-ASCII: {sorted(lignes_fautives)[:10]}"))

    if violations:
        print(f"ASCII VIOLE : {len(violations)}/{total} fichier(s) non-ASCII :")
        for f, detail in violations:
            print(f"  - {f} ({detail})")
        dire_zones_hors_champ(releve)
        return 1

    print(f"ASCII sain : {total} fichier(s) controles, 0 violation.")
    dire_zones_hors_champ(releve)
    return 0


if __name__ == "__main__":
    sys.exit(main())
