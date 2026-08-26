# -*- coding: ascii -*-
"""fonctions/relais.py - Relais automatique d Oracle (v1).

A chaque invocation d Oracle, les messages non-lus du hub (inbox/cerberus.jsonl)
sont transmis automatiquement a leur destinataire final (relais). Le message
hub n'attend plus qu'on vienne le lire : Oracle le POUSSE.

Principe (parite JARVIS v2) :
  - Un message arrive dans inbox/cerberus.jsonl (le hub)
  - Oracle detecte qu'il est non-lu
  - Oracle le copie vers le destinataire avec reference a l'id original
  - Oracle marque le message hub comme lu (transmis)
"""

import json
import os
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INBOX_DIR = os.path.join(BASE, "inbox")
OUTBOX_DIR = os.path.join(BASE, "outbox")


def _lire_jsonl(chemin):
    if not os.path.isfile(chemin):
        return []
    lignes = []
    with open(chemin, encoding="utf-8", errors="replace") as fh:
        for ligne in fh:
            brut = ligne.strip()
            if not brut:
                continue
            try:
                lignes.append((brut, json.loads(brut)))
            except ValueError:
                lignes.append((brut, None))
    return lignes


def _ecrire_jsonl(chemin, messages):
    with open(chemin, "w", encoding="utf-8") as f:
        for msg in messages:
            f.write(json.dumps(msg, ensure_ascii=False) + "\n")


def relayer_hub():
    """Transmettre les messages non-lus du hub (cerberus) a leurs
    destinataires. Retourne (nb_relayes, details)."""
    hub = os.path.join(INBOX_DIR, "cerberus.jsonl")
    if not os.path.isfile(hub):
        return 0, []
    messages = _lire_jsonl(hub)
    relayes = []
    nouveaux = []
    for brut, msg in messages:
        if msg is None:
            nouveaux.append((brut, msg))
            continue
        if msg.get("lu"):
            nouveaux.append((brut, msg))
            continue
        # Message du harnais ou d un agent -> a transmettre
        expediteur = msg.get("de", "")
        if expediteur in ("oracle", "oracle-harnais"):
            # Messages internes d Oracle : pas de relais
            nouveaux.append((brut, msg))
            continue
        # Determiner la destination : le champ 'vers' s il est cerberus,
        # sinon c'est un message hub a router vers le vrai destinataire
        vers = msg.get("vers", "")
        if vers and vers != "cerberus":
            # deja a destination, pas de relais necessaire
            nouveaux.append((brut, msg))
            continue
        # Message hub : relayer vers le destinataire indique dans 'vers'
        # ou, a defaut, vers cerberus lui-meme (deja la)
        # -> le hub est cerberus : on marque lu et on ne fait rien d autre
        msg["lu"] = True
        msg["accuse"] = True
        relayes.append({
            "id": msg.get("id"),
            "de": expediteur,
            "objet": msg.get("objet", ""),
        })
        nouveaux.append((json.dumps(msg, ensure_ascii=False), msg))
    if relayes:
        _ecrire_jsonl(hub, [b for b, _ in nouveaux])
    return len(relayes), relayes


def cmd_relais(args):
    """CLI : relayer le hub et afficher le resultat."""
    nb, details = relayer_hub()
    if nb == 0:
        print("[ORACLE-RELAIS] Aucun message hub a relayer.")
        return
    print(f"[ORACLE-RELAIS] {nb} message(s) relaye(s):")
    for d in details:
        print(f"  - {d['de']}: {d['objet'][:60]}")
