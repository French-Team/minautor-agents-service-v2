#!/usr/bin/env python3
# -*- coding: ascii -*-
# proteger-verrou-habilitation.py
#
# VERROU D HABILITATION : une protection d outil qui bloque l utilisation par
# un agent NON habilite, AVANT que l action ne soit executee.
#
# La regle de gouvernance (regles-groupes-agents.md) : certaines actions sont
# EXCLUSIVES a un agent (seul janus lance la non-regression, seul hygie
# supprime, seul morpheus ecrit les tests, seul clio met a jour le README).
# Le verrou mecanise cette regle A LA SOURCE : quand un agent veut utiliser un
# outil, il passe par le verrou avec --agent <nom> ; si l outil n est pas dans
# SA table d habilitation (agents/habilitation/habilitation-<agent>.json), le
# verrou BLOQUE et indique QUI est habilite et COMMENT l activer (cycle
# Cerberus -> agent).
#
# SOURCE DE VERITE : la table d habilitation DEDIEE (cerveau-projet/agents/
# habilitation/habilitation-<agent>.json, un fichier par agent, champ "outils").
# La table a ete creee le 2026-09-05 (migration v1->v2) en fusionnant les
# parcours v1 (retires depuis) + les arbres/themes v2 + les P0 partages.
# Un agent est habilite pour un outil SI ET SEULEMENT SI l outil figure dans
# SON fichier d habilitation. Aucune liste en dur dans ce script : la table
# EST la regle (anti-derive, meme philosophie que test-035/037/045).
#
# IDENTITE REELLE (v0.2.0, 2026-08-15, demande utilisateur) : le verrou
# verifie en plus que l agent DECLARE (--agent) est bien l agent REEL de la
# session (colonne Agent actif de la table '## Sessions connues' d AGENTS.md,
# reconstruite par activer-agent-principal). Un script lance par Cerberus qui
# se fait passer pour janus est ainsi BLOQUE : la session porte Cerberus, pas
# janus. Mode --audit (reserve aux tests) : verifie la table d habilitation
# SANS verifier l identite reelle, pour les preuves formelles.
#
# AUTO-JOURNALISATION (v0.2.0, demande utilisateur "flicage") : le verrou
# journalise lui-meme chaque appel :
#   - usage AUTORISE  -> registre-usages-outils.jsonl (mode verrou-auto)
#   - tentative BLOQUEE -> registre-tentatives-bloquees.jsonl (espionnage :
#     qui a essaye d utiliser quoi, et quel agent reel etait actif)
# L agent n a donc plus besoin de se declarer pour les outils passes au verrou :
# c est l outil qui signale son propre usage.
#
# Usage :
#   python3 proteger-verrou-habilitation.py --agent <nom> --outil <nom>
#   python3 proteger-verrou-habilitation.py --agent janus --outil tester-lancer-non-regression
#   python3 proteger-verrou-habilitation.py --agent janus --outil tester-lancer-non-regression --audit
#   python3 proteger-verrou-habilitation.py --liste            (affiche la table outil -> agents)
#
# Options :
#   --agent <nom>    : nom de l agent appelant (OBLIGATOIRE)
#   --outil <nom>    : nom de l outil a utiliser (OBLIGATOIRE)
#   --audit          : mode audit/tests - verifie la table d habilitation sans
#                      verifier l identite reelle de la session (reserve aux
#                      preuves formelles des tests ; les outils en production
#                      ne l utilisent jamais)
#   --liste          : affiche la table complete des habilitations
#   --verbose        : detail du verdict
#   --version
#
# Codes de sortie :
#   0 : OK - l agent est habilite pour l outil (verrou ouvert)
#   1 : BLOQUE - l agent n est pas habilite OU usurpation d identite
#   2 : erreur d utilisation (agent/outil manquant, agent inconnu,
#       identite de session indeterminable)
#
# Version : 0.6.0 (2026-09-05, migration v1->v2) : source de verite = table
# d habilitation DEDIEE (agents/habilitation/habilitation-<agent>.json) au
# lieu des cartes/parcours v1 (retires). Aucune perte d habilitation.
# Version : 0.5.0 (precedente : cartes de decision v1 = source)
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
# =============================================================================
# REGLE IMMUABLE DE NOMMAGE : le nom commence par le prefixe du dossier de
# categorie (proteger-).
# =============================================================================
"""
proteger-verrou-habilitation.py
proteger-verrou-habilitation

Usage:
  proteger-verrou-habilitation.py [OPTIONS]

Options:
  --version            Afficher la version
  --aide, -h           Afficher cette aide
"""

