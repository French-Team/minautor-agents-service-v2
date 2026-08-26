# -*- coding: ascii -*-
"""fonctions/harnais_jarvis.py - Harnais de COMPORTEMENT du serveur JARVIS.

Le harnais ne se contente pas de la sante statique : il scanne les
COMPORTEMENTS REELS de JARVIS (files, messages, activations, historique)
et detecte CHAQUE ecart par rapport aux regles attendues (config
harnais-jarvis-data.json, D15). Chaque ecart -> message d alerte format
JARVIS standard dans l inbox du destinataire (vision, le seul habilite a
modifier JARVIS). Dedup : un meme ecart (type + cle) n est signale qu une
fois (journal alertes-jarvis.jsonl) -- pas de spam.

Lecture seule des fichiers JARVIS sauf l ecriture de l alerte dans
l inbox/outbox du destinataire (canal standard, protocole 14 comme
EDITH). Le harnais ne modifie JAMAIS le fonctionnement de JARVIS.
"""

import json
import os
import sys
import uuid
from datetime import datetime, timezone

# P10 : detection de la racine via os_path
_sys_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "..", "os_path", "fonctions")
sys.path.insert(0, _sys_dir)
from racine import trouver_racine

RACINE = trouver_racine(__file__)
BASE = os.path.join(RACINE, "cerveau-projet", "freelance", "tools-commun")
JARVIS_DIR = os.path.join(BASE, "jarvis")
HARNAIS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(HARNAIS_DIR, "harnais-jarvis-data.json")
JOURNAL_PATH = os.path.join(HARNAIS_DIR, "alertes-jarvis.jsonl")

VERSION = "0.1.0"


def signal(niveau, message):
    """Afficher un signal [HARNAIS-JARVIS SIG <NIVEAU>]."""
    print("[HARNAIS-JARVIS SIG %s] %s" % (niveau, message))


