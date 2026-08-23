#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
routines-server.py -- Mini serveur de routines EDITH (H24, lecture seule,
sans LLM). Protocole 16.

Modes :
  --une-passe    execute une seule boucle (pour tests reels)
  --boucle [s]   boucle continue (defaut: intervalle du manifest)

Ce que fait chaque boucle :
  1. routines surveillance actives du manifest
  2. detection de modification du perimetre EDITH -> rapport forensique
     (quoi/comment/quand ; qui si git le sait) -> P1 [EDITH-RÉVEIL]
  3. observations ecrites en JSONL

LIMITES HONNETES : le "qui" n'est fiable que si git trace l'auteur ;
une modification non commitee est rapportee avec qui=inconnu.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone

from pathlib import Path

VERSION = "0.1.0"

BASE = Path(__file__).parent.parent.parent          # freelance/
RACINE = BASE.parent                                 # cerveau-projet/
WS = RACINE.parent                                   # workspace root
SERVEUR_DIR = Path(__file__).parent
OBS_DIR = SERVEUR_DIR / "observations"
JARVIS = Path(RACINE, "freelance", "tools-commun", "jarvis", "jarvis.py")


def charger_manifest():
    chemin = BASE / "routines" / "manifest.json"
    return json.loads(chemin.read_text(encoding="utf-8"))


def empreinte(fichier):
    h = hashlib.sha256()
    with open(fichier, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def qui_par_git(fichier):
    """Dernier auteur ayant commite ce fichier (inconnu sinon)."""
    try:
        p = subprocess.run(
            ["git", "log", "-1", "--format=%an %ad", "--", fichier],
            capture_output=True, text=True, cwd=str(WS), timeout=10)
        if p.returncode == 0 and p.stdout.strip():
            return p.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        pass
    return "inconnu (modification non commitée)"


def envoyer_reveil(motif, details):
    msg = {
        "de": "edith", "vers": "stark", "priorite": 1,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "objet": "[EDITH-RÉVEIL] " + motif[:60],
        "corps": details, "lu": False, "accuse": False, "type": "reveil",
    }
    for cible in ("inbox/stark.jsonl", "outbox/edith.jsonl"):
        chemin = Path(RACINE, "freelance", "tools-commun", "jarvis", cible)
        with open(chemin, "a", encoding="utf-8") as f:
            f.write(json.dumps(msg, ensure_ascii=False) + "\n")
    print("[EDITH-SERVER] Réveil demandé :", motif)


def surveiller_modifications(manifest, etat):
    """Detecter toute modification du perimetre EDITH -> reveil."""
    perimetre = manifest.get("perimetre_edith_surveille", [])
    alertes = manifest.get("seuils_alerte", {})
    if not alertes.get("modification_perimetre_edith"):
        return
    for relatif in perimetre:
        base = Path(RACINE, "freelance", relatif)
        for courant, dossiers, fichiers in os.walk(base):
            dossiers[:] = [d for d in dossiers if d != "__pycache__"
                           and d != "observations"]
            for f in fichiers:
                reel = os.path.join(courant, f)
                cle = str(reel)
                empreinte_actuelle = empreinte(reel)
                if etat.get(cle) and etat[cle] != empreinte_actuelle:
                    rel_ws = os.path.relpath(reel, WS).replace("\\", "/")
                    qui = qui_par_git(rel_ws)
                    details = (
                        "QUI: %s | QUOI: %s modifie | "
                        "COMMENT: changement d'empreinte SHA-256 | "
                        "QUAND: %s" % (qui, rel_ws,
                                       datetime.now(timezone.utc).isoformat()))
                    OBS_DIR.mkdir(exist_ok=True)
                    obs = OBS_DIR / ("observation-modif-%s.md"
                                     % datetime.now().strftime("%Y%m%d-%H%M%S"))
                    obs.write_text("# Observation - modification detectee\n\n"
                                   + details + "\n", encoding="utf-8")
                    envoyer_reveil("perimetre EDIT modifie : " + rel_ws,
                                   details + "\nRAPPORT: " + str(obs))
                etat[cle] = empreinte_actuelle


def surveiller_flux_jarvis(manifest):
    seuil = manifest.get("seuils_alerte", {}).get("p1_non_acquitte")
    if not seuil:
        return
    inbox_dir = Path(RACINE, "freelance", "tools-commun", "jarvis", "inbox")
    for f in inbox_dir.glob("*.jsonl"):
        for ligne in f.read_text(encoding="utf-8").splitlines():
            if not ligne.strip():
                continue
            try:
                m = json.loads(ligne)
            except ValueError:
                continue
            if not m.get("lu") and m.get("priorite") == 1:
                print("[EDITH-SERVER] ALERTE : P1 non-acquitte chez",
                      f.stem, "-", m.get("objet", "")[:50])


def boucle(manifest, une_passe=False):
    etat = {}
    fichier_etat = SERVEUR_DIR / "observations" / "etat-empreintes.json"
    OBS_DIR.mkdir(exist_ok=True)
    if fichier_etat.exists():
        try:
            etat = json.loads(fichier_etat.read_text(encoding="utf-8"))
        except ValueError:
            etat = {}
    intervalle = manifest.get("intervalle_boucle_secondes", 600)
    print("[EDITH-SERVER] v%s demarre (intervalle %ss)"
          % (VERSION, intervalle))
    while True:
        surveiller_modifications(manifest, etat)
        surveiller_flux_jarvis(manifest)
        fichier_etat.write_text(json.dumps(etat, ensure_ascii=False),
                                encoding="utf-8")
        if une_passe:
            print("[EDITH-SERVER] une passe terminee.")
            return
        time.sleep(intervalle)


def main():
    parser = argparse.ArgumentParser(description="Serveur de routines EDITH")
    parser.add_argument("--une-passe", action="store_true")
    parser.add_argument("--boucle", nargs="?", const=0, type=int)
    args = parser.parse_args()
    manifest = charger_manifest()
    if args.une_passe:
        boucle(manifest, une_passe=True)
        return 0
    if args.boucle is not None and args.boucle > 0:
        manifest["intervalle_boucle_secondes"] = args.boucle
    boucle(manifest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