import argparse
import datetime
import io
import json
import os
import re
import subprocess
import sys

VERSION = "0.6.0"

AGENTS_DIR = None          # racine/cerveau-projet/agents (detectee)
PROJECT_ROOT = None        # racine du projet (contient AGENTS.md)


def detecter_racine():
    """Detecte la racine du projet (dossier contenant AGENTS.md)."""
    global PROJECT_ROOT, AGENTS_DIR
    courant = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isfile(os.path.join(courant, "AGENTS.md")):
            PROJECT_ROOT = courant
            AGENTS_DIR = os.path.join(courant, "cerveau-projet", "agents")
            return
        parent = os.path.dirname(courant)
        if parent == courant:
            sys.stderr.write("ERREUR : racine du projet introuvable (AGENTS.md absent).\n")
            sys.exit(2)
        courant = parent


def charger_parcours(chemin):
    """Charge un parcours JSON (retourne {} si illisible)."""
    try:
        with io.open(chemin, "r", encoding="utf-8") as f:
            return json.load(f)
    except (IOError, ValueError):
        return {}


def lister_habilitation():
    """Liste les fichiers de la table d habilitation dediee
    (habilitation-<agent>.json) de tous les agents v1."""
    dossier = os.path.join(AGENTS_DIR, "habilitation")
    if not os.path.isdir(dossier):
        return []
    resultats = []
    for fichier in sorted(os.listdir(dossier)):
        if fichier.startswith("habilitation-") and fichier.endswith(".json"):
            nom_agent = fichier[len("habilitation-"):-len(".json")]
            resultats.append((nom_agent, os.path.join(dossier, fichier)))
    return resultats


# (2026-09-05, migration v1->v2) : les P0 partages (guider-arbre,
# guider-parcours, lire-activite-recente) sont desormais inscrits DANS la
# table d habilitation dediee de chaque agent (fichiers habilitation-*.json),
# plus besoin de les injecter ici : la table EST la regle.


def charger_outils_habilitation(chemin):
    """Charge le champ 'outils' d un fichier de la table d habilitation
    dediee (retourne set() si illisible)."""
    data = charger_parcours(chemin)
    if not isinstance(data, dict):
        return set()
    outils = data.get("outils", [])
    if not isinstance(outils, list):
        return set()
    return {o for o in outils if isinstance(o, str) and o}


def construire_table():
    """Construit la table outil -> set(agents habilites) depuis la table
    d habilitation DEDIEE (un fichier habilitation-<agent>.json par agent).
    La table contient tout (outils de la carte + P0 partages) : aucune
    injection supplementaire ici."""
    table = {}
    for nom_agent, chemin in lister_habilitation():
        for outil in charger_outils_habilitation(chemin):
            table.setdefault(outil, set()).add(nom_agent)
    return table


def session_par_defaut():
    """MULTI-SESSIONS (v0.2.2) : session de l appelant -- variable
    d environnement SESSION_LLM (ex: session-admin, session-llm-4), sinon
    premiere session du classeur-variables, sinon session-llm-1 en secours."""
    env = os.environ.get("SESSION_LLM", "").strip()
    if env:
        return env
    classeur = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                            "classeur-variables", "stockage",
                            "variables-actuelles.md")
    try:
        with io.open(classeur, "r", encoding="utf-8") as f:
            for ligne in f:
                m = re.search(r"session: (session-[A-Za-z0-9_-]+)", ligne)
                if m:
                    return m.group(1)
    except IOError:
        pass
    return "session-llm-1"


def trouver_session_agent(agent):
    """Trouve la session (session-<nom> ou session-llm-N) de l agent
    appelant dans AGENTS.md.
    MULTI-SESSIONS (v0.4.2) : utilise la table '## Sessions connues' et
    retourne la session la PLUS RECENTE (colonne Derniere activite) parmi
    celles dont l agent actif correspond -- plus de premier bloc du fichier
    (l ordre des blocs de session est independant de la recence, 2 sessions
    peuvent porter le meme agent actif : la commande suggeree par le verrou
    doit viser la session de l appelant).
    SESSIONS NOMMEES (v0.7.0) : session-admin / session-freelance acceptees.
    Fallback : session de l appelant (SESSION_LLM ou classeur)."""
    chemin = os.path.join(PROJECT_ROOT, "AGENTS.md")
    try:
        with io.open(chemin, "r", encoding="utf-8") as f:
            contenu = f.read()
    except IOError:
        return session_par_defaut()
    m = re.search(r"## Sessions connues\n(.*?)(?=\n## |\Z)", contenu, re.S)
    if not m:
        return session_par_defaut()
    candidats = []
    for ligne in m.group(1).splitlines():
        ligne = ligne.strip()
        if not ligne.startswith("| session-"):
            continue
        cellules = [c.strip() for c in ligne.strip("|").split("|")]
        if len(cellules) < 4:
            continue
        session, agent_actif, activite = cellules[0], cellules[2], cellules[3]
        if agent_actif.lower() != agent.lower():
            continue
        if not session.startswith("session-"):
            continue
        candidats.append((activite, session))
    if not candidats:
        return session_par_defaut()
    # Session la plus recente = Derniere activite max (colonne 4)
    candidats.sort(key=lambda c: c[0], reverse=True)
    return candidats[0][1]