def charger_config():
    """Charger harnais-jarvis-data.json (dict vide si absent/invalide)."""
    try:
        with open(CONFIG_PATH, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def _lire_jsonl(chemin):
    """Lire un fichier .jsonl : [(n_ligne, contenu_brut, dict_ou_None), ...]."""
    if not os.path.isfile(chemin):
        return []
    lignes = []
    with open(chemin, "r", encoding="utf-8", errors="replace") as fh:
        for n, ligne in enumerate(fh, 1):
            brut = ligne.strip()
            if not brut:
                continue
            try:
                lignes.append((n, brut, json.loads(brut)))
            except ValueError:
                lignes.append((n, brut, None))
    return lignes


def _agents_valides():
    """Agents declares dans jarvis-data.json (set)."""
    chemin = os.path.join(JARVIS_DIR, "jarvis-data.json")
    try:
        with open(chemin, encoding="utf-8") as fh:
            return {a["nom"] for a in json.load(fh).get("agents", [])
                    if isinstance(a, dict) and a.get("nom")}
    except (OSError, ValueError):
        return set()


# ------------------------------------------------------------------
# Detecteurs (un par regle de la config)
# ------------------------------------------------------------------

def _detecter_messages(config, ecarts):
    """Ecarts lies aux messages (inbox/outbox) + hub non route.
    Les messages du harnais lui-meme (type harnais-jarvis) sont IGNORES
    : il ne doit jamais s auto-alerter sur ses propres alertes."""
    agents = _agents_valides()
    expediteur = config.get("expediteur_alertes", "jarvis-harnais")
    regles = {r["nom"]: r for r in config.get("ecarts", [])}
    for sous_dossier in ("inbox", "outbox"):
        dossier = os.path.join(JARVIS_DIR, sous_dossier)
        if not os.path.isdir(dossier):
            continue
        for nom_fichier in sorted(os.listdir(dossier)):
            if not nom_fichier.endswith(".jsonl"):
                continue
            chemin = os.path.join(dossier, nom_fichier)
            rel = "%s/%s" % (sous_dossier, nom_fichier)
            comptes_id = {}
            for n, brut, msg in _lire_jsonl(chemin):
                cle_ligne = "%s:%d" % (rel, n)
                if msg is None:
                    r = regles.get("json_corrompu")
                    if r and r.get("actif"):
                        ecarts.append(_ecart(r, cle_ligne,
                                             fichier=rel, n=n))
                    continue
                if msg.get("type") == "harnais-jarvis":
                    continue  # jamais auto-alerte
                if msg.get("de") == expediteur:
                    continue  # jamais auto-alerte (outbox du harnais)
                if "id" not in msg:
                    r = regles.get("message_sans_id")
                    if r and r.get("actif"):
                        ecarts.append(_ecart(r, cle_ligne, fichier=rel))
                if not msg.get("date"):
                    r = regles.get("message_sans_date")
                    if r and r.get("actif"):
                        ecarts.append(_ecart(r, cle_ligne, fichier=rel))
                for champ in ("de", "vers"):
                    valeur = msg.get(champ, "")
                    if valeur and agents and valeur not in agents:
                        r = regles.get("agent_inconnu")
                        if r and r.get("actif"):
                            ecarts.append(_ecart(r, cle_ligne,
                                                 champ=champ, valeur=valeur,
                                                 fichier=rel))
                identifiant = msg.get("id", "")
                if identifiant:
                    comptes_id[identifiant] = comptes_id.get(identifiant, 0) + 1
                # P1 non lu : demandes d activation / missions non demarrees
                non_lu = not msg.get("lu")
                est_demande_activation = (
                    msg.get("type") == "activation"
                    or "ACTIVATION" in (msg.get("objet") or "").upper()
                    or "MISSION" in (msg.get("objet") or "").upper())
                if non_lu and msg.get("priorite") == 1:
                    cle = identifiant or cle_ligne
                    # le HUB est inbox/jarvis.jsonl uniquement : le
                    # fichier outbox/jarvis.jsonl porte le meme nom mais
                    # n est pas le hub (sinon chaque copie outbox serait
                    # un faux "jamais route").
                    if nom_fichier == "jarvis.jsonl" \
                            and sous_dossier == "inbox":
                        # JARVIS a recu une demande -> il doit activer.
                        # Restee non lue = JARVIS n a pas agi.
                        if est_demande_activation:
                            r = regles.get("activation_demandee_non_traitee")
                            if r and r.get("actif"):
                                ecarts.append(_ecart(
                                    r, cle,
                                    objet=(msg.get("objet") or "")[:60]))
                        else:
                            r = regles.get("hub_non_route")
                            if r and r.get("actif"):
                                ecarts.append(_ecart(
                                    r, cle,
                                    objet=(msg.get("objet") or "")[:60]))
                    elif msg.get("type") == "activation":
                        # activation ecrite mais jamais livree/incarnee
                        r = regles.get("mission_non_demarree")
                        if r and r.get("actif"):
                            ecarts.append(_ecart(
                                r, cle, agent=nom_fichier[:-6],
                                objet=(msg.get("objet") or "")[:60]))
                    else:
                        r = regles.get("p1_non_lu")
                        if r and r.get("actif"):
                            ecarts.append(_ecart(
                                r, cle, agent=nom_fichier[:-6],
                                objet=(msg.get("objet") or "")[:60]))
            for identifiant, nombre in comptes_id.items():
                if nombre > 1:
                    r = regles.get("doublon_id")
                    if r and r.get("actif"):
                        ecarts.append(_ecart(r, identifiant,
                                             id=identifiant, n=nombre,
                                             fichier=rel))
    _detecter_transmission(config, ecarts, regles)


def _detecter_transmission(config, ecarts, regles):
    """Correspondance outbox <-> inbox : JARVIS transmet-il les
    informations aux agents ?

    Contrat (envoyer/activer, CLI + MCP) : un message est ecrit dans
    inbox/<vers> ET outbox/<de> (meme id). Donc :
      - message dans outbox/<de> SANS correspondant dans inbox/<vers>
        -> JARVIS n a PAS transmis l information (boucle/round brise).
      - message dans inbox/<vers> SANS correspondant dans outbox/<de>
        -> transmission non tracee cote expediteur (asymetrie).
    Les messages du harnais (type harnais-jarvis) sont ignores.
    """
    expediteur = config.get("expediteur_alertes", "jarvis-harnais")
    # index : id -> (fichier, message) pour chaque inbox/outbox
    ids_inbox = {}
    ids_outbox = {}
    for sous_dossier, index in (("inbox", ids_inbox), ("outbox", ids_outbox)):
        dossier = os.path.join(JARVIS_DIR, sous_dossier)
        if not os.path.isdir(dossier):
            continue
        for nom_fichier in sorted(os.listdir(dossier)):
            if not nom_fichier.endswith(".jsonl"):
                continue
            for _, _, msg in _lire_jsonl(
                    os.path.join(dossier, nom_fichier)):
                if msg is None or msg.get("type") == "harnais-jarvis":
                    continue
                if msg.get("de") == expediteur:
                    continue
                identifiant = msg.get("id")
                if identifiant:
                    index.setdefault(identifiant, []).append(
                        (nom_fichier, msg))
    # outbox sans inbox (transmission cassee)
    r = regles.get("message_non_transmis")
    if r and r.get("actif"):
        for identifiant, occurrences in ids_outbox.items():
            for _, msg in occurrences:
                vers = (msg.get("vers") or "").lower()
                cibles = ids_inbox.get(identifiant, [])
                recu = any(nom == "%s.jsonl" % vers
                           for nom, _ in cibles)
                if not recu:
                    ecarts.append(_ecart(
                        r, identifiant, id=identifiant,
                        objet=(msg.get("objet") or "")[:60],
                        de=msg.get("de", "?"), vers=vers or "?"))
    # inbox sans outbox (asymetrie de trace)
    r2 = regles.get("message_non_trace")
    if r2 and r2.get("actif"):
        for identifiant, occurrences in ids_inbox.items():
            for _, msg in occurrences:
                de = (msg.get("de") or "").lower()
                if not de or de == "jarvis":
                    continue  # messages du hub : trace cote exp. variable
                cibles = ids_outbox.get(identifiant, [])
                envoye = any(nom == "%s.jsonl" % de for nom, _ in cibles)
                if not envoye:
                    ecarts.append(_ecart(
                        r2, identifiant, id=identifiant,
                        objet=(msg.get("objet") or "")[:60],
                        vers=msg.get("vers", "?"), de=de))


def _detecter_activations(config, ecarts):
    """Activation recente envoyee sans trace dans l historique du serveur.

    Fenetre de temps : 'activation_recente_jours' (config, defaut 14).
    Une activation est consideree tracee si l historique contient une
    entree action=='activer' mentionnant l agent cible.
    """
    regles = {r["nom"]: r for r in config.get("ecarts", [])}
    seuils = config.get("seuils", {})
    fenetre_jours = int(seuils.get("activation_recente_jours", 14))
    # Source de tracabilite : AGENTS-activite-recente.md (encart v2,
    # 50 entrees max, raison tronquee). Le texte complet vit dans
    # historique.db (BDD SQLite, 7 jours).
    agents_traces = set()
    # meme source que historique_agents_gele (plus bas)
    hist_path = os.path.join(RACINE, "AGENTS-activite-recente.md")
    try:
        with open(hist_path, encoding="utf-8") as fh:
            for ligne in fh:
                if not (ligne.startswith("| ") and "| R |" in ligne):
                    continue
                cols = [c.strip() for c in ligne.split("|")]
                # | heure | agent | llm | R | raison |
                if len(cols) < 6:
                    continue
                agent = cols[2]
                raison = cols[5].lower()
                if "activ" in raison:
                    agents_traces.add(agent)
                for mot in raison.replace(":", " ").replace(",", " ").split():
                    if mot in _agents_valides():
                        agents_traces.add(mot)
    except OSError:
        pass
    # messages d activation RECENTS dans les inbox
    inbox = os.path.join(JARVIS_DIR, "inbox")
    r = regles.get("activation_sans_historique")
    if not (r and r.get("actif")):
        return
    try:
        from datetime import timedelta
        borne = (datetime.now(timezone.utc) - timedelta(days=fenetre_jours))
        # comparer en naive (les dates des messages sont sans fuseau)
        borne = borne.replace(tzinfo=None)
    except Exception:
        borne = None
    if os.path.isdir(inbox):
        for nom_fichier in sorted(os.listdir(inbox)):
            if not nom_fichier.endswith(".jsonl"):
                continue
            for _, _, msg in _lire_jsonl(os.path.join(inbox, nom_fichier)):
                if msg is None or msg.get("type") != "activation":
                    continue
                if borne is not None:
                    try:
                        d = datetime.strptime(str(msg.get("date", ""))[:19],
                                              "%Y-%m-%dT%H:%M:%S")
                        if d < borne:
                            continue  # trop ancien : hors fenetre
                    except ValueError:
                        pass
                cible = msg.get("vers", "?")
                if cible in agents_traces:
                    continue
                # livraison directe : un message d activation marque LU a
                # ETE livre (marquer_lu fait partie de la livraison) -- la
                # tracabilite est prouvee par la livraison elle-meme.
                # L historique glissant (10 entrees/session) ne garde pas
                # assez de recul pour tracer toutes les activations.
                if msg.get("lu"):
                    continue
                identifiant = (msg.get("id", "")
                               or "%s:%s" % (msg.get("de", "?"),
                                              msg.get("objet", "?")))
                ecarts.append(_ecart(r, identifiant, agent=cible,
                                     objet=(msg.get("objet") or "")[:60]))


def _detecter_valeurs_en_dur(config, ecarts):
    """Valeurs codees en dur suspectes dans le CODE de JARVIS
    (esprit P4/M5 du protocole 18 : SIGNALER, pas bloquer).

    3 heuristiques prudentes sur jarvis/*.py (racine, fonctions/,
    serveur/, combos/) :
      1. p10_chemins_comptes : os.path.join/Path avec ".." ou .parent
         repetes >= 2 SANS detection os_path/racine sur la ligne.
      2. session_litterale : "session-..." code en dur (P4/M5).
      3. agent_litteral : nom d'agent en litteral chaine alors qu'il
         devrait venir de jarvis-data.json (D15) - lignes exclues :
         commentaires, lecture du data file, dictionnaires AGENTS/
         COULEURS, defaults documentes, tests.
    Dedup par fichier:ligne:regle. Faux positifs possibles : c est un
    signal WARN pour revue humaine, pas une erreur.
    """
    import re
    regles = {r["nom"]: r for r in config.get("ecarts", [])}
    r = regles.get("valeur_en_dur")
    if not (r and r.get("actif")):
        return
    agents = sorted(_agents_valides(), key=len, reverse=True)
    cibles = []
    for racine_rel, sous in (("jarvis.py", ""), ("jarvis-server.py", ""),
                             ("", "fonctions"), ("", "serveur"),
                             ("", "combos"), ("", os.path.join("combos",
                                                               "fonctions"))):
        dossier = os.path.join(JARVIS_DIR, sous) if sous else JARVIS_DIR
        if racine_rel:
            cibles.append(os.path.join(dossier, racine_rel))
        elif os.path.isdir(dossier):
            for n in sorted(os.listdir(dossier)):
                if n.endswith(".py") and not n.startswith("__"):
                    cibles.append(os.path.join(dossier, n))
    exclusions = re.compile(
        r"(jarvis-data|_charger_agents|AGENTS_VALIDES|_agents_valides"
        r"|NOTATEURS|dictionnaire|fallback|defaut|parite|#|\"\"\"|exemples"
        # defaults CLI documentes : choix de config legitime, pas un
        # oubli de D15 ; noms d'outil/serveur : auto-reference, pas un
        # agent cible
        r"|default=|verifier_outil|FastMCP\(|choices=|par=|getattr\("
        r"|\.get\()",
        re.IGNORECASE)
    # 'jarvis' est le nom de l'outil lui-meme : toute occurrence dans
    # son code est une auto-reference, jamais un agent code en dur.
    agents_scan = [a for a in agents if a != "jarvis"]
    for chemin in cibles:
        rel = os.path.relpath(chemin, JARVIS_DIR).replace(os.sep, "/")
        try:
            with open(chemin, encoding="utf-8") as fh:
                lignes = fh.readlines()
        except (OSError, ValueError):
            continue
        vus = set()
        for i, ligne in enumerate(lignes, 1):
            # 1. P10 : niveaux comptes SANS detection os_path. Seuil 3 :
            # remonter 1-2 niveaux INTRA-outil est legitime ; 3+, c est
            # du comptage vers la racine projet.
            compte_parent = (".." in ligne and 'os_path' not in ligne
                             and "trouver_racine" not in ligne
                             and ('"' in ligne or "'" in ligne)
                             and len(re.findall(r'"[.]+"', ligne)) >= 3)
            parents = len(re.findall(r"\.parent\b", ligne))
            if compte_parent or parents >= 3:
                cle = "%s:%d:p10" % (rel, i)
                if cle not in vus:
                    vus.add(cle)
                    ecarts.append(_ecart(r, cle, fichier=rel,
                                         detail="chemin compte en dur "
                                                "(P10) ligne %d : %s"
                                                % (i, ligne.strip()[:60])))
                continue
            # 2. P4/M5 : session litterale
            if re.search(r"[\"']session-(freelance|admin|llm-\d)[\"']",
                         ligne) and not exclusions.search(ligne):
                cle = "%s:%d:session" % (rel, i)
                if cle not in vus:
                    vus.add(cle)
                    ecarts.append(_ecart(r, cle, fichier=rel,
                                         detail="session litterale "
                                                "(P4/M5) ligne %d : %s"
                                                % (i, ligne.strip()[:60])))
                continue
            # 3. D15 : agent en litteral chaine
            for a in agents_scan:
                if re.search(r"[\"']%s[\"']" % a, ligne) and \
                        not exclusions.search(ligne):
                    cle = "%s:%d:agent-%s" % (rel, i, a)
                    if cle not in vus:
                        vus.add(cle)
                        ecarts.append(_ecart(
                            r, cle, fichier=rel,
                            detail="agent '%s' code en dur ligne %d "
                                   "(D15) : %s" % (a, i,
                                                   ligne.strip()[:50])))
                    break


def _detecter_files(config, ecarts):
    """Missions en file : sans statut, ou abandonnees (jamais reprises)."""
    regles = {r["nom"]: r for r in config.get("ecarts", [])}
    seuils = config.get("seuils", {})
    abandon_jours = int(seuils.get("mission_abandonnee_jours", 7))
    dossier = os.path.join(JARVIS_DIR, "files")
    if not os.path.isdir(dossier):
        return
    for nom_fichier in sorted(os.listdir(dossier)):
        if not nom_fichier.endswith(".jsonl"):
            continue
        if nom_fichier == "defcon.jsonl":
            # journal DEFCON (historique des niveaux), pas une file de
            # missions : ses entrees n ont pas de champ statut par design.
            continue
        chemin = os.path.join(dossier, nom_fichier)
        rel = "files/%s" % nom_fichier
        for n, brut, msg in _lire_jsonl(chemin):
            if msg is None:
                continue
            if "statut" not in msg:
                r = regles.get("mission_sans_statut")
                if r and r.get("actif"):
                    ecarts.append(_ecart(r, "%s:%d" % (rel, n),
                                         mission=(msg.get("mission")
                                                  or "")[:60],
                                         fichier=rel))
                continue
            # mission abandonnee : en attente depuis plus de N jours
            if msg.get("statut") not in ("EN_ATTENTE", "ATTENTE",
                                          "PREPAREE", "PRIORITAIRE",
                                          "SUIVANTE"):
                continue
            date_str = str(msg.get("date", ""))[:10]
            try:
                from datetime import datetime as _dt
                d = _dt.strptime(date_str, "%Y-%m-%d")
                age = (datetime.now(timezone.utc) - d).days
            except (ValueError, TypeError):
                continue
            if age > abandon_jours:
                r = regles.get("mission_abandonnee")
                if r and r.get("actif"):
                    ecarts.append(_ecart(
                        r, str(msg.get("mission", ""))[:60],
                        mission=(msg.get("mission") or "")[:60],
                        statut=msg.get("statut"), jours=age))


def _detecter_sante(config, ecarts):
    """Structure, syntaxe, config agents, .bak."""
    regles = {r["nom"]: r for r in config.get("ecarts", [])}
    for element in config.get("fichiers_critiques", []):
        if not os.path.isfile(os.path.join(JARVIS_DIR, element)):
            r = regles.get("structure_manquante")
            if r and r.get("actif"):
                ecarts.append(_ecart(r, element, element=element))
    for element in config.get("dossiers_critiques", []):
        if not os.path.isdir(os.path.join(JARVIS_DIR, element)):
            r = regles.get("structure_manquante")
            if r and r.get("actif"):
                ecarts.append(_ecart(r, element, element=element))
    # syntaxe de tous les .py
    for racine_d, dossiers, fichiers in os.walk(JARVIS_DIR):
        dossiers[:] = [d for d in dossiers if d != "__pycache__"]
        for nom in fichiers:
            if not nom.endswith(".py"):
                continue
            chemin = os.path.join(racine_d, nom)
            try:
                compile(open(chemin, encoding="utf-8-sig").read(),
                        chemin, "exec")
            except (SyntaxError, OSError) as exc:
                r = regles.get("syntaxe_invalide")
                if r and r.get("actif"):
                    rel = os.path.relpath(chemin, JARVIS_DIR)
                    ecarts.append(_ecart(r, rel, fichier=rel,
                                         erreur=str(exc)[:80]))
    # config agents
    chemin_data = os.path.join(JARVIS_DIR, "jarvis-data.json")
    detail = ""
    try:
        with open(chemin_data, encoding="utf-8") as fh:
            agents = json.load(fh).get("agents", [])
        for a in agents:
            for champ in ("fiche", "corrections"):
                p = os.path.join(RACINE, a.get(champ, ""))
                if champ in a and not os.path.isfile(p):
                    detail = "agent %s : %s introuvable (%s)" % (
                        a.get("nom", "?"), champ, a.get(champ))
                    break
            if detail:
                break
    except (OSError, ValueError) as exc:
        detail = "jarvis-data.json illisible : %s" % str(exc)[:60]
    if detail:
        r = regles.get("config_invalide")
        if r and r.get("actif"):
            ecarts.append(_ecart(r, detail, detail=detail))
    # .bak accumules
    for racine_d, dossiers, fichiers in os.walk(JARVIS_DIR):
        dossiers[:] = [d for d in dossiers if d != "__pycache__"]
        for nom in fichiers:
            if nom.endswith(".bak"):
                r = regles.get("bak_accumules")
                if r and r.get("actif"):
                    rel = os.path.relpath(os.path.join(racine_d, nom),
                                          JARVIS_DIR)
                    ecarts.append(_ecart(r, rel, fichier=rel))


def _ecart(regle, cle, **contexte):
    """Construire un ecart depuis une regle de la config + contexte."""
    message = regle.get("message", "")
    for k, v in contexte.items():
        message = message.replace("<%s>" % k, str(v))
    return {"type": regle.get("nom", "?"),
            "cle": str(cle),
            "severite": regle.get("severite", "WARN"),
            "message": message}


# ------------------------------------------------------------------
# Alerte vers Vision (dedup)
# ------------------------------------------------------------------

def _charger_journal():
    """Ensemble des (type, cle) deja signales."""
    signales = set()
    if os.path.isfile(JOURNAL_PATH):
        try:
            with open(JOURNAL_PATH, encoding="utf-8") as fh:
                for ligne in fh:
                    try:
                        e = json.loads(ligne)
                        signales.add((e.get("type", ""), e.get("cle", "")))
                    except ValueError:
                        continue
        except OSError:
            pass
    return signales


def _journaliser(ecart):
    """Ajouter un ecart au journal des alertes."""
    try:
        with open(JOURNAL_PATH, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({
                "date": datetime.now(timezone.utc).strftime(
                    "%Y-%m-%dT%H:%M:%S"),
                "type": ecart["type"],
                "cle": ecart["cle"],
                "severite": ecart["severite"],
            }, ensure_ascii=False) + "\n")
    except OSError:
        pass


def _envoyer_alerte(config, ecarts):
    """Ecrire UN message d alerte (format JARVIS standard) dans les inbox
    des destinataires selon la gravite + l outbox du harnais.

    Routage par gravite (config destinataires_par_severite) :
      WARN -> vision ; ERR -> vision + stark ; CRIT -> vision + stark
      (+ mention ESCALADE UTILISATEUR dans le corps des CRIT).
    """
    severites = [e.get("severite") for e in ecarts]
    severite_max = "WARN"
    if "CRIT" in severites:
        severite_max = "CRIT"
    elif "ERR" in severites:
        severite_max = "ERR"
    routage = config.get("destinataires_par_severite", {})
    destinataires = routage.get(severite_max, ["vision"])
    expediteur = config.get("expediteur_alertes", "jarvis-harnais")
    priorite = int(config.get("priorite_alerte", 1))
    LIMITE_CORPS = 30
    lignes_corps = ["- [%s] %s" % (e["severite"], e["message"])
                    for e in ecarts[:LIMITE_CORPS]]
    if len(ecarts) > LIMITE_CORPS:
        lignes_corps.append("... et %d autre(s) ecart(s) (voir le journal "
                            "alertes-jarvis.jsonl)" % (len(ecarts)
                                                        - LIMITE_CORPS))
    if severite_max == "CRIT":
        lignes_corps.append("")
        lignes_corps.append("ESCALADE UTILISATEUR REQUISE : aucun CRIT ne "
                            "doit rester sans traitement.")
    corps = "\n".join(lignes_corps)
    msg = {
        "id": uuid.uuid4().hex[:8],
        "de": expediteur,
        "vers": ",".join(destinataires),
        "priorite": priorite,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "objet": "[HARNAIS-JARVIS] %d ecart(s) %s detecte(s)"
                 % (len(ecarts), severite_max),
        "corps": corps,
        "lu": False,
        "accuse": False,
        "type": "harnais-jarvis",
    }
    cibles = [os.path.join(JARVIS_DIR, "inbox", "%s.jsonl" % d)
              for d in destinataires]
    cibles.append(os.path.join(JARVIS_DIR, "outbox",
                               "%s.jsonl" % expediteur))
    for cible in cibles:
        try:
            with open(cible, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(msg, ensure_ascii=False) + "\n")
        except OSError as exc:
            signal("ERR", "impossible d alerter %s : %s"
                   % (",".join(destinataires), str(exc)))
            return
    for e in ecarts:
        _journaliser(e)
    signal("OK", "alerte %s envoyee a %s (id=%s, %d ecart(s))"
           % (severite_max, ",".join(destinataires), msg["id"],
              len(ecarts)))


# ------------------------------------------------------------------
# Surveillance de la boucle (filet de securite)
# ------------------------------------------------------------------

def _detecter_surveillance(config, ecarts):
    """Les acteurs de la boucle : serveur vivant ? alertes traitees ?
    demandes utilisateur traitees ?

    - serveur_inactif : historique du serveur MCP gele depuis N jours
      -> le serveur ne tourne pas (down ou jamais lance).
    - alerte_non_traitee : une alerte (EDITH [EDITH-REVEIL], harnais
      [HARNAIS-JARVIS], type reveil) reste NON LUE depuis N jours -> la
      boucle de reparation ne se ferme pas (filet : surveiller le
      surveillant).
    - demande_utilisateur_non_traitee : une entree de USER-DEMANDES.md
      plus vieille que N jours sans marqueur de traitement.
    """
    import re as _re
    from datetime import timedelta
    regles = {r["nom"]: r for r in config.get("ecarts", [])}
    seuils = config.get("seuils", {})
    maintenant = datetime.now(timezone.utc)

    # --- serveur_inactif (historique gele) ---
    r = regles.get("serveur_inactif")
    if r and r.get("actif"):
        seuil_jours = int(seuils.get("serveur_inactif_jours", 7))
        historique = os.path.join(JARVIS_DIR, "historique",
                                  "historique.jsonl")
        derniere = None
        if os.path.isfile(historique):
            for _, _, msg in _lire_jsonl(historique):
                if msg is not None:
                    try:
                        d = datetime.strptime(
                            str(msg.get("date", ""))[:19],
                            "%Y-%m-%dT%H:%M:%S")
                    except ValueError:
                        continue
                    if derniere is None or d > derniere:
                        derniere = d
        if derniere is None:
            ecarts.append(_ecart(r, "fixe", jours=seuil_jours))
        else:
            age = (maintenant.replace(tzinfo=None) - derniere).days
            if age > seuil_jours:
                ecarts.append(_ecart(r, "fixe", jours=age))

    # --- alerte_non_traitee (messages d alerte non lus anciens) ---
    r2 = regles.get("alerte_non_traitee")
    if r2 and r2.get("actif"):
        seuil_jours = int(seuils.get("alerte_non_traitee_jours", 2))
        borne = (maintenant - timedelta(days=seuil_jours))
        borne = borne.replace(tzinfo=None)
        dossier = os.path.join(JARVIS_DIR, "inbox")
        if os.path.isdir(dossier):
            for nom_fichier in sorted(os.listdir(dossier)):
                if not nom_fichier.endswith(".jsonl"):
                    continue
                for _, _, msg in _lire_jsonl(
                        os.path.join(dossier, nom_fichier)):
                    if msg is None or msg.get("lu"):
                        continue
                    objet = (msg.get("objet") or "")
                    est_alerte = (
                        msg.get("type") in ("reveil", "harnais-jarvis")
                        or "[EDITH" in objet.upper()
                        or "[HARNAIS-JARVIS]" in objet.upper())
                    if not est_alerte:
                        continue
                    try:
                        d = datetime.strptime(str(msg.get("date", ""))[:19],
                                              "%Y-%m-%dT%H:%M:%S")
                    except ValueError:
                        continue
                    age = (maintenant.replace(tzinfo=None) - d).days
                    if age >= seuil_jours:
                        identifiant = msg.get("id", "") or "%s:%s" % (
                            nom_fichier, objet[:30])
                        ecarts.append(_ecart(
                            r2, identifiant, jours=age,
                            objet=objet[:60],
                            de=msg.get("de", "?"),
                            agent=nom_fichier[:-6]))

    # --- demandes utilisateur non traitees (USER-DEMANDES.md) ---
    r3 = regles.get("demande_utilisateur_non_traitee")
    if r3 and r3.get("actif"):
        seuil_jours = int(seuils.get("demande_non_traitee_jours", 7))
        mots_traitement = config.get("mots_cles_traitement", [])
        chemin = os.path.join(RACINE, config.get("user_demandes_path",
                                                  "USER-DEMANDES.md"))
        if os.path.isfile(chemin):
            try:
                texte = open(chemin, encoding="utf-8").read()
            except OSError:
                texte = ""
            # section 'Dernieres modifications' : les demandes dont le
            # titre (ou >= 2 mots significatifs) apparait dans les LIGNES
            # DU JOURNAL (celles commencant par '-') sont TRAITEES.
            # Seules les lignes du journal comptent : jamais les
            # instructions de la section (faux positifs).
            traitees = ""
            m_modif = _re.search(r"(?ms)^## Dernieres modifications\s*$(.*?)^## ",
                                 texte)
            if m_modif:
                lignes_journal = [l.strip().lower()
                                  for l in m_modif.group(1).splitlines()
                                  if l.strip().startswith("-")]
                traitees = "\n".join(lignes_journal)
            section = "autre"
            blocs = _re.split(r"(?m)^###\s+", texte)
            for bloc in blocs[1:]:
                lignes = bloc.splitlines()
                entete = lignes[0].strip()
                m_date = _re.match(r"([0-9]{4}-[0-9]{2}-[0-9]{2})", entete)
                if not m_date:
                    continue
                try:
                    d = datetime.strptime(m_date.group(1), "%Y-%m-%d")
                except ValueError:
                    continue
                age = (maintenant.replace(tzinfo=None) - d).days
                if age < seuil_jours:
                    continue
                titre = entete[len(m_date.group(1)):].lstrip(" -\"").strip()
                if not titre:
                    continue
                # traitee si le titre apparait dans 'Dernieres
                # modifications' : titre complet OU au moins 2 mots
                # significatifs (>= 5 caracteres) du titre presents.
                traitee_section = False
                if traitees:
                    if titre.lower() in traitees:
                        traitee_section = True
                    else:
                        mots_sig = [_re.sub(r"[^a-z0-9]", "", m.lower())
                                    for m in titre.split()
                                    if len(_re.sub(r"[^a-z0-9]", "",
                                                   m.lower())) >= 5]
                        presents = [m for m in mots_sig if m in traitees]
                        if len(presents) >= 2:
                            traitee_section = True
                if traitee_section:
                    continue
                contenu = " ".join(lignes[1:])
                marquee = any(mot.lower() in contenu.lower()
                              for mot in mots_traitement if mot)
                if marquee:
                    continue
                # section = derniere '## [xxx]' avant ce bloc
                avant = texte.split("### " + entete, 1)[0]
                ms = _re.findall(r"(?m)^## \[(\w+)\]", avant)
                if ms:
                    section = ms[-1]
                severite = ("ERR" if section == "urgent" else "WARN")
                ecarts.append(_ecart(
                    regles.get("demande_utilisateur_non_traitee"),
                    titre, jours=age, titre=titre[:60], section=section))

    # --- historique_agents_gele (AGENTS-activite-recente.md, encart v2) ---
    r4 = regles.get("historique_agents_gele")
    if r4 and r4.get("actif"):
        tolerance = int(seuils.get("historique_tolerance_minutes", 5))
        hist_path = os.path.join(RACINE, "AGENTS-activite-recente.md")
        h_hist = None
        j_hist = None
        if os.path.isfile(hist_path):
            texte_hist = open(hist_path, encoding="utf-8").read()
            # 1) premiere entree de l encart session-freelance
            m_encart = _re.search(
                r"(?ms)^## Activites recentes -- session-freelance\s*$"
                r"(.*?)^## ", texte_hist)
            if m_encart:
                m_entree = _re.search(
                    r"\|\s*(\d{2}:\d{2}:\d{2})", m_encart.group(1))
                if m_entree:
                    h_hist = m_entree.group(1)
                    # 2) dater : le fichier est ecrit par historiser() a
                    # CHAQUE action -> sa date de modification est celle
                    # de la derniere entree (approximation fiable).
                    mtime = datetime.fromtimestamp(
                        os.path.getmtime(hist_path))
                    j_hist = mtime.strftime("%d/%m/%Y")
        # 3) derniere activite : max des dates des messages (hors harnais)
        t_act = None
        for sous_dossier in ("inbox", "outbox"):
            dossier = os.path.join(JARVIS_DIR, sous_dossier)
            if not os.path.isdir(dossier):
                continue
            for nom_fichier in sorted(os.listdir(dossier)):
                if not nom_fichier.endswith(".jsonl"):
                    continue
                for _, _, msg in _lire_jsonl(
                        os.path.join(dossier, nom_fichier)):
                    if msg is None or msg.get("type") == "harnais-jarvis":
                        continue
                    try:
                        # dates des messages : UTC (timezone.utc) ->
                        # convertir en heure LOCALE pour comparer avec
                        # l encart (heure locale).
                        d = datetime.strptime(
                            str(msg.get("date", ""))[:19],
                            "%Y-%m-%dT%H:%M:%S")
                        d = d.replace(tzinfo=timezone.utc)
                        d = d.astimezone().replace(tzinfo=None)
                    except (ValueError, TypeError):
                        continue
                    if t_act is None or d > t_act:
                        t_act = d
        if h_hist and j_hist and t_act is not None:
            try:
                jj, mm, aaaa = j_hist.split("/")
                t_hist = datetime(int(aaaa), int(mm), int(jj),
                                  int(h_hist[:2]), int(h_hist[3:5]),
                                  int(h_hist[6:8]))
                retard = (t_act - t_hist).total_seconds() / 60.0
                if retard > tolerance:
                    ecarts.append(_ecart(
                        r4, "fixe",
                        derniere_activite=t_act.strftime("%d/%m %H:%M"),
                        derniere_trace=t_hist.strftime("%d/%m %H:%M")))
            except (ValueError, TypeError):
                pass

    # --- edith_silencieuse (cellule dormante muette) ---
    # Seuil en MINUTES (dev : le signal EDITH [EDITH-EVALUATION] arrive
    # toutes les 10 min via la routine evaluer-agents ; le harnais scanne
    # toutes les 5 min. 15 min = 1 cycle manque + marge : un serveur mort
    # est alerte sous ~15 min, sans faux positif quand tout va bien.)
    r5 = regles.get("edith_silencieuse")
    if r5 and r5.get("actif"):
        seuil_minutes = int(seuils.get("edith_silencieuse_minutes", 15))
        dernier_reveil = None
        # Signaux de vie EDITH : messages type 'reveil' OU objet
        # [EDITH-...] dans son outbox (outbox/edith.jsonl) et dans les
        # inbox des destinataires (stark.jsonl, jarvis.jsonl...).
        dossiers = [os.path.join(JARVIS_DIR, "outbox"),
                    os.path.join(JARVIS_DIR, "inbox")]
        for dossier in dossiers:
            if not os.path.isdir(dossier):
                continue
            for nom_fichier in sorted(os.listdir(dossier)):
                if not nom_fichier.endswith(".jsonl"):
                    continue
                if "edith" not in nom_fichier.lower() \
                        and nom_fichier not in ("stark.jsonl",
                                                "jarvis.jsonl"):
                    continue
                for _, _, msg in _lire_jsonl(
                        os.path.join(dossier, nom_fichier)):
                    if msg is None or msg.get("de") != "edith":
                        continue
                    objet = (msg.get("objet") or "")
                    est_reveil = (
                        msg.get("type") == "reveil"
                        or "[EDITH" in objet.upper()
                        or "[EDITH-REVEIL]" in objet.upper()
                        or "[EDITH-EVALUATION]" in objet.upper())
                    if not est_reveil:
                        continue
                    try:
                        d = datetime.strptime(
                            str(msg.get("date", ""))[:19],
                            "%Y-%m-%dT%H:%M:%S")
                    except (ValueError, TypeError):
                        continue
                    if dernier_reveil is None or d > dernier_reveil:
                        dernier_reveil = d
        if dernier_reveil is None:
            ecarts.append(_ecart(r5, "fixe", minutes=seuil_minutes,
                                 dernier_reveil="jamais"))
        else:
            age_min = ((maintenant.replace(tzinfo=None) - dernier_reveil)
                       .total_seconds() / 60.0)
            if age_min > seuil_minutes:
                ecarts.append(_ecart(r5, "fixe", minutes=int(age_min),
                                     dernier_reveil=dernier_reveil.strftime(
                                         "%d/%m %H:%M")))


# ------------------------------------------------------------------
# API publique
# ------------------------------------------------------------------

def verifier_comportement(alerter=True):
    """Scan complet : detecte les ecarts de comportement de JARVIS.

    Retourne (liste_ecarts_detectes, liste_ecarts_nouveaux_alertes).
    """
    config = charger_config()
    ecarts = []
    _detecter_sante(config, ecarts)
    _detecter_messages(config, ecarts)
    _detecter_activations(config, ecarts)
    _detecter_files(config, ecarts)
    _detecter_valeurs_en_dur(config, ecarts)
    _detecter_surveillance(config, ecarts)
    if not alerter:
        return ecarts, []
    signales = _charger_journal()
    nouveaux = [e for e in ecarts
                if (e["type"], e["cle"]) not in signales]
    if nouveaux:
        _envoyer_alerte(config, nouveaux)
    return ecarts, nouveaux


def rapport(ecarts):
    """Lignes de rapport lisibles pour le CLI."""
    if not ecarts:
        return ["AUCUN ECART : JARVIS se comporte conformement."]
    lignes = []
    for e in ecarts:
        lignes.append("[%s] %s" % (e["severite"], e["message"]))
    return lignes
