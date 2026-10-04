#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
detecteur-mots-cles.py -- Detecteur de mots-cles pour la Matrice

Detecte les mots-cles dans les demandes utilisateur et lance le pilote approprie.

Usage:
  python detecteur-mots-cles.py --texte "ma demande avec [bug]"
  python detecteur-mots-cles.py --lister
"""


import subprocess
import sys
from pathlib import Path

# --- DOMICILE DU LANCEMENT (EO-430 / MO-416, lot -- fin du residu) -----------
# La racine se DETECTE par marqueur (MO-088 : aucun parents[N] nu) : on remonte
# jusqu au dossier `matrix`, et on REFUSE plutot que de deviner (garde-foi L-006).
# Bloc AUTOSUFFISANT : il ne depend ni de l ordre des imports du fichier, ni de la
# presence d un `import subprocess` de module (mesure du 2026-09-25 : deux fichiers
# casses par ces deux pieges, invisibles au py_compile).
_RACINE_LANCEMENT = Path(__file__).resolve().parent
while _RACINE_LANCEMENT.name != "matrix":
    if _RACINE_LANCEMENT.parent == _RACINE_LANCEMENT:
        raise RuntimeError("racine `matrix` introuvable en remontant depuis " + __file__)
    _RACINE_LANCEMENT = _RACINE_LANCEMENT.parent
_REPERTOIRE_COMMUN_LANCEMENT = _RACINE_LANCEMENT / "matrice" / "data" / "commun"
if not (_REPERTOIRE_COMMUN_LANCEMENT / "lancement.py").is_file():
    raise RuntimeError("Structure inattendue : " + str(_REPERTOIRE_COMMUN_LANCEMENT)
                       + " ne porte pas le domicile du lancement")
if str(_REPERTOIRE_COMMUN_LANCEMENT) not in sys.path:
    sys.path.insert(0, str(_REPERTOIRE_COMMUN_LANCEMENT))
from lancement import drapeaux_popen  # noqa: E402


def lancer_enfant(*arguments, **options):
    """Le SEUL lancement de processus de cet outil : jamais de fenetre."""
    return subprocess.run(*arguments, **options, **drapeaux_popen())


def popen_enfant(*arguments, **options):
    """Le lancement DETACHE de cet outil : jamais de fenetre."""
    return subprocess.Popen(*arguments, **options, **drapeaux_popen())


import sys
import json
import argparse
import re
from pathlib import Path
from datetime import datetime


RACINE = Path(__file__).resolve().parent.parent.parent
PILOTE_OPTIMUS = RACINE / "_operateur" / "optimus-prime" / "pilote" / "main.py"


# Dictionnaire des mots-cles et leurs actions
MOTS_CLES = {
    "[bug]": {
        "description": "Bug detecte",
        "action": "corriger",
        "phase": "correction",
        "priorite": "haute"
    },
    "[probleme]": {
        "description": "Probleme dans les flux",
        "action": "diagnostiquer",
        "phase": "diagnostic",
        "priorite": "haute"
    },
    "[incoherence]": {
        "description": "Incoherence percue",
        "action": "analyser",
        "phase": "analyse",
        "priorite": "moyenne"
    },
    "[super-combos: #1]": {
        "description": "Lancer super-combos AUTO-XXX",
        "action": "executer-super-combos",
        "phase": "execution",
        "priorite": "normale"
    },
    "[test-reel]": {
        "description": "Validation reel",
        "action": "valider",
        "phase": "validation",
        "priorite": "normale"
    },
    "[revision]": {
        "description": "Demande de revision",
        "action": "reviser",
        "phase": "revision",
        "priorite": "normale"
    },
    "[mission]": {
        "description": "Demande de mission",
        "action": "creer-mission",
        "phase": "creation",
        "priorite": "normale"
    },
    "[tache]": {
        "description": "Tache specifique",
        "action": "executer-tache",
        "phase": "execution",
        "priorite": "normale"
    }
}


def detecter_mot_cle(texte: str) -> list:
    """Detecter les mots-cles dans un texte."""
    mots_cles_trouves = []
    
    for mot_cle, config in MOTS_CLES.items():
        if mot_cle in texte:
            mots_cles_trouves.append({
                "mot_cle": mot_cle,
                "config": config
            })
    
    return mots_cles_trouves


def lister_mots_cles():
    """Lister tous les mots-cles disponibles."""
    print("=" * 60)
    print("MOTS-CLES DISPONIBLES")
    print("=" * 60)
    print()
    
    for mot_cle, config in MOTS_CLES.items():
        print(f"  {mot_cle:25} : {config['description']}")
        print(f"  {' ':25}   Action: {config['action']}")
        print(f"  {' ':25}   Phase: {config['phase']}")
        print(f"  {' ':25}   Priorite: {config['priorite']}")
        print()
    
    print("Utilisation : python detecteur-mots-cles.py --texte \"ma demande avec [bug]\"")


def traiter_mot_cle(mot_cle: str, config: dict, texte: str):
    """Traiter un mot-cle detecte."""
    print("=" * 60)
    print(f"MOT-CLE DETECTE : {mot_cle}")
    print("=" * 60)
    print()
    print(f"Description : {config['description']}")
    print(f"Action : {config['action']}")
    print(f"Phase : {config['phase']}")
    print(f"Priorite : {config['priorite']}")
    print()
    
    # Lancer le pilote Optimus avec le mot-cle
    print("Lancement du pilote Optimus...")
    print()
    
    import subprocess
    cmd = [sys.executable, str(PILOTE_OPTIMUS), "mission", "--action", "debut", 
           "--id", f"MC-{datetime.now().strftime('%Y%m%d-%H%M%S')}", 
           "--theme", config['action']]
    
    result = lancer_enfant(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(result.stdout)
    else:
        print(f"ERREUR : {result.stderr}")


def main():
    parser = argparse.ArgumentParser(description="Detecteur de mots-cles")
    parser.add_argument("--texte", help="Texte a analyser")
    parser.add_argument("--lister", action="store_true", help="Lister les mots-cles")
    args = parser.parse_args()
    
    if args.lister or not args.texte:
        lister_mots_cles()
        return 0
    
    # Detecter les mots-cles
    mots_cles = detecter_mot_cle(args.texte)
    
    if not mots_cles:
        print("Aucun mot-cle detecte dans le texte.")
        return 0
    
    print(f"Mots-cles detectes : {len(mots_cles)}")
    print()
    
    # Traiter chaque mot-cle
    for mc in mots_cles:
        traiter_mot_cle(mc["mot_cle"], mc["config"], args.texte)
        print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
