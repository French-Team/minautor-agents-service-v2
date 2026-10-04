# -*- coding: utf-8 -*-
"""fonctions/lire-ecrire.py - D4 mecanique : lire/ecrire/detecter."""
import os
import sys

_sys_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "..", "os_path", "fonctions")
sys.path.insert(0, _sys_dir)
from racine import trouver_racine

RACINE = trouver_racine(__file__)


def lire(chemin_relatif):
    """Lire en UTF-8 (D4 v2). Retourne None si absent."""
    reel = os.path.join(RACINE, chemin_relatif)
    if not os.path.isfile(reel):
        return None
    return open(reel, encoding="utf-8").read()


def ecrire(chemin_relatif, contenu):
    """Ecrire en UTF-8 (D4 v2)."""
    reel = os.path.join(RACINE, chemin_relatif)
    open(reel, "w", encoding="utf-8", newline="").write(contenu)
    return reel


def detecter(chemin_relatif):
    """Detecter : encodage probable, non-ASCII, CRLF, header coding."""
    contenu = lire(chemin_relatif)
    if contenu is None:
        return {"erreur": "introuvable"}
    brut = open(os.path.join(RACINE, chemin_relatif), "rb").read()
    return {
        "non_ascii": sum(1 for c in contenu if ord(c) > 127),
        "crlf": brut.count(b"\r\n"),
        "header_coding": "coding:" in contenu[:200].lower(),
        "octets": len(brut),
    }
