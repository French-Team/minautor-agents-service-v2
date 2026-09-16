#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bdd-lecons-matrice/fonctions/bdd_lecons_matrice.py -- Porte unique lecons.json (JSON, pas de 2e stockage)
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any


def _load(db_path: Path) -> Dict[str, Any]:
    with open(db_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(db_path: Path, data: Dict[str, Any]):
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


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
    """Ajouter une lecon, retourner son ID (L-0NN via compteur)"""
    data = _load(db_path)
    data["compteur"] = data.get("compteur", 0) + 1
    new_id = f"L-{data['compteur']:03d}"
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data.setdefault("lecons", []).append({
        "id": new_id,
        "date": date,
        "lecon": lecon,
        "tags": [t.strip() for t in tags.split(",") if t.strip()],
        "source": source,
    })
    _save(db_path, data)
    return new_id


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
