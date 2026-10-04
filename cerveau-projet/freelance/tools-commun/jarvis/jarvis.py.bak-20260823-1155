#!/usr/bin/env python3
"""
JARVIS -- Outil de communication inter-agents (v2 freelance)

Usage:
    python3 jarvis.py envoyer --de <exp> --vers <dest> --priorite <1-5> --objet "<obj>" --corps "<corps>"
    python3 jarvis.py lire --agent <agent>
    python3 jarvis.py acquitter --agent <agent> --id <id>
    python3 jarvis.py lister --agent <agent> [--tous]
    python3 jarvis.py bloques
    python3 jarvis.py activer --agent <agent> --mission "..." [--session <session>] [--de <expediteur>]
"""

import argparse
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

JARVIS_DIR = Path(__file__).parent
INBOX_DIR = JARVIS_DIR / "inbox"
OUTBOX_DIR = JARVIS_DIR / "outbox"

# v0.1.1 (bootstrap autorise par l'utilisateur 2026-08-23) : la liste des
# agents est lue depuis jarvis-data.json (D15). Vision fait foi ensuite.
# v0.3.0 : agents = [{nom, role, fiche, corrections}, ...]
def _charger_donnees_agents():
    chemin = Path(__file__).parent / "jarvis-data.json"
    try:
        donnees = json.loads(chemin.read_text(encoding="utf-8"))["agents"]
    except (OSError, ValueError, KeyError):
        return {}
    return {a["nom"]: a for a in donnees if isinstance(a, dict) and "nom" in a}


AGENTS_INFOS = _charger_donnees_agents()
AGENTS_VALIDES = set(AGENTS_INFOS)


def get_inbox(agent: str) -> Path:
    return INBOX_DIR / f"{agent}.jsonl"


def get_outbox(agent: str) -> Path:
    return OUTBOX_DIR / f"{agent}.jsonl"


def lire_jsonl(path: Path) -> list[dict]:
    """Lire un fichier JSONL et retourner la liste de messages."""
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


def ecrire_jsonl(path: Path, messages: list[dict]):
    """Ecrire une liste de messages en JSONL."""
    with open(path, "w", encoding="utf-8") as f:
        for msg in messages:
            f.write(json.dumps(msg, ensure_ascii=False) + "\n")


def ajouter_message(path: Path, message: dict):
    """Ajouter un message a la fin d'un fichier JSONL."""
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(message, ensure_ascii=False) + "\n")


