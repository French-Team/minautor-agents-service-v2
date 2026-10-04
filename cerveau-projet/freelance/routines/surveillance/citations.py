# -*- coding: utf-8 -*-
# routine : citations (ex-battement-dev, renommee 2026-08-26, decision
# utilisateur : nom propre, fini le 'dev battement' temporaire)
# Repere visuel : toutes les 5 min, une citation de heros Marvel est
# historisee dans l'encart activites recentes v2.
# SIGNAL VISUEL : la colonne Grade de l encart affiche l emoji orange
# (grade G5, le plus bas) - l emoji n est PLUS mis dans la raison (la
# colonne le porte, decision utilisateur 2026-08-26).
# TEMPORAIRE (marqueur au manifest D15) : desactivee en fin de dev quand
# cette partie ne pose plus de probleme - Hygie pourra purger script +
# entree manifest.
import os
import random
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

CITATIONS_MARVEL = [
    ("Tony Stark", "Je suis Iron Man."),
    ("Captain America", "Je peux faire ca toute la journee."),
    ("Spider-Man", "De grands pouvoirs impliquent de grandes responsabilites."),
    ("Hulk", "Je suis toujours en colere."),
    ("Black Panther", "Wakanda a jamais !"),
    ("Hawkeye", "Je ne suis pas un heros, je fais juste mon travail."),
    ("Thanos", "Un equilibre parfait, comme toute chose devrait l'etre."),
    ("Loki", "Le temps, c'est tout ce que j'ai."),
    ("Nick Fury", "On jugera mon succes non pas par mes victoires mais par mes relevees."),
    ("Vision", "Dormez, Monsieur Stark, je veille sur vous."),
    ("Thor", "Je suis inebranlable."),
    ("Docteur Strange", "Le meilleur chemin est toujours le plus difficile."),
    ("Veuve Noire", "Faites un pas en arriere, evaluez, puis avancez."),
]


def main():
    nom, phrase = random.choice(CITATIONS_MARVEL)
    try:
        _fo = Path(RACINE, "cerveau-projet", "freelance", "tools-commun",
                   "os_path", "fonctions")
        _fj = RACINE / "cerveau-projet" / "freelance" / "tools-commun" / \
            "jarvis" / "fonctions"
        for p in (_fo, _fj):
            if str(p) not in sys.path:
                sys.path.insert(0, str(p))
        from historique import historiser, session_courante
        # Raison = UNIQUEMENT 'nom -- citation' (decision utilisateur
        # 2026-08-26 : pas de libelle [CITATIONS HH:MM], pas d emoji -
        # l heure est dans la colonne Heure, la couleur dans la colonne
        # Grade).
        historiser("citations", "%s -- %s" % (nom, phrase),
                   "R", session=session_courante())
    except Exception as e:
        print("[ROUTINE] ERREUR citations : %s" % e)
        return 1
    print("%s -- %s" % (nom, phrase))
    return 0


if __name__ == "__main__":
    sys.exit(main())
