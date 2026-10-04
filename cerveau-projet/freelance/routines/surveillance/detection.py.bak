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
# la racine DETECTEE EST la racine du workspace (pas son parent !)
WS = str(RACINE)
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
    """v1.2 (decision utilisateur 2026-08-26) : les routines d'EDITH ne
    distribuent PLUS le travail aux autres agents - elles demandent a
    JARVIS d'ACTIVER EDITH pour qu'elle fasse SON travail (protocole 18 :
    EDITH incarnee rapporte les 4 W). Deposer un message P1
    [EDITH-RÉVEIL] dans le hub (inbox/jarvis.jsonl) UNIQUEMENT :
    - JARVIS lit la demande et active EDITH (jamais stark/vision en
      direct - leur information passe par le rapport d'EDITH).
    + outbox d'EDITH (trace cote expediteur, protocole 14)."""
    base = {
        "de": "edith", "priorite": 1,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "objet": "[EDITH-RÉVEIL] demande activation EDITH : " + motif[:40],
        "corps": ("DEMANDE D'ACTIVATION EDITH (protocole 18). EDITH doit "
                  "etre activee pour analyser et rapporter les 4 W.\n"
                  + details),
        "lu": False, "accuse": False, "type": "reveil",
    }
    for destinataire in ("jarvis",):
        msg = dict(base)
        msg["id"] = str(uuid.uuid4())[:8]
        msg["vers"] = destinataire
        # outbox/edith = TRACE cote expediteur (jamais a lire) :
        # marque lu des la creation pour ne pas simuler un bloquant.
        msg_out = dict(msg)
        msg_out["lu"] = True
        msg_out["accuse"] = True
        for cible in (JARVIS_INBOX / ("%s.jsonl" % destinataire),
                      JARVIS_OUTBOX / "edith.jsonl"):
            cible.parent.mkdir(parents=True, exist_ok=True)
            ecrit = msg if "inbox" in str(cible) else msg_out
            with open(cible, "a", encoding="utf-8") as f:
                f.write(json.dumps(ecrit, ensure_ascii=False) + "\n")
    # Tracabilite : le reveil apparait dans les activites recentes
    try:
        _fj = BASE / "tools-commun" / "jarvis" / "fonctions"
        _fo = BASE / "tools-commun" / "os_path" / "fonctions"
        for p in (_fo, _fj):
            if str(p) not in sys.path:
                sys.path.insert(0, str(p))
        from historique import historiser
        # trace sous le nom de la routine vigie (decision utilisateur
        # 2026-08-26 : les routines sont des elements surveilles avec
        # LEUR propre nom/grade - la couleur rouge G4 s'affiche).
        historiser("vigie", f"Perimetre modifie: {motif[:60]}",
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


