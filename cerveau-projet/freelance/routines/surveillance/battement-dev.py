# -*- coding: ascii -*-
# routine : battement-dev -- TEMPORAIRE (dev uniquement)
# Repere visuel pendant le dev : toutes les 5 min, une citation de
# heros Marvel est historisee dans l'encart activites recentes.
# A RETIRER EN FIN DE DEV (marqueur temporaire au manifest D15) :
# Hygie pourra purger script + entree manifest.
import os
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

# P10 : racine DETECTEE en remontant jusqu'a AGENTS.md (jamais compte)
_d = os.path.dirname(os.path.abspath(__file__))
while not os.path.isfile(os.path.join(_d, "AGENTS.md")):
    _p = os.path.dirname(_d)
    if _p == _d:
        break
    _d = _p
RACINE = Path(_d)

CITATIONS_MARVEL = [
    "I am Iron Man. (Tony Stark)",
    "Je peux faire ca toute la journee. (Captain America)",
    "With great power comes great responsibility. (Spider-Man)",
    "I'm always angry. (Hulk)",
    "Wakanda forever ! (Black Panther)",
    "Je ne suis pas un heros, je fais juste mon travail. (Hawkeye)",
    "Perfectly balanced, as all things should be. (Thanos)",
    "I have nothing but time. (Loki)",
    "On ne jugera pas mon succes par mes victoires mais par mes relevailles. (Nick Fury)",
    "Dormez, Monsieur Stark, je vous garde un oeil. (Vision)",
    "Je suis inebranlable. (Thor)",
    "Le meilleur chemin est toujours le plus difficile. (Docteur Strange)",
    "C'est qui moi ? Je suis Iron Man. (Tony Stark)",
]


def main():
    citation = random.choice(CITATIONS_MARVEL)
    try:
        _fo = Path(RACINE, "cerveau-projet", "freelance", "tools-commun",
                   "os_path", "fonctions")
        _fj = RACINE / "cerveau-projet" / "freelance" / "tools-commun" / \
            "jarvis" / "fonctions"
        for p in (_fo, _fj):
            if str(p) not in sys.path:
                sys.path.insert(0, str(p))
        from historique import historiser, session_courante
        horodatage = datetime.now(timezone.utc).strftime("%H:%M")
        historiser("jarvis",
                   "[DEV-BATTEMENT %s] %s" % (horodatage, citation),
                   "R", session=session_courante())
    except Exception as e:
        print("[ROUTINE] ERREUR battement-dev : %s" % e)
        return 1
    print("[DEV-BATTEMENT] %s" % citation)
    return 0


if __name__ == "__main__":
    sys.exit(main())
