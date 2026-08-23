# -*- coding: ascii -*-
"""fonctions/messages.py - UNE tache : envoyer, lire, acquitter, lister,
recu, bloques (le flux de messages)."""

import sys
import uuid
from datetime import datetime, timezone

from core import (AGENTS_VALIDES, get_inbox, get_outbox, lire_jsonl,
                  ecrire_jsonl, ajouter_message, marquer_lu)
from historique import historiser
from activations import maj_bloc_session


def cmd_envoyer(args):
    """Envoyer un message."""
    de = args.de.lower()
    vers = args.vers.lower()
    priorite = args.priorite
    objet = args.objet
    corps = args.corps

    if de not in AGENTS_VALIDES:
        print(f"ERREUR: expediteur inconnu '{de}'. Agents valides: {AGENTS_VALIDES}")
        sys.exit(1)
    if vers not in AGENTS_VALIDES:
        print(f"ERREUR: destinataire inconnu '{vers}'. Agents valides: {AGENTS_VALIDES}")
        sys.exit(1)
    if priorite < 1 or priorite > 5:
        print("ERREUR: priorite doit etre entre 1 et 5")
        sys.exit(1)

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

    ajouter_message(get_inbox(vers), message)
    ajouter_message(get_outbox(de), message)

    # v0.3.1 : --type R|IR ; v0.5.0 : --sans-historique pour le technique/test.
    if not getattr(args, "sans_historique", False):
        historiser(de, f"Envoie a {vers}: {objet}",
                   getattr(args, "type_action", "R"),
                   session=getattr(args, "session", ""))

    # v0.3.0 : --activer = le message DECLENCHE l'activation du destinataire.
    if getattr(args, "activer", False):
        if vers == de:
            print("ERREUR: --activer impossible vers soi-meme")
            sys.exit(1)
        ok = maj_bloc_session(getattr(args, "session", ""), vers,
                              raison=f"Relais de {de}: {objet}")
        # v0.6.1 : livraison directe (affichage = livraison)
        marquer_lu(vers, [message["id"]])
        historiser(vers, f"Active par relais de {de}: {objet}",
                   getattr(args, "type_action", "R"),
                   session=getattr(args, "session", ""))
        print(f"  [ACTIVATION] '{vers}' prend le relais"
              + ("" if ok else "  (bloc session introuvable - message seul)"))
        print(f"  MISSION INJECTEE - DEMARRE DIRECTEMENT (livree = affichee).")
        print(f"  AVANT DE COMMENCER : lis ta fiche et tes corrections puis "
              f"INCARNE l agent qui prend le relais.")

    priorite_label = "BLOQUANT" if priorite == 1 else f"P{priorite}"
    print(f"[JARVIS] Message envoye ({priorite_label}): {de} -> {vers}")
    print(f"  Objet: {objet}")
    print(f"  ID: {message['id']}")


def cmd_lire(args):
    """Lire les messages en attente d'un agent.
    v0.5.0 : auto-accuse des P3-P5 des la lecture."""
    agent = args.agent.lower()
    if agent not in AGENTS_VALIDES:
        print(f"ERREUR: agent inconnu '{agent}'")
        sys.exit(1)

    messages = lire_jsonl(get_inbox(agent))
    non_lus = [m for m in messages if not m.get("lu", False)]

    if not non_lus:
        print(f"[JARVIS] Aucun message en attente pour {agent}.")
        return

    bloquants = [m for m in non_lus if m.get("priorite", 5) == 1]

    auto = [m["id"] for m in non_lus if m.get("priorite", 5) >= 3]
    n_auto = marquer_lu(agent, auto)
    if n_auto:
        print(f"[JARVIS] {n_auto} message(s) P3-P5 auto-acquitte(s) a la lecture.")

    a_afficher = [m for m in non_lus if m.get("priorite", 5) <= 2]
    if bloquants:
        print(f"[JARVIS] *** {len(bloquants)} MESSAGE(S) BLOQUANT(S) ***")
        print(f"  L'agent {agent} ne peut pas demarrer tant que ces messages ne sont pas acquittes.")
        print()

    for m in sorted(a_afficher or non_lus, key=lambda x: x.get("priorite", 5)):
        p = m.get("priorite", 5)
        label = "BLOQUANT" if p == 1 else f"P{p}"
        print(f"  [{label}] ID: {m['id']}")
        print(f"    De: {m['de']} | Date: {m['date']}")
        print(f"    Objet: {m['objet']}")
        print(f"    Corps: {m['corps']}")
        print()


