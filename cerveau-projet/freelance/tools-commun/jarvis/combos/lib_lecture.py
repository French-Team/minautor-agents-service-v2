#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: jarvis
#   commun: false
"""
lib-lecture.py

Fondation LECTURE SEULE des combos JARVIS (v0.1.0 - etape 0 du plan).
Tous les chemins sont relatifs a la racine du workspace et resolus en
lecture seule : les combos repondent, ils ne modifient jamais.

Fonctions :
  lire_texte(chemin_relatif)      -> str ou None
  lire_jsonl(chemin_relatif)     -> liste de dicts (lignes valides)
  dernieres_lignes(chemin, n)    -> n dernieres lignes non vides

Proprietaire : Vision (perimetre JARVIS)
Version : 0.1.0
"""

import json
import os

VERSION = "0.1.1"

import sys as _sys
_sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "os_path", "fonctions"))
from racine import trouver_racine as _trouver_racine

RACINE = _trouver_racine(__file__)


def chemin_reel(chemin_relatif):
    """Resoudre un chemin relatif a la racine, hors du workspace = refuse."""
    reel = os.path.abspath(os.path.join(RACINE, chemin_relatif))
    if not reel.startswith(RACINE):
        return None
    return reel


def lire_texte(chemin_relatif):
    """Lire un fichier texte (UTF-8). None si absent/hors perimetre."""
    reel = chemin_reel(chemin_relatif)
    if not reel or not os.path.isfile(reel):
        return None
    try:
        with open(reel, "r", encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def lire_jsonl(chemin_relatif):
    """Lire un JSONL -> liste de dicts (lignes invalides ignorees)."""
    contenu = lire_texte(chemin_relatif)
    if contenu is None:
        return []
    resultats = []
    for ligne in contenu.splitlines():
        ligne = ligne.strip()
        if not ligne:
            continue
        try:
            resultats.append(json.loads(ligne))
        except ValueError:
            continue
    return resultats


def dernieres_lignes(chemin_relatif, n=20):
    """Les n dernieres lignes non vides d'un fichier."""
    contenu = lire_texte(chemin_relatif)
    if contenu is None:
        return []
    lignes = [l.rstrip() for l in contenu.splitlines() if l.strip()]
    return lignes[-n:]
