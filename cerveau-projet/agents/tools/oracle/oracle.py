#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
Oracle v0.5.0 -- CLI de coordination des agents v1

Equivalent de JARVIS pour la session-admin (v1).
Route les messages, gere les activations, historise les actions.

Commandes:
    envoyer <de> <vers> <objet> <corps>   Envoyer un message
    lire <agent>                           Lire les messages non lus d un agent
    lire-message <id>                      Lire un message par son ID
    acquitter <agent> <id>                 Acquitter un message
    lister <agent>                         Lister les messages
    agents                                 Liste des agents avec statut
    nettoyer                               Supprimer les messages lus > 7j
    verifier                               Verifier la coherence inbox/outbox
    historiser <agent> <raison> [type]      Historiser une action
    activer <agent> <raison>               Activer un agent (dellegue a activer-agent-principal)
    sessions                               Lister les sessions actives
    status [--detail]                      Etat d Oracle
    help                                   Afficher cette aide

Fichier de config: oracle-data.json (meme principe que jarvis-data.json)
"""

import json
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path

VERSION = "0.5.2"

# Modules fonctions
_fonctions_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "fonctions")
if _fonctions_dir not in sys.path:
    sys.path.insert(0, _fonctions_dir)

import defcon as _defcon
import files as _files
import harnais_oracle as _harnais
import pilote as _pilote
import relais as _relais
import controle_processus as _controle_processus


def _cmd_defcon(args):
    _defcon.cmd_defcon(args)


def _cmd_defcon_changer(args):
    _defcon.cmd_changer_defcon(args)


def _cmd_defcon_declarer(args):
    _defcon.cmd_declarer(args)


def _cmd_defcon_escaler(args):
    _defcon.cmd_escaler_defcon(args)


def _cmd_mission_ajouter(args):
    _files.cmd_mission_ajouter(args)


def _cmd_mission_prendre(args):
    _files.cmd_mission_prendre(args)


def _cmd_mission_terminer(args):
    _files.cmd_mission_terminer(args)


def _cmd_mission_lister(args):
    _files.cmd_mission_lister(args)


def _cmd_harnais(args):
    _harnais.cmd_harnais(args)


def _cmd_relais(args):
    _relais.cmd_relais(args)


def _cmd_controle_processus(args):
    """Controle des processus v1 : verifie qu un seul processus tourne
    par serveur (oracle-server, routines-server v1). Signale tout
    doublon (processus fantome) et tout serveur mort."""
    resume = _controle_processus.verifier()
    print(_controle_processus.formatter(resume))
    if not resume.get("ok"):
        print("\n[ORACLE] ACTION REQUISE : arreter les fantomes ou relancer "
              "le serveur mort via oracle-demarrage.")
        return 1
    return 0


def _cmd_pilote(args):
    """Piloter la carte d un agent (maitre d hotel, vision 2026-08-27).

    Oracle prend le controle de la carte de l agent actif : lit la case
    courante, resout les questions verrouillees, sert chaque commande
    outil, avance jusqu a une decision libre ou la fin. L agent est un
    invite servi sur un plateau - n a plus qu a executer ce qu Oracle
    sert."""
    _pilote.cmd_pilote(args)


def _cmd_reactiver_fin(args):
    """Piloter la reintegration du maillon precedent avec pose du FIN.

    Oracle (maitre d hotel) : quand l agent a termine SA carte, il pose
    FIN:<bilan> sur lui (colonne Debut/Fin) puis reactiver le maillon
    precedent (celui qui l avait active) ou Cerberus pour la fin de
    chaine - le round ne se brise jamais a la main de l agent."""
    print(_pilote._reactiver_maillon(args.agent, args.bilan))


def _cmd_dashboard(args):
    """Vue d'ensemble temps reel : DEFCON, missions, messages, agents."""
    print("=" * 60)
    print(" ORACLE DASHBOARD - v%s" % VERSION)
    print("=" * 60)
    # DEFCON
    niveau = _defcon.niveau_courant()
    if niveau:
        print(f"  DEFCON: niveau {niveau} ({_defcon.ECHELLE.get(niveau, '?')})")
    else:
        print("  DEFCON: fonctionnement normal")
    print()
    # Missions
    missions = _files.lister()
    en_attente = sum(1 for m in missions if m.get("statut") == "EN_ATTENTE")
    print(f"  Missions: {len(missions)} total, {en_attente} en attente")
    for m in missions:
        if m.get("statut") == "EN_ATTENTE":
            print(f"    * [{m['_file']}] {m['id']} : {m['mission'][:50]}")
    print()
    # Messages non lus par agent
    print("  Messages non lus:")
    total_non_lus = 0
    agents = charger_agents()
    for a in agents:
        nom = a.get("nom", "?")
        inbox = INBOX_DIR / f"{nom}.jsonl"
        non_lus = 0
        if inbox.exists():
            with open(inbox, encoding="utf-8") as fh:
                for ligne in fh:
                    ligne = ligne.strip()
                    if not ligne:
                        continue
                    try:
                        msg = json.loads(ligne)
                        if isinstance(msg, dict) and not msg.get("lu"):
                            non_lus += 1
                    except (json.JSONDecodeError, ValueError):
                        continue
        if non_lus > 0:
            print(f"    - {nom}: {non_lus} non lu(s)")
            total_non_lus += non_lus
    if total_non_lus == 0:
        print("    - aucun message en attente")
    print()
    # Harnais (dernier scan)
    ecarts = _harnais.verifier()
    if ecarts:
        print(f"  Harnais: {len(ecarts)} ecart(s)")
        for e in ecarts[:5]:
            print(f"    ! [{e['type']}] {e['message'][:60]}")
    else:
        print("  Harnais: 0 ecart - tout va bien")
    print("=" * 60)

