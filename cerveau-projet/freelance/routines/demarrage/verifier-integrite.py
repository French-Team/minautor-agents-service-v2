# -*- coding: ascii -*-
# routine : integrite (demarrage) -- verifie l'integrite du systeme v2 au
# demarrage du serveur de routines et historise le resultat sous son nom
# (decision utilisateur 2026-08-26 : les routines sont des elements
# surveilles avec LEUR propre nom/grade - rouge G4).
# Creee 2026-08-26 (les entrees verifier-integrite/detecter-orphelins du
# manifest etaient mortes : scripts inexistants).
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


def verifier():
    """Retourne la liste des anomalies (vide si tout va bien)."""
    anomalies = []
    freelance = RACINE / "cerveau-projet" / "freelance"
    # 1. manifest JSON valide
    manifest = freelance / "routines" / "manifest.json"
    try:
        json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        anomalies.append("manifest illisible: %s" % e)
    # 2. fichiers racines de suivi presents
    for f in ("AGENTS.md", "AGENTS-activite-recente-v2.md",
              "AGENTS-historique-v2.md"):
        if not (RACINE / f).is_file():
            anomalies.append("%s absent" % f)
    # 3. grades-v2.json valide (colonne Grade de l encart)
    grades = (freelance / "tools-commun" / "grades" / "grades-v2.json")
    try:
        json.loads(grades.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        anomalies.append("grades illisible: %s" % e)
    # 4. scripts de surveillance declares existent
    try:
        m = json.loads(manifest.read_text(encoding="utf-8"))
        base = freelance / "routines"
        for r in m.get("routines_surveillance", []):
            if not (base / r.get("script", "")).is_file():
                anomalies.append("script manquant: %s" % r.get("script"))
    except Exception:
        pass  # deja signale en 1
    return anomalies


def main():
    try:
        anomalies = verifier()
        _fo = RACINE / "cerveau-projet" / "freelance" / "tools-commun" / \
            "os_path" / "fonctions"
        _fj = RACINE / "cerveau-projet" / "freelance" / "tools-commun" / \
            "jarvis" / "fonctions"
        for p in (_fo, _fj):
            if str(p) not in sys.path:
                sys.path.insert(0, str(p))
        from historique import historiser
        if anomalies:
            raison = "%d anomalie(s) d'integrite: %s" % (
                len(anomalies), anomalies[0][:60])
        else:
            raison = "Integrite v2 OK (manifest, fichiers, grades, scripts)"
        historiser("integrite", raison, "R", session="session-freelance")
        print("[INTEGRITE] %s" % raison)
    except Exception as e:
        print("[ROUTINE] ERREUR integrite : %s" % e)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
