#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
garde-perimetre-write.py -- Garde WRITE=matrix/ (M-098)

Signale tout fichier hors perimetre d ecriture d Optimus.
Perimetre : cerveau-projet/matrix/ (+ demarrer-optimus-prime.md racine, cree avec l utilisateur).
Usage: python garde-perimetre-write.py [--jours N] [--racine <path>]
  code 0 = perimetre sain, code 1 = ecritures suspectes hors perimetre.
"""

import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path


ALLOWLIST = {"demarrer-optimus-prime.md", "demarrer-cameleon.md"}

# Dossiers techniques exclus (activite git/python, jamais ecritures Optimus).
EXCLUS_DIRS = {".git", "__pycache__"}

# La zone JETABLE du cameleon est une exception NOMMEE a ce perimetre : elle vit
# HORS de la Matrice (workspace/tmp-cameleon) parce que le cameleon CONSTRUIT
# dans workspace/ (regle R-005, MO-189). Son domicile se CITE -- il est declare
# une seule fois dans le moteur partage des zones (data/commun/zone_tmp.py).
import sys as _sys

_MATRICE = Path(__file__).resolve()
while _MATRICE.name != 'matrix' and _MATRICE.parent != _MATRICE:
    _MATRICE = _MATRICE.parent
_sys.path.insert(0, str(_MATRICE / 'matrice' / 'data' / 'commun'))
from zone_tmp import est_dans_zone_cameleon  # noqa: E402

EXCLUS_EXT = {'.pyc', '.pid'}


def main():
    parser = argparse.ArgumentParser(description="Garde perimetre WRITE=matrix/")
    parser.add_argument("--jours", type=int, default=7, help="Fenetre de suspicion en jours (defaut: 7)")
    parser.add_argument("--racine", default=".", help="Racine projet (defaut: cwd)")
    args = parser.parse_args()

    racine = Path(args.racine).resolve()
    # Perimetre = le dossier matrix/ : cerveau-projet/matrix prefere (sinon racine/matrix)
    # Priorite a cerveau-projet/matrix car c'est le vrai perimetre de la Matrice.
    candidats = [racine / "cerveau-projet" / "matrix", racine / "matrix"]
    if racine.name == "matrix":
        candidats.insert(0, racine)
    perimetre = next((c for c in candidats if c.is_dir()), None)
    if perimetre is None:
        print(f"Dossier matrix/ introuvable sous {racine}")
        return 2
    seuil = datetime.now() - timedelta(days=args.jours)
    suspects = []

    import os
    # Elagage Matrice: si on walk depuis la racine, on elague le sous-arbre matrix/ en tete
    perimetre_parts = perimetre.resolve().parts
    racine_parts = racine.resolve().parts
    for dirpath, dirnames, filenames in os.walk(racine):
        # Elagage : ne jamais descendre dans les dossiers techniques
        dirnames[:] = [d for d in dirnames if d not in EXCLUS_DIRS]
        # Elagage perimetre : le sous-arbre matrix/ entier est sain par definition
        cur = Path(dirpath).resolve()
        try:
            rel = cur.relative_to(racine.resolve())
        except ValueError:
            rel = None
        if rel is not None:
            # cur est sous racine -> regarder si cur est prefixe de perimetre ou dans perimetre
            try:
                perimetre.resolve().relative_to(cur)
                # cur est ancetre de perimetre (ex: racine, cerveau-projet) : elaguer la branche perimetre
                # le premier element de perimetre sous cur est a retirer de dirnames
                reste = perimetre.resolve().relative_to(cur)
                if reste.parts:
                    tete = reste.parts[0]
                    if tete in dirnames:
                        dirnames.remove(tete)
                continue
            except ValueError:
                pass
            # cur est deja dans perimetre -> skip
            try:
                cur.relative_to(perimetre.resolve())
                dirnames.clear()
                continue
            except ValueError:
                pass
        for name in filenames:
            p = Path(dirpath) / name
            if not p.is_file():
                continue
            try:
                rel = p.relative_to(racine)
            except ValueError:
                continue
            # Dans le perimetre : sous matrix/ ou allowlist racine
            try:
                p.relative_to(perimetre)
                continue
            except ValueError:
                pass
            # ZONE DECLAREE du cameleon (R-005) : elle vit HORS de la Matrice,
            # donc elle serait suspecte ici a chaque mission du cameleon.
            # L exemption est NOMMEE (exemptions visibles, MO-075), jamais muette.
            if est_dans_zone_cameleon(p, racine):
                continue
            if len(rel.parts) == 1 and rel.parts[0] in ALLOWLIST:
                continue
            # Bruit technique exclu (.pyc, .pid ; dossiers deja elagues au walk)
            if p.suffix in EXCLUS_EXT:
                continue
            # Hors perimetre : suspect si modifie dans la fenetre
            try:
                mtime = datetime.fromtimestamp(p.stat().st_mtime)
            except OSError:
                continue
            if mtime >= seuil:
                suspects.append((str(rel), mtime.strftime("%Y-%m-%d %H:%M:%S")))

    if suspects:
        print(f"PERIMETRE VIOLE : {len(suspects)} fichier(s) hors matrix/ modifies (fenetre {args.jours}j) :")
        for rel, date in sorted(suspects):
            print(f"  - {rel} ({date})")
        return 1

    print(f"Perimetre sain : aucune ecriture hors matrix/ (fenetre {args.jours}j).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
