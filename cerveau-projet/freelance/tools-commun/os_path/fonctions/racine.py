# -*- coding: ascii -*-
"""fonctions/racine.py - DETECTION de la racine du workspace (v0.1.0).

Regle : on ne COMPTE jamais les niveaux ("../.."). On CHERCHE un point de
reperage connu (AGENTS.md a la racine) en remontant depuis le fichier
appelant. La detection ne se trompe pas : elle verifie.
"""

import os

_MARQUEUR = "AGENTS.md"
_cache = {}


def trouver_racine(depuis=None):
    """Remonter depuis `depuis` (defaut: ce fichier) jusqu'a trouver le
    marqueur de racine. Retourne le chemin absolu ou None."""
    if depuis is None:
        depuis = __file__
    courant = os.path.dirname(os.path.abspath(depuis))
    if courant in _cache:
        return _cache[courant]
    while True:
        if os.path.isfile(os.path.join(courant, _MARQUEUR)):
            _cache[courant] = courant
            return courant
        parent = os.path.dirname(courant)
        if parent == courant:
            return None  # atteint la racine du disque sans trouver
        courant = parent
