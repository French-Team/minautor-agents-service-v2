#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
watchdog-flux2.py -- Monitoring temps reel des violations Flux 2

Surveille en continu les modifications de fichiers et detecte
toute violation du perimetre Flux 2 (Optimus).

Usage: python watchdog-flux2.py [--racine <path>] [--interval <sec>] [--log <fichier>]
  code 0 = arret normal, code 1 = violation detectee.
"""

import sys
import time
import argparse
import json
from pathlib import Path
from datetime import datetime
from typing import Set, Dict


# Zones autorisees pour Optimus (Flux 2)
ZONES_AUTORISEES = [
    "cerveau-projet/matrix/",
    "cerveau-projet/matrix/_operateur/",
    "cerveau-projet/matrix/_operateur/optimus-prime/",
    "cerveau-projet/matrix/matrice/",
    "cerveau-projet/matrix/matrice/data/",
    "cerveau-projet/matrix/matrice/routines/",
    "cerveau-projet/matrix/matrice/pilote/",
    "cerveau-projet/matrix/matrice/intercom/",
]

# Zones interdites pour Optimus (Flux 1 - Cameleon)
ZONES_INTERDITES = [
    "cerveau-projet/matrix/matrice/pilote/file-missions.json",
    "cerveau-projet/matrix/matrice/pilote/entonnoir-files.json",
    "cerveau-projet/matrix/matrice/pilote/main.py",
    "cerveau-projet/agents/",
    "cerveau-projet/freelance/",
    "cerveau-projet/matrix/_operateur/cameleon/",
]

# Fichiers a ignorer
FICHIERS_A_IGNORER = [
    ".tmp",
    ".bak",
    ".pid",
    "__pycache__",
    ".pyc",
]


class WatchdogFlux2:
    def __init__(self, racine: Path, interval: int = 5, log_file: str = None):
        self.racine = racine.resolve()
        self.interval = interval
        self.log_file = log_file
        self.snapshots: Dict[str, float] = {}
        self.violations: list = []
        
    def prendre_snapshot(self) -> Dict[str, float]:
        """Prendre une image de tous les fichiers avec leur mtime."""
        snapshot = {}
        try:
            for f in self.racine.rglob("*"):
                if f.is_file():
                    # Ignorer les fichiers a ignorer
                    if any(f.suffix.endswith(ext) or ext in f.parts for ext in FICHIERS_A_IGNORER):
                        continue
                    
                    try:
                        mtime = f.stat().st_mtime
                        rel = str(f.relative_to(self.racine))
                        snapshot[rel] = mtime
                    except OSError:
                        pass
        except PermissionError:
            pass
        return snapshot
    
    def detecter_violations(self, ancienne: Dict[str, float], nouvelle: Dict[str, float]) -> list:
        """Detecter les violations entre deux snapshots."""
        violations = []
        
        for fichier, mtime in nouvelle.items():
            # Verifier si le fichier est nouveau ou modifie
            if fichier not in ancienne or ancienne[fichier] < mtime:
                # Verifier si le fichier est dans une zone interdite
                for zone in ZONES_INTERDITES:
                    try:
                        Path(fichier).relative_to(zone)
                        violations.append({
                            "fichier": fichier,
                            "type": "modification" if fichier in ancienne else "creation",
                            "zone_interdite": zone,
                            "timestamp": datetime.now().isoformat()
                        })
                        break
                    except ValueError:
                        continue
                
                # Verifier si le fichier est hors zone autorisee
                if not any(Path(fichier).relative_to(zone) is not None for zone in ZONES_AUTORISEES if Path(fichier).parts[:len(Path(zone).parts)] == Path(zone).parts):
                    # Verifier si le fichier a ete modifie aujourd'hui
                    try:
                        mtime_date = datetime.fromtimestamp(mtime)
                        if mtime_date.date() == datetime.now().date():
                            # Verifier si c'est un vrai changement
                            if fichier in ancienne and ancienne[fichier] != mtime:
                                violations.append({
                                    "fichier": fichier,
                                    "type": "modification_hors_zone",
                                    "timestamp": datetime.now().isoformat()
                                })
                    except OSError:
                        pass
        
        return violations
    
    def logger_violation(self, violation: dict):
        """Logger une violation."""
        self.violations.append(violation)
        
        # Afficher dans la console
        print(f"[VIOLATION] {violation['timestamp']}")
        print(f"  Fichier: {violation['fichier']}")
        print(f"  Type: {violation['type']}")
        if 'zone_interdite' in violation:
            print(f"  Zone interdite: {violation['zone_interdite']}")
        print()
        
        # Ecrire dans le fichier de log si specifie
        if self.log_file:
            try:
                with open(self.log_file, "a", encoding="utf-8") as f:
                    json.dump(violation, f, ensure_ascii=False)
                    f.write("\n")
            except Exception as e:
                print(f"[ERREUR] Impossible d'ecrire dans le log: {e}")
    
    def verifier_processus(self) -> list:
        """Verifier les processus en cours (etection des processus Fantome)."""
        # Placeholder pour detection de processus
        # Serait implemente avec psutil ou similaire
        return []
    
    def executer(self):
        """Boucle principale du watchdog."""
        print(f"Watchdog Flux 2 demarre - Surveillance de: {self.racine}")
        print(f"Intervalle: {self.interval} secondes")
        print("Appuyez sur Ctrl+C pour arreter")
        print()
        
        # Premiere snapshot
        self.snapshots = self.prendre_snapshot()
        print(f"[{datetime.now().isoformat()}] Snapshot initiale: {len(self.snapshots)} fichiers")
        
        try:
            while True:
                time.sleep(self.interval)
                
                # Nouvelle snapshot
                nouvelle_snapshot = self.prendre_snapshot()
                
                # Detecter les violations
                violations = self.detecter_violations(self.snapshots, nouvelle_snapshot)
                
                # Logger les violations
                for violation in violations:
                    self.logger_violation(violation)
                
                # Mettre a jour la snapshot
                self.snapshots = nouvelle_snapshot
                
                # Verifier les processus
                processus_suspects = self.verifier_processus()
                for proc in processus_suspects:
                    self.logger_violation({
                        "fichier": "processus",
                        "type": "processus_fantome",
                        "details": proc,
                        "timestamp": datetime.now().isoformat()
                    })
                
                # Afficher statut
                print(f"[{datetime.now().isoformat()}] Surveillance active - {len(self.snapshots)} fichiers surveilles")
                
        except KeyboardInterrupt:
            print("\nWatchdog arrete.")
            print(f"Total violations detectees: {len(self.violations)}")
            return 1 if self.violations else 0


def main():
    parser = argparse.ArgumentParser(description="Watchdog Flux 2 pour Optimus")
    parser.add_argument("--racine", default=".", help="Racine projet (defaut: cwd)")
    parser.add_argument("--interval", type=int, default=5, help="Intervalle en secondes (defaut: 5)")
    parser.add_argument("--log", help="Fichier de log pour les violations")
    args = parser.parse_args()

    watchdog = WatchdogFlux2(
        racine=Path(args.racine),
        interval=args.interval,
        log_file=args.log
    )
    
    return watchdog.executer()


if __name__ == "__main__":
    sys.exit(main())
