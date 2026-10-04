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
     (quoi/comment/quand ; qui si git le sait) -> P1 [EDITH-REVEIL]
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

# P10 : racine DETECTEE en remontant jusqu'a AGENTS.md (jamais compte)
_d = os.path.dirname(os.path.abspath(__file__))
while not os.path.isfile(os.path.join(_d, "AGENTS.md")):
    _p = os.path.dirname(_d)
    if _p == _d:
        break
    _d = _p
RACINE = Path(_d)
BASE = RACINE / "cerveau-projet" / "freelance"
WS = RACINE.parent
SERVEUR_DIR = Path(__file__).parent
OBS_DIR = SERVEUR_DIR / "observations"
JARVIS = Path(RACINE, "freelance", "tools-commun", "jarvis", "jarvis.py")

VERSION = "0.2.0"


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
        flags_git = subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0
        p = subprocess.run(
            ["git", "log", "-1", "--format=%an %ad", "--", fichier],
            capture_output=True, text=True, cwd=str(WS), timeout=10,
            creationflags=flags_git)
        if p.returncode == 0 and p.stdout.strip():
            return p.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        pass
    return "inconnu (modification non commitee)"


def envoyer_reveil(motif, details):
    msg = {
        "id": str(uuid.uuid4())[:8],
        "de": "edith", "vers": "stark", "priorite": 1,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "objet": "[EDITH-REVEIL] " + motif[:60],
        "corps": details, "lu": False, "accuse": False, "type": "reveil",
    }
    for cible in ("inbox/stark.jsonl", "outbox/edith.jsonl"):
        chemin = Path(RACINE, "freelance", "tools-commun", "jarvis", cible)
        with open(chemin, "a", encoding="utf-8") as f:
            f.write(json.dumps(msg, ensure_ascii=False) + "\n")
    print("[EDITH-SERVER] Reveil demande :", motif)


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
                    # v0.3.0 (protocole 18) : validation post-modification
                    try:
                        import validations
                        violations = validations.valider(reel)
                    except Exception as err:
                        violations = [{"regle": "ERREUR",
                                       "detail": str(err)[:80]}]
                    details = (
                        "QUI: %s | QUOI: %s modifie | "
                        "COMMENT: changement d'empreinte SHA-256 | "
                        "QUAND: %s" % (qui, rel_ws,
                                       datetime.now(timezone.utc).isoformat()))
                    if violations:
                        details += "\nVIOLATIONS SUSPECTEES : " + "; ".join(
                            v["regle"] + " - " + v["detail"]
                            for v in violations)
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


def _tick(manifest, etat, dernieres_executions):
    """UN tour de boucle : dispatch D15 + surveillance du perimetre."""
    maintenant = time.time()
    for routine in manifest.get("routines_surveillance", []):
        if not routine.get("actif", True):
            continue
        nom = routine.get("nom")
        script = BASE / "routines" / routine.get("script", "")
        intervalle = routine.get("intervalles_secondes",
                                 manifest.get("intervalle_boucle_secondes",
                                              600))
        dernier = dernieres_executions.get(nom, 0)
        if maintenant - dernier < intervalle:
            continue
        dernieres_executions[nom] = maintenant
        try:
            # v0.2.2 : CREATE_NO_WINDOW - pas de fenetre cmd qui clignote
            flags_sans_fenetre = 0
            if hasattr(subprocess, "CREATE_NO_WINDOW"):
                flags_sans_fenetre = subprocess.CREATE_NO_WINDOW
            p = subprocess.run(
                [sys.executable, str(script)],
                capture_output=True, text=True, timeout=120,
                creationflags=flags_sans_fenetre)
            print(f"[EDITH-SERVER] routine {nom} executee (rc={p.returncode})")
            for ligne in p.stdout.splitlines():
                if ligne.strip():
                    print(f"  {ligne.strip()[:100]}")
        except (OSError, subprocess.TimeoutExpired) as e:
            print(f"[EDITH-SERVER] ERREUR routine {nom}: {e}")
    surveiller_modifications(manifest, etat)


def boucle(manifest, une_passe=False):
    etat = {}
    fichier_etat = SERVEUR_DIR / "observations" / "etat-empreintes.json"
    OBS_DIR.mkdir(exist_ok=True)
    if fichier_etat.exists():
        try:
            etat = json.loads(fichier_etat.read_text(encoding="utf-8"))
        except ValueError:
            etat = {}
    dernieres_executions = {}
    intervalle_defaut = manifest.get("intervalle_boucle_secondes", 600)
    print("[EDITH-SERVER] v%s demarre (intervalle %ss)"
          % (VERSION, intervalle_defaut))
    while True:
        try:
            _tick(manifest, etat, dernieres_executions)
            fichier_etat.write_text(json.dumps(etat, ensure_ascii=False),
                                    encoding="utf-8")
        except Exception as e:
            # v0.2.1 : un crash de routine ne tue JAMAIS le serveur
            crash = OBS_DIR / "crash.log"
            with open(crash, "a", encoding="utf-8") as f:
                f.write(str(datetime.now(timezone.utc)) + " "
                        + repr(e) + "\n")
        if une_passe:
            print("[EDITH-SERVER] une passe terminee.")
            return
        time.sleep(1)  # tick fin : les compteurs par routine font le reste


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
