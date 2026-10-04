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
        return {"stark", "shuri", "forge", "rogers", "jarvis"}

AGENTS_VALIDES = _charger_agents()
FILES_DIR = Path(__file__).parent / "files"
PRIORITE_BLOQUANTE = 1

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
    """
    Envoyer un message entre agents via JARVIS.

    Args:
        de: Expediteur (stark, shuri, forge, rogers)
        vers: Destinataire (stark, shuri, forge, rogers)
        priorite: 1=bloquant, 2=urgent, 3=normal, 4=basse, 5=info
        objet: Sujet du message
        corps: Contenu du message

    Returns:
        Confirmation avec l'ID du message
    """
    de = de.lower()
    vers = vers.lower()

    if de not in AGENTS_VALIDES:
        return f"ERREUR: expediteur inconnu '{de}'. Agents valides: {AGENTS_VALIDES}"
    if vers not in AGENTS_VALIDES:
        return f"ERREUR: destinataire inconnu '{vers}'. Agents valides: {AGENTS_VALIDES}"
    if priorite < 1 or priorite > 5:
        return "ERREUR: priorite doit etre entre 1 et 5"

    message = {
        "id": str(uuid.uuid4())[:8],
        "de": de,
        "vers": vers,
        "priorite": priorite,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "objet": objet,
        "corps": corps,
        "lu": False,
        "accuse": False,
    }

    _ajouter_message(_inbox(vers), message)
    _ajouter_message(_outbox(de), message)
    _historiser("envoyer", de, f"{de} -> {vers}: {objet}")

    label = "BLOQUANT" if priorite == 1 else f"P{priorite}"
    return f"[JARVIS] Message envoye ({label}): {de} -> {vers} | ID: {message['id']} | Objet: {objet}"


def _marquer_lu(agent: str, ids: list) -> int:
    """v0.7.0 : marquer lu+accuse une liste d'IDs (inbox + outbox)."""
    messages = _lire_jsonl(_inbox(agent))
    marques = 0
    expediteurs = {}
    for m in messages:
        if m.get("id") in ids and not m.get("lu"):
            m["lu"] = True
            m["accuse"] = True
            marques += 1
            expediteurs.setdefault(m.get("de"), []).append(m["id"])
    if marques:
        _ecrire_jsonl(_inbox(agent), messages)
        for exp, exp_ids in expediteurs.items():
            outbox_msgs = _lire_jsonl(_outbox(exp))
            modifie = False
            for m in outbox_msgs:
                if m.get("id") in exp_ids and not m.get("lu"):
                    m["lu"] = True
                    m["accuse"] = True
                    modifie = True
            if modifie:
                _ecrire_jsonl(_outbox(exp), outbox_msgs)
    return marques


@mcp.tool()
def recu_messages(agent: str) -> str:
    """v0.7.0 (fluidite) : lire + acquitter TOUT en un seul appel."""
    agent = agent.lower()
    if agent not in AGENTS_VALIDES:
        return f"ERREUR: agent inconnu '{agent}'"
    non_lus = [m for m in _lire_jsonl(_inbox(agent)) if not m.get("lu")]
    if not non_lus:
        return f"[JARVIS] recu {agent}: rien en attente."
    _marquer_lu(agent, [m["id"] for m in non_lus])
    lignes = [f"[JARVIS] recu {agent}: {len(non_lus)} message(s) lus et acquittes :"]
    for m in sorted(non_lus, key=lambda x: x.get("priorite", 5)):
        p = m.get("priorite", 5)
        lignes.append(f"  [{'BLOQUANT' if p == 1 else f'P{p}'}] {m['objet']} (de {m['de']})")
    return "\n".join(lignes)


