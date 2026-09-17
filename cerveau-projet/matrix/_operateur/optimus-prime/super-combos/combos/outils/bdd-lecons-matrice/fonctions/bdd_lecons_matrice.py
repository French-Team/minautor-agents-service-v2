#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bdd-lecons-matrice/fonctions/bdd_lecons_matrice.py -- Porte unique lecons.json (JSON, pas de 2e stockage)
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any


def _load(db_path: Path) -> Dict[str, Any]:
    with open(db_path, "r", encoding="utf-8") as f:
        return json.load(f)


# Lecons SANS tag : la porte proprietaire exige au moins un tag. Un tag par
# defaut NOMME vaut mieux qu'un refus : la lecon est rangee, jamais perdue.
TAGS_DEFAUT = "auto-evolution"


def _porte_proprietaire(db_path: Path) -> Path:
    """Le chemin de la PORTE PROPRIETAIRE de cette BDD (matrice/data/outils/bdd-lecons).

    Pourquoi DELEGUER au lieu d'ecrire : `lecons.json` est une BDD du REGISTRE,
    surveillee par son empreinte `.sha256`. Deux fabriques d'ecriture = deux
    verites, et la fabrique locale etait CRLF (Windows), non atomique, en
    `ensure_ascii=False` (des accents DANS une BDD scellee) et SANS resceller
    l'empreinte : mesure MO-135 = 1382 CRLF / 0 LF, 2 octets non-ASCII, empreinte
    fausse, deux maillons de la non-regression KO (chapitres, observations).
    Un fichier = un ecrivain : l'ecrivain, c'est la porte proprietaire, qui force
    LF (L-001), l'ASCII, l'atomicite ET l'empreinte.
    """
    return db_path.parent / "outils" / "bdd-lecons" / "main.py"


def init_db(db_path: Path):
    """Verifie que lecons.json existe (pas de creation : porte unique sur fichier existant)"""
    if not db_path.exists():
        raise FileNotFoundError(f"BDD lecons introuvable: {db_path}")


def ajouter_lecon(
    db_path: Path,
    lecon: str,
    tags: str = "",
    source: str = "auto-evolution",
) -> str:
    """Ajouter une lecon PAR LA PORTE PROPRIETAIRE, et retourner son ID (L-0NN).

    La fabrique d'ecriture n'est PAS ici : elle appartient a la porte qui POS-
    SEDE la BDD. Cette porte ORCHESTRE -- elle lit les arguments, appelle le
    proprietaire, rend l'id -- et ne touche jamais un octet elle-meme.
    """
    porte = _porte_proprietaire(db_path)
    if not porte.is_file():
        raise FileNotFoundError("Porte proprietaire introuvable : " + str(porte))
    resultat = subprocess.run(
        [sys.executable, str(porte), "ajouter",
         "--lecon", lecon, "--tags", tags or TAGS_DEFAUT, "--source", source],
        capture_output=True, text=True, encoding="utf-8",
    )
    if resultat.returncode != 0:
        raise RuntimeError(
            "La porte proprietaire a refuse (code " + str(resultat.returncode) + ") : "
            + ((resultat.stdout or "") + (resultat.stderr or "")).strip()
        )
    return _load(db_path)["lecons"][-1]["id"]


def lister_lecons(db_path: Path, limite: int = 10) -> List[Dict[str, Any]]:
    """Lister les dernieres lecons"""
    data = _load(db_path)
    return data.get("lecons", [])[-limite:]


def chercher_lecons(
    db_path: Path,
    mot_cle: Optional[str] = None,
    tag: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Chercher par mot-cle (dans lecon) et/ou tag"""
    data = _load(db_path)
    res = []
    for l in data.get("lecons", []):
        ok = True
        if mot_cle and mot_cle.lower() not in l.get("lecon", "").lower():
            ok = False
        if tag and tag.lower() not in [t.lower() for t in l.get("tags", [])]:
            ok = False
        if ok:
            res.append(l)
    return res
