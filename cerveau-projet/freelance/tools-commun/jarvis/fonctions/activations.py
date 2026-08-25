# -*- coding: ascii -*-
"""fonctions/activations.py - UNE tache : activer un agent (bloc session +
message P1 + incarnation + livraison directe)."""

import sys
import uuid
from datetime import datetime, timezone

from core import (AGENTS_INFOS, AGENTS_VALIDES, ajouter_message,
                  marquer_lu)
from historique import historiser, AGENTS_FILE


def maj_bloc_session(session: str, agent: str, raison: str = "") -> bool:
    """v0.3.0 : active le destinataire dans AGENTS.md - met a jour
    le bloc session (Nom Agent, Role, Fiche, Corrections, Date, Raison).
    Ne touche qu'aux lignes de tableau existantes ('|')."""
    try:
        contenu = AGENTS_FILE.read_text(encoding="utf-8")
    except FileNotFoundError:
        return False
    lignes = contenu.split("\n")
    debut = None
    for i, ligne in enumerate(lignes):
        if ligne.strip().startswith("### Session :") and \
                ligne.strip() == f"### Session : {session}":
            debut = i
            break
    if debut is None:
        return False
    fin = len(lignes)
    for i in range(debut + 1, len(lignes)):
        if lignes[i].startswith("### Session") or lignes[i].startswith("## "):
            fin = i
            break
    infos = AGENTS_INFOS.get(agent, {})
    date = datetime.now().strftime("%Y-%m-%d")
    champs = {
        "**Nom Agent**": agent,
        "**Role Agent**": infos.get("role", ""),
        "**Derniere mise a jour**": date,
        "**Raison**": raison,
    }
    if infos.get("fiche"):
        champs["**Fiche**"] = "[%s](%s)" % (infos["fiche"], infos["fiche"])
    if infos.get("corrections"):
        champs["**Corrections**"] = "[%s](%s)" % (
            infos["corrections"], infos["corrections"])
    for i in range(debut, fin):
        if "|" not in lignes[i]:
            continue  # ne jamais toucher aux lignes hors tableau
        parties = [p.strip() for p in lignes[i].split("|")]
        for j, p in enumerate(parties):
            if p in champs and j + 1 < len(parties) and champs[p]:
                parties[j + 1] = champs[p]
        lignes[i] = "| " + " | ".join(
            p for p in parties if p != "") .strip("| ") + " |"
    lignes[debut] = f"### Session : {session}"
    AGENTS_FILE.write_text("\n".join(lignes), encoding="utf-8")
    return True


def cmd_activer(args):
    """Activer un agent via JARVIS (remplace activer-agent-principal)."""
    agent = args.agent.lower()
    session = getattr(args, "session", "")
    mission = args.mission
    expediteur = getattr(args, 'de', 'stark').lower()

    if not session:
        print("ERREUR: --session obligatoire (convention session-llm-N) - "
              "jamais de session devinee (v0.1.1, anti valeur en dur)")
        sys.exit(1)

    if agent not in AGENTS_VALIDES:
        print(f"ERREUR: agent inconnu '{agent}'. Agents valides: {AGENTS_VALIDES}")
        sys.exit(1)

    # v0.2.0 : incarnation obligatoire dans le corps du message
    message = {
        "id": str(uuid.uuid4())[:8],
        "de": expediteur,
        "vers": agent,
        "priorite": 1,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "objet": "ACTIVATION",
        "corps": (
            f"Tu es l agent {agent}. AVANT DE COMMENCER : lis ta fiche et "
            f"tes corrections puis PRENDS LE RELAIS.\n\n" + mission
        ),
        "lu": False,
        "accuse": False,
        "type": "activation",
    }
    ajouter_message(get_inbox(agent), message)
    ajouter_message(get_outbox(expediteur), message)

    # v0.6.1 : livraison directe - l'affichage EST la livraison.
    marquer_lu(agent, [message["id"]])
    historiser(agent, f"Active par {expediteur}: {mission[:80]}", "R", session=session)

    ok = maj_bloc_session(session, agent,
                          raison=f"Active par {expediteur}: {mission[:80]}")

    print(f"[JARVIS] Agent '{agent}' active via JARVIS.")
    print(f"  Expediteur: {expediteur}")
    print(f"  Session: {session}")
    print(f"  Mission: {mission}")
    print(f"  Bloc session AGENTS.md: {'mis a jour' if ok else 'INTROUVABLE'}")
    print(f"  ID: {message['id']}")
    print(f"  MISSION INJECTEE - DEMARRE DIRECTEMENT (livree = affichee).")


# import tardif pour eviter la circularite (messages -> activations)
from core import get_inbox, get_outbox  # noqa: E402
