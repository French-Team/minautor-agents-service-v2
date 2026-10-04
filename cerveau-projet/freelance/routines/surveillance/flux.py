# -*- coding: ascii -*-
# routine : flux -- surveille le flux de messages JARVIS, alerte sur les
# P1 non-acquittes (ex-surveiller-flux-jarvis, renommee 2026-08-26 : nom
# simple qui exprime ce qu'elle est). Historise UNIQUEMENT quand des P1
# non-acquittes sont trouves (evenementiel - la routine est un element
# surveille avec son grade rouge G4).
import json
import os
import sys
from pathlib import Path

# P10 : racine DETECTEE en remontant jusqu'a AGENTS.md (jamais compte)
_d = os.path.dirname(os.path.abspath(__file__))
while not os.path.isfile(os.path.join(_d, "AGENTS.md")):
    _p = os.path.dirname(_d)
    if _p == _d:
        break
    _d = _p
RACINE = Path(_d)
INBOX_DIR = RACINE / "cerveau-projet" / "freelance" / "tools-commun" / \
    "jarvis" / "inbox"


# Fichier de persistance pour la derniere valeur connue
_DERNIERE_VALEUR = Path(__file__).parent / ".flux_derniere.txt"

def main():
    alertes = 0
    for f in INBOX_DIR.glob("*.jsonl"):
        for ligne in f.read_text(encoding="utf-8").splitlines():
            if not ligne.strip():
                continue
            try:
                m = json.loads(ligne)
            except ValueError:
                continue
            if not m.get("lu") and m.get("priorite") == 1:
                alertes += 1
                print(f"ALERTE : P1 non-acquitte chez {f.stem} - "
                      f"{m.get('objet', '')[:50]}")
    
    # Historiser UNIQUEMENT si le nombre de P1 a change
    # (evite de noyer l'encart avec des entrees identiques)
    derniere_valeur = 0
    if _DERNIERE_VALEUR.exists():
        try:
            derniere_valeur = int(_DERNIERE_VALEUR.read_text().strip())
        except ValueError:
            pass
    
    if alertes != derniere_valeur:
        # Le nombre a change : historiser
        if alertes:
            try:
                _fo = RACINE / "cerveau-projet" / "freelance" / "tools-commun" \
                    / "os_path" / "fonctions"
                _fj = RACINE / "cerveau-projet" / "freelance" / "tools-commun" \
                    / "jarvis" / "fonctions"
                for p in (_fo, _fj):
                    if str(p) not in sys.path:
                        sys.path.insert(0, str(p))
                from historique import historiser
                historiser("flux",
                           "%d P1 non-acquitte(s) detecte(s)" % alertes,
                           "R", session="session-freelance")
            except Exception:
                pass
        else:
            # Retour a zero : historiser aussi (le probleme est regle)
            try:
                _fo = RACINE / "cerveau-projet" / "freelance" / "tools-commun" \
                    / "os_path" / "fonctions"
                _fj = RACINE / "cerveau-projet" / "freelance" / "tools-commun" \
                    / "jarvis" / "fonctions"
                for p in (_fo, _fj):
                    if str(p) not in sys.path:
                        sys.path.insert(0, str(p))
                from historique import historiser
                historiser("flux",
                           "Aucun P1 non-acquitte (probleme regle)",
                           "R", session="session-freelance")
            except Exception:
                pass
        # Sauvegarder la nouvelle valeur
        _DERNIERE_VALEUR.write_text(str(alertes))
        print(f"[FLUX] Changement : {derniere_valeur} -> {alertes} P1")
    else:
        print(f"[FLUX] Inchang : {alertes} P1 (pas d'historisation)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
