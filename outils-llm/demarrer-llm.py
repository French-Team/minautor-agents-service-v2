#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
outils-llm/demarrer-llm.py - DEMARRAGE EXCLUSIF DU LLM (ni v1, ni v2).

Un seul but : faire demarrer une session LLM SANS que le LLM ait a reflechir.
L'utilisateur fournit : id=<id> + session=<admin|freelance>.
L'outil fait TOUT le reste :
  1. Verifier/creer l'id (liaison id <-> session, agent principal Cerberus)
  2. Determiner l'agent actif REEL du bloc session dans AGENTS.md
     (admin -> Cerberus si le bloc est vide/cerberus, sinon l'agent actif ;
      freelance -> l'agent actif du bloc, jamais un agent par defaut)
  3. Synchroniser les 3 sources d'etat (bloc AGENTS.md, table Sessions
     connues, classeur variables) - le bloc est la source de verite
  4. Afficher l'agent actif, sa fiche, ses corrections et son parcours

Pour session-admin, l historisation du cycle de demarrage est centralisee
par oracle-demarrage.py afin d eviter les traces en double.

Neutre : ne depend d AUCUN dossier v1 (agents/) ni v2 (freelance/) en
import. Python stdlib uniquement. Appelle activer-agent-principal en
sous-processus uniquement pour sidentifier (creation/retrouvaille de la
session), jamais pour autre chose.
"""

import json
import os
import re
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path

VERSION = "0.1.1"
RACINE = Path(__file__).resolve().parent.parent

AGENTS_MD = RACINE / "AGENTS.md"
# Fichiers SEPARES par session (decision utilisateur 2026-08-26 : la v2
# est l evolution de la v1, chaque session a SES fichiers avec SON format) :
#   v1 (session-admin)      : AGENTS-activite-recente.md  (ASCII+LF)
#   v2 (session-freelance)  : AGENTS-activite-recente-v2.md (UTF8+CRLF)
# Le choix se fait dans demarrer() selon la session demandee.
ENCART_FILE = RACINE / "AGENTS-activite-recente.md"
CORPS_FILE = RACINE / "AGENTS-historique.md"
ENCART_FILE_V2 = RACINE / "AGENTS-activite-recente-v2.md"
CORPS_FILE_V2 = RACINE / "AGENTS-historique-v2.md"
GRADES_FILE = RACINE / "cerveau-projet" / "freelance" / "tools-commun" \
    / "grades" / "grades-v2.json"


def _couleur_agent(agent):
    """Emoji couleur du grade d un agent/routine v2 (grades-v2.json, D15).
    La colonne Grade de l encart v2 est remplie par cette couleur ; pour la
    v1 (session-admin) la colonne n existe pas (vide)."""
    try:
        data = json.loads(GRADES_FILE.read_text(encoding="utf-8"))
    except Exception:
        return ""
    grade = data.get("agents", {}).get(agent)
    if grade is None:
        grade = data.get("routines", {}).get(agent)
    if grade is None:
        return data.get("defaut", {}).get("emoji", "")
    for e in data.get("echelle", []):
        if e.get("grade") == grade:
            return e.get("emoji", "")
    return data.get("defaut", {}).get("emoji", "")


def _secteur_agent(agent):
    """Emoji secteur d un agent/routine v2 (grades-v2.json, D15).
    La colonne Secteur de l encart v2 est remplie par cette emoji."""
    try:
        data = json.loads(GRADES_FILE.read_text(encoding="utf-8"))
    except Exception:
        return "📋"
    secteurs = data.get("secteurs", {})
    for mot_cle, emoji in secteurs.items():
        if mot_cle.lower() in agent.lower():
            return emoji
    return data.get("defaut", {}).get("secteur_emoji", "📋")
CLASSEUR = RACINE / "cerveau-projet" / "agents" / "classeur-variables" / "stockage" / "variables-actuelles.md"
ACTIVER_PRINCIPAL = RACINE / "cerveau-projet" / "agents" / "tools" / "activer" / "activer-agent-principal" / "activer-agent-principal.py"
BDD_DIR = RACINE / "cerveau-projet" / "freelance" / "tools-commun" / "jarvis" / "historique"
BDD_FILE = BDD_DIR / "historique.db"

# Agents connus par session (repli uniquement si le bloc est vide ou cerberus)
AGENT_DEFAUT_ADMIN = "cerberus"
# Point d'entree de la session-freelance : TOUJOURS Stark (le coordinateur),
# jamais l'agent actif du bloc (ex: vision avec une mission en attente).
# Stark passe par JARVIS qui reprend le controle et rappelle les agents
# (ex: Vision pour finir sa mission) si besoin.
AGENT_ENTREE_FREELANCE = "stark"


# ---------------------------------------------------------------- utils texte

def lire(path):
    try:
        return path.read_text(encoding="utf-8").replace("\r\n", "\n")
    except (OSError, UnicodeDecodeError):
        try:
            return path.read_text(encoding="latin-1").replace("\r\n", "\n")
        except OSError:
            return ""


def ecrire(path, contenu):
    """Ecrire au format du fichier cible : les fichiers v1 (sans '-v2')
    sont en ASCII+LF, les fichiers -v2 en UTF8+CRLF (convention v2, D4).
    write_text nu sur Windows ecrit en CRLF -> corromprait les v1."""
    path.parent.mkdir(parents=True, exist_ok=True)
    contenu = contenu.replace("\r\n", "\n")
    if "-v2." in path.name:
        contenu = contenu.replace("\n", "\r\n")
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(contenu)
    else:
        contenu = contenu.encode("ascii", errors="replace").decode("ascii")
        with open(path, "w", encoding="ascii", newline="\n") as fh:
            fh.write(contenu)


def timestamp_3():
    return datetime.now().strftime("%H:%M:%S.") + datetime.now().strftime("%f")[:3]


def tronquer(texte, n=80):
    if len(texte) <= n:
        return texte
    return texte[:n] + "..."


# ------------------------------------------------------------ bloc session

def lire_bloc_session(contenu_agents, session):
    """Extraire le bloc '### Session : <session>' et ses champs (dict)."""
    lignes = contenu_agents.splitlines()
    debut = None
    for i, ligne in enumerate(lignes):
        if ligne.strip() == "### Session : %s" % session:
            debut = i
            break
    if debut is None:
        return {}
    fin = len(lignes)
    for i in range(debut + 1, len(lignes)):
        if lignes[i].startswith("### Session") or lignes[i].startswith("## "):
            fin = i
            break
    champs = {}
    for ligne in lignes[debut:fin]:
        if "|" not in ligne:
            continue
        parties = [p.strip() for p in ligne.split("|")]
        for j, p in enumerate(parties):
            if p.startswith("**") and p.endswith("**") and j + 1 < len(parties):
                cle = p.strip("*").strip()
                champs[cle] = parties[j + 1].strip()
    return champs


def lire_table_sessions(contenu_agents):
    """Extraire la table '## Sessions connues' : {session: {id, agent, date}}."""
    result = {}
    m = re.search(r"## Sessions connues\n(.*?)(?:\n## |\Z)", contenu_agents, re.S)
    if not m:
        return result
    for ligne in m.group(1).splitlines():
        if not ligne.strip().startswith("|") or "---" in ligne:
            continue
        parties = [p.strip() for p in ligne.strip().strip("|").split("|")]
        if len(parties) >= 4 and parties[0].startswith("session-"):
            result[parties[0]] = {
                "id": parties[1], "agent": parties[2], "date": parties[3]}
    return result


def lire_classeur_profils(contenu_classeur):
    """Extraire les profils session du classeur : {session: ligne_brute}."""
    profils = {}
    for ligne in contenu_classeur.splitlines():
        if "profil-session-" not in ligne or not ligne.strip().startswith("|"):
            continue
        m = re.search(r"profil-session-([a-z0-9-]+)", ligne)
        if m:
            profils["session-" + m.group(1)] = ligne
    return profils


def maj_table_sessions(contenu_agents, session, id_llm, agent, date_heure):
    """Mettre a jour la ligne de la table Sessions connues (alignement bloc)."""
    lignes = contenu_agents.splitlines()
    in_table = False
    trouve = False
    for i, ligne in enumerate(lignes):
        if ligne.strip().startswith("## Sessions connues"):
            in_table = True
            continue
        if in_table and ligne.strip().startswith("## "):
            break
        if in_table and ligne.strip().startswith("|") and "session-" in ligne:
            parties = [p.strip() for p in ligne.strip().strip("|").split("|")]
            if len(parties) >= 4 and parties[0] == session:
                parties[1] = id_llm
                parties[2] = agent
                parties[3] = date_heure
                lignes[i] = "| " + " | ".join(parties) + " |"
                trouve = True
    if not trouve:
        # ajouter une ligne a la fin de la table
        for i, ligne in enumerate(lignes):
            if ligne.strip().startswith("| Session | Nom LLM"):
                j = i + 1
                while j < len(lignes) and lignes[j].strip().startswith("|"):
                    j += 1
                lignes.insert(j, "| %s | %s | %s | %s |"
                              % (session, id_llm, agent, date_heure))
                break
    return "\n".join(lignes)


def maj_classeur(contenu_classeur, session, id_llm, agent, date_heure):
    """Mettre a jour la ligne profil-session-<session> du classeur."""
    id_session = session[len("session-"):] if session.startswith("session-") else session
    cle = "profil-session-" + id_session
    date_jour = datetime.now().strftime("%Y-%m-%d")
    nouvelle = ("| `%s` | session: %s / id: %s / agent: %s / date: %s | "
                "activer-agent-principal | %s | [OK] |"
                % (cle, session, id_llm, agent, date_heure, date_jour))
    lignes = contenu_classeur.splitlines()
    for i, ligne in enumerate(lignes):
        if "profil-session-" + id_session in ligne and ligne.strip().startswith("|"):
            lignes[i] = nouvelle
            return "\n".join(lignes)
    # ajouter apres la derniere ligne de tableau
    for i in range(len(lignes) - 1, -1, -1):
        if lignes[i].strip().startswith("|"):
            lignes.insert(i + 1, nouvelle)
            return "\n".join(lignes)
    lignes.append(nouvelle)
    return "\n".join(lignes)


# ------------------------------------------------------------- historisation

def _historiser_v1_via_aap(agent, raison):
    """Historiser le demarrage v1 via la voie officielle
    (activer-agent-principal.ajouter_historique) : corps + encart 10
    colonnes avec EXECUTEUR=demarrer-llm + BDD. Retourne 0 si OK."""
    aap_path = RACINE / "cerveau-projet" / "agents" / "tools" / "activer" \
        / "activer-agent-principal" / "activer-agent-principal.py"
    if not aap_path.is_file():
        print("  [HISTORISATION] aap introuvable, repli sur l ancien format")
        return 1
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("aap_v1", str(aap_path))
        aap = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(aap)
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.000")
        rc = aap.ajouter_historique(ts, "session-admin", agent, raison,
                                    type_round="R", executeur="demarrer-llm")
        return 0 if rc == 0 else 1
    except Exception as exc:
        print("  [HISTORISATION] erreur aap : %s" % exc)
        return 1


def historiser(agent, raison, session):
    """Ecrire dans les 3 destinations (encart 50 max, corps 100 max, BDD 7j).
    Chaque session ecrit dans SES fichiers (decision 2026-08-26) :
    session-admin -> AGENTS-activite-recente.md + AGENTS-historique.md (v1,
    ASCII+LF) ; session-freelance -> AGENTS-activite-recente-v2.md +
    AGENTS-historique-v2.md (v2, UTF8+CRLF).

    v0.1.2 (2026-08-29, decision utilisateur : la case Executeur reste
    vide) : pour la session-admin (v1), l historisation est DELEGUEE a
    activer-agent-principal.ajouter_historique (la voie officielle) avec
    executeur="demarrer-llm" -> la ligne de l encart v1 porte le bon format
    10 colonnes (Grade | Agent | Defcon | EXECUTEUR | Etat | Secteur |
    Raison | Heure | id | Type) et la colonne Executeur n est plus vide.
    L ancien format 5 colonnes de demarrer-llm (| Heure | Agent | id |
    Type | Raison |) etait obsolete et faisait hurler la routine encart
    (Etat inconnu). La v2 (freelance) garde sa logique existante (fichiers
    v2 distincts)."""
    if session == "session-admin":
        return _historiser_v1_via_aap(agent, raison)
    global ENCART_FILE, CORPS_FILE
    if session == "session-freelance":
        ENCART_FILE = ENCART_FILE_V2
        CORPS_FILE = CORPS_FILE_V2
    else:
        ENCART_FILE = RACINE / "AGENTS-activite-recente.md"
        CORPS_FILE = RACINE / "AGENTS-historique.md"
    date_iso = datetime.now().strftime("%Y-%m-%d")
    heure = timestamp_3()

    # 1. Encart AGENTS-activite-recente.md
    contenu = lire(ENCART_FILE)
    section = "## Activites recentes -- %s" % session
    # trouver l'id LLM dans le bloc pour la colonne id
    agents = lire(AGENTS_MD)
    bloc = lire_bloc_session(agents, session)
    id_llm = bloc.get("Nom LLM", "")
    v2 = (session == "session-freelance")
    if v2:
        # v2 : colonne Grade + Secteur (7 colonnes, decision 2026-08-27)
        ligne = "| %s | %s | %s | %s | %s | %s | R |" % (
            _couleur_agent(agent), agent, _secteur_agent(agent),
            tronquer(raison), heure, id_llm)
    else:
        ligne = "| %s | %s | %s | R | %s |" % (heure, agent, id_llm, tronquer(raison))
    if section in contenu:
        # ORDRE : plus recent EN HAUT (juste apres l'en-tete du tableau).
        # Ne JAMAIS inserer en bas de section (les activations disparaissent
        # du champ de vision - lecon 2026-08-26, retour utilisateur).
        lignes = contenu.splitlines()
        idx = lignes.index(section) if section in lignes else None
        if idx is not None:
            # trouver la ligne d'en-tete du tableau (la 1re ligne '|' apres
            # la section) puis la 2e ligne de donnees... on insere APRES
            # l'en-tete (ligne 1) et la ligne de separation (ligne 2).
            j = idx + 1
            while j < len(lignes) and not lignes[j].strip().startswith("|"):
                j += 1
            # j = en-tete (| Heure | Agent | ... |)
            k = j + 1
            # k = ligne de separation (|-------|) - on insere APRES
            if k < len(lignes) and "---" in lignes[k]:
                k += 1
            lignes.insert(k, ligne)
            # limiter a 50 lignes de donnees dans la section (les plus
            # recentes = les premieres lignes du tableau)
            debut = idx
            fin = len(lignes)
            for t in range(idx + 1, len(lignes)):
                if lignes[t].strip().startswith("## "):
                    fin = t
                    break
            donnees = [l for l in lignes[debut + 1:fin]
                       if l.strip().startswith("|") and "---" not in l]
            if len(donnees) > 50:
                a_retirer = donnees[50:]
                for l in a_retirer:
                    if l in lignes:
                        lignes.remove(l)
            contenu = "\n".join(lignes)
    else:
        if v2:
            entete = ("| Grade | Agent | Secteur | Raison | Heure | id | Type |\n"
                      "|-------|-------|---------|--------|-------|----|------|")
        else:
            entete = ("| Heure | Agent | id | Type | Raison |\n"
                      "|-------|-------|----|------|--------|")
        contenu += "\n%s\n\n%s\n%s\n" % (section, entete, ligne)
    ecrire(ENCART_FILE, contenu)

    # 2. Corps AGENTS-historique(-v2).md -- format de section : ## JJ/MM/AAAA
    #    (meme format que la v1 et que historique.py v2 ; NE PAS utiliser
    #    ISO YYYY-MM-DD : cree des sections paralleles vides, detectees
    #    comme KO par test-098).
    contenu = lire(CORPS_FILE)
    entree = "- %s | %s | R | %s" % (heure, agent, raison)
    date_jour = datetime.now().strftime("%d/%m/%Y")
    if date_jour in contenu:
        lignes = contenu.splitlines()
        idx = None
        for i, l in enumerate(lignes):
            if l.strip() == "## %s" % date_jour:
                idx = i
                break
        if idx is not None:
            lignes.insert(idx + 1, entree)
        else:
            lignes.append("")
            lignes.append("## %s" % date_jour)
            lignes.append("")
            lignes.append(entree)
        contenu = "\n".join(lignes)
    else:
        contenu += "\n## %s\n\n%s\n" % (date_jour, entree)
    # limiter le corps a 100 entrees (les plus recentes conservees)
    entrees = [l for l in contenu.splitlines() if l.strip().startswith("- ")]
    if len(entrees) > 100:
        surplus = entrees[:-100]
        for e in surplus:
            contenu = contenu.replace(e + "\n", "", 1)
            contenu = contenu.replace(e, "", 1)
    ecrire(CORPS_FILE, contenu)

    # 3. BDD SQLite (7 jours, purge lazy) - schema partage partout
    #    (id, date_iso, agent, llm, type_action, raison)
    BDD_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(BDD_FILE))
    conn.execute("CREATE TABLE IF NOT EXISTS historique ("
                 "id INTEGER PRIMARY KEY AUTOINCREMENT, date_iso TEXT, "
                 "agent TEXT, llm TEXT, type_action TEXT, raison TEXT)")
    # purge : supprimer les entrees de plus de 7 jours (date_iso ISO)
    seuil = (datetime.now().timestamp() - 7 * 86400)
    try:
        conn.execute("DELETE FROM historique WHERE date_iso < ?",
                     (datetime.fromtimestamp(seuil).strftime("%Y-%m-%dT%H:%M:%S"),))
    except sqlite3.OperationalError:
        pass  # schema ancien sans date_iso : purge ignoree
    ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    conn.execute("INSERT INTO historique (date_iso, agent, llm, type_action, raison) "
                 "VALUES (?,?,?,?,?)", (ts, agent, id_llm or "", "R", raison))
    conn.commit()
    conn.close()


# ------------------------------------------------------------------ actions

def verifier_coherence(agents_contenu, classeur_contenu, session):
    """Comparer bloc / table Sessions connues / classeur. Retour liste ecarts."""
    ecarts = []
    bloc = lire_bloc_session(agents_contenu, session)
    table = lire_table_sessions(agents_contenu)
    profils = lire_classeur_profils(classeur_contenu)

    agent_bloc = bloc.get("Nom Agent", "")
    id_bloc = bloc.get("Nom LLM", "")

    if session in table:
        ligne_table = table[session]
        if ligne_table.get("agent", "") != agent_bloc:
            ecarts.append("table Sessions connues: agent=%s vs bloc=%s"
                          % (ligne_table.get("agent"), agent_bloc))
        if ligne_table.get("id", "") != id_bloc:
            ecarts.append("table Sessions connues: id=%s vs bloc=%s"
                          % (ligne_table.get("id"), id_bloc))
    else:
        ecarts.append("session absente de la table Sessions connues")

    if session in profils:
        ligne = profils[session]
        m_agent = re.search(r"agent:\s*([a-z0-9-]+)", ligne)
        m_id = re.search(r"id:\s*([a-z0-9-]+)", ligne)
        if m_agent and m_agent.group(1) != agent_bloc:
            ecarts.append("classeur: agent=%s vs bloc=%s"
                          % (m_agent.group(1), agent_bloc))
        if m_id and m_id.group(1) != id_bloc:
            ecarts.append("classeur: id=%s vs bloc=%s" % (m_id.group(1), id_bloc))
    else:
        ecarts.append("profil classeur absent pour %s" % session)
    return ecarts


def demarrer(llm_id, session):
    print("=== DEMARRAGE LLM (outils-llm/demarrer-llm.py v%s) ===" % VERSION)
    print("  id     : %s" % llm_id)
    print("  session: %s" % session)

    # 0. Pour admin, le nettoyage/serveur de demarrage est responsable de
    #    l activation de Cerberus. On ne lit plus ni ne restaure un agent ici.
    #    Cela evite une activation prematuree et les doubles traces.
    agents_avant = lire(AGENTS_MD)
    bloc_avant = lire_bloc_session(agents_avant, session)
    agent_avant = bloc_avant.get("Nom Agent", "")

    # 0bis. DETECTION DES ERREURS BLOQUANTES (decision utilisateur
    #   2026-08-29) : appeler detecter-erreur-bloquante AVANT sidentifier
    #   pour AFFICHER le diagnostic debranchant (marbre divise, daemon mort,
    #   etat-carte incoherent) AU LIEU de bloquer sur le message cryptique de
    #   sidentifier. Affichage NON bloquant : on poursuit quand meme.
    detecteur = RACINE / "cerveau-projet" / "agents" / "tools" / "detecter" \
        / "detecter-erreur-bloquante" / "detecter-erreur-bloquante.py"
    if detecteur.is_file():
        try:
            rd = subprocess.run([sys.executable, str(detecteur), "--status"],
                                capture_output=True, text=True, timeout=60)
            if rd.stdout:
                print((rd.stdout or "").rstrip())
            if rd.returncode == 4:
                print("[DEMARRAGE] La routine detecter-erreur-bloquante a signale"
                      " AU MOINS UNE condition bloquante (voir ci-dessus).")
                print("[DEMARRAGE] Traitez les blocs OU CHERCHER / REPARER avant"
                      " de lancer le round, sinon il risque de ne pas s enclencher.")
        except Exception as e:
            print("[DEMARRAGE] detecter-erreur-bloquante indisponible (%s)" % e)

    # 1. Verifier/creer l'id via activer-agent-principal sidentifier.
    # Pour admin, sidentifier initialise uniquement l identite; Cerberus
    # sera active une seule fois par oracle-demarrage apres lecture Oracle.
    cmd = [sys.executable, str(ACTIVER_PRINCIPAL), "sidentifier", llm_id, session]
    r = subprocess.run(cmd, capture_output=True, text=True)
    for ligne in (r.stdout or "").splitlines():
        if ligne.strip():
            print("  [sidentifier] %s" % ligne.strip())
    if r.returncode != 0:
        print("ERREUR: sidentifier a echoue (code %s)" % r.returncode)
        if r.stderr:
            print((r.stderr or "")[-2000:])
        return 1

    # 2. Determiner l'agent a incarner
    #    session-freelance : TOUJOURS Stark (point d'entree, decision
    #    utilisateur 2026-08-26) - jamais l'agent actif du bloc (ex: vision
    #    avec une mission en attente). Stark passe par JARVIS.
    #    session-admin : l'agent actif du bloc PRESERVE (sidentifier vient de
    #    poser Cerberus ; on restaure l'agent reel s'il existait avant).
    agents = lire(AGENTS_MD)
    bloc = lire_bloc_session(agents, session)
    id_bloc = bloc.get("Nom LLM", "")
    if session == "session-freelance":
        agent_actif = AGENT_ENTREE_FREELANCE
        print("  point d'entree freelance : Stark (coordinateur, decision"
              " utilisateur) - pas l'agent du bloc (%s)" % bloc.get("Nom Agent", "?"))
    else:
        agent_actif = AGENT_DEFAUT_ADMIN
        print("  session-admin : initialisation systeme; Cerberus sera active par oracle-demarrage")

    # 3. Synchroniser les 3 sources (bloc = source de verite)
    classeur = lire(CLASSEUR)
    ecarts = verifier_coherence(agents, classeur, session)
    date_heure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if ecarts:
        print("  [ALIGNEMENT] %d ecart(s) detecte(s) :" % len(ecarts))
        for e in ecarts:
            print("    - %s" % e)
        agents = maj_table_sessions(agents, session, id_bloc or llm_id,
                                    agent_actif, date_heure)
        classeur = maj_classeur(classeur, session, id_bloc or llm_id,
                                agent_actif, date_heure)
        ecrire(AGENTS_MD, agents)
        ecrire(CLASSEUR, classeur)
        print("  [ALIGNEMENT] table Sessions connues + classeur realignes"
              " sur le bloc (source de verite).")
    else:
        print("  [COHERENCE] 3 sources alignees (bloc / table / classeur).")

    # 3bis. session-freelance : activer Stark dans le bloc session
    #    (sidentifier a pose Cerberus / l'ancien agent ; il faut Stark)
    #    puis lancer la chaine de demarrage JARVIS (daemon routines + DEFCON
    #    + files + operationnel) pour que les serveurs tournent.
    if session == "session-freelance":
        raison_act = ("DEMARRAGE SESSION FREELANCE : Stark prend le relais,"
                      " JARVIS reprendra le controle (rappel Vision si"
                      " mission en attente)")
        cmd_act = [sys.executable, str(ACTIVER_PRINCIPAL), "activer",
                   session, agent_actif, raison_act]
        r_act = subprocess.run(cmd_act, capture_output=True, text=True)
        if r_act.returncode == 0:
            print("  [ACTIVATION] Stark active dans le bloc session-freelance.")
        else:
            print("  [ATTENTION] activation Stark a echoue (code %s)"
                  % r_act.returncode)
        # relire le bloc apres activation (la table + classeur sont sync par
        # activer-agent-principal)
        agents = lire(AGENTS_MD)
        bloc = lire_bloc_session(agents, session)
        id_bloc = bloc.get("Nom LLM", "")
        # lancer la chaine de demarrage JARVIS (daemon routines + DEFCON +
        # files + operationnel) - le serveur de demarrage reprend la main
        jarvis_py = RACINE / "cerveau-projet" / "freelance" / "tools-commun" / "jarvis" / "jarvis.py"
        if jarvis_py.exists():
            cmd_jarvis = [sys.executable, str(jarvis_py), "demarrage",
                          "--session", session]
            r_j = subprocess.run(cmd_jarvis, capture_output=True, text=True)
            for ligne in (r_j.stdout or "").splitlines():
                print("  [JARVIS] %s" % ligne.strip())
            if r_j.stderr:
                print("  [JARVIS-ERR] %s" % (r_j.stderr or "")[-500:])
        else:
            print("  [ATTENTION] jarvis.py introuvable, serveurs non demarres")

    # 4. L historisation du demarrage admin est centralisee par
    #    oracle-demarrage.py. Cela evite le doublon entre sidentifier,
    #    demarrer-llm et le serveur de demarrage. Le freelance conserve son
    #    chemin d historisation existant.
    if session != "session-admin":
        raison = "DEMARRAGE LLM : id=%s, session=%s, agent actif=%s, parcours demarre" \
                 % (llm_id, session, agent_actif)
        historiser(agent_actif, raison, session)
        print("  [HISTORISATION] demarrage trace (encart + corps + BDD).")
    else:
        print("  [HISTORISATION] session-admin : cycle centralise par oracle-demarrage.")

    # 5. Afficher l'agent actif et son parcours
    print()
    print("=== RESULTAT DU DEMARRAGE ===")
    print("  Agent actif   : %s" % agent_actif)
    print("  Session       : %s" % session)
    print("  ID LLM        : %s" % (id_bloc or llm_id))
    def _md_lien(valeur):
        """Extraire le lien d'un champ markdown [texte](lien) ou retourner brut."""
        m = re.search(r"\((\S+?)\)", valeur)
        return m.group(1) if m else valeur
    fiche = _md_lien(bloc.get("Fiche", ""))
    corrections = _md_lien(bloc.get("Corrections", ""))
    if fiche:
        print("  Fiche         : %s" % fiche)
    if corrections:
        print("  Corrections   : %s" % corrections)
    print()
    print("  PROCHAINES ETAPES POUR LE LLM :")
    print("  1. Relis TA fiche puis TES corrections (chacun lit les siens).")
    # L'arbre v2 PRIME (decision 2026-08-29 : les agents v1 ont migre vers les
    # arbres v2 - protocole-reparer-arbres / protocole-carte-decision).
    # Un agent v1 (agents/) qui a un arbre v2 -> guider-arbre arbre-<agent>.json
    # (l'arbre pilote via oracle, PAS le parcours v1). Repli : parcours v1.
    dossier_v1 = RACINE / "cerveau-projet" / "agents" / agent_actif
    dossier_v2 = RACINE / "cerveau-projet" / "freelance" / agent_actif
    # Le nom du DOSSIER est en minuscules (convention cerveau-projet) alors que
    # agent_actif vient du bloc AGENTS.md (ex: 'Cerberus'). Normaliser pour
    # pointer vers le chemin REEL sur les systemes sensibles a la casse.
    nom_dossier = agent_actif.lower()
    arbre_v1 = dossier_v1 / "parcours" / ("arbre-%s.json" % nom_dossier)
    arbre_v2 = dossier_v2 / "parcours" / ("arbre-%s.json" % nom_dossier)
    if arbre_v1.exists():
        print("  2. Suis TON arbre de decisions (v2) : guider-arbre.py")
        print("     cerveau-projet/agents/%s/parcours/arbre-%s.json"
              % (nom_dossier, nom_dossier))
    elif arbre_v2.exists():
        print("  2. Suis TON arbre de decisions (v2) :")
        print("     cerveau-projet/freelance/%s/parcours/arbre-%s.json"
              % (nom_dossier, nom_dossier))
    elif (dossier_v1 / "parcours" / ("parcours-%s.json" % nom_dossier)).exists():
        print("  2. Suis ton parcours (v1, pas encore migre vers l arbre v2) :")
        print("     guider-parcours.py cerveau-projet/agents/%s/parcours/parcours-%s.json"
              % (nom_dossier, nom_dossier))
    else:
        print("  2. (aucun parcours/arbre detecte pour %s)" % agent_actif)
    print()
    print("=== DEMARRAGE TERMINE - LE LLM EST ACTIVE + HISTORISE + PRET ===")
    return 0


