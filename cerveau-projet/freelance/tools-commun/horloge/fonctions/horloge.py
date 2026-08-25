# -*- coding: utf-8 -*-
"""fonctions/horloge.py - formats d horodatage uniques."""
from datetime import datetime, timezone


def maintenant():
    """Horodatage message : UTC ISO secondes (format JARVIS)."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")


def date_fichier():
    """Suffixe de nommage fichier : AAAAMMJJ-HHmm (conventions)."""
    return datetime.now().strftime("%Y%m%d-%H%M")


def date_tableau():
    """Date courte pour tableaux : YYYY-MM-DD."""
    return datetime.now().strftime("%Y-%m-%d")


def heure_historique():
    """Heure pour AGENTS-historique : HH:MM:SS.mmm (3 chiffres)."""
    return datetime.now().strftime("%H:%M:%S.%f")[:12]
