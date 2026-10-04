#!/usr/bin/env python3
"""
JARVIS -- Serveur MCP pour l'equipe Freelance (v2)
Hub central de communication, activation et coordination.

Lancement:
    python jarvis-server.py                    # Stdio (local)
    python jarvis-server.py --transport http   # HTTP (distant)
"""

import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fastmcp import FastMCP

# --- Configuration ---

JARVIS_DIR = Path(__file__).parent
INBOX_DIR = JARVIS_DIR / "inbox"
OUTBOX_DIR = JARVIS_DIR / "outbox"
HISTORIQUE_DIR = JARVIS_DIR / "historique"

INBOX_DIR.mkdir(exist_ok=True)
OUTBOX_DIR.mkdir(exist_ok=True)
HISTORIQUE_DIR.mkdir(exist_ok=True)

# v0.7.0 : agents lus depuis jarvis-data.json (D15, parite avec jarvis.py)
def _charger_agents():
    chemin = Path(__file__).parent / "jarvis-data.json"
    try:
        donnees = json.loads(chemin.read_text(encoding="utf-8"))["agents"]
        return {a["nom"] for a in donnees if isinstance(a, dict) and "nom" in a}
    except (OSError, ValueError, KeyError):
        # fallback ASSUME (valeur_en_dur signalee) : si jarvis-data.json
        # est illisible, un set vide rendrait le serveur muet ; on garde
        # un plancher minimal en attendant la reparation du data file.
        return {"stark", "shuri", "forge", "rogers", "jarvis"}  # fallback assume

AGENTS_VALIDES = _charger_agents()
FILES_DIR = Path(__file__).parent / "files"
PRIORITE_BLOQUANTE = 1

import sys as _sys
_sys.path.insert(0, str(Path(__file__).parent / 'serveur'))
import logique_files as _files
import logique_messages as _msg
import logique_activations as _act

# HARNAIS (PROTOCOLE 21) : l outil s auto-verifie au demarrage.
_sys.path.insert(0, str(Path(__file__).parent.parent / "harnais" / "fonctions"))
try:
    from harnais import verifier_outil
except ImportError:
    verifier_outil = None

# --- v0.11.0 : l'HORLOGE vit avec le serveur (decision utilisateur
# 2026-08-24) - CHAQUE routine possede SON PROPRE tic (constructeur +
# decorateur dans horloge/fonctions/tic.py), avec un decalage initial
# pour desenlever les declenchements. Intervalles lus du manifest (D15).

def _demarrer_horloge():
    outils = JARVIS_DIR.parent                      # tools-commun/
    _sys.path.insert(0, str(outils / "horloge" / "fonctions"))
    _sys.path.insert(0, str(JARVIS_DIR / "fonctions"))
    try:
        from tic import construire_tic, arreter_tous
        from routines import infos_routines, executer_routine
        journal = outils / "horloge" / "signaux.jsonl"
        tics = []
        rang = 0
        for nom, _, intervalle, actif in infos_routines():
            if not actif:
                continue
            # decalage : 15 s de plus par routine -> moments differents
            tics.append(construire_tic(
                intervalle,
                lambda n=nom: executer_routine(n),
                nom=f"horloge-{nom}",
                journal=journal,
                decalage=rang * 15))
            rang += 1
        return tics
    except Exception as e:
        print(f"[JARVIS-SERVER] horloge non demarree: {e}")
        return []

_TICS_HORLOGE = _demarrer_horloge()

# --- Serveur MCP ---

mcp = FastMCP("jarvis", instructions="JARVIS - Hub de communication et coordination pour l'equipe freelance v2.")

# --- Fonctions internes ---

def _inbox(agent: str) -> Path:
    return INBOX_DIR / f"{agent}.jsonl"

def _outbox(agent: str) -> Path:
    return OUTBOX_DIR / f"{agent}.jsonl"

def _lire_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    messages = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    messages.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return messages

def _ecrire_jsonl(path: Path, messages: list[dict]):
    with open(path, "w", encoding="utf-8") as f:
        for msg in messages:
            f.write(json.dumps(msg, ensure_ascii=False) + "\n")

def _ajouter_message(path: Path, message: dict):
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(message, ensure_ascii=False) + "\n")