def agent_actif_session():
    """Retourne l agent actif REEL de la session (colonne 'Agent actif' de la
    table '## Sessions connues' d AGENTS.md, session la plus recente), ou None
    si la table est absente/illisible."""
    chemin = os.path.join(PROJECT_ROOT, "AGENTS.md")
    try:
        with io.open(chemin, "r", encoding="utf-8") as f:
            contenu = f.read()
    except IOError:
        return None
    m = re.search(r"## Sessions connues\n(.*?)(?=\n## |\Z)", contenu, re.S)
    if not m:
        return None
    lignes = []
    for ligne in m.group(1).splitlines():
        ligne = ligne.strip()
        if not ligne.startswith("| session-"):
            continue
        cellules = [c.strip() for c in ligne.strip("|").split("|")]
        if len(cellules) >= 4:
            lignes.append(cellules)
    if not lignes:
        return None
    # session la plus recente = Derniere activite max (colonne 4)
    lignes.sort(key=lambda c: c[3], reverse=True)
    actif = lignes[0][2].strip()
    return actif if actif and actif != "-" else None


def verif_missions_oracle(agent):
    """Verrou interne (v0.5.0) : interroge oracle pour verifier qu une
    mission EN_ATTENTE ou PRISE existe pour l agent declare. Retourne
    (ok, detail). En mode hybride du blueprint, le fait qu une mission
    reliee DESIGN E cet agent (et non seulement reecrite a la main dans
    AGENTS.md) est le signal d une incarnation reelle.
    Ne lance jamais d erreur : en cas d indisponibilite d oracle, retourne
    (None, "oracle indisponible") pour que l appelant decide (mode strict
    = bloque ; le verrou par defaut n ajoute pas ce croisement)."""
    # Interroge les deux statuts actifs (PRISE = mission relayee, EN_ATTENTE
    # = mission passee en file non encore relayee). Une incarnation reelle
    # correspond a une mission PRISE ou EN_ATTENTE pour l agent declare.
    # Chemin fiable vers oracle.py : on remonte depuis __file__ de CE script
    # (chemin natif correct en Windows) plutot que de PROJECT_ROOT (forme
    # MSYS /z/ qui serait double-prefixe Z:\z\ une fois lance a nouveau).
    # Si __file__ est en forme MSYS (/z/...), on convertit en X:\... : un
    # subprocess Windows ne resout pas les chemins MSYS.
    def _chemin_natif(chemin):
        if re.match(r"^/[a-zA-Z]/", chemin):
            return chemin[1].upper() + ":" + chemin[2:].replace("/", "\\")
        return chemin

    try:
        ici = os.path.dirname(os.path.abspath(__file__))
        oracle_py = _chemin_natif(os.path.normpath(os.path.join(
            ici, "..", "..", "oracle", "oracle.py")))
        env = os.environ.copy()
        env.pop("AGENTS_FILE", None)
        env.pop("AGENTS_HISTORIQUE", None)
        env.pop("CLASSEUR_STOCKAGE", None)
    except (OSError, subprocess.SubprocessError):
        return (None, "oracle indisponible")
    entreees = []
    for statut in ("PRISE", "EN_ATTENTE"):
        try:
            r = subprocess.run(
                [sys.executable, oracle_py, "mission-lister",
                 "--statut", statut, "--agent", agent],
                capture_output=True, text=True, env=env, timeout=20)
        except (OSError, subprocess.SubprocessError):
            return (None, "oracle indisponible")
        if r.returncode != 0:
            continue
        lignes = [l.strip() for l in r.stdout.splitlines() if l.strip()]
        # Une entree de mission commence par '[<file>' (ex '[asap   ] id')
        # alors que l en-tete commence par '[ORACLE]'.
        entreees += [l for l in lignes
                     if l.startswith("[") and not l.startswith("[ORACLE]")]
    if entreees:
        return (True, "%d mission(s) PRISE/EN_ATTENTE" % len(entreees))
    return (False, "aucune mission PRISE/EN_ATTENTE pour cet agent")