# Racine du projet (detectee dynamiquement)
RACINE = Path(__file__).parent.parent.parent.parent.parent  # oracle/ -> tools/ -> agents/ -> cerveau-projet/ -> racine

# --- Configuration ---
ORACLE_DIR = Path(__file__).parent
INBOX_DIR = ORACLE_DIR / "inbox"
OUTBOX_DIR = ORACLE_DIR / "outbox"
FILES_DIR = ORACLE_DIR / "files"
DATA_FILE = ORACLE_DIR / "oracle-data.json"
HISTORIQUE_BDD = ORACLE_DIR / "historique"

# Creer les dossiers
INBOX_DIR.mkdir(exist_ok=True)
OUTBOX_DIR.mkdir(exist_ok=True)
HISTORIQUE_BDD.mkdir(exist_ok=True)


def charger_agents():
    """Liste des agents depuis oracle-data.json."""
    if not DATA_FILE.exists():
        return []
    try:
        with open(DATA_FILE, encoding="utf-8") as f:
            return json.load(f).get("agents", [])
    except (json.JSONDecodeError, OSError):
        return []


def agent_valide(nom):
    """Verifier si un agent est declare."""
    agents = charger_agents()
    return any(a.get("nom") == nom for a in agents)


# --- Messages ---

def cmd_envoyer(args):
    """Envoyer un message entre agents."""
    msg = {
        "id": uuid.uuid4().hex[:8],
        "de": args.de,
        "vers": args.vers,
        "priorite": getattr(args, "priorite", 2),
        "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "objet": args.objet,
        "corps": args.corps,
        "lu": False,
        "accuse": False
    }
    outbox_file = OUTBOX_DIR / f"{args.de}.jsonl"
    with open(outbox_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(msg, ensure_ascii=False) + "\n")
    inbox_file = INBOX_DIR / f"{args.vers}.jsonl"
    with open(inbox_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(msg, ensure_ascii=False) + "\n")
    print(f"[ORACLE] Message envoye: {args.de} -> {args.vers} (id={msg['id']})")
    # Historisation automatique
    _historiser_auto(args.de, f"Envoyer a {args.vers}: {args.objet[:50]}")


