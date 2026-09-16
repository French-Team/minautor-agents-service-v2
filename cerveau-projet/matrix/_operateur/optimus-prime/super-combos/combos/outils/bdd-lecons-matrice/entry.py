#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bdd-lecons-matrice/entry.py -- Orchestrateur porte unique lecons.json
"""

import sys
import argparse
from pathlib import Path

# NOTE (L-017) : dossier a tiret = pas un package -> chargement via importlib
import importlib.util as _ilu

_fonc_path = Path(__file__).parent / "fonctions" / "bdd_lecons_matrice.py"
_spec = _ilu.spec_from_file_location("bdd_lecons_matrice_fonc", str(_fonc_path))
_fonc = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_fonc)

ajouter_lecon = _fonc.ajouter_lecon
lister_lecons = _fonc.lister_lecons
chercher_lecons = _fonc.chercher_lecons


# Racine matrix/ DETECTEE par le marqueur partage (M-076 : matrice/data/commun/racine.py),
# jamais comptee a la main (L-013).
BORNES_REMONTEE = 30
_courant = Path(__file__).resolve().parent
for _ in range(BORNES_REMONTEE):
    if (_courant / "matrice" / "data" / "commun" / "racine.py").is_file():
        break
    _courant = _courant.parent
else:
    raise RuntimeError("Racine matrix/ introuvable en remontant.")
DB_PATH = _courant / "matrice" / "data" / "lecons.json"


def run(commande, args):
    _fonc.init_db(DB_PATH)

    if commande == "ajouter":
        return cmd_ajouter(args)
    elif commande == "lister":
        return cmd_lister(args)
    elif commande == "chercher":
        return cmd_chercher(args)
    else:
        print(f"Sous-commande inconnue: {commande}")
        return 1


def cmd_ajouter(args):
    parser = argparse.ArgumentParser(description="Ajouter une lecon")
    parser.add_argument("lecon", help="Texte de la lecon")
    parser.add_argument("--tags", default="", help="Tags separes par virgules")
    parser.add_argument("--source", default="auto-evolution")
    parsed = parser.parse_args(args)

    new_id = ajouter_lecon(DB_PATH, parsed.lecon, parsed.tags, parsed.source)
    print(f"Lecon ajoutee: {new_id}")
    return 0


def _affiche(lecons):
    if not lecons:
        print("Aucune lecon trouvee.")
        return
    for l in lecons:
        print(f"  {l['id']} | {l['date']} | tags={','.join(l.get('tags', []))} | src={l.get('source', '')}")
        print(f"    {l['lecon'][:200]}")


def cmd_lister(args):
    parser = argparse.ArgumentParser(description="Lister les dernieres lecons")
    parser.add_argument("--n", type=int, default=10)
    parsed = parser.parse_args(args)

    _affiche(lister_lecons(DB_PATH, parsed.n))
    return 0


def cmd_chercher(args):
    parser = argparse.ArgumentParser(description="Chercher des lecons")
    parser.add_argument("--mot-cle", default=None)
    parser.add_argument("--tag", default=None)
    parsed = parser.parse_args(args)

    if not parsed.mot_cle and not parsed.tag:
        print("Preciser --mot-cle et/ou --tag")
        return 1
    _affiche(chercher_lecons(DB_PATH, parsed.mot_cle, parsed.tag))
    return 0