def commande_activation(agent_habilite, session, raison=""):
    """Construit la commande d activation de l agent habilite."""
    raison = raison or "activation par le verrou"
    return (
        "python3 cerveau-projet/agents/tools/activer/activer-agent-principal/"
        "activer-agent-principal.py activer " + session + " " + agent_habilite +
        " '" + raison + "'"
    )


def trier_registre(registre):
    """Trie un registre JSONL par date puis heure, DECROISSANT (le plus
    recent en premier - regle utilisateur 2026-08-14). Les lignes non-JSON
    sont PRESERVEES et placees en fin de fichier. Idempotent : appelle apres
    chaque ajout, comme le fait enregistrer-usage-outil."""
    try:
        with io.open(registre, encoding="utf-8") as fh:
            lignes = [l.rstrip("\n") for l in fh if l.strip()]
    except (IOError, OSError):
        return
    valides = []
    invalides = []
    for l in lignes:
        try:
            e = json.loads(l)
            valides.append((e.get("date", ""), l))
        except ValueError:
            invalides.append(l)
    valides.sort(key=lambda paire: paire[0], reverse=True)
    triees = [l for _, l in valides] + invalides
    try:
        with io.open(registre, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(triees) + "\n")
    except (IOError, OSError):
        pass


def journaliser(agent, outil, verdict_str, agent_reel="", mode=""):
    """Auto-journalisation (espionnage) : l OUTIL signale lui-meme son usage.
    Usage autorise -> registre-usages-outils.jsonl (mode verrou-auto, ou
    verrou-dev pour un essai de validation developpeur - liste blanche
    v0.2.2). Tentative bloquee -> registre-tentatives-bloquees.jsonl (qui,
    quoi, quel agent reel etait actif). Non-bloquant : un echec d ecriture
    ne change pas le verdict du verrou. Le registre est TRIE apres chaque
    ajout (date/heure decroissant, regle utilisateur)."""
    traces = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "traces")
    if not os.path.isdir(traces):
        return
    try:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if verdict_str == "OK":
            registre = os.path.join(traces, "registre-usages-outils.jsonl")
            mode_reel = mode or "verrou-auto"
            entree = {
                "date": now,
                "agent": agent,
                "outil": outil,
                "mode": mode_reel,
                "commande": "",
                "contexte": ("auto-journalisation verrou d habilitation (validation "
                              "developpeur - liste blanche)" if mode_reel == "verrou-dev"
                              else "auto-journalisation verrou d habilitation (usage autorise)"),
            }
        else:
            registre = os.path.join(traces, "registre-tentatives-bloquees.jsonl")
            entree = {
                "date": now,
                "agent": agent,
                "outil": outil,
                "mode": "verrou-bloque",
                "commande": "",
                "contexte": "tentative " + verdict_str + " (agent reel actif : "
                           + (agent_reel or "?") + ")",
            }
        with io.open(registre, "a", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(entree, ensure_ascii=True, separators=(",", ":")) + "\n")
        trier_registre(registre)
    except (IOError, OSError):
        pass


# REGLE IMMUABLE CLE EXCLUSIVE (v0.2.1) : SEUL MORPHEUS ECRIT/ADAPTE LES
# TESTS (regles-groupes-agents.md). Meme si un outil figure dans la carte d un
# autre agent, la MODIFICATION d un fichier de test (zone tester/tests/) est
# BLOQUEE hors morpheus. Les autres agents passent par lui (cycle activer).
# Outils de modification couverts par la zone protegee :
# v0.6.0 (migration v1->v2) : editer-parcours retire (outil v1 archive -
# les arbres v2 s editer via editer-fichier).
OUTILS_MODIF = frozenset([
    "editer-fichier", "creer-fichier", "ecrire-fichier",
    "supprimer-fichier", "supprimer-dossier", "corriger-symboles",
    "corriger-fins-de-ligne", "corriger-accents-zones-sensibles",
])
ZONE_TESTS = "tester/tests/"
GARDIEN_TESTS = frozenset(["morpheus"])

