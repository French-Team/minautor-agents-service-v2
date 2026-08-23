# -*- coding: ascii -*-
"""fonctions/localiser.py - retrouver un fichier par nom (v0.1.0)."""

import os

from racine import trouver_racine


def localiser(nom_fichier, sous_dossier="."):
    """Chercher un fichier par nom dans tout le workspace (ou un sous-
    dossier). Retourne la liste des chemins RELATIFS trouves."""
    racine = trouver_racine()
    if racine is None:
        return []
    base = os.path.join(racine, sous_dossier)
    exclus = {".git", "__pycache__", "node_modules"}
    resultats = []
    for courant, dossiers, fichiers in os.walk(base):
        dossiers[:] = [d for d in dossiers if d not in exclus]
        for f in fichiers:
            if f.lower() == nom_fichier.lower():
                resultats.append(
                    os.path.relpath(os.path.join(courant, f),
                                    racine).replace("\\", "/"))
                if len(resultats) >= 20:
                    return resultats
    return resultats
