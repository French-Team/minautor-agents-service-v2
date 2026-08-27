# -*- coding: utf-8 -*-
# routine : encart -- verification de l integrite de l encart v2
# Format tableau simple : Grade | Agent | Secteur | Raison | Heure | id | Type
import json
import os
import sys
from pathlib import Path

# P10 : racine detectee
_d = os.path.dirname(os.path.abspath(__file__))
while not os.path.isfile(os.path.join(_d, "AGENTS.md")):
    _p = os.path.dirname(_d)
    if _p == _d:
        break
    _d = _p
RACINE = Path(_d)

ACTIVITE_FILE = RACINE / "AGENTS-activite-recente-v2.md"


def _lire(path):
    try:
        return path.read_text(encoding="utf-8").replace("\r\n", "\n")
    except FileNotFoundError:
        return ""


def main():
    contenu = _lire(ACTIVITE_FILE)
    if not contenu:
        print("[ENCART] Fichier absent ou vide")
        return 0

    lignes = contenu.split("\n")
    anomalies = []
    nb_entrees = 0
    i = 0

    for ligne in lignes:
        ligne = ligne.strip()
        # Detecter les lignes de donnees (commencent par | et contiennent un emoji grade)
        if ligne.startswith("|") and any(e in ligne for e in ["\u2b50", "\U0001f535", "\U0001f7e2", "\U0001f7e1", "\U0001f7e0", "\U0001f534", "\U0001f338"]):
            # Verifier que c est bien une ligne de donnees (pas l en-tete)
            if "Grade" in ligne and "Agent" in ligne and "Secteur" in ligne:
                continue  # C est l en-tete du tableau
            parties = [p.strip() for p in ligne.split("|") if p.strip()]
            if len(parties) < 5:
                anomalies.append(f"Ligne incomplet: {len(parties)} champs au lieu de 7")
            nb_entrees += 1

    if anomalies:
        print(f"[ENCART] {len(anomalies)} anomalie(s):")
        for a in anomalies[:5]:
            print(f"  ! {a}")
        try:
            sys.path.insert(0, str(RACINE / "cerveau-projet" / "freelance" / "tools-commun" / "jarvis" / "fonctions"))
            from historique import historiser
            historiser("encart", f"{len(anomalies)} anomalie(s): " + "; ".join(anomalies[:3]), "R", session="session-freelance")
        except Exception:
            pass
        return 1
    else:
        print(f"[ENCART] OK ({nb_entrees} entrees, format tableau simple)")
        return 0


if __name__ == "__main__":
    sys.exit(main())
