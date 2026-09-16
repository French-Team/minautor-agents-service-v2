#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bdd-modifs/entry.py -- Orchestrateur categorie modifications
"""

import sys
import argparse
from pathlib import Path

# Charger les fonctions depuis le fichier (nom dossier avec tiret = pas un package)
import importlib.util as _ilu

_fonc_path = Path(__file__).parent / "fonctions" / "bdd_modifs.py"
_spec = _ilu.spec_from_file_location("bdd_modifs_fonc", str(_fonc_path))
_fonc = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_fonc)

init_db = _fonc.init_db
ajouter_modif = _fonc.ajouter_modif
verrouiller_fichier = _fonc.verrouiller_fichier
deverrouiller_fichier = _fonc.deverrouiller_fichier
annuler_modif = _fonc.annuler_modif
lister_modifs = _fonc.lister_modifs
# Le vocabulaire des statuts vient du domicile (fonctions/bdd_modifs.py) : la
# porte ne recopie ni les statuts admis, ni le statut par defaut (MO-127).
STATUTS = _fonc.STATUTS


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
DB_PATH = _courant / "matrice" / "data" / "modifications.db"


def run(commande, args):
    init_db(DB_PATH)

    if commande == "ajouter":
        return cmd_ajouter(args)
    elif commande == "verrouiller":
        return cmd_verrouiller(args)
    elif commande == "deverrouiller":
        return cmd_deverrouiller(args)
    elif commande == "annuler":
        return cmd_annuler(args)
    elif commande == "lister":
        return cmd_lister(args)
    else:
        print(f"Sous-commande inconnue: {commande}")
        return 1


def cmd_ajouter(args):
    parser = argparse.ArgumentParser(description="Ajouter une modification")
    parser.add_argument("--fichier", required=True)
    parser.add_argument("--hash-avant", required=True)
    parser.add_argument("--hash-apres", required=True)
    parser.add_argument("--diff", required=True)
    parser.add_argument("--raison", required=True)
    parser.add_argument("--friction-id", type=int, required=True)
    parsed = parser.parse_args(args)

    modif_id = ajouter_modif(
        DB_PATH,
        parsed.fichier,
        parsed.hash_avant,
        parsed.hash_apres,
        parsed.diff,
        parsed.raison,
        parsed.friction_id,
    )
    print(f"Modification ajoutee: ID={modif_id}")
    return 0


def cmd_verrouiller(args):
    parser = argparse.ArgumentParser(description="Verrouiller un fichier")
    parser.add_argument("--fichier", required=True)
    parsed = parser.parse_args(args)

    verrouiller_fichier(DB_PATH, parsed.fichier)
    print(f"Fichier verrouille: {parsed.fichier}")
    return 0


def cmd_deverrouiller(args):
    parser = argparse.ArgumentParser(description="Deverrouiller un fichier")
    parser.add_argument("--fichier", required=True)
    parsed = parser.parse_args(args)

    deverrouiller_fichier(DB_PATH, parsed.fichier)
    print(f"Fichier deverrouille: {parsed.fichier}")
    return 0


def cmd_annuler(args):
    parser = argparse.ArgumentParser(description="Annuler une modification")
    parser.add_argument("--fichier", required=True)
    parser.add_argument("--raison", required=True)
    parsed = parser.parse_args(args)

    annuler_modif(DB_PATH, parsed.fichier, parsed.raison)
    print(f"Modification annulee pour: {parsed.fichier}")
    return 0


def cmd_lister(args):
    parser = argparse.ArgumentParser(description="Lister les modifications")
    parser.add_argument("--fichier", help="Filtrer par fichier")
    parser.add_argument("--statut", choices=list(STATUTS),
                        help="Filtrer par statut (defaut : tous les statuts)")
    parser.add_argument("--n", type=int, default=20)
    parsed = parser.parse_args(args)

    modifs = lister_modifs(DB_PATH, parsed.fichier, parsed.statut, parsed.n)
    if not modifs:
        if parsed.statut:
            print("Aucune modification pour le statut '" + parsed.statut
                  + "' -- la BDD peut en contenir d'autres : essayer sans --statut.")
        else:
            print("Aucune modification trouvee.")
        return 0

    for m in modifs:
        print(f"  ID={m['id']} | {m['date']} | fichier={m['fichier']} | statut={m['statut']} | friction={m['friction_id']}")
        print(f"    hash_avant={m['hash_avant'][:16]}... | hash_apres={m['hash_apres'][:16]}...")
        print(f"    raison={m['raison']}")
    return 0