# -*- coding: ascii -*-
"""logique_messages.py - UNE tache : la logique des messages pour le
serveur MCP (protocole 14 - extrait v0.9.0)."""

import uuid
from datetime import datetime, timezone
from pathlib import Path

JARVIS_DIR = Path(__file__).parent.parent
INBOX_DIR = JARVIS_DIR / "inbox"
OUTBOX_DIR = JARVIS_DIR / "outbox"


def _inbox(agent):
    return INBOX_DIR / f"{agent}.jsonl"


def _outbox(agent):
    return OUTBOX_DIR / f"{agent}.jsonl"


def _lire_jsonl(path):
    if not path.exists():
        return []
    resultats = []
    for l in path.read_text(encoding="utf-8").splitlines():
        if not l.strip():
            continue
        try:
            resultats.append(json.loads(l))
        except ValueError:
            continue
    return resultats


def _ecrire_jsonl(path, messages):
    with open(path, "w", encoding="utf-8") as f:
        for m in messages:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")


def _ajouter_message(path, message):
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(message, ensure_ascii=False) + "\n")


import json  # noqa: E402


def marquer_lu(agent, ids):
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
            try:
                outbox_msgs = _lire_jsonl(_outbox(exp))
            except OSError:
                continue
            modifie = False
            for m in outbox_msgs:
                if m.get("id") in exp_ids and not m.get("lu"):
                    m["lu"] = True
                    m["accuse"] = True
                    modifie = True
            if modifie:
                _ecrire_jsonl(_outbox(exp), outbox_msgs)
    return marques


def envoyer_message(de, vers, priorite, objet, corps,
                    agents_valides, historiser_fn):
    de, vers = de.lower(), vers.lower()
    if de not in agents_valides:
        return f"ERREUR: expediteur inconnu '{de}'. Agents valides: {agents_valides}"
    if vers not in agents_valides:
        return f"ERREUR: destinataire inconnu '{vers}'. Agents valides: {agents_valides}"
    if priorite < 1 or priorite > 5:
        return "ERREUR: priorite doit etre entre 1 et 5"
    message = {
        "id": str(uuid.uuid4())[:8],
        "de": de, "vers": vers, "priorite": priorite,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "objet": objet, "corps": corps, "lu": False, "accuse": False,
    }
    _ajouter_message(_inbox(vers), message)
    _ajouter_message(_outbox(de), message)
    historiser_fn("envoyer", de, f"{de} -> {vers}: {objet}")
    label = "BLOQUANT" if priorite == 1 else f"P{priorite}"
    return (f"[JARVIS] Message envoye ({label}): {de} -> {vers} | "
            f"ID: {message['id']} | Objet: {objet}")


def recu_messages(agent, agents_valides):
    agent = agent.lower()
    if agent not in agents_valides:
        return f"ERREUR: agent inconnu '{agent}'"
    non_lus = [m for m in _lire_jsonl(_inbox(agent))
               if not m.get("lu") and m.get("id")]
    marquer_lu(agent, [m["id"] for m in non_lus])
    lignes = [f"[JARVIS] recu {agent}: {len(non_lus)} message(s) lus et acquittes :"]
    for m in sorted(non_lus, key=lambda x: x.get("priorite", 5)):
        p = m.get("priorite", 5)
        lignes.append(f"  [{'BLOQUANT' if p == 1 else f'P{p}'}] {m['objet']} (de {m['de']})")
    return "\n".join(lignes)


def lire_messages(agent, tous, agents_valides, priorite_bloquante=1):
    agent = agent.lower()
    if agent not in agents_valides:
        return f"ERREUR: agent inconnu '{agent}'"
    messages = _lire_jsonl(_inbox(agent))
    sans_id = [m for m in messages
               if not m.get("lu", False) and not m.get("id")]
    non_lus = [m for m in messages
               if not m.get("lu", False) and m.get("id")]
    auto = [m["id"] for m in non_lus if m.get("priorite", 5) >= 3]
    n_auto = marquer_lu(agent, auto)
    afficher = messages if tous else \
        [m for m in messages if not m.get("lu", False)]
    entete = []
    if n_auto and not tous:
        entete.append(f"[JARVIS] {n_auto} message(s) P3-P5 auto-acquitte(s).")
    if sans_id and not tous:
        entete.append(f"[JARVIS] ATTENTION: {len(sans_id)} message(s) sans id ignore(s).")
    if not afficher:
        return "\n".join(entete) or f"[JARVIS] Aucun message pour {agent}."
    bloquants = [m for m in afficher
                 if m.get("priorite", 5) == priorite_bloquante]
    result = entete
    if bloquants:
        result.append(f"*** {len(bloquants)} MESSAGE(S) BLOQUANT(S) - "
                      f"{agent} ne peut pas demarrer ***")
        result.append("")
    for m in sorted(afficher, key=lambda x: x.get("priorite", 5)):
        p = m.get("priorite", 5)
        label = "BLOQUANT" if p == 1 else f"P{p}"
        statut = "LU" if m.get("lu") else "NON-LU"
        result.append(f"[{label}] [{statut}] ID: {m.get('id', 'N/A')}")
        result.append(f"  De: {m['de']} | Date: {m['date']}")
        result.append(f"  Objet: {m['objet']}")
        result.append(f"  Corps: {m['corps']}")
        result.append("")
    return "\n".join(result)


def acquitter_message(agent, id_message, agents_valides, historiser_fn):
    agent = agent.lower()
    if agent not in agents_valides:
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
    expediteur = next((m["de"] for m in messages
                       if m.get("id") == id_message), None)
    if expediteur:
        outbox_msgs = _lire_jsonl(_outbox(expediteur))
        for m in outbox_msgs:
            if m.get("id") == id_message:
                m["lu"] = True
                m["accuse"] = True
                break
        _ecrire_jsonl(_outbox(expediteur), outbox_msgs)
    historiser_fn("acquitter", agent, f"Message {id_message} acquitte")
    return f"[JARVIS] Message {id_message} acquitte par {agent}."
