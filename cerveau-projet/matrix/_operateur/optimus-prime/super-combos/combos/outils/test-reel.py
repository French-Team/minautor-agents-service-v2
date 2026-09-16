#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test-reel.py -- Processus de validation reel

Lance un processus complet de validation des changements.

Usage:
  python test-reel.py --fichier <fichier>
  python test-reel.py --dossier <dossier>
  python test-reel.py --tout
"""

import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime


RACINE = Path(__file__).resolve().parent.parent.parent.parent.parent.parent
# Les super-combos vivent dans super-combos/ (un cran AU-DESSUS de combos/) :
# le dossier a ete corrige le 2026-09-13 (MO-067) -- ce chemin pointait
# combos/, ou sc-001 ne vit plus.
SUPERCMBOS_DIR = Path(__file__).parent.parent.parent
if SUPERCMBOS_DIR.name != "super-combos":
    raise RuntimeError(
        "Structure inattendue : " + str(SUPERCMBOS_DIR) + " n'est pas super-combos/"
    )


class TestReel:
    def __init__(self):
        self.resultats = []
        
    def verifier_fichier(self, fichier: Path) -> dict:
        """Verifier un fichier complet."""
        resultat = {
            "fichier": str(fichier),
            "nom": fichier.name,
            "debut": datetime.now().isoformat(),
            "phases": []
        }
        
        # Phase 1 : py_compile
        try:
            cmd = [sys.executable, "-m", "py_compile", str(fichier)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            resultat["phases"].append({
                "nom": "py_compile",
                "statut": "OK" if result.returncode == 0 else "ERREUR",
                "details": result.stderr if result.returncode != 0 else None
            })
        except Exception as e:
            resultat["phases"].append({
                "nom": "py_compile",
                "statut": "ERREUR",
                "details": str(e)
            })
        
        # Phase 2 : Verification ASCII
        try:
            with open(fichier, "r", encoding="utf-8") as f:
                contenu = f.read()
            
            # Verifier les caracteres non-ASCII
            non_ascii = [c for c in contenu if ord(c) > 127]
            resultat["phases"].append({
                "nom": "ascii-check",
                "statut": "OK" if not non_ascii else "AVERTISSEMENT",
                "details": f"{len(non_ascii)} caracteres non-ASCII trouves" if non_ascii else None
            })
        except Exception as e:
            resultat["phases"].append({
                "nom": "ascii-check",
                "statut": "ERREUR",
                "details": str(e)
            })
        
        # Phase 3 : Super-combos #1
        try:
            cmd = [sys.executable, str(SUPERCMBOS_DIR / "sc-001-auto-xxx" / "main.py"), 
                   "executer", "--fichier", str(fichier), "--mission", "TEST-REEL"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            resultat["phases"].append({
                "nom": "super-combos-1",
                "statut": "OK" if result.returncode == 0 else "ERREUR",
                "details": None if result.returncode == 0 else result.stderr
            })
        except Exception as e:
            resultat["phases"].append({
                "nom": "super-combos-1",
                "statut": "ERREUR",
                "details": str(e)
            })
        
        resultat["fin"] = datetime.now().isoformat()
        resultat["statut"] = "OK" if all(p["statut"] == "OK" for p in resultat["phases"]) else "ERREUR"
        
        return resultat
    
    def executer(self, cible: str):
        """Executer le test reel sur une cible."""
        print("=" * 60)
        print("TEST REEL - VALIDATION DES CHANGEMENTS")
        print("=" * 60)
        print()
        
        if cible == "tout":
            # Tester tous les fichiers Python du pilote
            pilote_dir = RACINE / "_operateur" / "optimus-prime" / "pilote"
            for fichier in pilote_dir.rglob("*.py"):
                resultat = self.verifier_fichier(fichier)
                self.resultats.append(resultat)
                
                statut = "OK" if resultat["statut"] == "OK" else "ERREUR"
                print(f"  {statut:8} : {resultat['nom']}")
        else:
            fichier = Path(cible)
            if fichier.exists():
                resultat = self.verifier_fichier(fichier)
                self.resultats.append(resultat)
                
                statut = "OK" if resultat["statut"] == "OK" else "ERREUR"
                print(f"  {statut:8} : {resultat['nom']}")
            else:
                print(f"ERREUR : Fichier introuvable : {cible}")
                return
        
        # Resume
        print()
        print("=" * 60)
        print("RESUME")
        print("=" * 60)
        
        total = len(self.resultats)
        ok = sum(1 for r in self.resultats if r["statut"] == "OK")
        erreurs = total - ok
        
        print(f"  Total : {total}")
        print(f"  OK : {ok}")
        print(f"  Erreurs : {erreurs}")
        
        if erreurs > 0:
            print()
            print("ERREURS DETECTEES :")
            for r in self.resultats:
                if r["statut"] != "OK":
                    print(f"  - {r['nom']}")
                    for p in r["phases"]:
                        if p["statut"] != "OK":
                            print(f"    {p['nom']} : {p['details']}")
        
        return 0 if erreurs == 0 else 1


def main():
    parser = argparse.ArgumentParser(description="Test reel de validation")
    parser.add_argument("--fichier", help="Fichier a tester")
    parser.add_argument("--tout", action="store_true", help="Tester tous les fichiers")
    args = parser.parse_args()
    
    if not args.fichier and not args.tout:
        parser.print_help()
        return 1
    
    test = TestReel()
    
    if args.tout:
        return test.executer("tout")
    else:
        return test.executer(args.fichier)


if __name__ == "__main__":
    sys.exit(main())