def cmd_lire(args):
    """Lire les messages non lus d'un agent."""
    inbox_file = INBOX_DIR / f"{args.agent}.jsonl"
    if not inbox_file.exists():
        print(f"[ORACLE] Aucun message pour {args.agent}")
        return
    with open(inbox_file, encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                msg = json.loads(ligne)
            except json.JSONDecodeError:
                continue
            if not isinstance(msg, dict) or not msg.get("lu"):
                statut = "PRIORITE 1" if msg.get("priorite") == 1 else ""
                print(f"  [{msg.get('id', '?')}] {msg.get('de', '?')} -> {msg.get('vers', '?')} {statut}")
                print(f"    Objet: {msg.get('objet', '')}")
                print(f"    Corps: {msg.get('corps', '')[:100]}")
                print()


def _historiser_auto(agent, raison, agent_effectif="Oracle"):
    """Historisation automatique (silencieuse).

    agent_effectif : agent affiche dans la colonne Agent du tableau.
    Defaut Oracle (pour les actions propres d Oracle : envoyer, acquitter).
    Pour les activations : passer l agent cible pour que le tableau
    affiche le bon nom.
    """
    try:
        import importlib.util
        aap_path = os.path.join(
            os.path.dirname(ORACLE_DIR),
            "activer", "activer-agent-principal", "activer-agent-principal.py"
        )
        if not os.path.isfile(aap_path):
            return
        spec = importlib.util.spec_from_file_location("aap", aap_path)
        aap = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(aap)
        aap.ajouter_historique(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S.000"),
            "session-admin", agent, raison, "R",
            agent_effectif=agent_effectif,
            executeur="Oracle")
    except Exception:
        pass


def cmd_acquitter(args):
    """Marquer un message comme lu."""
    inbox_file = INBOX_DIR / f"{args.agent}.jsonl"
    if not inbox_file.exists():
        print(f"[ORACLE] Aucun fichier pour {args.agent}")
        return
    lignes = []
    trouve = False
    with open(inbox_file, encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                msg = json.loads(ligne)
                if isinstance(msg, dict) and msg.get("id") == args.id:
                    msg["lu"] = True
                    msg["accuse"] = True
                    trouve = True
                lignes.append(json.dumps(msg, ensure_ascii=False))
            except json.JSONDecodeError:
                lignes.append(ligne)
    if trouve:
        with open(inbox_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lignes) + "\n")
        print(f"[ORACLE] Message {args.id} acquitte pour {args.agent}")
        _historiser_auto(args.agent, f"Acquittement message {args.id}")
    else:
        print(f"[ORACLE] Message {args.id} non trouve pour {args.agent}")


def cmd_lister(args):
    """Lister tous les messages d'un agent (lus et non lus)."""
    inbox_file = INBOX_DIR / f"{args.agent}.jsonl"
    if not inbox_file.exists():
        print(f"[ORACLE] Aucun message pour {args.agent}")
        return
    total = 0
    non_lus = 0
    with open(inbox_file, encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                msg = json.loads(ligne)
                total += 1
                if not isinstance(msg, dict) or not msg.get("lu"):
                    non_lus += 1
            except json.JSONDecodeError:
                continue
    print(f"[ORACLE] {args.agent}: {total} message(s), {non_lus} non lu(s)")


def cmd_historiser(args):
    """Historiser une action dans la BDD et le corps AGENTS-historique.md."""
    import importlib.util
    aap_path = os.path.join(
        os.path.dirname(ORACLE_DIR),
        "activer", "activer-agent-principal", "activer-agent-principal.py"
    )
    if not os.path.isfile(aap_path):
        print(f"[ORACLE] ERREUR: activer-agent-principal.py introuvable: {aap_path}")
        return
    spec = importlib.util.spec_from_file_location("aap", aap_path)
    aap = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(aap)
    type_action = getattr(args, "type", "R") or "R"
    if args.raison.upper().startswith(("INTER-ROUND", "FIN D INTER-ROUND")):
        type_action = "IR"
    rc = aap.ajouter_historique(
        datetime.now().strftime("%Y-%m-%d %H:%M:%S.000"),
        "session-admin",
        args.agent,
        args.raison,
        type_action
    )
    if rc == 0:
        print(f"[ORACLE] Historise: {args.agent} | {args.raison[:60]}")
    else:
        print(f"[ORACLE] ERREUR historisation (rc={rc})")


def _lire_tous_messages():
    """Lire tous les messages de tous les inbox/outbox."""
    tous = []
    for dossier in [INBOX_DIR, OUTBOX_DIR]:
        if not dossier.exists():
            continue
        for f in dossier.glob("*.jsonl"):
            with open(f, encoding="utf-8") as fh:
                for ligne in fh:
                    ligne = ligne.strip()
                    if not ligne:
                        continue
                    try:
                        msg = json.loads(ligne)
                        if not isinstance(msg, dict):
                            continue
                        msg["_fichier"] = str(f)
                        msg["_source"] = "inbox" if "inbox" in str(f) else "outbox"
                        tous.append(msg)
                    except json.JSONDecodeError:
                        continue
    return tous


def cmd_nettoyer(args):
    """Supprimer les messages lus de plus de 7 jours."""
    from datetime import timedelta
    seuil = datetime.now() - timedelta(days=7)
    supprimes = 0
    for dossier in [INBOX_DIR, OUTBOX_DIR]:
        if not dossier.exists():
            continue
        for f in dossier.glob("*.jsonl"):
            messages = []
            with open(f, encoding="utf-8") as fh:
                for ligne in fh:
                    ligne = ligne.strip()
                    if not ligne:
                        continue
                    try:
                        msg = json.loads(ligne)
                        messages.append(msg)
                    except json.JSONDecodeError:
                        continue
            avant = len(messages)
            gardes = []
            for msg in messages:
                if not isinstance(msg, dict) or not msg.get("lu"):
                    gardes.append(msg)
                    continue
                try:
                    date_msg = datetime.strptime(msg.get("date", "")[:19], "%Y-%m-%dT%H:%M:%S")
                    if date_msg > seuil:
                        gardes.append(msg)
                    else:
                        supprimes += 1
                except (ValueError, TypeError):
                    gardes.append(msg)
            if len(gardes) < avant:
                with open(f, "w", encoding="utf-8") as fh:
                    for msg in gardes:
                        fh.write(json.dumps(msg, ensure_ascii=False) + "\n")
    print(f"[ORACLE] Nettoyage: {supprimes} message(s) supprime(s) (lus > 7j)")


def cmd_agents(args):
    """Liste des agents avec leur statut."""
    agents = charger_agents()
    print(f"[ORACLE] {len(agents)} agent(s) declare(s):")
    print()
    for a in agents:
        nom = a.get("nom", "?")
        role = a.get("role", "?")
        # Verifier fiche
        fiche = a.get("fiche", "")
        fiche_ok = os.path.isfile(os.path.join(RACINE, fiche)) if fiche else False
        # Verifier corrections (dossier meme nom que l agent)
        agent_dir = os.path.dirname(fiche) if fiche else ""
        corrections = os.path.join(agent_dir, "corrections.md") if agent_dir else ""
        corr_ok = os.path.isfile(os.path.join(RACINE, corrections)) if corrections else False
        # Messages non lus
        inbox = INBOX_DIR / f"{nom}.jsonl"
        non_lus = 0
        if inbox.exists():
            with open(inbox, encoding="utf-8") as fh:
                for ligne in fh:
                    try:
                        msg = json.loads(ligne.strip())
                        if not isinstance(msg, dict) or not msg.get("lu"):
                            non_lus += 1
                    except (json.JSONDecodeError, ValueError):
                        continue
        statut_fiche = "OK" if fiche_ok else "MANQUANT"
        statut_corr = "OK" if corr_ok else "MANQUANT"
        statut_msg = f"{non_lus} non lu(s)" if non_lus > 0 else "0"
        print(f"  {nom:15s} | {role:30s} | fiche: {statut_fiche:8s} | corr: {statut_corr:8s} | msg: {statut_msg}")


def cmd_lire_message(args):
    """Lire un message par son ID."""
    for dossier in [INBOX_DIR, OUTBOX_DIR]:
        if not dossier.exists():
            continue
        for f in dossier.glob("*.jsonl"):
            with open(f, encoding="utf-8") as fh:
                for ligne in fh:
                    ligne = ligne.strip()
                    if not ligne:
                        continue
                    try:
                        msg = json.loads(ligne)
                    except json.JSONDecodeError:
                        continue
                    if isinstance(msg, dict) and msg.get("id") == args.id:
                        print(f"[ORACLE] Message {args.id}:")
                        print(f"  De: {msg.get('de', '?')}")
                        print(f"  Vers: {msg.get('vers', '?')}")
                        print(f"  Date: {msg.get('date', '?')}")
                        print(f"  Priorite: {msg.get('priorite', '?')}")
                        print(f"  Objet: {msg.get('objet', '')}")
                        print(f"  Corps: {msg.get('corps', '')}")
                        print(f"  Lu: {msg.get('lu', False)}")
                        print(f"  Acquitte: {msg.get('accuse', False)}")
                        print(f"  Source: {f.name}")
                        return
    print(f"[ORACLE] Message {args.id} non trouve")


def cmd_verifier(args):
    """Verifier la coherence des inbox/outbox."""
    print("[ORACLE] Verification de la coherence...")
    problemes = []
    # 1. Verifier que chaque outbox a une correspondance inbox
    for f_out in OUTBOX_DIR.glob("*.jsonl"):
        with open(f_out, encoding="utf-8") as fh:
            for ligne in fh:
                ligne = ligne.strip()
                if not ligne:
                    continue
                try:
                    msg = json.loads(ligne)
                except json.JSONDecodeError:
                    continue
                identifiant = msg.get("id")
                vers = msg.get("vers", "")
                if not vers:
                    continue
                inbox_corr = INBOX_DIR / f"{vers}.jsonl"
                if not inbox_corr.exists():
                    problemes.append(f"outbox {f_out.name}: message {identifiant} vers {vers} - inbox introuvable")
                    continue
                # Verifier que le message est aussi dans l inbox
                trouve = False
                with open(inbox_corr, encoding="utf-8") as fh_in:
                    for ligne_in in fh_in:
                        try:
                            msg_in = json.loads(ligne_in.strip())
                            if msg_in.get("id") == identifiant:
                                trouve = True
                                break
                        except json.JSONDecodeError:
                            continue
                if not trouve:
                    problemes.append(f"outbox {f_out.name}: message {identifiant} vers {vers} - absent de l inbox")
    # 2. Verifier les messages sans ID
    for dossier in [INBOX_DIR, OUTBOX_DIR]:
        if not dossier.exists():
            continue
        for f in dossier.glob("*.jsonl"):
            with open(f, encoding="utf-8") as fh:
                for ligne in fh:
                    ligne = ligne.strip()
                    if not ligne:
                        continue
                    try:
                        msg = json.loads(ligne)
                        if not msg.get("id"):
                            problemes.append(f"{f.name}: message sans ID")
                    except json.JSONDecodeError:
                        problemes.append(f"{f.name}: ligne JSON invalide")
    # 3. Verifier les doublons d ID
    tous_id = []
    for dossier in [INBOX_DIR, OUTBOX_DIR]:
        if not dossier.exists():
            continue
        for f in dossier.glob("*.jsonl"):
            with open(f, encoding="utf-8") as fh:
                for ligne in fh:
                    try:
                        msg = json.loads(ligne.strip())
                        identifiant = msg.get("id")
                        if identifiant:
                            tous_id.append((identifiant, f.name))
                    except (json.JSONDecodeError, ValueError):
                        continue
    vus = {}
    for identifiant, fichier in tous_id:
        if identifiant in vus:
            problemes.append(f"doublon ID {identifiant}: {vus[identifiant]} et {fichier}")
        else:
            vus[identifiant] = fichier
    if problemes:
        print(f"[ORACLE] {len(problemes)} probleme(s) detecte(s):")
        for p in problemes:
            print(f"  - {p}")
    else:
        print("[ORACLE] Aucun probleme - inbox/outbox coherents")


def cmd_status_detail(args):
    """Etat detaille d'Oracle."""
    agents = charger_agents()
    print(f"[ORACLE] Version: {VERSION}")
    print(f"[ORACLE] Agents declares: {len(agents)}")
    print()
    for a in agents:
        nom = a.get("nom", "?")
        role = a.get("role", "?")
        fiche = a.get("fiche", "")
        # Fiche
        fiche_ok = os.path.isfile(os.path.join(RACINE, fiche)) if fiche else False
        # Corrections
        agent_dir = os.path.dirname(fiche) if fiche else ""
        corrections = os.path.join(agent_dir, "corrections.md") if agent_dir else ""
        corr_ok = os.path.isfile(os.path.join(RACINE, corrections)) if corrections else False
        # Messages
        inbox = INBOX_DIR / f"{nom}.jsonl"
        non_lus = 0
        total = 0
        if inbox.exists():
            with open(inbox, encoding="utf-8") as fh:
                for ligne in fh:
                    try:
                        msg = json.loads(ligne.strip())
                        total += 1
                        if not isinstance(msg, dict) or not msg.get("lu"):
                            non_lus += 1
                    except (json.JSONDecodeError, ValueError):
                        continue
        # Dernier message
        dernier = "-"
        if inbox.exists():
            with open(inbox, encoding="utf-8") as fh:
                dernier_msg = None
                for ligne in fh:
                    try:
                        dernier_msg = json.loads(ligne.strip())
                    except (json.JSONDecodeError, ValueError):
                        continue
                if dernier_msg:
                    dernier = dernier_msg.get("date", "?")[:16]
        print(f"  {nom} ({role})")
        print(f"    Fiche: {'OK' if fiche_ok else 'MANQUANT'} | Corrections: {'OK' if corr_ok else 'MANQUANT'}")
        print(f"    Messages: {total} total, {non_lus} non lu(s) | Dernier: {dernier}")
        print()


def cmd_activer(args):
    """Activer un agent + transmettre la mission dans son inbox."""
    import importlib.util
    aap_path = os.path.join(
        os.path.dirname(ORACLE_DIR),
        "activer", "activer-agent-principal", "activer-agent-principal.py"
    )
    if not os.path.isfile(aap_path):
        print(f"[ORACLE] ERREUR: activer-agent-principal.py introuvable")
        return
    spec = importlib.util.spec_from_file_location("aap", aap_path)
    aap = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(aap)
    # 0. Capturer le maillon precedent (l agent actif avant cette
    #    activation) : Oracle en aura besoin pour piloter la reactivation
    #    du bon maillon en fin de mission (pose du FIN).
    try:
        contenu = aap.lire_agents()
        agent_precedent = aap.agent_actif_bloc(contenu, "session-admin")
    except Exception:
        agent_precedent = None
    # Bug corrige 2026-08-28 : lors d une auto-reactivation, l agent actif
    # est l agent lui-meme. Le precedent doit etre Cerberus quand
    # l activation vient de Cerberus, pas l agent lui-meme.
    if agent_precedent and (args.agent or "").lower() == agent_precedent.lower():
        agent_precedent = "cerberus"
    # 1. Activer l agent (change le bloc AGENTS.md). L historisation est
    #    deferree a Oracle (vision 2026-08-27 : Oracle maitre d hotel pose
    #    DEBUT) pour remplir la colonne Debut/Fin et eviter le doublon
    #    d entrees.
    rc = aap.activer_agent("session-admin", args.agent, args.raison,
                           historiser=False)
    if rc != 0:
        print(f"[ORACLE] ERREUR activation (rc={rc})")
        return
    print(f"[ORACLE] Agent {args.agent} active")
    # 2. Injecter la mission dans la sortie (l agent la recoit directement)
    print()
    print("=" * 60)
    print(f"MISSION POUR {args.agent.upper()} :")
    print(f"{args.raison}")
    print()
    print(f"Tu es {args.agent}. Relis ta fiche puis tes corrections.")
    print(f"Ensuite, lis le message ci-dessus et AGIS.")
    print(f"Ne demand pas de question, ne propose pas d alternative.")
    print(f"Execute la mission, puis suis ta carte pour la suite.")
    print("=" * 60)
    # 3. Historiser en marquant clairement le DEBUT (colonne Debut/Fin)
    #    Vision 2026-08-27 : Oracle est le maitre d hotel, il pose le
    #    marqueur DEBUT a l activation (la colonne se remplit) au lieu de
    #    compter sur l agent pour historiser lui-meme. L agent modifie/
    #    construit/audite SA mission : DEBUT -> lui, activation -> trace
    #    Cerberus/Oracle sans marqueur.
    _historiser_auto(
        args.agent,
        "DEBUT: " + args.raison,
        agent_effectif=args.agent)

    # 4. Initialiser l etat de carte du pilote Oracle (maitre d hotel)
    #    Oracle se souvient de la mission confiee pour piloter la carte.
    try:
        parcours = _pilote_parcours_agent(args.agent)
        mission_type = _pilote._type_mission_auto(args.raison)
        etat = _pilote.init_etat(
            args.agent, parcours, mission_type, args.raison,
            precedent=agent_precedent)
        # Marquer DEBUT deja historise (evite le double dans le pilote)
        if etat:
            etat["historise_debut"] = True
            _pilote._sauver_etat(etat)
    except Exception as exc:
        print("[ORACLE] WARNING etat-carte : %s" % exc)


def _pilote_parcours_agent(agent):
    """Chemin du parcours/arbre d un agent v1.

    ORACLE_DIR = .../agents/tools/oracle. Le parcours vit dans
    .../agents/<agent>/parcours/ (pas sous tools/).
    On remonte de oracle vers tools puis agents (3 parents).
    Priorite : arbre-<agent>.json (v2-like) > parcours-<agent>.json (v1)."""
    agents_dir = os.path.dirname(os.path.dirname(ORACLE_DIR))  # .../agents
    parcours_dir = os.path.join(agents_dir, agent, "parcours")
    # Priorite : arbre v2-like
    arbre = os.path.join(parcours_dir, "arbre-%s.json" % agent)
    if os.path.isfile(arbre):
        return arbre
    # Fallback : carte v1
    p = os.path.join(parcours_dir, "parcours-%s.json" % agent)
    if os.path.isfile(p):
        return p
    return None


def cmd_sessions(args):
    """Afficher les sessions actives."""
    import importlib.util
    aap_path = os.path.join(
        os.path.dirname(ORACLE_DIR),
        "activer", "activer-agent-principal", "activer-agent-principal.py"
    )
    if not os.path.isfile(aap_path):
        print("[ORACLE] activer-agent-principal.py introuvable")
        return
    spec = importlib.util.spec_from_file_location("aap", aap_path)
    aap = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(aap)
    aap.cmd_sessions(args)


def cmd_status(args):
    """Afficher l'etat d'Oracle."""
    agents = charger_agents()
    print(f"[ORACLE] Version: {VERSION}")
    print(f"[ORACLE] Agents declares: {len(agents)}")
    for a in agents:
        nom = a.get("nom", "?")
        inbox = INBOX_DIR / f"{nom}.jsonl"
        non_lus = 0
        if inbox.exists():
            with open(inbox, encoding="utf-8") as f:
                for ligne in f:
                    try:
                        msg = json.loads(ligne.strip())
                        if not isinstance(msg, dict) or not msg.get("lu"):
                            non_lus += 1
                    except (json.JSONDecodeError, ValueError):
                        continue
        statut = f" ({non_lus} non lu(s))" if non_lus > 0 else ""
        print(f"  - {nom}{statut}")


def _pid_file():
    """Chemin vers le fichier PID du serveur."""
    return ORACLE_DIR / "oracle-server.pid"


def _serveur_tourne():
    """Verifier si le serveur tourne (PID file valide)."""
    pid_file = _pid_file()
    if not pid_file.exists():
        return False, None
    try:
        pid = int(pid_file.read_text().strip())
        os.kill(pid, 0)  # signal 0 = juste verifier que le process existe
        return True, pid
    except (ValueError, OSError):
        pid_file.unlink(missing_ok=True)
        return False, None


def cmd_demarrage(args):
    """Demarrer Oracle : init, lancer le serveur si absent, historiser."""
    INBOX_DIR.mkdir(exist_ok=True)
    OUTBOX_DIR.mkdir(exist_ok=True)
    FILES_DIR.mkdir(exist_ok=True)
    # Verifier/lancer le serveur
    tourne, pid = _serveur_tourne()
    if tourne:
        print(f"[ORACLE] Serveur deja actif (PID {pid})")
    else:
        # Lancer le serveur en arriere-plan
        import subprocess
        server_path = ORACLE_DIR / "oracle-server.py"
        try:
            proc = subprocess.Popen(
                [sys.executable, str(server_path), "--transport", "stdio"],
                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                if hasattr(subprocess, "CREATE_NEW_PROCESS_GROUP") else 0)
            pid_file = _pid_file()
            pid_file.write_text(str(proc.pid))
            print(f"[ORACLE] Serveur lance (PID {proc.pid})")
        except OSError as exc:
            print(f"[ORACLE] WARNING: serveur non lance: {exc}")
    # Historiser le demarrage
    cmd_historiser(type("Args", (), {
        "agent": "oracle", "raison": f"Demarrage Oracle v{VERSION}",
        "type": "R"
    })())
    cmd_status(args)
    print(f"[ORACLE] Pret. Session: session-admin")


def cmd_arret(args):
    """Arreter proprement Oracle (serveur inclus)."""
    tourne, pid = _serveur_tourne()
    if tourne:
        try:
            os.kill(pid, 9)  # SIGKILL (Windows-compatible via terminate)
            print(f"[ORACLE] Serveur arrete (PID {pid})")
        except OSError as exc:
            print(f"[ORACLE] WARNING: arret serveur echoue: {exc}")
        _pid_file().unlink(missing_ok=True)
    cmd_historiser(type("Args", (), {
        "agent": "oracle",
        "raison": getattr(args, "raison", "Arret propre Oracle"),
        "type": "R"
    })())
    print("[ORACLE] Arret propre termine")


# --- Main ---

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Oracle v%s -- Coordination des agents v1" % VERSION
    )
    subparsers = parser.add_subparsers(dest="commande")

    # envoyer
    p_env = subparsers.add_parser("envoyer", help="Envoyer un message")
    p_env.add_argument("de", help="Expediteur")
    p_env.add_argument("vers", help="Destinataire")
    p_env.add_argument("objet", help="Objet du message")
    p_env.add_argument("corps", help="Corps du message")
    p_env.add_argument("--priorite", type=int, default=2)

    # lire
    p_lire = subparsers.add_parser("lire", help="Lire les messages non lus")
    p_lire.add_argument("agent", help="Agent")

    # acquitter
    p_acq = subparsers.add_parser("acquitter", help="Acquitter un message")
    p_acq.add_argument("agent", help="Agent")
    p_acq.add_argument("id", help="ID du message")

    # lister
    p_list = subparsers.add_parser("lister", help="Lister les messages")
    p_list.add_argument("agent", help="Agent")

    # lire-message
    p_lm = subparsers.add_parser("lire-message", help="Lire un message par ID")
    p_lm.add_argument("id", help="ID du message")

    # agents
    subparsers.add_parser("agents", help="Liste des agents avec statut")

    # nettoyer
    subparsers.add_parser("nettoyer", help="Supprimer les messages lus > 7j")

    # verifier
    subparsers.add_parser("verifier", help="Verifier coherence inbox/outbox")

    # historiser
    p_hist = subparsers.add_parser("historiser", help="Historiser une action")
    p_hist.add_argument("agent", help="Agent")
    p_hist.add_argument("raison", help="Raison de l'action")
    p_hist.add_argument("--type", default="R", help="Type (R ou IR)")

    # activer
    p_act = subparsers.add_parser("activer", help="Activer un agent")
    p_act.add_argument("agent", help="Agent a activer")
    p_act.add_argument("raison", help="Raison de l'activation")

    # sessions
    subparsers.add_parser("sessions", help="Afficher les sessions")

    # status
    p_stat = subparsers.add_parser("status", help="Etat d'Oracle")
    p_stat.add_argument("--detail", action="store_true", help="Affichage detaille")

    # demarrage
    subparsers.add_parser("demarrage", help="Demarrer Oracle")

    # arret
    p_arret = subparsers.add_parser("arret", help="Arreter Oracle")
    p_arret.add_argument("--raison", default="Arret propre Oracle")

    # pilote (maitre d hotel de la carte - vision 2026-08-27)
    p_pil = subparsers.add_parser("pilote", help="Piloter la carte d un agent (sert la case + repond aux questions)")
    p_pil.add_argument("agent", help="Agent a piloter")
    p_pil.add_argument("--parcours", help="Parcours perso (defaut: etat de carte)")
    p_pil.add_argument("--limite", type=int, default=1, help="Nb max de pas (defaut 1 : servir UNE etape de travail a la fois)")

    # reactiver-fin (pilotage de la reintegration du maillon precedent)
    p_rf = subparsers.add_parser("reactiver-fin", help="Piloter la reintegration du maillon precedent avec pose du FIN")
    p_rf.add_argument("agent", help="Agent qui termine (c est lui qu on historise FIN)")
    p_rf.add_argument("bilan", help="Bilan de fin de mission")

    # defcon
    p_def = subparsers.add_parser("defcon", help="Etat DEFCON")
    p_defc = subparsers.add_parser("defcon-changer", help="Descendre d'un niveau (5->4->3->2)")
    p_defc.add_argument("niveau", type=int, choices=[4, 3, 2], help="Nouveau niveau")
    p_defc.add_argument("commentaire", help="Commentaire")
    p_defd = subparsers.add_parser("defcon-declarer", help="Declarer un DEFCON 5 (arret total)")
    p_defd.add_argument("raison", help="Raison de l'arret")
    p_defe = subparsers.add_parser("defcon-escaler", help="Escalader vers le haut (ex: URGENT -> DEFCON 4)")
    p_defe.add_argument("niveau", type=int, choices=[3, 4], help="Niveau cible (escalade)")
    p_defe.add_argument("commentaire", help="Commentaire")

    # missions
    p_maj = subparsers.add_parser("mission-ajouter", help="Ajouter une mission dans une file")
    p_maj.add_argument("mission", help="Description de la mission")
    p_maj.add_argument("--file", default="asap",
                       choices=["asap", "normale", "plus-tard", "attente"])
    p_maj.add_argument("--agent", default="", help="Agent assigne (optionnel)")
    p_mp = subparsers.add_parser("mission-prendre", help="Prendre la premiere mission en attente")
    p_mp.add_argument("--file", default="asap",
                      choices=["asap", "normale", "plus-tard", "attente"])
    p_mt = subparsers.add_parser("mission-terminer", help="Terminer une mission")
    p_mt.add_argument("id", help="ID de la mission")
    p_mt.add_argument("--file", default="asap",
                      choices=["asap", "normale", "plus-tard", "attente"])
    p_ml = subparsers.add_parser("mission-lister", help="Lister les missions")
    p_ml.add_argument("--file", default=None,
                      choices=["asap", "normale", "plus-tard", "attente"])

    # harnais
    subparsers.add_parser("harnais", help="Verifier la sante de la coordination v1")

    # controle-processus
    subparsers.add_parser("controle-processus",
                          help="Verifier qu un seul processus tourne par serveur (detection des fantomes)")

    # relais
    subparsers.add_parser("relais", help="Relayer les messages du hub vers leurs destinataires")

    # dashboard
    subparsers.add_parser("dashboard", help="Vue d'ensemble temps reel")

    args = parser.parse_args()

    if not args.commande:
        parser.print_help()
        return

    commandes = {
        "envoyer": cmd_envoyer,
        "lire": cmd_lire,
        "lire-message": cmd_lire_message,
        "acquitter": cmd_acquitter,
        "lister": cmd_lister,
        "agents": cmd_agents,
        "nettoyer": cmd_nettoyer,
        "verifier": cmd_verifier,
        "historiser": cmd_historiser,
        "activer": cmd_activer,
        "sessions": cmd_sessions,
        "status": cmd_status,
        "demarrage": cmd_demarrage,
        "arret": cmd_arret,
        "defcon": _cmd_defcon,
        "defcon-changer": _cmd_defcon_changer,
        "defcon-declarer": _cmd_defcon_declarer,
        "defcon-escaler": _cmd_defcon_escaler,
        "mission-ajouter": _cmd_mission_ajouter,
        "mission-prendre": _cmd_mission_prendre,
        "mission-terminer": _cmd_mission_terminer,
        "mission-lister": _cmd_mission_lister,
        "harnais": _cmd_harnais,
        "controle-processus": _cmd_controle_processus,
        "relais": _cmd_relais,
        "dashboard": _cmd_dashboard,
        "pilote": _cmd_pilote,
        "reactiver-fin": _cmd_reactiver_fin,
    }
    if args.commande == "status" and getattr(args, "detail", False):
        cmd_status_detail(args)
    elif args.commande in commandes:
        commandes[args.commande](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
