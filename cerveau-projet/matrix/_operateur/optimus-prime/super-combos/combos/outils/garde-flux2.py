#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
garde-flux2.py -- Garde Flux 2 pour Optimus Prime

Verifie qu'Optimus ne travaille QUE dans le Flux 2 (maintenance).
Detecte toute violation du perimetre Flux 2.

Usage: python garde-flux2.py [--racine <path>] [--verbose] [--strict]
  code 0 = Flux 2 respecte, code 1 = violation detectee.
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime


# Zones autorisees pour Optimus (Flux 2)
ZONES_AUTORISEES = [
    "cerveau-projet/matrix/",  # Perimetre d'ecriture principal
    "cerveau-projet/matrix/_operateur/",  # Zone operateurs
    "cerveau-projet/matrix/_operateur/optimus-prime/",  # Zone Optimus
    "cerveau-projet/matrix/matrice/",  # Zone Matrice (lecture seule)
    "cerveau-projet/matrix/matrice/data/",  # BDD (lecture seule)
    "cerveau-projet/matrix/matrice/routines/",  # Routines (lecture seule)
    "cerveau-projet/matrix/matrice/pilote/",  # Pilote (lecture seule)
    "cerveau-projet/matrix/matrice/intercom/",  # Intercom (ecriture limitez)
]

# Zones interdites pour Optimus (Flux 1 - Cameleon)
ZONES_INTERDITES = [
    "cerveau-projet/matrix/matrice/pilote/file-missions.json",  # File du cameleon
    "cerveau-projet/matrix/matrice/pilote/entonnoir-files.json",  # Entonnoir du cameleon
    "cerveau-projet/matrix/matrice/pilote/main.py",  # Pilote du cameleon
    "cerveau-projet/agents/",  # Agents v1/v2
    "cerveau-projet/freelance/",  # Agents freelance
    "cerveau-projet/matrix/_operateur/cameleon/",  # Zone cameleon
]

# Fichiers temporaires autorises
FICHIERS_TEMPORAIRES = [
    ".tmp",
    ".bak",
    ".pid",
]


def main():
    parser = argparse.ArgumentParser(description="Garde Flux 2 pour Optimus")
    parser.add_argument("--racine", default=".", help="Racine projet (defaut: cwd)")
    parser.add_argument("--verbose", action="store_true", help="Afficher les details")
    parser.add_argument("--strict", action="store_true", help="Mode strict (toute modification = violation)")
    args = parser.parse_args()

    racine = Path(args.racine).resolve()
    violations = []
    avertissements = []

    # Verifier les zones interdites
    for zone in ZONES_INTERDITES:
        zone_path = racine / zone
        if zone_path.exists():
            if zone_path.is_file():
                # Verifier si le fichier a ete modifie recemment
                try:
                    mtime = datetime.fromtimestamp(zone_path.stat().st_mtime)
                    if mtime >= datetime.now().replace(hour=0, minute=0, second=0):
                        violations.append(f"FICHIER INTERDIT MODIFIE AUJOURD'HUI: {zone}")
                except OSError:
                    pass
            else:
                # Verifier si le dossier contient des fichiers modifies
                try:
                    for f in zone_path.rglob("*"):
                        if f.is_file():
                            try:
                                mtime = datetime.fromtimestamp(f.stat().st_mtime)
                                if mtime >= datetime.now().replace(hour=0, minute=0, second=0):
                                    violations.append(f"FICHIER INTERDIT MODIFIE: {f.relative_to(racine)}")
                            except OSError:
                                pass
                except PermissionError:
                    pass

    # Verifier les fichiers hors perimetre
    try:
        for f in racine.rglob("*"):
            if f.is_file():
                # Ignorer les fichiers temporaires
                if f.suffix in FICHIERS_TEMPORAIRES:
                    continue
                
                # Ignorer les dossiers techniques
                if any(part.startswith(".") or part == "__pycache__" for part in f.parts):
                    continue
                
                # Verifier si le fichier est dans une zone autorisee
                rel = f.relative_to(racine)
                dans_zone_autorisee = False
                for zone in ZONES_AUTORISEES:
                    try:
                        rel.relative_to(zone)
                        dans_zone_autorisee = True
                        break
                    except ValueError:
                        continue
                
                if not dans_zone_autorisee:
                    # Verifier si le fichier a ete modifie aujourd'hui
                    try:
                        mtime = datetime.fromtimestamp(f.stat().st_mtime)
                        if mtime >= datetime.now().replace(hour=0, minute=0, second=0):
                            if args.strict:
                                violations.append(f"FICHIER HORS ZONE MODIFIE (STRICT): {rel}")
                            else:
                                avertissements.append(f"FICHIER HORS ZONE MODIFIE: {rel}")
                    except OSError:
                        pass
    except PermissionError:
        pass

    # Afficher les resultats
    if violations:
        print("VIOLATIONS FLUX 2 DETECTEES:")
        for v in violations:
            print(f"  - {v}")
        print(f"\nTotal: {len(violations)} violation(s)")
        return 1

    if avertissements and args.verbose:
        print("AVERTISSEMENTS (fichiers hors zone modifies):")
        for a in avertissements:
            print(f"  - {a}")
        print(f"\nTotal: {len(avertissements)} avertissement(s)")

    if not violations:
        print("FLUX 2 RESPECTE: Aucune violation detectee.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
