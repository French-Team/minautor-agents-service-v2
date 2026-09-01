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
import time
from datetime import datetime, timezone

ACK_TIMEOUT_SECONDS = 120
MAX_RETRIES = 2


def _etat_ack_path():
    return os.path.join(BASE, "data", "ack-pending.json")


def _charger_ack():
    try:
        with open(_etat_ack_path(), encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def _sauver_ack(data):
    os.makedirs(os.path.dirname(_etat_ack_path()), exist_ok=True)
    with open(_etat_ack_path(), "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=True, indent=2)


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


def _ajouter_unique(chemin, message):
    """Ajouter un message seulement si son id n existe pas deja."""
    existants = [m for _, m in _lire_jsonl(chemin) if isinstance(m, dict)]
    if any(m.get("id") == message.get("id") for m in existants):
        return False
    _ecrire_jsonl(chemin, existants + [message])
    return True


def _ecrire_jsonl(chemin, messages):
    """Ecrire une liste de lignes dans un JSONL.
    NB (correction 2026-08-29) : les elements de la liste sont des
    BRUTS (deja serialises, chaines JSON). Appliquer json.dumps sur un
    brut re-echappait le JSON a chaque ecriture -> corruption en cascade
    (le hub cerberus.jsonl a atteint 1 Go de guillemets imbriques). On
    ecrit les bruts TELS QUELS ; un dict passe est serialize une seule
    fois (normalisation)."""
    with open(chemin, "w", encoding="utf-8") as f:
        for msg in messages:
            if isinstance(msg, str):
                f.write(msg + "\n")
            else:
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
        if isinstance(msg, str):
            # JSON double-encode (historique) : tenter un second parse
            try:
                msg = json.loads(msg)
            except ValueError:
                nouveaux.append((brut, msg))
                continue
        if not isinstance(msg, dict):
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
        # Une remise n est pas une reaction. Le message reste suivi jusqu a
        # reception d un accuse explicite de l agent cible.
        msg["lu"] = True
        msg["accuse"] = False
        msg["requis_accuse"] = True
        msg["accuse_avant"] = time.time() + ACK_TIMEOUT_SECONDS
        msg["tentatives"] = int(msg.get("tentatives", 0)) + 1
        msg["destinataire_final"] = msg.get("vers") or "cerberus"
        relayes.append({
            "id": msg.get("id"),
            "de": expediteur,
            "objet": msg.get("objet", ""),
        })
        nouveaux.append((json.dumps(msg, ensure_ascii=False), msg))
    if relayes:
        _ecrire_jsonl(hub, [b for b, _ in nouveaux])
    _surveiller_accuses()
    return len(relayes), relayes


def _surveiller_accuses():
    """Relance un agent qui n a pas accuse reception; escalade Oracle si
    le nombre maximal de tentatives est atteint. La fonction est idempotente.
    """
    suivis = _charger_ack()
    maintenant = time.time()
    for nom_fichier, msg in _lire_jsonl(os.path.join(INBOX_DIR, "cerberus.jsonl")):
        if not isinstance(msg, dict) or not msg.get("requis_accuse"):
            continue
        ident = msg.get("id")
        if msg.get("accuse") or not ident:
            continue
        if maintenant < float(msg.get("accuse_avant", maintenant)):
            continue
        cle = str(ident)
        tentatives = int(msg.get("tentatives", 1))
        if suivis.get(cle) == tentatives:
            continue
        suivis[cle] = tentatives
        if tentatives <= MAX_RETRIES:
            cible = msg.get("destinataire_final") or msg.get("vers")
            if cible and cible != "cerberus":
                msg2 = dict(msg)
                msg2["id"] = "%s-r%d" % (ident, tentatives)
                msg2["de"] = "oracle"
                msg2["vers"] = cible
                msg2["lu"] = False
                msg2["accuse"] = False
                msg2["accuse_avant"] = maintenant + ACK_TIMEOUT_SECONDS
                msg2["tentatives"] = tentatives + 1
                _ajouter_unique(os.path.join(INBOX_DIR, cible + ".jsonl"), msg2)
        else:
            # Le relais ne declenche pas de boucle: il depose une alerte
            # unique a Oracle, qui decide d une reactivation/escalade.
            alerte = dict(msg)
            alerte["id"] = "ack-timeout-" + str(ident)
            alerte["de"] = "relais"
            alerte["vers"] = "oracle"
            alerte["priorite"] = 1
            alerte["objet"] = "[ACK TIMEOUT] Agent sans reaction"
            alerte["corps"] = "L agent cible n a pas accuse reception: %s" % ident
            alerte["lu"] = False
            alerte["accuse"] = False
            _ajouter_unique(os.path.join(INBOX_DIR, "oracle.jsonl"), alerte)
    _sauver_ack(suivis)


def cmd_relais(args):
    """CLI : relayer le hub et afficher le resultat."""
    nb, details = relayer_hub()
    if nb == 0:
        print("[ORACLE-RELAIS] Aucun message hub a relayer.")
        return
    print(f"[ORACLE-RELAIS] {nb} message(s) relaye(s):")
    for d in details:
        print(f"  - {d['de']}: {d['objet'][:60]}")
