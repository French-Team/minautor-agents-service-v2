#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
Oracle Server v0.2.0 -- Serveur de l'equipe v1 (session-admin)

Hub central de communication, activation et coordination.
Tourne en arriere-plan et route les messages en temps reel.

Lancement:
    python oracle-server.py                    # Stdio (local)
    python oracle-server.py --transport http   # HTTP (distant)
    python oracle-server.py --boucle [--intervalle N]  # daemon resident (v0.2.0)

Fonctionnalites:
    - Routing des messages entre agents (inbox/outbox)
    - Historisation automatique a chaque action
    - Surveillance des agents (harnais)
    - Gestion des files de missions
    - DEFCON (niveau de menace)
    - Mode --boucle : daemon resident (harnais + relais + DEFCON),
      lance par le serveur de demarrage v1 (oracle-demarrage).
      Le mode stdio historique (lecture de commandes JSON sur stdin)
      reste disponible pour les appels ponctuels.
"""

import io
import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

VERSION = "0.2.0"

# --- Configuration ---
ORACLE_DIR = Path(__file__).parent
INBOX_DIR = ORACLE_DIR / "inbox"
OUTBOX_DIR = ORACLE_DIR / "outbox"
DATA_FILE = ORACLE_DIR / "oracle-data.json"
FILES_DIR = ORACLE_DIR / "files"
PID_FILE = ORACLE_DIR / "oracle-server.pid"
LOG_DIR = ORACLE_DIR / "observations"
# Production: arret apres 30 minutes d inactivite du dernier agent actif.
INACTIVITE_MAX_SECONDES = 30 * 60
INACTIVITE_ETAT = ORACLE_DIR / "session-admin-inactivite.json"
AGENTS_FILE = ORACLE_DIR.parents[2] / "AGENTS.md"
DEMARRAGE_SESSION = time.time()


def _dernier_agent_actif():
    """Lire l agent actif de session-admin depuis AGENTS.md."""
    try:
        texte = AGENTS_FILE.read_text(encoding="utf-8")
    except OSError:
        return "cerberus"
    actif = None
    dans_session = False
    for ligne in texte.splitlines():
        if ligne.startswith("### Session :"):
            dans_session = "session-admin" in ligne.lower()
        elif dans_session and ligne.startswith("| **Agent actif** |"):
            actif = ligne.split("|", 2)[1].strip(" *")
            break
    return actif or "cerberus"


def _dernier_agent_a_agit():
    """Retourner un timestamp fiable de la derniere activite de l agent actif.

    L encart ne contient que l heure; on utilise donc la date de modification
    du fichier comme date de reference et l heure de la ligne pour eviter de
    comparer une heure du jour avec un timestamp d un autre jour.
    """
    try:
        activite = AGENTS_FILE.parent / "AGENTS-activite-recente.md"
        lignes = activite.read_text(encoding="utf-8").splitlines()
        base = datetime.fromtimestamp(activite.stat().st_mtime)
    except OSError:
        return time.time()
    agent = _dernier_agent_actif().lower()
    for ligne in lignes:
        if not ligne.startswith("| ") or "| Grade |" in ligne or "|---" in ligne:
            continue
        c = [x.strip() for x in ligne.split("|")]
        if len(c) < 9 or c[2].lower() != agent:
            continue
        try:
            moment = base.replace(hour=int(c[8][0:2]), minute=int(c[8][3:5]),
                                  second=int(c[8][6:8]), microsecond=0)
            if moment.timestamp() > time.time() + 60:
                moment -= __import__("datetime").timedelta(days=1)
            return moment.timestamp()
        except (ValueError, IndexError):
            return time.time()
    return time.time()


def _demande_utilisateur_recente():
    """Retourne le timestamp de la derniere demande utilisateur connue.

    Les missions/messages internes ne renouvellent pas ce timestamp. Le
    marqueur est mis a jour par le demarrage et par les APIs d entree user.
    """
    try:
        if INACTIVITE_ETAT.exists():
            data = json.loads(INACTIVITE_ETAT.read_text(encoding="utf-8"))
            return float(data.get("derniere_demande_user", DEMARRAGE_SESSION))
    except (OSError, ValueError, TypeError):
        pass
    return DEMARRAGE_SESSION


def _marquer_demande_utilisateur():
    """Enregistrer une entree utilisateur sans creer d activite interne."""
    try:
        INACTIVITE_ETAT.write_text(
            json.dumps({"derniere_demande_user": time.time()}, ensure_ascii=True),
            encoding="utf-8")
    except OSError:
        pass


def _historiser_arret_inactivite():
    """Tracer l arret automatique dans les activites recentes."""
    _historiser("oracle", "ARRET AUTO: dernier agent actif inactif >= 30 min")


def _arret_si_inactif():
    """Arreter apres inactivite du dernier agent actif."""
    if time.time() - _dernier_agent_a_agit() < INACTIVITE_MAX_SECONDES:
        return False
    _historiser_arret_inactivite()
    _arreter_pid_associe(ORACLE_DIR / "routines-server.pid")
    _arreter_pid_associe(ORACLE_DIR / "super-combos" / "super-pilote.pid")
    _nettoyer_pid()
    return True


def _arreter_pid_associe(pid_file):
    """Arreter un serveur associe puis supprimer son PID file."""
    try:
        if not pid_file.exists():
            return
        pid = int(pid_file.read_text(encoding="utf-8").strip())
        if pid != os.getpid():
            os.kill(pid, 15)
    except (OSError, ValueError):
        pass
    try:
        pid_file.unlink()
    except OSError:
        pass

INBOX_DIR.mkdir(exist_ok=True)
OUTBOX_DIR.mkdir(exist_ok=True)
FILES_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# Import du CLI pour reutiliser les fonctions
sys.path.insert(0, str(ORACLE_DIR))
from oracle import charger_agents, agent_valide


def _historiser(action, agent, details):
    """Historiser une action via activer-agent-principal."""
    try:
        aap_path = ORACLE_DIR.parent / "activer" / "activer-agent-principal" / "activer-agent-principal.py"
        if not aap_path.exists():
            return
        import importlib.util
        spec = importlib.util.spec_from_file_location("aap", str(aap_path))
        aap = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(aap)
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.000")
        aap.ajouter_historique(ts, "session-admin", agent, f"{action}: {details}", "R")
    except Exception:
        pass


def _lire_jsonl(chemin):
    """Lire un fichier JSONL."""
    if not chemin.exists():
        return []
    messages = []
    with open(chemin, encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                messages.append(json.loads(ligne))
            except json.JSONDecodeError:
                continue
    return messages


def _ecrire_jsonl(chemin, messages):
    """Ecrire une liste de messages dans un JSONL."""
    with io.open(chemin, "w", encoding="utf-8", newline="\n") as f:
        for msg in messages:
            f.write(json.dumps(msg, ensure_ascii=False) + "\n")


# --- API MCP ---

def envoyer_message(de: str, vers: str, objet: str, corps: str, priorite: int = 2) -> dict:
    """Envoyer un message entre agents."""
    if str(de).lower() in ("user", "utilisateur"):
        _marquer_demande_utilisateur()
    msg = {
        "id": uuid.uuid4().hex[:8],
        "de": de,
        "vers": vers,
        "priorite": priorite,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "objet": objet,
        "corps": corps,
        "lu": False,
        "accuse": False,
        "requis_accuse": True,
        "accuse_avant": time.time() + 120,
        "tentatives": 1
    }
    # Ecrire dans outbox de l'expediteur
    outbox_file = OUTBOX_DIR / f"{de}.jsonl"
    messages = _lire_jsonl(outbox_file)
    messages.append(msg)
    _ecrire_jsonl(outbox_file, messages)
    # Ecrire dans inbox du destinataire avec ROTATION (decision utilisateur
    # 2026-08-29 : ne garder que les 5 messages les plus recents). Le outbox
    # reste en append (trace complete).
    sys.path.insert(0, str(ORACLE_DIR / "fonctions"))
    import rotation as _rotation
    _rotation.ajouter_message(INBOX_DIR, vers, msg)
    _historiser("envoyer", de, f"{de} -> {vers}: {objet[:50]}")
    return {"id": msg["id"], "statut": "envoye"}


def lire_messages(agent: str) -> list:
    """Lire les messages non lus d'un agent."""
    inbox_file = INBOX_DIR / f"{agent}.jsonl"
    messages = _lire_jsonl(inbox_file)
    non_lus = [m for m in messages if not m.get("lu")]
    return non_lus


