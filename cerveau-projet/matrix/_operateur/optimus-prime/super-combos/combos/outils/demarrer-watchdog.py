#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
demarrer-watchdog.py -- Demarrer/Arreter le Watchdog Flux 2

Usage:
  python demarrer-watchdog.py demarrer [--interval <sec>]
  python demarrer-watchdog.py arreter
  python demarrer-watchdog.py status
  python demarrer-watchdog.py violations [--dernieres <n>]
"""

import sys
import os
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime


RACINE = Path(__file__).resolve().parent.parent.parent.parent.parent
WATCHDOG_SCRIPT = Path(__file__).parent / "watchdog-flux2-bg.py"
PID_FILE = Path(__file__).parent / "watchdog-flux2.pid"
LOG_FILE = Path(__file__).parent / "watchdog-flux2-bg.jsonl"


def demarrer(interval: int = 30):
    """Demarrer le watchdog."""
    if PID_FILE.exists():
        try:
            pid = int(PID_FILE.read_text().strip())
            # Verifier si le processus existe (Windows)
            result = subprocess.run(["tasklist", "/FI", f"PID eq {pid}"], capture_output=True, text=True)
            if str(pid) in result.stdout:
                print(f"Le watchdog est deja demarre (PID: {pid})")
                return
        except (ValueError, Exception):
            pass
    
    cmd = [
        sys.executable,
        str(WATCHDOG_SCRIPT),
        "--racine", str(RACINE),
        "--interval", str(interval),
        "--log", str(LOG_FILE),
        "--pid", str(PID_FILE)
    ]
    
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)
    
    if PID_FILE.exists():
        pid = PID_FILE.read_text().strip()
        print(f"Watchdog demarre (PID: {pid})")
    else:
        print("Erreur lors du demarrage du watchdog")


def arreter():
    """Arreter le watchdog."""
    if not PID_FILE.exists():
        print("Le watchdog n'est pas en cours d'execution")
        return
    
    try:
        pid = int(PID_FILE.read_text().strip())
        # Arreter le processus (Windows)
        subprocess.run(["taskkill", "/F", "/PID", str(pid)], capture_output=True)
        PID_FILE.unlink()
        print(f"Watchdog arrete (PID: {pid})")
    except Exception as e:
        if PID_FILE.exists():
            PID_FILE.unlink()
        print(f"Watchdog arrete")


def status():
    """Verifier le statut du watchdog."""
    if not PID_FILE.exists():
        print("Watchdog: ARRETE")
        return
    
    try:
        pid = int(PID_FILE.read_text().strip())
        # Verifier si le processus existe (Windows)
        result = subprocess.run(["tasklist", "/FI", f"PID eq {pid}"], capture_output=True, text=True)
        if str(pid) in result.stdout:
            print(f"Watchdog: EN COURS (PID: {pid})")
            
            # Compter les violations
            if LOG_FILE.exists():
                with open(LOG_FILE, "r", encoding="utf-8") as f:
                    violations = [json.loads(line) for line in f if line.strip()]
                    print(f"Violations detectees: {len(violations)}")
                    
                    # Derniere violation
                    if violations:
                        derniere = violations[-1]
                        print(f"Derniere violation: {derniere['timestamp']}")
                        print(f"  Fichier: {derniere['fichier']}")
            else:
                print("Violations detectees: 0")
        else:
            PID_FILE.unlink()
            print("Watchdog: ARRETE (processus non trouve)")
            
    except Exception as e:
        if PID_FILE.exists():
            PID_FILE.unlink()
        print("Watchdog: ARRETE")


def violations(dernieres: int = 10):
    """Afficher les dernieres violations."""
    if not LOG_FILE.exists():
        print("Aucune violation detectee")
        return
    
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lignes = [json.loads(line) for line in f if line.strip()]
    
    if not lignes:
        print("Aucune violation detectee")
        return
    
    print(f"Dernieres {min(dernieres, len(lignes))} violations:")
    for v in lignes[-dernieres:]:
        print(f"  {v['timestamp']}: {v['fichier']} ({v['type']})")
        if 'zone_interdite' in v:
            print(f"    Zone interdite: {v['zone_interdite']}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python demarrer-watchdog.py [demarrer|arreter|status|violations]")
        return 1
    
    commande = sys.argv[1].lower()
    
    if commande == "demarrer":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        demarrer(interval)
    elif commande == "arreter":
        arreter()
    elif commande == "status":
        status()
    elif commande == "violations":
        dernieres = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        violations(dernieres)
    else:
        print("Commande inconnue:", commande)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
