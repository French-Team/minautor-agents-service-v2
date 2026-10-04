#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
defcon-server.py -- Serveur MCP DEDIE a l'etat DEFCON (protocole 15).

Isole volontairement de jarvis-server : la gestion d'urgence ne doit
jamais dependre de (ni surcharger) l'intercom.

Demarre par jarvis (server) a l'entree en DEFCON 5.
Stoppe par jarvis (server) au retour en DEFCON 2 (fin du cycle).

Outils MCP :
  etat_defcon      - niveau courant + journal recent
  changer_defcon   - descente legale 5->4->3->2 avec commentaire

Proprietaire : Vision (perimetre JARVIS)
Version : 0.1.0
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from fastmcp import FastMCP

# HARNAIS (PROTOCOLE 21) : l outil s auto-verifie au demarrage.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "harnais", "fonctions"))
try:
    from harnais import verifier_outil
except ImportError:
    verifier_outil = None

mcp = FastMCP("defcon", instructions=(
    "DEFCON - echelle d'urgence v2. 5=arret total, 4=validation des "
    "reparations, 3=reprise surveillee, 2=reprise totale."))

DEFCON_FILE = Path(__file__).parent.parent / "jarvis" / "files" / "defcon.jsonl"

ECHELLE = {
    5: "ARRET TOTAL",
    4: "VALIDATION DES REPARATIONS",
    3: "REPRISE SURVEILLEE",
    2: "REPRISE TOTALE",
}


def _journal():
    if not DEFCON_FILE.exists():
        return []
    resultats = []
    for l in DEFCON_FILE.read_text(encoding="utf-8").splitlines():
        if not l.strip():
            continue
        try:
            resultats.append(json.loads(l))
        except ValueError:
            continue
    return resultats


@mcp.tool()
def etat_defcon() -> str:
    """Niveau DEFCON courant + journal recent."""
    courant = None
    for e in _journal():
        if e.get("niveau"):
            courant = e["niveau"]
    if courant is None:
        return "[DEFCON] Aucun etat DEFCON (fonctionnement normal)."
    lignes = [f"[DEFCON] Niveau {courant} : {ECHELLE[courant]}", "  Journal :"]
    for e in _journal()[-5:]:
        niv = e.get("niveau", 5 if e.get("missions_gelees") is not None else "?")
        lignes.append(f"    {e.get('date')} - niveau {niv} - "
                      f"{str(e.get('signification', e.get('raison', '')))[:60]}")
    return "\n".join(lignes)


@mcp.tool()
def changer_defcon(nouveau_niveau: int, commentaire: str = "") -> str:
    """Descendre d'un niveau (transitions legales uniquement : 5->4->3->2)."""
    if nouveau_niveau not in ECHELLE:
        return f"ERREUR: niveau invalide '{nouveau_niveau}'"
    courant = None
    for e in _journal():
        if e.get("niveau"):
            courant = e["niveau"]
    if courant is None:
        return "ERREUR: aucun DEFCON 5 declare : rien a faire"
    attendu = {5: 4, 4: 3, 3: 2}.get(courant)
    if nouveau_niveau != attendu:
        return (f"ERREUR: transition illegale {courant}->{nouveau_niveau}. "
                f"Seule transition legale depuis DEFCON {courant} : DEFCON {attendu}")
    entree = {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "niveau": nouveau_niveau,
        "signification": ECHELLE[nouveau_niveau],
        "commentaire": commentaire,
        "par": "stark",
    }
    with open(DEFCON_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entree, ensure_ascii=False) + "\n")
    return (f"[DEFCON] Niveau {nouveau_niveau} : {ECHELLE[nouveau_niveau]}\n"
            f"  {commentaire}")


if __name__ == "__main__":
    if verifier_outil is not None:
        verifier_outil(os.path.dirname(os.path.abspath(__file__)),
                       agent="defcon")
    mcp.run()