def _historiser(action: str, agent: str, details: str):
    """Enregistrer une action dans l'historique."""
    entree = {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "action": action,
        "agent": agent,
        "details": details,
    }
    fichier = HISTORIQUE_DIR / "historique.jsonl"
    _ajouter_message(fichier, entree)

# --- Tools MCP ---

@mcp.tool()
def envoyer_message(de: str, vers: str, priorite: int = 3, objet: str = "", corps: str = "") -> str:
    """Envoyer un message entre agents via JARVIS."""
    return _msg.envoyer_message(de, vers, priorite, objet, corps,
                                AGENTS_VALIDES,
                                lambda a, x, d: _historiser(a, x, d))


@mcp.tool()
def recu_messages(agent: str) -> str:
    """v0.7.0 (fluidite) : lire + acquitter TOUT en un seul appel."""
    return _msg.recu_messages(agent, AGENTS_VALIDES)


@mcp.tool()
def lire_messages(agent: str, tous: bool = False) -> str:
    """Lire les messages en attente d'un agent (auto-accuse P3-P5)."""
    return _msg.lire_messages(agent, tous, AGENTS_VALIDES, PRIORITE_BLOQUANTE)


@mcp.tool()
def acquitter_message(agent: str, id_message: str) -> str:
    """Acquitter un message (marquer lu + accuse)."""
    return _msg.acquitter_message(agent, id_message, AGENTS_VALIDES,
                                  lambda a, x, d: _historiser(a, x, d))


@mcp.tool()
def activer_agent(agent: str, mission: str, session: str = "", de: str = "jarvis") -> str:
    """Activer un agent via JARVIS (message P1 + incarnation + livraison directe)."""
    sortie = _act.activer_agent(agent, mission, session, de, AGENTS_VALIDES,
                                PRIORITE_BLOQUANTE)
    _historiser("activer", de, f"Activation de {agent}: {mission[:50]}...")
    return sortie


# --- v0.9.0 (protocole 14) : la logique files vit dans serveur/logique_files.py ---

@mcp.tool()
def mettre_en_attente(mission: str, contexte: str = "", niveau: str = "attente", agent: str = "") -> str:
    """v0.9.0 (protocole 13 v2) : placer une mission selon le declencheur.
    niveau: attente (EN_ATTENTE) / attention (SUIVANTE en file-asap) /
    urgent (PRIORITAIRE en file-attente)."""
    return _files.mettre_en_attente(mission, contexte, niveau, agent)


@mcp.tool()
def stop_dev(raison: str) -> str:
    """v0.9.0 ([stop] DEFCON 5) : arret complet du dev, gel de toutes les
    missions en files. Reprendre exige decision explicite de l'utilisateur."""
    sortie = _files.stop_dev(raison)
    _historiser("stop", "jarvis", f"DEFCON 5 - arret du dev: {raison[:50]}")
    return sortie


@mcp.tool()
def lister_files() -> str:
    """v0.9.0 : lister les files d'attente (file-attente + file-asap)."""
    return _files.lister_files()


@mcp.tool()
def reprendre_mission(file: str = "file-attente") -> str:
    """v0.9.0 : depiler la mission la plus prioritaire et retourner son
    contexte de reprise (statut passe a REPRISE).
    Ordre : PRIORITAIRE > SUIVANTE > EN_ATTENTE/PREPAREE."""
    sortie = _files.reprendre_mission(file)
    _historiser("file", "jarvis", f"Reprise depuis {file}")
    return sortie


@mcp.tool()
def status_equipe() -> str:
    """
    Tableau de bord de l'equipe freelance.

    Returns:
        Etat de chaque agent
    """
    result = ["=== STATUS DE L'EQUIPE ===", ""]

    for agent in AGENTS_VALIDES:
        messages = _lire_jsonl(_inbox(agent))
        non_lus = [m for m in messages if not m.get("lu", False)]
        bloquants = [m for m in non_lus if m.get("priorite", 5) == PRIORITE_BLOQUANTE]

        if bloquants:
            etat = "BLOQUE"
        elif non_lus:
            etat = "EN ATTENTE"
        else:
            etat = "INACTIF"

        dernier = non_lus[-1]["date"] if non_lus else "aucun"

        result.append(f"  {agent:10s} | {etat:12s} | {len(non_lus)} message(s) en attente | Dernier: {dernier}")

    result.append("")
    return "\n".join(result)


