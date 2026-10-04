# -*- coding: ascii -*-
"""fonctions/resoudre.py - chemin relatif -> absolu securise (v0.1.0)."""

import os

from racine import trouver_racine


def resoudre(chemin_relatif, racine=None):
    """Resoudre un chemin relatif a la racine du workspace.
    Retourne le chemin absolu, ou None si hors workspace / invalide."""
    if os.path.isabs(chemin_relatif):
        reel = os.path.normpath(chemin_relatif)
    else:
        if racine is None:
            racine = trouver_racine()
        if racine is None:
            return None
        reel = os.path.normpath(os.path.join(racine, chemin_relatif))
    racine_connue = racine or trouver_racine()
    if racine_connue and not reel.startswith(racine_connue):
        return None  # hors workspace : refuse
    return reel


def existe(chemin_relatif):
    """Le chemin resolu existe-t-il ?"""
    reel = resoudre(chemin_relatif)
    return reel is not None and os.path.exists(reel)