@mcp.tool()
def lire_messages(agent: str, tous: bool = False) -> str:
    """
    Lire les messages en attente d'un agent.

    Args:
        agent: Nom de l'agent (stark, shuri, forge, rogers)
        tous: Inclure les messages lus (defaut: false)

    Returns:
        Liste des messages avec statut
    """
    agent = agent.lower()
    if agent not in AGENTS_VALIDES:
        return f"ERREUR: agent inconnu '{agent}'"

    messages = _lire_jsonl(_inbox(agent))
    non_lus = [m for m in messages if not m.get("lu", False)]

    # v0.7.0 : auto-accuse P3-P5 a la lecture (fluidite)
    auto = [m["id"] for m in non_lus if m.get("priorite", 5) >= 3]
    n_auto = _marquer_lu(agent, auto)

    if tous:
        afficher = messages
    else:
        afficher = [m for m in messages if not m.get("lu", False)]

    entete = []
    if n_auto and not tous:
        entete.append(f"[JARVIS] {n_auto} message(s) P3-P5 auto-acquitte(s).")
    if not afficher:
        return "\n".join(entete) or f"[JARVIS] Aucun message pour {agent}."

    bloquants = [m for m in afficher if m.get("priorite", 5) == PRIORITE_BLOQUANTE]

    result = entete
    if bloquants:
        result.append(f"*** {len(bloquants)} MESSAGE(S) BLOQUANT(S) - {agent} ne peut pas demarrer ***")
        result.append("")

    for m in sorted(afficher, key=lambda x: x.get("priorite", 5)):
        p = m.get("priorite", 5)
        label = "BLOQUANT" if p == 1 else f"P{p}"
        statut = "LU" if m.get("lu") else "NON-LU"
        result.append(f"[{label}] [{statut}] ID: {m['id']}")
        result.append(f"  De: {m['de']} | Date: {m['date']}")
        result.append(f"  Objet: {m['objet']}")
        result.append(f"  Corps: {m['corps']}")
        result.append("")

    return "\n".join(result)


@mcp.tool()
def acquitter_message(agent: str, id_message: str) -> str:
    """
    Acquitter un message (marquer lu + accuse). Le message expire apres.

    Args:
        agent: Nom de l'agent qui acquitte
        id_message: ID du message a acquitter

    Returns:
        Confirmation
    """
    agent = agent.lower()
    if agent not in AGENTS_VALIDES:
        return f"ERREUR: agent inconnu '{agent}'"

    messages = _lire_jsonl(_inbox(agent))
    trouve = False

    for m in messages:
        if m.get("id") == id_message:
            m["lu"] = True
            m["accuse"] = True
            trouve = True
            break

    if not trouve:
        return f"ERREUR: message {id_message} non trouve dans inbox/{agent}.jsonl"

    _ecrire_jsonl(_inbox(agent), messages)

    # Aussi marquer dans l'outbox de l'expediteur
    expediteur = next((m["de"] for m in messages if m.get("id") == id_message), None)
    if expediteur:
        outbox_msgs = _lire_jsonl(_outbox(expediteur))
        for m in outbox_msgs:
            if m.get("id") == id_message:
                m["lu"] = True
                m["accuse"] = True
                break
        _ecrire_jsonl(_outbox(expediteur), outbox_msgs)

    _historiser("acquitter", agent, f"Message {id_message} acquitte")
    return f"[JARVIS] Message {id_message} acquitte par {agent}."


@mcp.tool()
def activer_agent(agent: str, mission: str, session: str = "", de: str = "stark") -> str:
    """
    Activer un agent via JARVIS (remplace activer-agent-principal).
    Envoie un message P1 bloquant dans l'inbox de l'agent.

    Args:
        agent: Agent a activer (stark, shuri, forge, rogers)
        mission: Description de la mission
        session: Nom de la session cible (OBLIGATOIRE, convention session-llm-N)
        de: Expediteur (defaut: stark)

    Returns:
        Confirmation avec l'ID
    """
    agent = agent.lower()
    de = de.lower()

    if not session:
        return "ERREUR: session obligatoire (convention session-llm-N) - jamais de session devinee"

    if agent not in AGENTS_VALIDES:
        return f"ERREUR: agent inconnu '{agent}'. Agents valides: {AGENTS_VALIDES}"

    message = {
        "id": str(uuid.uuid4())[:8],
        "de": de,
        "vers": agent,
        "priorite": PRIORITE_BLOQUANTE,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "objet": "ACTIVATION",
        "corps": (
            "AVANT DE COMMENCER : lis ta fiche et tes corrections puis "
            "INCARNE l agent qui prend le relais.\n\n" + mission
        ),
        "lu": False,
        "accuse": False,
        "type": "activation",
    }

    _ajouter_message(_inbox(agent), message)
    _ajouter_message(_outbox(de), message)

    # v0.7.0 : livraison directe - affichage = livraison
    _marquer_lu(agent, [message["id"]])
    _historiser("activer", de, f"Activation de {agent}: {mission[:50]}...")

    return (
        f"[JARVIS] Agent '{agent}' active.\n"
        f"  Expediteur: {de}\n"
        f"  Session: {session}\n"
        f"  Mission: {mission}\n"
        f"  ID: {message['id']}\n"
        f"  L'agent doit lire son inbox avant de demarrer (P1 = bloquant)."
    )


