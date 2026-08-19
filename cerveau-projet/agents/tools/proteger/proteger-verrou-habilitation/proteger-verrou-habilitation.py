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
# SA carte de decision (indices outil du parcours), le verrou BLOQUE et
# indique QUI est habilite et COMMENT l activer (cycle Cerberus -> agent).
#
# SOURCE DE VERITE : les cartes de decision (cerveau-projet/agents/*/parcours/
# parcours-*.json). Un agent est habilite pour un outil SI ET SEULEMENT SI
# l outil figure dans les indices de type "outil" de sa carte. Aucune liste en
# dur dans ce script : la carte EST la regle (anti-derive, meme philosophie que
# test-035/037/045).
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
# Version : 0.4.0
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
import sys

VERSION = "0.4.0"

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


def lister_parcours():
    """Liste les parcours-*.json de tous les agents."""
    if not os.path.isdir(AGENTS_DIR):
        return []
    resultats = []
    for nom_agent in sorted(os.listdir(AGENTS_DIR)):
        dossier = os.path.join(AGENTS_DIR, nom_agent, "parcours")
        if not os.path.isdir(dossier):
            continue
        for fichier in sorted(os.listdir(dossier)):
            if fichier.startswith("parcours-") and fichier.endswith(".json"):
                resultats.append((nom_agent, os.path.join(dossier, fichier)))
    return resultats


# Outils P0 PARTAGES : outils de base communs a TOUS les agents (navigation
# de parcours, lecture de contexte) qui ne sont PAS des exclusivites. Ils sont
# references dans les fiches (P0) mais pas systematiquement dans les indices
# outil des cartes - le verrou ne les bloque jamais (lecon Vulcain
# 2026-08-15 : guider-parcours etait derive 'exclusif buffy' a tort, fausse
# exclusivite declenchant test-035).
OUTILS_P0_PARTAGES = frozenset([
    "guider-parcours",
    "lire-activite-recente",
    # LECONS (BDD partagee) : chaque agent ecrit SES lecons (enregistrer-
    # lecon, anti-usurpation interne) et lit celles des autres (consulter-
    # lecons) - ce sont des outils communs, pas des exclusivites.
    "enregistrer-lecon",
    "consulter-lecons",
])


def extraire_indices_outils(parcours):
    """Extrait les noms d outils des indices de type 'outil' de toutes les cases."""
    outils = set()
    cases = parcours.get("cases", {}) if isinstance(parcours, dict) else {}
    for cid, case in cases.items():
        if not isinstance(case, dict):
            continue
        indices = case.get("indices", [])
        if not isinstance(indices, list):
            continue
        for indice in indices:
            if not isinstance(indice, dict):
                continue
            if indice.get("type") == "outil":
                nom = indice.get("nom") or indice.get("catalogue")
                if nom:
                    outils.add(nom)
    return outils


def construire_table():
    """Construit la table outil -> set(agents habilites) depuis les cartes.
    Les outils P0 partages (OUTILS_P0_PARTAGES) sont ajoutes a TOUS les
    agents : ce sont des outils de base communs, pas des exclusivites."""
    table = {}
    tous = set()
    for nom_agent, chemin in lister_parcours():
        tous.add(nom_agent)
        for outil in extraire_indices_outils(charger_parcours(chemin)):
            table.setdefault(outil, set()).add(nom_agent)
    for outil in OUTILS_P0_PARTAGES:
        table[outil] = set(tous)
    return table


def trouver_session_agent(agent):
    """Trouve la session (session-llm-N) de l agent appelant dans AGENTS.md."""
    chemin = os.path.join(PROJECT_ROOT, "AGENTS.md")
    try:
        with io.open(chemin, "r", encoding="utf-8") as f:
            contenu = f.read()
    except IOError:
        return "session-llm-1"
    # Blocs : ### Session : session-llm-N ... | **Nom Agent** | X |
    blocs = re.split(r"### Session : (session-llm-\d+)", contenu)
    for i in range(1, len(blocs) - 1, 2):
        session = blocs[i]
        corps = blocs[i + 1]
        if re.search(r"\*\*Nom Agent\*\*\s*\|\s*" + re.escape(agent) + r"\s*\|", corps):
            return session
    return "session-llm-1"


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
        if not ligne.startswith("| session-llm-"):
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
OUTILS_MODIF = frozenset([
    "editer-fichier", "editer-parcours", "creer-fichier", "ecrire-fichier",
    "supprimer-fichier", "supprimer-dossier", "corriger-symboles",
    "corriger-fins-de-ligne", "corriger-accents-zones-sensibles",
])
ZONE_TESTS = "tester/tests/"
GARDIEN_TESTS = frozenset(["morpheus"])

# CLE EXCLUSIVE PILOTE (v0.2.3, regle utilisateur 2026-08-18) : CHIRON est le
# SEUL agent autorise a CORRIGER SA PROPRE carte (parcours-chiron.json) via
# editer-parcours, dans le cadre de son parcours d'auto-correction (exception
# pilote gravee dans regles-groupes-agents.md). La cle est PAR CIBLE :
# editer-parcours sur SA carte = autorise ; editer-parcours sur TOUTE AUTRE
# carte = BLOQUE (les autres cartes restent exclusives a buffy).
CARTE_CHIRON = "parcours-chiron.json"
PILOTE_AUTO_CORRECTION = frozenset(["chiron"])

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
    # CLE EXCLUSIVE PILOTE (v0.2.3) : chiron -> editer-parcours sur SA carte
    # uniquement (exception pilote auto-correction). Sur toute AUTRE carte,
    # chiron est BLOQUE (les cartes restent exclusives a buffy).
    if (outil == "editer-parcours" and agent.lower()
            in [p.lower() for p in PILOTE_AUTO_CORRECTION]):
        if cible and os.path.basename(cible.replace("\\", "/")) == CARTE_CHIRON:
            return (0, "OK : l agent '" + agent + "' est habilite (cle exclusive pilote "
                       "auto-correction) pour 'editer-parcours' sur SA carte " + cible + ".")
        session = trouver_session_agent(agent)
        return (1, "BLOQUE : l auto-correction de chiron est limitee a SA PROPRE carte "
                   "(parcours-chiron.json) - les autres cartes sont exclusives a buffy.\n"
                   "  Cible : " + (cible or "?") + "\n"
                   "  Action requise : activez buffy puis redemandez.\n"
                   "  Commande : " + commande_activation("buffy", session))
    habiles = table.get(outil)
    if habiles is None:
        return (1, "BLOQUE : l outil '" + outil + "' n est assigne a AUCUNE carte "
                   "(verifier qu il est declare dans les indices outil d un parcours).")
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
        msg += "\n  Source : cartes de decision (indices outil des parcours)."
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
    for nom_agent, _ in lister_parcours():
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
