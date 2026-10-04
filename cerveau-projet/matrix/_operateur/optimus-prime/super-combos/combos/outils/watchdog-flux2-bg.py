#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
watchdog-flux2-bg.py -- Watchdog Flux 2 en arriere-plan

Lance le watchdog en arriere-plan et ecrit les violations dans un fichier de log.

Usage: python watchdog-flux2-bg.py [--racine <path>] [--interval <sec>] [--log <fichier>] [--pid <fichier>]
"""

import sys
import time
import argparse
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Set, Dict
import threading


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


class WatchdogFlux2BG:
    def __init__(self, racine: Path, interval: int = 30, log_file: str = None, pid_file: str = None):
        self.racine = racine.resolve()
        self.interval = interval
        self.log_file = log_file or str(self.racine / "cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/outils/watchdog-flux2-bg.jsonl")
        self.pid_file = pid_file or str(self.racine / "cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/outils/watchdog-flux2.pid")
        self.running = False
        self.thread = None
        
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
        
        return violations
    
    def logger_violation(self, violation: dict):
        """Logger une violation."""
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                json.dump(violation, f, ensure_ascii=False)
                f.write("\n")
        except Exception as e:
            pass
    
    def surveiller(self):
        """Boucle de surveillance."""
        snapshot = self.prendre_snapshot()
        
        while self.running:
            time.sleep(self.interval)
            
            nouvelle_snapshot = self.prendre_snapshot()
            violations = self.detecter_violations(snapshot, nouvelle_snapshot)
            
            for violation in violations:
                self.logger_violation(violation)
            
            snapshot = nouvelle_snapshot
    
    def demarrer(self):
        """Demarrer le watchdog en arriere-plan."""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self.surveiller, daemon=True)
        self.thread.start()
        
        # Ecrire le PID
        try:
            with open(self.pid_file, "w") as f:
                f.write(str(os.getpid()))
        except Exception:
            pass
    
    def arreter(self):
        """Arreter le watchdog."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        
        # Supprimer le PID
        try:
            if os.path.exists(self.pid_file):
                os.remove(self.pid_file)
        except Exception:
            pass


def main():
    parser = argparse.ArgumentParser(description="Watchdog Flux 2 en arriere-plan")
    parser.add_argument("--racine", default=".", help="Racine projet (defaut: cwd)")
    parser.add_argument("--interval", type=int, default=30, help="Intervalle en secondes (defaut: 30)")
    parser.add_argument("--log", help="Fichier de log pour les violations")
    parser.add_argument("--pid", help="Fichier PID")
    args = parser.parse_args()

    watchdog = WatchdogFlux2BG(
        racine=Path(args.racine),
        interval=args.interval,
        log_file=args.log,
        pid_file=args.pid
    )
    
    watchdog.demarrer()
    print(f"Watchdog Flux 2 demarre en arriere-plan")
    print(f"PID: {os.getpid()}")
    print(f"Log: {watchdog.log_file}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        watchdog.arreter()
        print("Watchdog arrete.")


if __name__ == "__main__":
    main()