def afficher_aide():
    print("usage: demarrer-llm.py <id> <session>")
    print()
    print("DEMARRAGE EXCLUSIF DU LLM (ni v1, ni v2) - outils-llm/")
    print("L'utilisateur fournit : id=<id> + session=<admin|freelance>.")
    print("L'outil fait tout le reste : verifier/creer l'id, initialiser la")
    print("bonne session, synchroniser les 3 sources et afficher le")
    print("parcours de l'agent actif.")
    print()
    print("exemples :")
    print("  python3 outils-llm/demarrer-llm.py glm5 admin")
    print("  python3 outils-llm/demarrer-llm.py freebuff freelance")
    print()
    print("options :")
    print("  --help, -h   Afficher cette aide")


def main(argv):
    if argv and argv[0] in ("--help", "-h", "aide"):
        afficher_aide()
        return 0
    if argv and argv[0] == "--version":
        print("demarrer-llm v%s" % VERSION)
        return 0
    if not argv:
        print("ERREUR: id et session obligatoires (ex: demarrer-llm.py glm5 admin)")
        afficher_aide()
        return 1
    if len(argv) < 2:
        print("ERREUR: id et session obligatoires (ex: demarrer-llm.py glm5 admin)")
        afficher_aide()
        return 1
    llm_id = argv[0]
    session = argv[1]
    if session in ("admin", "freelance"):
        session = "session-" + session
    if not session.startswith("session-"):
        print("ERREUR: session invalide '%s' (admin ou freelance attendu)" % argv[1])
        return 1
    return demarrer(llm_id, session)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