def maj_bloc_session(session: str, agent: str, raison: str = "") -> bool:
    """v0.3.0 (Vision) : active le destinataire dans AGENTS.md - met a jour
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
    # restaurer l'entete exacte si elle a ete alternee
    lignes[debut] = f"### Session : {session}"
    AGENTS_FILE.write_text("\n".join(lignes), encoding="utf-8")
    return True


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

    # Ecrire dans l'inbox du destinataire
    ajouter_message(get_inbox(vers), message)
    # Ecrire dans l'outbox de l'expediteur
    ajouter_message(get_outbox(de), message)

    # Historiser (seul JARVIS ecrit l'historique)
    # v0.3.1 : --type R|IR - les interventions INTER-ROUND doivent etre
    # tracees IR (colonne type de l historique), plus jamais tout en R.
    # v0.5.0 : --sans-historique pour le technique/test (fluidite).
    if not getattr(args, "sans_historique", False):
        historiser(de, f"Envoie a {vers}: {objet}",
                   getattr(args, "type_action", "R"),
                   session=getattr(args, "session", ""))

    # v0.3.0 (Vision) : --activer = le message DECLENCHE l'activation du
    # destinataire (transparence : le round ne s'arrete jamais).
    if getattr(args, "activer", False):
        if vers == de:
            print("ERREUR: --activer impossible vers soi-meme")
            sys.exit(1)
        ok = maj_bloc_session(getattr(args, "session", ""), vers,
                              raison=f"Relais de {de}: {objet}")
        # v0.6.1 : livraison directe (affichage = livraison)
        _marquer_lu(vers, [message["id"]])
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


def _marquer_lu(agent, ids):
    """v0.5.0 (Vision) : marquer lu+accuse une liste d'IDs dans l'inbox de
    l'agent ET l'outbox de chaque expediteur. Retourne le nb marques."""
    messages = lire_jsonl(get_inbox(agent))
    marques = 0
    expediteurs = {}
    for m in messages:
        if m.get("id") in ids and not m.get("lu"):
            m["lu"] = True
            m["accuse"] = True
            marques += 1
            expediteurs.setdefault(m.get("de"), []).append(m["id"])
    if marques:
        ecrire_jsonl(get_inbox(agent), messages)
        for exp, exp_ids in expediteurs.items():
            try:
                outbox_msgs = lire_jsonl(get_outbox(exp))
            except OSError:
                continue
            modifie = False
            for m in outbox_msgs:
                if m.get("id") in exp_ids and not m.get("lu"):
                    m["lu"] = True
                    m["accuse"] = True
                    modifie = True
            if modifie:
                ecrire_jsonl(get_outbox(exp), outbox_msgs)
    return marques


def cmd_lire(args):
    """Lire les messages en attente d'un agent.
    v0.5.0 (Vision) : auto-accuse des P3-P5 des la lecture - seuls P1/P2
    exigent un acquittement explicite (fluidite de l'intercom)."""
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

    # v0.5.0 : auto-accuse P3-P5
    auto = [m["id"] for m in non_lus if m.get("priorite", 5) >= 3]
    n_auto = _marquer_lu(agent, auto)
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


# ---- files d'attente (v0.6.0 - protocole 13 UR-1/AT-1) ----

FILES_DIR = Path(__file__).parent / "files"


def _chemin_file(nom):
    return FILES_DIR / f"{nom}.jsonl"


def cmd_mettre_en_attente(args):
    """Protocole 13 v2 : placer une mission en file selon le declencheur.
    --niveau attente/attention/urgent determine file et statut."""
    niveaux = {
        "attente":  ("file-attente", "EN_ATTENTE", "ATTENTE"),
        "attention": ("file-asap",   "SUIVANTE",   "AT-1"),
        "urgent":   ("file-attente", "PRIORITAIRE", "UR-1"),
    }
    niveau = getattr(args, "niveau", None) or (
        "attente" if args.file == "file-attente" else "attention")
    file, statut, type_declencheur = niveaux[niveau]
    entree = {
        "type": type_declencheur,
        "mission": args.mission,
        "agent": args.agent,
        "contexte_avant": args.contexte,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "statut": statut,
    }
    with open(_chemin_file(file), "a", encoding="utf-8") as f:
        f.write(json.dumps(entree, ensure_ascii=False) + "\n")
    # v0.6.2 (URGENT) : l'intervention de JARVIS doit etre TRACEE
    historiser("jarvis", f"Mise en attente [{niveau}] ({file}): "
               f"{args.mission[:60]}",
               "R", session=getattr(args, "session", ""))
    print(f"[JARVIS] Mission placee en {file} (statut: {statut}, "
          f"declencheur: [{niveau}]).")
    print(f"  Mission: {args.mission}")
    if args.contexte:
        print(f"  Contexte de reprise: {args.contexte}")


def cmd_stop_dev(args):
    """[stop] DEFCON 5 : arret complet du dev. Gele TOUTES les missions
    en files et enregistre la raison dans files/defcon.jsonl."""
    raison = args.raison
    gelees = 0
    for nom in ("file-attente", "file-asap"):
        chemin = _chemin_file(nom)
        if not chemin.exists():
            continue
        lignes = [l for l in chemin.read_text(encoding="utf-8").splitlines()
                  if l.strip()]
        modifie = False
        for i, l in enumerate(lignes):
            try:
                e = json.loads(l)
            except ValueError:
                continue
            if e.get("statut") in ("EN_ATTENTE", "PREPAREE", "SUIVANTE",
                                   "PRIORITAIRE"):
                e["statut"] = "DEFCON5"
                lignes[i] = json.dumps(e, ensure_ascii=False)
                modifie = True
                gelees += 1
        if modifie:
            chemin.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    defcon = {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "raison": raison,
        "missions_gelees": gelees,
        "declare_par": "utilisateur via stark",
    }
    (FILES_DIR / "defcon.jsonl").parent.mkdir(exist_ok=True)
    with open(FILES_DIR / "defcon.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(defcon, ensure_ascii=False) + "\n")
    historiser("jarvis", f"[STOP] DEFCON 5 - arret du dev: {raison[:60]}",
               "R", session=getattr(args, "session", ""))
    print(f"[JARVIS] *** [STOP] DEFCON 5 - ARRET COMPLET DU DEV ***")
    print(f"  Raison: {raison}")
    print(f"  Missions gelees: {gelees}")
    print(f"  Toute reprise exige une decision explicite de l'utilisateur.")


def cmd_file(args):
    """Lister les deux files d'attente."""
    for nom in ("file-attente", "file-asap"):
        chemin = _chemin_file(nom)
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
        print(f"[{nom}] {len(entrees)} entree(s)")
        for e in entrees:
            print(f"  [{e.get('statut')}] {e.get('mission', '')[:70]}"
                  f" ({e.get('date', '')})")


def cmd_reprendre(args):
    """Protocole 13 v2 : reprendre la mission prioritaire.
    Ordre : PRIORITAIRE > SUIVANTE > EN_ATTENTE/PREPAREE."""
    ordre = ["PRIORITAIRE", "SUIVANTE", "EN_ATTENTE", "PREPAREE"]
    fichiers = [("file-attente", _chemin_file("file-attente")),
                ("file-asap", _chemin_file("file-asap"))]
    if getattr(args, "file", None) and args.file != "file-attente":
        fichiers = [f for f in fichiers if f[0] == args.file]
    # chercher la mission la plus prioritaire, de la plus recente a l'ancienne
    candidates = []
    for nom, chemin in fichiers:
        if not chemin.exists():
            continue
        lignes = [l for l in chemin.read_text(encoding="utf-8").splitlines()
                  if l.strip()]
        for i in range(len(lignes) - 1, -1, -1):
            try:
                e = json.loads(lignes[i])
            except ValueError:
                continue
            statut = e.get("statut")
            if statut in ordre:
                candidates.append((ordre.index(statut), len(candidates), nom,
                                   chemin, lignes, i, e))
    if not candidates:
        print("[JARVIS] Aucune mission en attente.")
        return
    _, _, nom, chemin, lignes, i, e = min(candidates,
                                          key=lambda c: (c[0], -c[1]))
    e["statut"] = "REPRISE"
    e["date_reprise"] = datetime.now(timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%S")
    lignes[i] = json.dumps(e, ensure_ascii=False)
    chemin.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print(f"[JARVIS] Mission reprise depuis {nom} :")
    print(f"  Mission: {e.get('mission')}")
    if e.get("contexte_avant"):
        print(f"  Contexte avant mise en attente: {e['contexte_avant']}")
    historiser("jarvis",
               f"Reprise de mission depuis {nom}: "
               f"{e.get('mission', '')[:50]}",
               "R", session=getattr(args, "session", ""))


def cmd_recu(args):
    """v0.5.0 (Vision) : lire + acquitter TOUT en un seul appel.
    Usage : jarvis.py recu --agent <agent>
    Fluidite : remplace lire + acquitter xN (2-3 appels -> 1)."""
    agent = args.agent.lower()
    if agent not in AGENTS_VALIDES:
        print(f"ERREUR: agent inconnu '{agent}'")
        sys.exit(1)
    messages = lire_jsonl(get_inbox(agent))
    non_lus = [m for m in messages if not m.get("lu", False)]
    if not non_lus:
        print(f"[JARVIS] recu {agent}: rien en attente.")
        return
    _marquer_lu(agent, [m["id"] for m in non_lus])
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

    # Aussi marquer dans l'outbox de l'expediteur
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

    # 1. Envoyer le message d'activation dans l'inbox de l'agent
    # v0.2.0 (Vision) : incarnation obligatoire - l agent lit SA fiche et
    # SES corrections AVANT de commencer.
    message = {
        "id": str(uuid.uuid4())[:8],
        "de": expediteur,
        "vers": agent,
        "priorite": 1,  # BLOQUANT - l'agent doit lire avant de demarrer
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
    ajouter_message(get_inbox(agent), message)
    ajouter_message(get_outbox(expediteur), message)

    # v0.6.1 (Vision) : livraison directe - l'affichage EST la livraison.
    # Le message d'activation est marque lu+accuse a l'emission : l'agent
    # demarre directement, plus de lire/acquitter obligatoire apres
    # activation. Les autres P1/P2 gardent le parcours explicite.
    _marquer_lu(agent, [message["id"]])
    historiser(agent, f"Active par {expediteur}: {mission[:80]}", "R", session=session)

    # v0.3.0 (Vision) : l'activation met a jour le bloc session AGENTS.md
    ok = maj_bloc_session(session, agent,
                          raison=f"Active par {expediteur}: {mission[:80]}")

    print(f"[JARVIS] Agent '{agent}' active via JARVIS.")
    print(f"  Expediteur: {expediteur}")
    print(f"  Session: {session}")
    print(f"  Mission: {mission}")
    print(f"  Bloc session AGENTS.md: {'mis a jour' if ok else 'INTROUVABLE'}")
    print(f"  ID: {message['id']}")
    print(f"  MISSION INJECTEE - DEMARRE DIRECTEMENT (livree = affichee).")


def main():
    parser = argparse.ArgumentParser(description="JARVIS -- Communication inter-agents")
    subparsers = parser.add_subparsers(dest="commande", help="Commande")

    # envoyer
    p_env = subparsers.add_parser("envoyer", help="Envoyer un message")
    p_env.add_argument("--de", required=True, help="Expediteur")
    p_env.add_argument("--vers", required=True, help="Destinataire")
    p_env.add_argument("--priorite", type=int, default=3, choices=range(1, 6), help="Priorite (1-5)")
    p_env.add_argument("--objet", required=True, help="Objet du message")
    p_env.add_argument("--corps", required=True, help="Corps du message")
    p_env.add_argument("--session", default="", help="Session (pour historiser le bon Nom LLM)")
    p_env.add_argument("--activer", action="store_true",
                       help="Le message declenche l'activation du destinataire (le round continue)")
    p_env.add_argument("--type", dest="type_action", default="R", choices=["R", "IR"],
                       help="Type d'intervention : R (round) ou IR (inter-round)")
    p_env.add_argument("--sans-historique", dest="sans_historique", action="store_true",
                       help="Ne pas ecrire dans l'historique (messages techniques/test)")

    # recu (v0.5.0)
    p_recu = subparsers.add_parser("recu",
                                   help="Lire + acquitter tout en un appel (fluidite)")
    p_recu.add_argument("--agent", required=True, help="Agent")

    # lire
    p_lire = subparsers.add_parser("lire", help="Lire les messages en attente")
    p_lire.add_argument("--agent", required=True, help="Agent")

    # acquitter
    p_acq = subparsers.add_parser("acquitter", help="Acquitter un message")
    p_acq.add_argument("--agent", required=True, help="Agent")
    p_acq.add_argument("--id", required=True, help="ID du message")

    # lister
    p_list = subparsers.add_parser("lister", help="Lister les messages")
    p_list.add_argument("--agent", required=True, help="Agent")
    p_list.add_argument("--tous", action="store_true", help="Inclure les messages lus")

    # bloques
    subparsers.add_parser("bloques", help="Lister les agents bloques")

    # activer
    p_act = subparsers.add_parser("activer", help="Activer un agent via JARVIS")
    p_act.add_argument("--agent", required=True, help="Agent a activer")
    p_act.add_argument("--session", required=True, help="Session cible (convention session-llm-N)")
    p_act.add_argument("--mission", required=True, help="Mission de l agent")
    p_act.add_argument("--de", default="stark", help="Expediteur (defaut: stark)")

    # historiser
    p_hist = subparsers.add_parser("historiser", help="Enregistrer dans l'historique")
    p_hist.add_argument("--agent", required=True, help="Agent")
    p_hist.add_argument("--raison", required=True, help="Raison de l'action")
    p_hist.add_argument("--type", default="R", help="Type: R=Round, IR=Inter-round")
    p_hist.add_argument("--session", default="", help="Session (pour lire le Nom LLM dans AGENTS.md)")

    # files d'attente (protocole 13 v2 - 6 declencheurs)
    p_meatt = subparsers.add_parser(
        "mettre-en-attente",
        help="placer une mission en file selon le declencheur")
    p_meatt.add_argument("--mission", required=True, help="Mission en cours")
    p_meatt.add_argument("--contexte", default="", help="Contexte de reprise")
    p_meatt.add_argument("--niveau", default=None,
                         choices=["attente", "attention", "urgent"],
                         help="[attente]=file normale / [attention]=SUIVANTE / [urgent]=PRIORITAIRE")
    p_meatt.add_argument("--file", default=None,
                         choices=["file-attente", "file-asap"],
                         help="(compat) file cible si --niveau absent")
    p_meatt.add_argument("--agent", default="", help="Agent porteur (optionnel)")

    subparsers.add_parser("file", help="Lister les files d'attente")

    p_rep = subparsers.add_parser(
        "reprendre",
        help="Reprendre la mission la plus prioritaire (PRIORITAIRE > SUIVANTE > EN_ATTENTE)")
    p_rep.add_argument("--file", default=None,
                       choices=["file-attente", "file-asap"],
                       help="(option) restreindre a une seule file")

    p_stop = subparsers.add_parser(
        "stop-dev",
        help="[stop] DEFCON 5 : arret complet du dev, gel de toutes les missions")
    p_stop.add_argument("--raison", required=True, help="Raison de l'arret")

    args = parser.parse_args()

    if args.commande == "envoyer":
        cmd_envoyer(args)
    elif args.commande == "lire":
        cmd_lire(args)
    elif args.commande == "acquitter":
        cmd_acquitter(args)
    elif args.commande == "recu":
        cmd_recu(args)
    elif args.commande == "mettre-en-attente":
        cmd_mettre_en_attente(args)
    elif args.commande == "file":
        cmd_file(args)
    elif args.commande == "reprendre":
        cmd_reprendre(args)
    elif args.commande == "stop-dev":
        cmd_stop_dev(args)
    elif args.commande == "lister":
        cmd_lister(args)
    elif args.commande == "activer":
        cmd_activer(args)
    elif args.commande == "bloques":
        cmd_bloques(args)
    elif args.commande == "historiser":
        cmd_historiser(args)
    else:
        parser.print_help()


# --- HISTORIQUE ---
RACINE = Path(__file__).parent.parent.parent.parent.parent
HISTORIQUE_FILE = RACINE / "AGENTS-historique.md"
AGENTS_FILE = Path(os.environ.get("AGENTS_FILE", str(RACINE / "AGENTS.md")))


def lire_nom_llm(session: str = "") -> str:
    """Lit le champ 'Nom LLM' du bloc session dans AGENTS.md (jamais de valeur en dur)."""
    try:
        contenu = AGENTS_FILE.read_text(encoding="utf-8")
    except FileNotFoundError:
        return "inconnu"
    lignes = contenu.split("\n")
    if session:
        debut = None
        for i, ligne in enumerate(lignes):
            if ligne.strip() == f"### Session : {session}":
                debut = i
                break
        if debut is None:
            return "inconnu"
        fin = debut
        while fin < len(lignes) and not lignes[fin].startswith("## "):
            fin += 1
        bloc = lignes[debut:fin]
    else:
        bloc = lignes
    for ligne in bloc:
        if "**Nom LLM**" in ligne:
            parties = [p.strip() for p in ligne.split("|")]
            for j, p in enumerate(parties):
                if p == "**Nom LLM**" and j + 1 < len(parties):
                    return parties[j + 1]
    return "inconnu"


def historiser(agent: str, raison: str, type_action: str = "R", session: str = ""):
    """JARVIS enregistre une entree dans AGENTS-historique.md."""
    now = datetime.now()
    heure = now.strftime("%H:%M:%S.%f")[:15]
    llm = lire_nom_llm(session)
    try:
        contenu = HISTORIQUE_FILE.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"[JARVIS] ERREUR: {HISTORIQUE_FILE} introuvable")
        return False
    lignes = contenu.split("\n")
    idx_tableau = -1
    for i, ligne in enumerate(lignes):
        if "| Heure | Agent |" in ligne:
            idx_tableau = i
            break
    if idx_tableau == -1:
        print("[JARVIS] ERREUR: Section Activites recentes non trouvee")
        return False
    nouvelle_entree = f"| {heure} | {agent} | {llm} | {type_action} | {raison} |"
    idx_separateur = idx_tableau + 1
    while idx_separateur < len(lignes) and not lignes[idx_separateur].startswith("|---"):
        idx_separateur += 1
    insert_pos = idx_separateur + 1
    lignes.insert(insert_pos, nouvelle_entree)
    debut_entrees = insert_pos + 1
    fin_entrees = debut_entrees
    while fin_entrees < len(lignes) and lignes[fin_entrees].startswith("| "):
        fin_entrees += 1
    nb_entrees = fin_entrees - debut_entrees
    if nb_entrees > 10:
        # les entrees sont triees plus recent en haut : les plus vieilles sont en BAS
        lignes = lignes[:fin_entrees - (nb_entrees - 10)] + lignes[fin_entrees:]
    HISTORIQUE_FILE.write_text("\n".join(lignes), encoding="utf-8")
    print(f"[JARVIS] Historique: {agent} a {heure}")
    return True


def cmd_historiser(args):
    historiser(args.agent, args.raison, args.type, session=getattr(args, "session", ""))


if __name__ == "__main__":
    main()