# LISTE BLANCHE DEVELOPPEUR (v0.2.2, regle utilisateur 2026-08-16) : le
# CONSTRUCTEUR de l outil tester-lancer-non-regression doit pouvoir VALIDER
# ses modifications sans attendre janus. Autorisation DIRECTE dans le verrou,
# comme janus (qui est habilite via sa carte). Ne couvre QUE cet outil et QUE
# son developpeur : les autres agents restent bloques (carte = regle). La
# journalisation de ces essais porte le mode "verrou-dev" (traces distinctes,
# ignorees par evaluer-processus et autorisees par test-037).
OUTIL_NON_REGRESSION = "tester-lancer-non-regression"
DEV_NON_REGRESSION = frozenset(["vulcain"])


def est_zone_tests(cible):
    """Vrai si la cible pointe un fichier de test de la non-regression."""
    if not cible:
        return False
    normalise = cible.replace("\\", "/")
    return ZONE_TESTS in normalise


def verdict(agent, outil, table, verbose, cible=""):
    """Verifie l habilitation et renvoie (code, message).
    Comparaison INSENSIBLE A LA CASSE : l agent actif lu dans AGENTS.md porte
    la casse du nom (ex 'Cerberus') alors que les parcours sont minuscules
    (parcours-cerberus.json) - les deux doivent matcher.
    v0.2.1 : si cible est un fichier de test ET outil de modification, seul
    morpheus est habilite (cle exclusive, depasse la table des cartes)."""
    if est_zone_tests(cible) and outil in OUTILS_MODIF:
        if agent.lower() in [g.lower() for g in GARDIEN_TESTS]:
            return (0, "OK : l agent '" + agent + "' est habilite (cle exclusive tests) pour '"
                       + outil + "' sur " + cible + ".")
        session = trouver_session_agent(agent)
        return (1, "BLOQUE : la modification d un fichier de test est EXCLUSIVE a morpheus "
                   "(regle immuable - meme si l outil est dans ta carte).\n"
                   "  Cible : " + cible + "\n"
                   "  Action requise : activez morpheus puis redemandez.\n"
                   "  Commande : " + commande_activation("morpheus", session))
    # LISTE BLANCHE DEVELOPPEUR (v0.2.2) : le constructeur de l outil
    # tester-lancer-non-regression valide ses modifications sans attendre janus.
    if outil == OUTIL_NON_REGRESSION and agent.lower() in [d.lower() for d in DEV_NON_REGRESSION]:
        return (0, "OK : l agent '" + agent + "' est habilite (liste blanche developpeur) "
                   "pour '" + outil + "' - validation de ses modifications.")
    # (v0.6.0 : la cle exclusive pilote chiron/editer-parcours a ete retiree
    # avec l outil editer-parcours archive - l auto-correction passe par
    # editer-fichier sur son arbre.)
    habiles = table.get(outil)
    if habiles is None:
        return (1, "BLOQUE : l outil '" + outil + "' n est assigne a AUCUNE table "
                   "d habilitation (verifier qu il figure dans agents/habilitation/).")
    if agent.lower() in [h.lower() for h in habiles]:
        msg = "OK : l agent '" + agent + "' est habilite pour l outil '" + outil + "' (verrou ouvert)."
        if verbose:
            msg += "\n  Habilites : " + ", ".join(sorted(habiles))
        return (0, msg)
    session = trouver_session_agent(agent)
    habiles_tries = sorted(habiles)
    msg = (
        "BLOQUE : l agent '" + agent + "' n est PAS habilite pour l outil '" + outil + "' (verrou ferme).\n"
        "  Agent(s) habilite(s) : " + ", ".join(habiles_tries) + "\n"
        "  Action requise : activez l agent habilite puis redemandez l outil.\n"
        "  Commande : " + commande_activation(habiles_tries[0], session)
    )
    if verbose:
        msg += "\n  Source : table d habilitation dediee (agents/habilitation/habilitation-<agent>.json)."
    return (1, msg)


