# -*- coding: utf-8 -*-
"""detection.py - UNE tache : detecter les modifications du perimetre
EDITH et alerter [EDITH-RÉVEIL] via jarvis.py."""
import hashlib
import json
import os
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

_sys_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "..", "tools-commun", "os_path",
                        "fonctions")
sys.path.insert(0, _sys_dir)
from racine import trouver_racine

RACINE = Path(trouver_racine(__file__))
BASE = RACINE / "cerveau-projet" / "freelance"
WS = RACINE.parent
JARVIS_DIR = BASE / "tools-commun" / "jarvis"
JARVIS_INBOX = JARVIS_DIR / "inbox"
JARVIS_OUTBOX = JARVIS_DIR / "outbox"
OBS_DIR = BASE / "tools-commun" / "routines-server" / "observations"


def empreinte(fichier):
    h = hashlib.sha256()
    with open(fichier, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def envoyer_reveil(motif, details):
    """v1.0 : Deposer un message P1 [EDITH-RÉVEIL] dans l'inbox de stark
    ET l'outbox d'EDITH, avec un id unique (protocole 14)."""
    msg = {
        "id": str(uuid.uuid4())[:8],
        "de": "edith", "vers": "stark", "priorite": 1,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "objet": "[EDITH-RÉVEIL] " + motif[:60],
        "corps": details, "lu": False, "accuse": False, "type": "reveil",
    }
    for cible in (JARVIS_INBOX / "stark.jsonl",
                  JARVIS_OUTBOX / "edith.jsonl"):
        cible.parent.mkdir(parents=True, exist_ok=True)
        with open(cible, "a", encoding="utf-8") as f:
            f.write(json.dumps(msg, ensure_ascii=False) + "\n")
    # Tracabilite : le reveil apparait dans les activites recentes
    try:
        _fj = BASE / "tools-commun" / "jarvis" / "fonctions"
        _fo = BASE / "tools-commun" / "os_path" / "fonctions"
        for p in (_fo, _fj):
            if str(p) not in sys.path:
                sys.path.insert(0, str(p))
        from historique import historiser
        historiser("edith", f"Reveil emis: {motif[:60]}",
                   "R", session="session-freelance")
    except Exception:
        pass
    print("[EDITH] Réveil demandé :", motif)


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
    return "inconnu (modification non commitée)"


def surveiller_modifications(manifest, etat):
    """Detecter toute modification du perimetre EDITH -> reveil."""
    perimetre = manifest.get("perimetre_edith_surveille", [])
    alertes = manifest.get("seuils_alerte", {})
    if not alertes.get("modification_perimetre_edith"):
        return
    for relatif in perimetre:
        base = Path(BASE, relatif)
        for courant, dossiers, fichiers in os.walk(base):
            dossiers[:] = [d for d in dossiers if d != "__pycache__"
                           and d != "observations"]
            for f in fichiers:
                # Fichiers volatils exclus : etat des routines reecrit a
                # chaque invocation de jarvis - jamais surveillable.
                if f == "etat-executions.json":
                    continue
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