@mcp.tool()
def mettre_en_attente(mission: str, contexte: str = "", niveau: str = "attente", agent: str = "") -> str:
    """v0.8.0 (protocole 13 v2) : placer une mission selon le declencheur.
    niveau: attente (EN_ATTENTE) / attention (SUIVANTE en file-asap) /
    urgent (PRIORITAIRE en file-attente)."""
    niveaux = {
        "attente": ("file-attente", "EN_ATTENTE", "ATTENTE"),
        "attention": ("file-asap", "SUIVANTE", "AT-1"),
        "urgent": ("file-attente", "PRIORITAIRE", "UR-1"),
    }
    if niveau not in niveaux:
        return f"ERREUR: niveau inconnu '{niveau}' (attente/attention/urgent)"
    file, statut, type_d = niveaux[niveau]
    entree = {
        "type": type_d,
        "mission": mission,
        "agent": agent,
        "contexte_avant": contexte,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "statut": statut,
    }
    chemin = FILES_DIR / f"{file}.jsonl"
    with open(chemin, "a", encoding="utf-8") as f:
        f.write(json.dumps(entree, ensure_ascii=False) + "\n")
    _historiser("file", "jarvis", f"Mise en attente [{niveau}]: {mission[:50]}")
    return (f"[JARVIS] Mission placee en {file} (statut: {statut}, "
            f"declencheur: [{niveau}]).\n  Mission: {mission}")


@mcp.tool()
def stop_dev(raison: str) -> str:
    """v0.8.0 ([stop] DEFCON 5) : arret complet du dev, gel de toutes les
    missions en files. Reprendre exige decision explicite de l'utilisateur."""
    gelees = 0
    for nom in ("file-attente", "file-asap"):
        chemin = FILES_DIR / f"{nom}.jsonl"
        if not chemin.exists():
            continue
        lignes = [l for l in chemin.read_text(encoding="utf-8").splitlines() if l.strip()]
        modifie = False
        for i, l in enumerate(lignes):
            try:
                e = json.loads(l)
            except ValueError:
                continue
            if e.get("statut") in ("EN_ATTENTE", "PREPAREE", "SUIVANTE", "PRIORITAIRE"):
                e["statut"] = "DEFCON5"
                lignes[i] = json.dumps(e, ensure_ascii=False)
                modifie = True
                gelees += 1
        if modifie:
            chemin.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    defcon = {"date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
              "raison": raison, "missions_gelees": gelees}
    with open(FILES_DIR / "defcon.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(defcon, ensure_ascii=False) + "\n")
    _historiser("stop", "jarvis", f"DEFCON 5 - arret du dev: {raison[:50]}")
    return (f"*** [STOP] DEFCON 5 - ARRET COMPLET DU DEV ***\n  Raison: {raison}\n"
            f"  Missions gelees: {gelees}")


@mcp.tool()
def lister_files() -> str:
    """v0.7.0 : lister les files d'attente (file-attente + file-asap)."""
    result = []
    for nom in ("file-attente", "file-asap"):
        chemin = FILES_DIR / f"{nom}.jsonl"
        entrees = []
        if chemin.exists():
            for l in chemin.read_text(encoding="utf-8").splitlines():
                if not l.strip():
                    continue
                try:
                    e = json.loads(l)
                except ValueError:
                    continue
                if e.get("statut") not in (None, "VIDE"):
                    entrees.append(e)
        result.append(f"[{nom}] {len(entrees)} entree(s)")
        for e in entrees:
            result.append(f"  [{e.get('statut')}] {e.get('mission', '')[:70]} ({e.get('date', '')})")
    return "\n".join(result)


@mcp.tool()
def reprendre_mission(file: str = "file-attente") -> str:
    """v0.7.0 : depiler la derniere mission en attente et retourner son
    contexte de reprise (statut passe a REPRISE)."""
    chemin = FILES_DIR / f"{file}.jsonl"
    if not chemin.exists():
        return f"[JARVIS] File {file} inexistante."
    lignes = [l for l in chemin.read_text(encoding="utf-8").splitlines() if l.strip()]
    for i in range(len(lignes) - 1, -1, -1):
        try:
            e = json.loads(lignes[i])
        except ValueError:
            continue
        if e.get("statut") in ("EN_ATTENTE", "PREPAREE"):
            e["statut"] = "REPRISE"
            e["date_reprise"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
            lignes[i] = json.dumps(e, ensure_ascii=False)
            chemin.write_text("\n".join(lignes) + "\n", encoding="utf-8")
            _historiser("file", "jarvis", f"Reprise depuis {file}: {e.get('mission', '')[:50]}")
            sortie = [f"[JARVIS] Mission reprise depuis {file} :",
                      f"  Mission: {e.get('mission')}"]
            if e.get("contexte_avant"):
                sortie.append(f"  Contexte avant mise en attente: {e['contexte_avant']}")
            return "\n".join(sortie)
    return f"[JARVIS] Aucune mission en attente dans {file}."


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