def _marquer_accuse(agent: str, id_message: str, reaction: str = "") -> dict:
    """Marquer un message comme accuse et enregistrer la reaction de l agent."""
    inbox_file = INBOX_DIR / f"{agent}.jsonl"
    messages = _lire_jsonl(inbox_file)
    trouve = False
    for msg in messages:
        if msg.get("id") == id_message:
            msg["accuse"] = True
            msg["lu"] = True
            msg["reaction"] = reaction
            msg["reaction_date"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
            trouve = True
    if trouve:
        _ecrire_jsonl(inbox_file, messages)
        _historiser("reaction", agent, "Message %s traite: %s" % (id_message, reaction[:80]))
    return {"trouve": trouve, "accuse": trouve}


def acquitter_message(agent: str, id_message: str) -> dict:
    """Acquitter un message : le RETIRE de l inbox (consommation reelle,
    decision utilisateur 2026-08-29 : les messages s accumulaient sans
    traitement)."""
    inbox_file = INBOX_DIR / f"{agent}.jsonl"
    messages = _lire_jsonl(inbox_file)
    trouve = False
    conserves = []
    for msg in messages:
        if msg.get("id") == id_message:
            trouve = True
            continue
        conserves.append(msg)
    if trouve:
        _ecrire_jsonl(inbox_file, conserves)
        _historiser("acquitter", agent, f"Message {id_message} acquitte (consomme)")
    return {"trouve": trouve}


def lister_messages(agent: str) -> dict:
    """Lister tous les messages d'un agent."""
    inbox_file = INBOX_DIR / f"{agent}.jsonl"
    messages = _lire_jsonl(inbox_file)
    total = len(messages)
    non_lus = sum(1 for m in messages if not m.get("lu"))
    return {"total": total, "non_lus": non_lus}


def historiser_action(agent: str, raison: str, type_action: str = "R") -> dict:
    """Historiser une action."""
    try:
        aap_path = ORACLE_DIR.parent / "activer" / "activer-agent-principal" / "activer-agent-principal.py"
        if not aap_path.exists():
            return {"erreur": "activer-agent-principal introuvable"}
        import importlib.util
        spec = importlib.util.spec_from_file_location("aap", str(aap_path))
        aap = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(aap)
        # Detecter IR
        if raison.upper().startswith(("INTER-ROUND", "FIN D INTER-ROUND")):
            type_action = "IR"
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.000")
        rc = aap.ajouter_historique(ts, "session-admin", agent, raison, type_action)
        return {"statut": "ok", "rc": rc}
    except Exception as exc:
        return {"erreur": str(exc)[:80]}


def activer_agent(agent: str, raison: str) -> dict:
    """Activer un agent."""
    try:
        aap_path = ORACLE_DIR.parent / "activer" / "activer-agent-principal" / "activer-agent-principal.py"
        if not aap_path.exists():
            return {"erreur": "activer-agent-principal introuvable"}
        import importlib.util
        spec = importlib.util.spec_from_file_location("aap", str(aap_path))
        aap = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(aap)
        rc = aap.activer_agent("session-admin", agent, raison)
        return {"statut": "ok", "rc": rc}
    except Exception as exc:
        return {"erreur": str(exc)[:80]}


def status() -> dict:
    """Etat d'Oracle."""
    agents = charger_agents()
    resultats = {}
    for a in agents:
        nom = a.get("nom", "?")
        inbox_file = INBOX_DIR / f"{nom}.jsonl"
        messages = _lire_jsonl(inbox_file)
        non_lus = sum(1 for m in messages if not m.get("lu"))
        resultats[nom] = {"messages": len(messages), "non_lus": non_lus}
    return {"version": VERSION, "agents": resultats}


# --- Mode boucle (daemon resident v0.2.0) ---

def _ecrire_pid():
    try:
        with io.open(PID_FILE, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(str(os.getpid()))
    except OSError:
        pass


def _nettoyer_pid():
    try:
        PID_FILE.unlink()
    except OSError:
        pass


def _boucle_missions(max_par_tic=5):
    """Consommer les missions asap de facon AUTONOME (demande utilisateur
    2026-08-29). IMPASSE v1 : sans session Oracle vivante, les missions
    EN_ATTENTE de la file asap n etaient jamais consommees -> les agents ne
    demarraient plus (accumulation d alertes URGENT + missions en attente).
    Le daemon prend le relais : chaque tic, il rejoue la meme logique que
    `oracle.py mission-relais` (prendre la mission, historiser le DEBUT a la
    place de l agent, envoyer le message, initier le pilote) tant qu il reste
    des missions, borne a max_par_tic. Tolerant : une erreur ne tue jamais
    le daemon (jamais d epuisement ni de boucle infinie)."""
    try:
        # Reutilise la logique existante d oracle.py (source de verite
        # unique : mission-relais) + le compteur de files.py pour borner la
        # boucle sans message bruyant quand la file est vide.
        from oracle import _cmd_mission_relais, _files
        from types import SimpleNamespace as _NS
        consomme = 0
        while _files.en_attente_count("asap") > 0 and consomme < max_par_tic:
            _cmd_mission_relais(_NS(file="asap"))
            consomme += 1
        if consomme:
            print("[ORACLE-SERVER] %d mission(s) asap relayee(s) ce tic."
                  % consomme, flush=True)
    except Exception as exc:
        print("[ORACLE-SERVER] ERREUR missions : %s" % exc, flush=True)


def _boucle_tic():
    """Un tic du daemon : controle processus + harnais (surveillance)
    + relais (transmission) + missions asap (consommation autonome).
    Tolerant : une erreur ne tue jamais le daemon."""
    # 0. Controle des processus fantomes : chaque serveur v1 doit avoir
    # UNE seule instance (pid officiel du pid file). Un doublon = risque
    # de concurrence (double tic, double routing) -> alerte cerberus.
    try:
        sys.path.insert(0, str(ORACLE_DIR / "fonctions"))
        import controle_processus as _cp
        _cp_r = _cp.verifier()
        if not _cp_r.get("ok"):
            _alerte_fantomes(_cp.formatter(_cp_r))
    except Exception as exc:
        print("[ORACLE-SERVER] ERREUR controle processus : %s" % exc,
              flush=True)
    try:
        sys.path.insert(0, str(ORACLE_DIR / "fonctions"))
        import harnais_oracle as _h
        ecarts = _h.verifier()
        if ecarts:
            _h.signaler(ecarts)
    except Exception as exc:
        print("[ORACLE-SERVER] ERREUR harnais : %s" % exc, flush=True)
    try:
        sys.path.insert(0, str(ORACLE_DIR / "fonctions"))
        import relais as _r
        nb, _ = _r.relayer_hub()
        if nb:
            print("[ORACLE-SERVER] %d message(s) relaye(s)" % nb, flush=True)
    except Exception as exc:
        print("[ORACLE-SERVER] ERREUR relais : %s" % exc, flush=True)
    # Consommation AUTONOME des missions asap (demande utilisateur
    # 2026-08-29) : sans session Oracle vivante, plus rien ne consommait la
    # file -> les agents ne demarraient plus. Le daemon prend le relais.
    _boucle_missions()


def _alerte_fantomes(rapport):
    """Deposer une alerte P1 dans l inbox de cerberus : un processus
    fantome (doublon) ou un serveur mort a ete detecte."""
    try:
        import uuid
        msg = {
            "id": "fantome-" + uuid.uuid4().hex[:6],
            "de": "oracle-harnais",
            "vers": "cerberus",
            "priorite": 1,
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
            "objet": "[FANTOMES] processus concurrent(s) ou serveur mort detecte(s)",
            "corps": rapport,
            "lu": False, "accuse": False, "type": "harnais-oracle",
        }
        cible = INBOX_DIR / "cerberus.jsonl"
        cible.parent.mkdir(parents=True, exist_ok=True)
        with open(cible, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(msg, ensure_ascii=False) + "\n")
    except Exception:
        pass


def boucler(intervalle_secondes):
    """Boucle residente avec arret apres 30 min sans demande utilisateur."""
    _ecrire_pid()
    print("[ORACLE-SERVER] DEMARRAGE SERVEUR: daemon lance (tic toutes les %ds, pid %d)"
          % (intervalle_secondes, os.getpid()), flush=True)
    _historiser("oracle", "DEMARRAGE SERVEUR: oracle-server actif pid=%d" % os.getpid())
    try:
        while True:
            if _arret_si_inactif():
                print("[ORACLE-SERVER] arret automatique: dernier agent actif inactif >= 30 min", flush=True)
                return
            _boucle_tic()
            time.sleep(intervalle_secondes)
    finally:
        _nettoyer_pid()


# --- Lancement ---

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Oracle Server v0.2.0")
    parser.add_argument("--transport", default="stdio", choices=["stdio", "http"])
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--boucle", action="store_true",
                        help="Mode daemon resident (harnais + relais en boucle)")
    parser.add_argument("--intervalle", type=int, default=30,
                        help="Secondes entre deux tics (defaut 30)")
    args = parser.parse_args()

    if args.boucle:
        boucler(args.intervalle)
        return 0

    print(f"[ORACLE-SERVER] Demarrage (transport={args.transport})")
    print(f"[ORACLE-SERVER] Version: {VERSION}")
    print(f"[ORACLE-SERVER] Agents: {len(charger_agents())}")

    if args.transport == "http":
        try:
            from fastmcp import FastMCP
            mcp = FastMCP("Oracle")
            mcp.tool()(envoyer_message)
            mcp.tool()(lire_messages)
            mcp.tool()(acquitter_message)
            mcp.tool()(_marquer_accuse)
            mcp.tool()(lister_messages)
            mcp.tool()(historiser_action)
            mcp.tool()(activer_agent)
            mcp.tool()(status)
            mcp.run(transport="http", port=args.port)
        except ImportError:
            print("[ORACLE-SERVER] fastmcp non installe. Mode stdio.")
            args.transport = "stdio"

    if args.transport == "stdio":
        # Mode stdio : boucle de lecture de commandes JSON
        print("[ORACLE-SERVER] Mode stdio - en attente de commandes JSON...")
        for ligne in sys.stdin:
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                cmd = json.loads(ligne)
            except json.JSONDecodeError:
                print(json.dumps({"erreur": "JSON invalide"}))
                continue
            action = cmd.get("action", "")
            if action == "envoyer":
                r = envoyer_message(cmd["de"], cmd["vers"], cmd["objet"], cmd["corps"], cmd.get("priorite", 2))
            elif action == "lire":
                r = lire_messages(cmd["agent"])
            elif action == "reagir":
                r = _marquer_accuse(cmd["agent"], cmd["id"], cmd.get("reaction", ""))
            elif action == "acquitter":
                r = acquitter_message(cmd["agent"], cmd["id"])
            elif action == "lister":
                r = lister_messages(cmd["agent"])
            elif action == "historiser":
                r = historiser_action(cmd["agent"], cmd["raison"], cmd.get("type", "R"))
            elif action == "activer":
                r = activer_agent(cmd["agent"], cmd["raison"])
            elif action == "status":
                r = status()
            else:
                r = {"erreur": f"Action inconnue: {action}"}
            print(json.dumps(r, ensure_ascii=False))


if __name__ == "__main__":
    main()
