# -*- coding: ascii -*-
"""logique_activations.py - UNE tache : activer un agent depuis le
serveur MCP (message P1 + incarnation + livraison directe)."""

import uuid
from datetime import datetime, timezone

from logique_messages import _inbox, _outbox, _ajouter_message, marquer_lu


def activer_agent(agent, mission, session, de, agents_valides,
                  priorite_bloquante=1):
    agent, de = agent.lower(), de.lower()
    if not session:
        return ("ERREUR: session obligatoire (convention session-llm-N) - "
                "jamais de session devinee")
    if agent not in agents_valides:
        return f"ERREUR: agent inconnu '{agent}'. Agents valides: {agents_valides}"
    message = {
        "id": str(uuid.uuid4())[:8],
        "de": de,
        "vers": agent,
        "priorite": priorite_bloquante,
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
    marquer_lu(agent, [message["id"]])
    return (
        f"[JARVIS] Agent '{agent}' active.\n"
        f"  Expediteur: {de}\n"
        f"  Session: {session}\n"
        f"  Mission: {mission}\n"
        f"  ID: {message['id']}\n"
        f"  MISSION INJECTEE - DEMARRE DIRECTEMENT (livree = affichee)."
    )
