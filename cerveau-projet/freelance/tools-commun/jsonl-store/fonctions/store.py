# -*- coding: utf-8 -*-
"""fonctions/store.py - UNE implementation JSONL testee."""
import json
import os
import sys

_sys_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "..", "os_path", "fonctions")
sys.path.insert(0, _sys_dir)
from racine import trouver_racine

RACINE = trouver_racine(__file__)


def _chemin(chemin_relatif):
    if os.path.isabs(chemin_relatif):
        return chemin_relatif
    return os.path.join(RACINE, chemin_relatif)


def lire(chemin_relatif):
    """Lire un JSONL -> liste de dicts (lignes invalides ignorees)."""
    reel = _chemin(chemin_relatif)
    if not os.path.isfile(reel):
        return []
    resultats = []
    for l in open(reel, encoding="utf-8"):
        l = l.strip()
        if not l:
            continue
        try:
            resultats.append(json.loads(l))
        except ValueError:
            continue
    return resultats


def ajouter(chemin_relatif, dictionnaire):
    """Append une ligne JSON."""
    with open(_chemin(chemin_relatif), "a", encoding="utf-8") as f:
        f.write(json.dumps(dictionnaire, ensure_ascii=False) + "\n")


def reecrire(chemin_relatif, liste):
    """Reecrire tout le fichier depuis une liste de dicts."""
    with open(_chemin(chemin_relatif), "w", encoding="utf-8") as f:
        for d in liste:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")


def filtrer(chemin_relatif, **critères):
    """Filtrer les entrees par egalite de champs."""
    resultats = lire(chemin_relatif)
    for cle, valeur in critères.items():
        resultats = [e for e in resultats if e.get(cle) == valeur]
    return resultats