@mcp.tool()
def detecter_alertes() -> str:
    """
    Detecter les problemes et alertes de l'equipe.

    Returns:
        Liste des alertes
    """
    alertes = []

    for agent in AGENTS_VALIDES:
        messages = _lire_jsonl(_inbox(agent))
        non_lus = [m for m in messages if not m.get("lu", False)]
        bloquants = [m for m in non_lus if m.get("priorite", 5) == PRIORITE_BLOQUANTE]

        if bloquants:
            alertes.append(f"[URGENT] {agent} bloque par {len(bloquants)} message(s) P1 non lu(s)")
        elif non_lus:
            alertes.append(f"[INFO] {agent} a {len(non_lus)} message(s) en attente")
        else:
            alertes.append(f"[OK] {agent} operationnel, aucun message en attente")

    if not alertes:
        alertes.append("[OK] Tous les agents sont operationnels")

    return "\n".join(alertes)


@mcp.tool()
def historique(agent: Optional[str] = None, limite: int = 20) -> str:
    """
    Historique des actions de la session.

    Args:
        agent: Filtrer par agent (optionnel)
        limite: Nombre d'entrees (defaut: 20)

    Returns:
        Liste des actions recentes
    """
    fichier = HISTORIQUE_DIR / "historique.jsonl"
    entrees = _lire_jsonl(fichier)

    if agent:
        entrees = [e for e in entrees if e.get("agent") == agent.lower()]

    entrees = entrees[-limite:]

    if not entrees:
        return "[JARVIS] Aucune action dans l'historique."

    result = ["=== HISTORIQUE ===", ""]
    for e in entrees:
        result.append(f"  {e['date']} | {e['agent']:10s} | {e['action']:12s} | {e['details']}")

    return "\n".join(result)


# --- Resources MCP ---

@mcp.resource("inbox://{agent}")
def resource_inbox(agent: str) -> str:
    """Messages recus par un agent (JSONL)."""
    messages = _lire_jsonl(_inbox(agent))
    return json.dumps(messages, ensure_ascii=False, indent=2)


@mcp.resource("outbox://{agent}")
def resource_outbox(agent: str) -> str:
    """Messages envoyes par un agent (JSONL)."""
    messages = _lire_jsonl(_outbox(agent))
    return json.dumps(messages, ensure_ascii=False, indent=2)


@mcp.resource("jarvis://status")
def resource_status() -> str:
    """Etat actuel de l'equipe."""
    status = {}
    for agent in AGENTS_VALIDES:
        messages = _lire_jsonl(_inbox(agent))
        non_lus = [m for m in messages if not m.get("lu", False)]
        bloquants = [m for m in non_lus if m.get("priorite", 5) == PRIORITE_BLOQUANTE]
        status[agent] = {
            "messages_en_attente": len(non_lus),
            "bloque": len(bloquants) > 0,
        }
    return json.dumps(status, ensure_ascii=False, indent=2)


@mcp.resource("jarvis://config")
def resource_config() -> str:
    """Configuration de JARVIS."""
    config = {
        "agents_valides": AGENTS_VALIDES,
        "priorite_bloquante": PRIORITE_BLOQUANTE,
        "expiration_apres_lu": True,
        "version": "0.7.0",
    }
    return json.dumps(config, ensure_ascii=False, indent=2)


# --- Point d'entree ---

if __name__ == "__main__":
    if verifier_outil is not None:
        verifier_outil(str(Path(__file__).parent), agent="jarvis-server")
    import argparse

    parser = argparse.ArgumentParser(description="JARVIS - Serveur MCP")
    parser.add_argument("--transport", default="stdio", choices=["stdio", "http"],
                        help="Transport: stdio (local) ou http (distant)")
    parser.add_argument("--port", type=int, default=8080, help="Port pour le transport HTTP")
    args = parser.parse_args()

    if args.transport == "http":
        mcp.run(transport="http", port=args.port)
    else:
        mcp.run()