def cmd_recu(args):
    """v0.5.0 : lire + acquitter TOUT en un seul appel."""
    agent = args.agent.lower()
    if agent not in AGENTS_VALIDES:
        print(f"ERREUR: agent inconnu '{agent}'")
        sys.exit(1)
    messages = lire_jsonl(get_inbox(agent))
    non_lus = [m for m in messages if not m.get("lu", False)]
    if not non_lus:
        print(f"[JARVIS] recu {agent}: rien en attente.")
        return
    marquer_lu(agent, [m["id"] for m in non_lus])
    print(f"[JARVIS] recu {agent}: {len(non_lus)} message(s) lus et acquittes :")
    for m in sorted(non_lus, key=lambda x: x.get("priorite", 5)):
        p = m.get("priorite", 5)
        label = "BLOQUANT" if p == 1 else f"P{p}"
        print(f"  [{label}] {m['objet']} (de {m['de']})")


def cmd_acquitter(args):
    """Acquitter un message (marquer lu + accuse)."""
    agent = args.agent.lower()
    msg_id = args.id

    if agent not in AGENTS_VALIDES:
        print(f"ERREUR: agent inconnu '{agent}'")
        sys.exit(1)

    messages = lire_jsonl(get_inbox(agent))
    trouve = False

    for m in messages:
        if m.get("id") == msg_id:
            m["lu"] = True
            m["accuse"] = True
            trouve = True
            break

    if not trouve:
        print(f"ERREUR: message {msg_id} non trouve dans inbox/{agent}.jsonl")
        sys.exit(1)

    ecrire_jsonl(get_inbox(agent), messages)

    expediteur = next((m["de"] for m in messages if m.get("id") == msg_id), None)
    if expediteur:
        outbox_msgs = lire_jsonl(get_outbox(expediteur))
        for m in outbox_msgs:
            if m.get("id") == msg_id:
                m["lu"] = True
                m["accuse"] = True
                break
        ecrire_jsonl(get_outbox(expediteur), outbox_msgs)

    print(f"[JARVIS] Message {msg_id} acquitte par {agent}.")


def cmd_lister(args):
    """Lister les messages d'un agent."""
    agent = args.agent.lower()
    tous = args.tous

    if agent not in AGENTS_VALIDES:
        print(f"ERREUR: agent inconnu '{agent}'")
        sys.exit(1)

    messages = lire_jsonl(get_inbox(agent))

    if tous:
        afficher = messages
    else:
        afficher = [m for m in messages if not m.get("lu", False)]

    if not afficher:
        print(f"[JARVIS] Aucun message {'(tous)' if tous else 'en attente'} pour {agent}.")
        return

    for m in afficher:
        statut = "LU" if m.get("lu") else "NON-LU"
        p = m.get("priorite", 5)
        label = "BLOQUANT" if p == 1 else f"P{p}"
        print(f"  [{label}] [{statut}] ID: {m['id']} | {m['de']} -> {m['vers']}")
        print(f"    Objet: {m['objet']} | {m['date']}")


def cmd_bloques(args):
    """Lister les agents bloques par des messages priorite 1."""
    bloques = []
    for agent in AGENTS_VALIDES:
        messages = lire_jsonl(get_inbox(agent))
        non_lus_p1 = [m for m in messages if not m.get("lu", False) and m.get("priorite", 5) == 1]
        if non_lus_p1:
            bloques.append((agent, non_lus_p1))

    if not bloques:
        print("[JARVIS] Aucun agent bloque.")
        return

    print("[JARVIS] Agents bloques (priorite 1 non-lue) :")
    for agent, msgs in bloques:
        print(f"  {agent}: {len(msgs)} message(s) bloquant(s)")
        for m in msgs:
            print(f"    - {m['objet']} (de {m['de']}, {m['date']})")