def main():
    detecter_racine()
    parser = argparse.ArgumentParser(
        prog="proteger-verrou-habilitation",
        description="Verrou d habilitation : bloque l utilisation d un outil par un agent non habilite.")
    parser.add_argument("--agent", metavar="NOM", help="nom de l agent appelant (obligatoire)")
    parser.add_argument("--outil", metavar="NOM", help="nom de l outil a utiliser (obligatoire)")
    parser.add_argument("--cible", metavar="CHEMIN", default="",
                        help="fichier cible (permet la cle exclusive tests : tester/tests/ = morpheus seul)")
    parser.add_argument("--audit", action="store_true",
                        help="mode audit/tests : table d habilitation sans verifier l identite reelle")
    parser.add_argument("--verrou-interne", action="store_true",
                        help="Verrou bleu (v0.5.0) : croise ET EXIGE une mission oracle\n"
                             "EN_ATTENTE/PRISE pour l agent declare (source de verite du\n"
                             "round, pas la seule reecriture d AGENTS.md)")
    parser.add_argument("--liste", action="store_true", help="affiche la table outil -> agents habilites")
    parser.add_argument("--verbose", action="store_true", help="detail du verdict")
    parser.add_argument("--version", action="store_true", help="affiche la version")
    parser.add_argument("--aide", action="help",
                  help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    if args.version:
        sys.stdout.write("proteger-verrou-habilitation v" + VERSION + "\n")
        sys.exit(0)

    table = construire_table()

    if args.liste:
        for outil in sorted(table):
            sys.stdout.write(outil + " -> " + ", ".join(sorted(table[outil])) + "\n")
        sys.exit(0)

    if not args.agent:
        sys.stderr.write("ERREUR : --agent est OBLIGATOIRE (le verrou doit savoir qui appelle).\n")
        sys.exit(2)
    if not args.outil:
        sys.stderr.write("ERREUR : --outil est OBLIGATOIRE (le verrou verifie un outil precis).\n")
        sys.exit(2)

    agents_connus = set()
    for nom_agent, _ in lister_habilitation():
        agents_connus.add(nom_agent)
    if args.agent.lower() not in [a.lower() for a in agents_connus]:
        sys.stderr.write("ERREUR : agent inconnu '" + args.agent + "'. Agents connus : "
                         + ", ".join(sorted(agents_connus)) + "\n")
        sys.exit(2)

    # IDENTITE REELLE (v0.2.0) : en mode production (sans --audit), l agent
    # declare doit etre l agent reel de la session. Un script lance par
    # Cerberus qui se fait passer pour janus est BLOQUE ici.
    agent_reel = None
    if not args.audit:
        agent_reel = agent_actif_session()
        if agent_reel is None:
            sys.stderr.write("ERREUR : identite de session indeterminable (table "
                             "'## Sessions connues' absente ou illisible). "
                             "Activez d abord un agent.\n")
            sys.exit(2)
        if agent_reel.lower() != args.agent.lower():
            msg = ("BLOQUE : usurpation d identite - la session est sur l agent '"
                   + agent_reel + "', pas '" + args.agent + "'. "
                   "Activez d abord l agent habilite (activer-agent-principal).")
            journaliser(args.agent, args.outil, "USURPATION_IDENTITE", agent_reel)
            sys.stdout.write(msg + "\n")
            sys.exit(1)

    # VERROU INTERNE (v0.5.0, Verrou bleu) : quand active, exige en PLUS
    # qu une mission oracle EN_ATTENTE/PRISE designe l agent declare
    # (source de verite du round). Cela bloque l usurpation d identite par
    # simple reecriture d AGENTS.md : meme si l agent y est pose a la main,
    # sans mission relayee par oracle le verrou reste FERME.
    if args.verrou_interne:
        ok_mission, detail = verif_missions_oracle(args.agent)
        # ok_mission None = oracle indisponible/erreur -> on bloque par
        # la route stricte (l incarnation ne peut pas etre prouvee).
        if ok_mission is not True:
            raison = detail if ok_mission is not None else detail
            msg = ("BLOQUE (verrou interne) : aucune preuve d une mission oracle\n"
                   "relayee EN_ATTENTE/PRISE pour l agent '" + args.agent
                   + "' (" + raison + "). La simple presence dans AGENTS.md ne\n"
                   "sert plus d autorite : re-routez la demande par oracle\n"
                   "(mission-relais) puis redemandez l outil.")
            journaliser(args.agent, args.outil, "VERROU_INTERNE", agent_reel)
            sys.stdout.write(msg + "\n")
            sys.exit(1)

    code, msg = verdict(args.agent, args.outil, table, args.verbose, args.cible)
    sys.stdout.write(msg + "\n")
    if not args.audit:
        mode_dev = (code == 0 and args.outil == OUTIL_NON_REGRESSION
                    and args.agent.lower() in [d.lower() for d in DEV_NON_REGRESSION])
        journaliser(args.agent, args.outil, "OK" if code == 0 else "BLOQUE", agent_reel,
                    "verrou-dev" if mode_dev else "")
    sys.exit(code)


if __name__ == "__main__":
    main()
