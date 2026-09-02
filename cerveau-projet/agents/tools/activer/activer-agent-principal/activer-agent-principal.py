#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
activer-agent-principal.py

Outil pour modifier AGENTS.md de maniere fiable lors des activations
et reactivations d'agents, en supportant plusieurs sessions LLM en
parallele (chacune avec son bloc dedie et son agent principal).

Actions:
  sidentifier [session]          - Creer/choisir sa session (agent principal = Cerberus)
  activer <session> <agent> <raison> [mission]  - Activer un agent (cerberus = fin de mission)
  sessions                       - Lister les sessions et leur agent principal
  aide                           - Afficher cette aide

Vision 2026-08-27 : toujours 'activer', JAMAIS 'reactiver'. Activer Cerberus
en fin de mission ferme le chrono de l agent sortant et signe le bilan.

Variable d'environnement:
  AGENTS_FILE         - surcharger le chemin de AGENTS.md (tests sur copie)
  AGENTS_HISTORIQUE   - surcharger le chemin du fichier historique
  CLASSEUR_STOCKAGE   - surcharger le chemin du classeur-variables (tests sur copie)

Proprietaire : Vulcain
Version : 0.8.11
Statut : prepare
"""

import importlib.util
import io
import json
import os
import re
import subprocess
import sys
from datetime import datetime

VERSION = "0.8.11"
STATUT = "prepare"
REGEX_RESIDU = re.compile(r"^v?\d+\.\d+\.\d+$")

AGENTS_FILE = os.environ.get("AGENTS_FILE", "AGENTS.md")
AGENTS_HISTORIQUE = os.environ.get("AGENTS_HISTORIQUE", "AGENTS-historique.md")
CLASSEUR_STOCKAGE = os.environ.get("CLASSEUR_STOCKAGE", "cerveau-projet/agents/classeur-variables/stockage/variables-actuelles.md")
CERBERUS_FICHE = "cerveau-projet/agents/cerberus/cerberus.md"
MAX_ENTREES_HISTORIQUE = 150
AGENTS_ACTIVITE_RECENTE = os.environ.get("AGENTS_ACTIVITE_RECENTE", "AGENTS-activite-recente.md")
GRADES_V1 = os.environ.get("GRADES_V1", "cerveau-projet/agents/tools/oracle/grades-v1.json")
# v0.8.4 : la colonne Etat est DYNAMIQUE - la liste des etats + leurs
# regles de detection vivent dans etats-actions.json (editable sans toucher
# au code, decision utilisateur 2026-08-29). Repli : logique v0.8.3.
# Le defaut est ABSOLU (resolu depuis ce fichier) : les routines lancees
# avec cwd=routines/ ne resolvaient pas le chemin relatif -> repli v0.8.3
# (bug 2026-08-29 : vigie-perimetre historise ACTIF au lieu de AUTO).
_ETATS_ACTIONS_DEFAUT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "oracle", "etats-actions.json")
ETATS_ACTIONS = os.environ.get("ETATS_ACTIONS", "") or _ETATS_ACTIONS_DEFAUT

# v0.8.7 : colonne Executeur des routines v1 - l intervalle de chaque
# routine vit dans le manifest (oracle/routines/manifest.json), pas dans
# le code (decision utilisateur 2026-08-29 : afficher routine + temps
# defini, style RT(300s)).
_MANIFEST_ROUTINES_DEFAUT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "oracle", "routines", "manifest.json")
MANIFEST_ROUTINES = os.environ.get("MANIFEST_ROUTINES", "") or _MANIFEST_ROUTINES_DEFAUT

# v0.8.1 : l encart v1 porte desormais les colonnes Grade | Agent |
# Debut/Fin | Secteur | Raison | Heure | id | Type (inspire du tableau v2
# qui a Grade/Secteur, decision utilisateur 2026-08-27 : rattraper le
# retard v1 pour oracle/routines ; colonne Debut/Fin demandee car les
# agents historisent leur DEBUT et leur FIN). ASCII strict : grades [GX]
# et secteurs [XXX] (pas d emoji, contrairement au v2).
ENTETE_ENCART_V1 = "| Grade | Agent | Defcon | Executeur | Etat | Secteur | Raison | Heure | id | Type |"
SEPARATEUR_ENCART_V1 = "|-------|-------|--------|-----------|------|---------|--------|-------|----|------|"


def _lire_defcon_v1():
    """Niveau DEFCON courant (str) ou '' si aucun, depuis le journal
    defcon.jsonl d Oracle (colonne Defcon de l encart v1, decision
    utilisateur 2026-08-29 : afficher le DEFCON a cote de l agent)."""
    try:
        import importlib.util
        # activer-agent-principal.py -> remonte jusqu a .../cerveau-projet/
        # (5 x dirname depuis le fichier).
        p = os.path.abspath(__file__)
        for _ in range(5):
            p = os.path.dirname(p)
        defcon_path = os.path.join(p, "agents", "tools", "oracle",
                                   "fonctions", "defcon.py")
        if not os.path.isfile(defcon_path):
            return ""
        spec = importlib.util.spec_from_file_location("_defcon_v1", defcon_path)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        n = m.niveau_courant()
        return str(n) if n is not None else ""
    except Exception:
        return ""


def _charger_grades_v1():
    """Charger grades-v1.json (grades + secteurs des agents/routines v1)."""
    try:
        with io.open(GRADES_V1, "r", encoding="utf-8", errors="replace") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def _grade_label(agent):
    """Label du grade d un agent/routine depuis grades-v1.
    Repli : Inconnu"""
    data = _charger_grades_v1()
    ag = (agent or "").lower()
    grade = data.get("agents", {}).get(ag)
    if grade is None:
        grade = data.get("routines", {}).get(ag)
    if grade is None:
        return data.get("defaut", {}).get("label", "Inconnu")
    for e in data.get("echelle", []):
        if e.get("grade") == grade:
            return e.get("label", "Inconnu")
    return data.get("defaut", {}).get("label", "Inconnu")


def _secteur_label(agent):
    """Secteur ASCII d un agent/routine depuis grades-v1 (mapping mots-cles).
    Repli : [GEN]"""
    data = _charger_grades_v1()
    mapping = data.get("secteurs", {}).get("mapping", {})
    defaut = data.get("secteurs", {}).get("defaut", "[GEN]")
    ag = (agent or "").lower()
    if not ag:
        return defaut
    # Priorite 1 : nom d agent present dans le mapping
    if ag in mapping:
        return mapping[ag]
    # Priorite 2 : premier mot-cle contenu dans le nom d agent
    for mot, secteur in mapping.items():
        if mot in ag:
            return secteur
    return defaut


def _executeur_routine(agent):
    """Executeur d une routine v1 : "RT(<intervalle>s)" (ex: RT(300s))
    si l agent est une routine active du manifest (oracle/routines/
    manifest.json), sinon "". La colonne Executeur du tableau affiche
    ainsi le type routine + son intervalle defini (decision utilisateur
    2026-08-29)."""
    if not agent:
        return ""
    try:
        with io.open(MANIFEST_ROUTINES, "r", encoding="utf-8",
                     errors="replace") as fh:
            data = json.load(fh)
        for r in data.get("routines_surveillance", []):
            if r.get("nom") == agent and r.get("actif") and \
                    r.get("intervalles_secondes"):
                return "RT(%ds)" % r["intervalles_secondes"]
    except (OSError, ValueError):
        pass
    return ""


def _charger_etats_actions():
    """Charger etats-actions.json : liste des etats + regles de detection
    de la colonne Etat (dynamique, editable sans toucher au code).
    Repli : dictionnaire vide -> _etat_action retombe sur la logique v0.8.3."""
    try:
        with io.open(ETATS_ACTIONS, "r", encoding="utf-8", errors="replace") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def _etat_action(raison, agent=""):
    """Colonne Etat : l etat de l activite au moment de l action.
    Etats DYNAMIQUES (v0.8.4, decision utilisateur 2026-08-29) charges
    depuis etats-actions.json : DECOLLAGE, RECUPERE, RETOUR, LARGUE
    (etats de vol du pilote, v0.1.2 decision utilisateur 2026-09-02),
    DEBUT, FIN, URGENT, BUG, DEV, ATTENTE,
    AUTO, ACTION + defaut ACTIF. Les regles de detection (prefixes /
    mots_cles / agents) sont appliquees DANS L ORDRE du fichier (la
    premiere regle qui matche gagne). Repli : logique v0.8.3 si le
    fichier est absent/invalide."""
    data = _charger_etats_actions()
    etats = data.get("etats")
    if isinstance(etats, dict) and etats:
        r = (raison or "").strip().upper()
        ag = (agent or "").lower()
        for nom, spec in etats.items():
            det = spec.get("detection") if isinstance(spec, dict) else None
            if not isinstance(det, dict):
                continue
            for pre in det.get("prefixes") or []:
                if r.startswith(str(pre).upper()):
                    return nom
            for mot in det.get("mots_cles") or []:
                if str(mot).upper() in r:
                    return nom
            for a in det.get("agents") or []:
                if ag == str(a).lower():
                    return nom
        defaut = data.get("defaut")
        if isinstance(defaut, str) and defaut:
            return defaut
    # Repli v0.8.3 : fichier absent/invalide.
    r = (raison or "").strip().upper()
    if r.startswith("DEBUT") or r.startswith("RETOUR"):
        return "DEBUT"
    if r.startswith("FIN"):
        return "FIN"
    mots_urgent = ("ANOMALIE", "DEFCON", "P1 NON", "DEBORDEMENT",
                   "FANTOME", "VIOLATION", "SERVEUR MORT", "PIDFILE",
                   "INBOX:", "NON-ACQUITTE")
    for m in mots_urgent:
        if m in r:
            return "URGENT"
    mots_bug = ("CORRUPTION", "RE-ECHAPPEMENT", "BUG", "PLANTE",
                "ERREUR", "FAUX POSITIF", "KO ", " ECHEC")
    for m in mots_bug:
        if m in r:
            return "BUG"
    ag = (agent or "").lower()
    if ag in ("citations", "notation", "compter-entree", "compter-sortie"):
        return "ATTENTE"
    return "ACTIF"


def _trouver_entete_encart(lignes, zone_debut):
    """Trouver la ligne d entete du tableau v1 (ancien ou nouveau format)."""
    for i in range(zone_debut, len(lignes)):
        ligne = lignes[i]
        if ligne.startswith("| Grade | Agent |"):
            return i
        if ligne.startswith("| Heure | Agent |"):
            return i
    return -1


# v0.5.14 : couleur HTML fixe PAR AGENT dans l historique (rendu markdown).
# NB : nom SINGULIER - un nom pluriel terminc par 'AGENTS' casserait les
# regex permissives qui extraient le dictionnaire des agents (ex: test-092).
# Les couleurs ne sont appliquees QUE sur la ligne '###' (repere humain),
# JAMAIS sur la ligne de table (format machine exige par lire-activite-recente
# et evaluer-processus). Valeurs ASCII (#rrggbb), lisibles sur fond clair.
COULEURS_PAR_AGENT = {
    "cerberus": "#dc2626",  # gardien - rouge
    "vulcain": "#ea580c",   # forge - orange
    "morpheus": "#7c3aed",  # reves - violet
    "janus": "#0d9488",     # deux visages - teal
    "buffy": "#2563eb",     # developpeur principal - bleu
    "atlas": "#ca8a04",     # cartographe - ocre
    "themis": "#be185d",    # justice - rose
    "clio": "#65a30d",      # histoire - vert olive
    "hygie": "#16a34a",     # sante/nettoyage - vert
    "hermes": "#0284c7",    # langue - bleu ciel
    "gardien": "#475569",   # securite - ardoise
    "argus": "#9333ea",     # detection - violet vif
    "chiron": "#0891b2",    # education - cyan
    "ferrari": "#dc2626",   # freelance v1 - rouge (confidentiel)
    "athena": "#c026d3",    # pense-betes - fuchsia
    "promethee": "#d97706",  # specs - ambre
    "minerve": "#059669",   # todos - emeraude
    "socrate": "#a855f7",   # revision strategique - violet clair
    "redacteur-v2": "#7c3aed",
    "hades": "#4b5563",  # redaction docs v2 - violet profond
    "oracle": "#0d9488",  # coordination v1 - teal
    "nemesis": "#6d28d9",  # avis contradictoire - violet profond
    "stark": "#f59e0b",    # communication - ambre (Iron Man)
}
COULEUR_DEFAUT = "#334155"

# v0.5.15 : une entree d historique commence par une ligne de table
# ('| <span ...>agent</span> | HH:MM | AAAA-MM-JJ | session | ...') OU par
# son repere humain ('### <span ...>' colore). Les lignes '#>', '###>' et
# les continuations sont attachees a l entree precedente. NB : le repere se
# reconnait par son prefixe '### ' (aucun autre '### ' dans l historique).
# v0.5.24 : ajout de l agent redacteur-v2 (redaction des docs v2, round
# solo dedie) : couleur + triplet (role, fiche, corrections) dans AGENTS et
# COULEURS_PAR_AGENT (py + sh).
# v0.5.20 : le corps et l encart affichent l ID LLM (ex: freebuff) au lieu
# de la session (demande utilisateur : heure | agent | id | raison).
ENTREE_HISTORIQUE_RE = re.compile(r"^- \d{2}:\d{2} \|")


def couleur_agent(agent):
    """Couleur ANSI de l agent (pour affichage terminal)."""
    return COULEURS_PAR_AGENT.get((agent or "").lower(), COULEUR_DEFAUT)


def composer_bloc_historique(timestamp, identifiant, agent, raison, type_round="R"):
    """Compose une ligne d entree (format v0.6.1 timeline).

    Format sous un bloc ### Agent :
      - HH:MM | id | TYPE | raison   (TYPE = R round ou IR inter-round)
    (id = id LLM, ex: freebuff ; repli sur la session si inconnue)
    """
    heure = (timestamp or "").split(" ")[-1] if " " in (timestamp or "") else ""
    raison_nettoyee = " ".join((raison or "").split())
    # JAMAIS tronquer - l historique doit etre complet pour audit/retour
    return "- %s | %s | %s | %s\n" % (heure, identifiant or "", type_round, raison_nettoyee)
PREFIXE_SESSION = "session-llm-"

# agent : (role, fiche, corrections)
AGENTS = {
    "cerberus": ("Gardien de l'entree -- analyse et active les agents",
                 "cerveau-projet/agents/cerberus/cerberus.md",
                 "cerveau-projet/agents/cerberus/corrections.md"),
    "buffy": ("Developpeur principal -- contenu et structures",
              "cerveau-projet/agents/buffy/buffy.md",
              "cerveau-projet/agents/buffy/corrections.md"),
    "atlas": ("Explorateur -- recherche et decouverte",
              "cerveau-projet/agents/atlas/atlas.md",
              "cerveau-projet/agents/atlas/corrections.md"),
    "janus": ("Controleur des statuts -- validation et verification",
              "cerveau-projet/agents/janus/janus.md",
              "cerveau-projet/agents/janus/corrections.md"),
    "vulcain": ("Constructeur d'outils -- creation et developpement",
                "cerveau-projet/agents/vulcain/vulcain.md",
                "cerveau-projet/agents/vulcain/corrections.md"),
    "athena": ("Redactrice de pense-betes -- transformation des demandes",
               "cerveau-projet/agents/athena/athena.md",
               "cerveau-projet/agents/athena/corrections.md"),
    "morpheus": ("Testeur -- validation des outils et des tests",
                 "cerveau-projet/agents/morpheus/morpheus.md",
                 "cerveau-projet/agents/morpheus/corrections.md"),
    "promethee": ("Redacteur de specs -- specification technique",
                  "cerveau-projet/agents/promethee/promethee.md",
                  "cerveau-projet/agents/promethee/corrections.md"),
    "minerve": ("Redactrice de todos -- organisation des taches",
                "cerveau-projet/agents/minerve/minerve.md",
                "cerveau-projet/agents/minerve/corrections.md"),
    "clio": ("Muse de l'histoire -- mise a jour du README",
             "cerveau-projet/agents/clio/clio.md",
             "cerveau-projet/agents/clio/corrections.md"),
    "themis": ("Evaluatrice croisee -- evaluation et audit",
               "cerveau-projet/agents/themis/themis.md",
               "cerveau-projet/agents/themis/corrections.md"),
    "hygie": ("Agent de nettoyage -- seul agent habilite a acceder a tout le workspace et a supprimer sans demande prealable",
              "cerveau-projet/agents/hygie/hygie.md",
              "cerveau-projet/agents/hygie/corrections.md"),
    "hermes": ("Agent de la langue -- orthographe, vocabulaire et fautes de francais commises par les agents",
               "cerveau-projet/agents/hermes/hermes.md",
               "cerveau-projet/agents/hermes/corrections.md"),
    "gardien": ("Gardien du marbre -- propose la modification des zones protegees (l utilisateur valide), verifie l integrite du noyau",
                 "cerveau-projet/agents/gardien/gardien.md",
                 "cerveau-projet/agents/gardien/corrections.md"),
    "argus": ("Detecteur de contradictions -- trouve et compare les incoherences (cases, regles, protocoles, git)",
               "cerveau-projet/agents/argus/argus.md",
               "cerveau-projet/agents/argus/corrections.md"),
    "chiron": ("Educateur des agents -- formation continue",
                "cerveau-projet/agents/chiron/chiron.md",
                "cerveau-projet/agents/chiron/corrections.md"),
    "socrate": ("Conversateur de revision strategique -- discute et priorise les problemes",
                "cerveau-projet/agents/socrate/socrate.md",
                "cerveau-projet/agents/socrate/corrections.md"),
    "hades": ("Gardien des archives git -- SEUL habilite aux commandes git",
              "cerveau-projet/agents/hades/hades.md",
              "cerveau-projet/agents/hades/corrections.md"),
    "oracle": ("Coordinateur de l'equipe v1 (session-admin) -- traite les alertes de coordination (processus fantomes, serveurs morts, roulage messages) + controle processus",
               "cerveau-projet/agents/oracle/oracle.md",
               "cerveau-projet/agents/oracle/corrections.md"),
    "nemesis": ("Analyste en Chef -- avis contradictoire avant validation (audit 3 axes : cas limites, optimisation, securite/integrite), reponse 'Oui, mais...'",
                "cerveau-projet/agents/nemesis/nemesis.md",
                "cerveau-projet/agents/nemesis/corrections.md"),
    "redacteur-v2": ("Redacteur des docs de la v2 (proposition, regles, conventions) -- mode conversation (reactive Cerberus sur fin de cycle)",
                "cerveau-projet/agents/redacteur-v2/redacteur-v2.md",
                "cerveau-projet/agents/redacteur-v2/corrections.md"),
    "ferrari": ("Agent v1 specialise freelance -- corrige et modifie le dossier v2 (conventions v2)",
                "cerveau-projet/agents/ferrari/ferrari.md",
                "cerveau-projet/agents/ferrari/corrections.md"),
    "stark": ("Coordinateur de l'equipe freelance, responsable JARVIS (D16) -- mode conversation",
                "cerveau-projet/freelance/stark/stark.md",
                "cerveau-projet/freelance/stark/corrections.md"),
}

def get_agent_info(agent):
    """Retourner (role, fiche, corrections) d'un agent (casse insensible)."""
    return AGENTS.get(agent.lower(), None)


def verifier_ascii(chaine):
    """Retourner True si la chaine est 100% ASCII."""
    return all(ord(c) < 128 for c in chaine)


def verrouiller_constitution():
    """Verrou du marbre : refuser l ecriture si la zone constitution diverge.

    Active uniquement en mode reel (AGENTS_FILE non surcharge par les tests).
    Le verrou-marbre est la source unique du calcul d empreinte.
    """
    if os.environ.get("AGENTS_FILE"):
        return True  # mode test : copies temporaires, marbre non applicable
    outil = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                         "proteger", "proteger-verrou-marbre", "proteger-verrou-marbre.py")
    try:
        rc = subprocess.call([sys.executable, outil, "--zone", "constitution"])
    except OSError as e:
        print("[AVERTISSEMENT] verrou-marbre injoignable : %s" % e)
        return True
    if rc != 0:
        print("")
        print("[BLOQUE] MARBRE : la zone constitution a ete modifiee sans protocole.")
        print("  Refus d ecrire dans AGENTS.md : le marbre protege la Constitution.")
        print("  Protocole : cerveau-projet/agents/regles-immuables/general/protocole-securite-marbre.md")
        return False
    return True


def verifier_fichier_ascii(fichier):
    """Verifier qu'un fichier entier est ASCII. Afficher les lignes concernees."""
    nb = 0
    try:
        with io.open(fichier, "r", encoding="utf-8", errors="replace") as fh:
            for i, ligne in enumerate(fh, 1):
                for ch in ligne:
                    if ord(ch) > 127:
                        nb += 1
                        print("  Ligne %d: caractere non-ASCII U+%04X" % (i, ord(ch)))
                        break
    except IOError:
        pass
    return nb == 0


def verifier_residus_racine():
    """GARDE-FOU (v0.5.2) : detecter dans le repertoire courant les fichiers
    nommes comme des versions semver pures (ex: 0.2.1, v0.2.6). Ces fichiers
    sont des residus probables de redirections accidentelles de sortie (une
    commande precedente a redirige sa sortie, souvent celle de cet outil, vers
    un fichier nomme comme une version). Anti-residu : les supprimer - les
    sources de verite de version vivent dans cerveau-projet/agents/clio/."""
    try:
        residus = sorted(n for n in os.listdir(".")
                         if os.path.isfile(n) and REGEX_RESIDU.match(n))
    except OSError:
        return
    if not residus:
        return
    print("=" * 60)
    print("!!! WARNING GARDE-FOU (activer-agent-principal v%s) !!!" % VERSION)
    print("Des fichiers nommes comme des versions semver sont presents dans le")
    print("repertoire courant (residus probables de redirections accidentelles")
    print("de sortie) :")
    for n in residus[:10]:
        print("    - %s" % n)
    print("ANTI-RESIDU : supprimez-les. Les sources de verite de version vivent")
    print("dans cerveau-projet/agents/clio/ (version-readme.txt,")
    print("statut-projet.txt), JAMAIS a la racine.")
    print("=" * 60)


def _trouver_racine():
    """DETECTER la racine du workspace en remontant jusqu a AGENTS.md.
    Pattern os_path v2 (v0.1.0, decision 2026-08-30) : on ne compte JAMAIS
    les niveaux (../..), on CHERCHE le marqueur. Retourne chemin absolu ou
    None."""
    courant = os.path.abspath(os.path.dirname(__file__))
    while True:
        if os.path.isfile(os.path.join(courant, "AGENTS.md")):
            return courant
        parent = os.path.dirname(courant)
        if parent == courant:
            return None
        courant = parent


def instruction_demarrage(agent):
    """Bloc DEMARRAGE OBLIGATOIRE pour un agent active (sauf Cerberus).
    v0.5.9 : la norme est l arbre v2 (guider-arbre). L agent lance SON arbre
    des decisions (racine -> themes -> fins) des que l arbre existe ; sinon
    repli sur le parcours v1 (couvre les parcours nommes, ex: socrate).
    v0.5.4 : corrige le bug d arret a c0 - l agent sait comment lancer son
    parcours depuis la case de depart."""
    # PATTERN v2 (os_path) : on ne compte JAMAIS les niveaux ("../..").
    # On DETECTE la racine en remontant jusqu a trouver AGENTS.md, puis on
    # derive le chemin du haut vers le bas - a la v1 on comptait les ".."
    # a la main (bug de niveau), la v2 a fiabilise ca (decision 2026-08-30).
    racine = _trouver_racine()
    arbre = os.path.join(
        racine, "cerveau-projet", "agents", agent, "parcours",
        "arbre-%s.json" % agent) if racine else os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        agent, "parcours", "arbre-%s.json" % agent)
    if os.path.isfile(arbre):
        return (
            "DEMARRAGE OBLIGATOIRE (v2) : lance ton arbre des decisions avec :\n"
            "python3 cerveau-projet/agents/tools/guider/guider-arbre/guider-arbre.py \\\n"
            "  cerveau-projet/agents/%s/parcours/arbre-%s.json\n"
            "(racine : choisis TON theme selon ta mission, puis suis les besoins /\n"
            "procedures du theme ; Oracle te pilote via l arbre - PAS le parcours v1 ;\n"
            "si tu reprends apres une interruption, relance l arbre et poursuis)."
        ) % (agent, agent)
    return (
        "DEMARRAGE OBLIGATOIRE : lance ta mission avec :\n"
        "python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \\\n"
        "  cerveau-projet/agents/%s/parcours/parcours-%s.json --case c0\n"
        "(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds\n"
        "a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis\n"
        "ensuite les branches case par case ; si tu reprends apres une interruption,\n"
        "reprends a la case courante avec --case <cid> --reponses '<reponse>')."
    ) % (agent, agent)


def instruction_demarrage_v2(agent):
    """Bloc DEMARRAGE V2 pour un agent FREELANCE active.
    v0.5.30 : les agents freelance n'utilisent PAS les outils v1
    (guider-parcours, activer-agent-principal) - JARVIS les remplace.
    Demarrage : fiche + corrections puis ARBRE des decisions."""
    return (
        "DEMARRAGE V2 (agents freelance) : relis ta fiche puis tes corrections.\n"
        "Pour toute action, suis TON arbre des decisions :\n"
        "  cerveau-projet/freelance/%s/parcours/arbre-%s.json\n"
        "(themes : selon ton arbre ; JARVIS = point d'entree OBLIGATOIRE pour\n"
        "toute mission)\n"
        "REGLE V2 : les agents freelance n'utilisent PAS les outils v1\n"
        "(guider-parcours, activer-agent-principal) -- JARVIS les remplace :\n"
        "tout passe par jarvis.py (envoyer/lire/acquitter/lister/activer)."
    ) % (agent, agent)


def lire_agents():
    """Lire AGENTS.md (erreur si absent)."""
    if not os.path.isfile(AGENTS_FILE):
        print("ERREUR: Le fichier %s n'existe pas" % AGENTS_FILE)
        return None
    with io.open(AGENTS_FILE, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def ecrire_agents(contenu):
    """Ecrire AGENTS.md (LF)."""
    with io.open(AGENTS_FILE, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(contenu)


def migrer_si_necessaire(contenu):
    """Convertir l'ancienne structure mono-session en multi-session.
    Retourne (contenu, migre) ou migre indique si la conversion a eu lieu."""
    if "## Sessions LLM" in contenu:
        return contenu, False
    if "## Agent Principal Actuel" not in contenu:
        return contenu, False
    m = re.search(r"## Agent Principal Actuel\n(.*?)(?=\n## |\Z)", contenu, re.DOTALL)
    if not m:
        return contenu, False
    ancien = m.group(0)
    bloc = m.group(1)
    nouveau = "## Sessions LLM\n\n### Session : session-llm-1\n" + bloc + "\n"
    return contenu.replace(ancien, nouveau, 1), True


def extraire_blocs_session(contenu):
    """Retourner la liste des (session_id, texte_du_bloc) presents."""
    blocs = []
    lignes = contenu.split("\n")
    i = 0
    while i < len(lignes):
        m = re.match(r"^### Session : (.+?)\s*$", lignes[i])
        if m:
            session_id = m.group(1)
            j = i + 1
            bloc = []
            while j < len(lignes):
                if re.match(r"^### Session : ", lignes[j]) or lignes[j].startswith("## "):
                    break
                bloc.append(lignes[j])
                j += 1
            blocs.append((session_id, "\n".join(bloc)))
            i = j
        else:
            i += 1
    return blocs


def trouver_prochaine_session(contenu):
    """Trouver le prochain session-llm-N libre."""
    existantes = set(s for s, _ in extraire_blocs_session(contenu))
    n = 1
    while (PREFIXE_SESSION + str(n)) in existantes:
        n += 1
    return PREFIXE_SESSION + str(n)


def _routine_classeur():
    """Charger la routine centrale du classeur sans dependance externe."""
    chemin = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", "..", "oracle", "fonctions", "classeur.py"))
    try:
        spec = importlib.util.spec_from_file_location("classeur_v1", chemin)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except (OSError, ImportError, AttributeError):
        return None


def lire_classeur(variable="*", source="activer-agent-principal", agent="oracle", session="session-admin", tracer=True):
    """Lire le classeur via la routine centrale et tracer CLASSEUR ENTREE."""
    module = _routine_classeur()
    if module is None:
        return None, None
    return module.lire_fichier(CLASSEUR_STOCKAGE, variable, source, agent, session, tracer=tracer)


def ecrire_classeur(lignes, variable="*", source="activer-agent-principal", agent="oracle", session="session-admin", ancienne_valeur=None, nouvelle_valeur=None, raison=None):
    """Ecrire le classeur via la routine centrale et tracer CLASSEUR SORTIE."""
    module = _routine_classeur()
    if module is None:
        return False
    return module.ecrire_lignes(CLASSEUR_STOCKAGE, lignes, variable, source, agent, session, ancienne_valeur, nouvelle_valeur, raison)


def trouver_session_par_id(llm_id):
    """Retrouver la session liee a un llm-id (ou None).
    SOURCE DOUBLE (v0.4.0) : 1) AGENTS.md -- bloc avec le champ '**Nom LLM** | <id>'
    (ancien nom **Id LLM** accepte) ; 2) classeur -- ligne profil-session avec
    'id: <llm-id>'. Permet au LLM de se reconnaitre directement en lisant AGENTS.md."""
    # 1. AGENTS.md : champ Nom LLM dans les blocs de session
    if os.path.isfile(AGENTS_FILE):
        with io.open(AGENTS_FILE, "r", encoding="utf-8", errors="replace") as fh:
            contenu = fh.read()
        for session, bloc in extraire_blocs_session(contenu):
            m = re.search(r"\*\*(?:Id LLM|Nom LLM)\*\* \| ([^|]+)", bloc)
            if m and m.group(1).strip() == llm_id:
                return session
    # 2. Classeur : liaison id dans les lignes profil-session
    fichier = CLASSEUR_STOCKAGE
    if os.path.isfile(fichier):
        lignes_classeur, _ = lire_classeur("*", "activer-agent-principal", "oracle", "session-admin", tracer=False)
        for ligne in lignes_classeur or []:
            if "id: " + llm_id in ligne:
                m = re.search(r"session: (session-[A-Za-z0-9_-]+)", ligne)
                if m:
                    return m.group(1)
    return None


def id_lie_a_session(session_id):
    """Retourner l'id LLM lie a une session (AGENTS.md champ Nom LLM, puis classeur),
    ou None si la session n'est liee a aucun id. Utile pour detecter un CONFLIT
    d'alignement (v0.4.0) : session-llm-N deja liee a un autre id."""
    # 1. AGENTS.md
    if os.path.isfile(AGENTS_FILE):
        with io.open(AGENTS_FILE, "r", encoding="utf-8", errors="replace") as fh:
            contenu = fh.read()
        for session, bloc in extraire_blocs_session(contenu):
            if session == session_id:
                m = re.search(r"\*\*(?:Id LLM|Nom LLM)\*\* \| ([^|]+)", bloc)
                if m and m.group(1).strip():
                    return m.group(1).strip()
    # 2. Classeur
    fichier = CLASSEUR_STOCKAGE
    if os.path.isfile(fichier):
        lignes_classeur, _ = lire_classeur("*", "activer-agent-principal", "oracle", "session-admin", tracer=False)
        for ligne in lignes_classeur or []:
            if "session: " + session_id in ligne:
                m = re.search(r"id: (\S+)", ligne)
                if m:
                    return m.group(1)
    return None


def session_cible_pour_id(llm_id):
    """REGLE ALIGNEMENT (v0.4.0) : id llm-N -> session-llm-N (le numero de session
    porte le numero de l'id). Retourne la session cible, ou None si l'id n'est pas
    de la forme llm-N (ex: llm-atlas -> pas d'alignement, prochaine libre)."""
    m = re.match(r"^llm-(\d+)$", llm_id)
    if m:
        return PREFIXE_SESSION + m.group(1)
    return None


def poser_nom_llm_bloc(contenu, session_id, llm_id):
    """Ajouter ou mettre a jour le champ '**Nom LLM** | <id>' EN TETE du bloc de
    session (convention v0.5.0 : nom-llm avant nom-agent). L'ancien champ
    **Id LLM** est migre automatiquement vers **Nom LLM**. Retourne le contenu."""
    return editer_champs_session(contenu, session_id, {"Nom LLM": llm_id})


def creer_session(contenu, session_id, llm_id=None):
    """Ajouter un bloc de session (Cerberus par defaut) apres ## Sessions LLM.
    Si llm_id fourni (v0.4.0), le champ **Nom LLM** est ecrit en tete du bloc."""
    if any(s == session_id for s, _ in extraire_blocs_session(contenu)):
        return contenu
    info = get_agent_info("cerberus")
    role, fiche, corrections = info
    date = datetime.now().strftime("%Y-%m-%d")
    champ_id = ""
    if llm_id:
        champ_id = "| **Nom LLM** | %s |\n" % llm_id
    bloc = (
        "\n### Session : %s\n\n"
        "| Champ | Valeur |\n"
        "|---|---|\n"
    ) % session_id
    bloc += champ_id
    bloc += (
        "| **Nom Agent** | Cerberus |\n"
        "| **Role Agent** | %s |\n"
        "| **Derniere mise a jour** | %s |\n"
        "| **Fiche** | [%s](%s) |\n"
        "| **Corrections** | [%s](%s) |\n"
        "| **Active par** | Identification |\n"
        "| **Raison** | Identification LLM - demarrage de session |\n"
    ) % (role, date, fiche, fiche, corrections, corrections)
    lignes = contenu.split("\n")
    sortie = []
    insere = False
    for ligne in lignes:
        sortie.append(ligne)
        if re.match(r"^## Sessions LLM\s*$", ligne) and not insere:
            sortie.append(bloc)
            insere = True
    if not insere:
        print("ERREUR: Section ## Sessions LLM introuvable dans %s" % AGENTS_FILE)
        return None
    return "\n".join(sortie)


def editer_champs_session(contenu, session_id, champs):
    """Remplacer les champs (dict nom -> valeur) du bloc de session_id uniquement.
    Convention v0.5.0 : reconstruction complete du bloc dans l'ordre canonique --
    les anciens noms de champs (Nom, Role, Id LLM) sont migres automatiquement vers
    les nouveaux (Nom Agent, Role Agent, Nom LLM), les champs manquants sont inseres
    a leur position, Nom LLM est place EN TETE."""
    ORDRE = ["Nom LLM", "Nom Agent", "Role Agent", "Derniere mise a jour",
             "Fiche", "Corrections", "Active par", "Raison"]

    def reconstruire_bloc(bloc, champs):
        """Analyser les lignes d'un bloc, appliquer les champs, reemettre dans l'ordre.
        v0.5.4 : la Raison peut etre MULTILIGNE (les lignes suivantes sans '| **')
        sont des continuations de la Raison - elles sont conservees et recollees."""
        valeurs = {}
        continuations = {}
        i = 0
        while i < len(bloc):
            ligne = bloc[i]
            m = re.match(r"^\| \*\*([^*]+)\*\* \| (.*) \|$", ligne)
            if not m:
                i += 1
                continue
            champ = m.group(1).strip()
            valeur = m.group(2).strip()
            # capturer les lignes de continuation de ce champ (Raison multiligne)
            suivantes = []
            j = i + 1
            while j < len(bloc) and not re.match(r"^\| \*\*([^*]+)\*\* \|", bloc[j]):
                suivantes.append(bloc[j])
                j += 1
            if suivantes:
                continuations[champ] = suivantes
            # Migration anciens noms
            if champ == "Nom":
                champ = "Nom Agent"
            elif champ == "Role":
                champ = "Role Agent"
            elif champ == "Id LLM":
                champ = "Nom LLM"
            # Fiche/Corrections : extraire le chemin depuis [x](x)
            if champ in ("Fiche", "Corrections"):
                mm = re.match(r"^\[(.*)\]\((.*)\)$", valeur)
                if mm:
                    valeur = mm.group(2)
            valeurs[champ] = valeur
            i = j
        valeurs.update(champs)
        # Recollement des continuations (Raison multiligne) sur le champ mis a jour.
        # v0.5.5 : si le champ a ETE REMPLACE (present dans champs), l'ancienne
        # suite est IGNOREE (y compris la Raison) - le bug v0.5.4 faisait une
        # exception pour la Raison et recolait les anciennes continuations
        # (blocs DEMARRAGE) a chaque nouvelle raison -> accumulation infinie.
        for champ_c, suite in continuations.items():
            if champ_c in champs:
                # champ remplace par un nouveau : ignorer l'ancienne suite
                continue
            if champ_c in valeurs:
                valeurs[champ_c] = valeurs[champ_c] + "\n" + "\n".join(suite)
        nouvelles = ["", "| Champ | Valeur |", "|---|---|"]
        for champ in ORDRE:
            if champ in valeurs:
                v = valeurs[champ]
                if champ in ("Fiche", "Corrections"):
                    nouvelles.append("| **%s** | [%s](%s) |" % (champ, v, v))
                elif champ == "Raison" and "\n" in v:
                    # Raison multiligne : premiere ligne dans la cellule, les
                    # suivantes en lignes brutes (format historique de AGENTS.md)
                    lignes_raison = v.split("\n")
                    nouvelles.append("| **%s** | %s |" % (champ, lignes_raison[0]))
                    for suite in lignes_raison[1:]:
                        nouvelles.append(suite)
                else:
                    nouvelles.append("| **%s** | %s |" % (champ, v))
        # Champs inconnus conserves (s'ils existaient dans le bloc)
        for champ, v in valeurs.items():
            if champ not in ORDRE:
                nouvelles.append("| **%s** | %s |" % (champ, v))
        return nouvelles

    lignes = contenu.split("\n")
    sortie = []
    i = 0
    while i < len(lignes):
        ligne = lignes[i]
        if re.match(r"^### Session : " + re.escape(session_id) + r"\s*$", ligne):
            sortie.append(ligne)
            i += 1
            bloc = []
            while i < len(lignes) and not (re.match(r"^### Session : ", lignes[i]) or lignes[i].startswith("## ")):
                bloc.append(lignes[i])
                i += 1
            sortie.extend(reconstruire_bloc(bloc, champs))
            continue
        sortie.append(ligne)
        i += 1
    return "\n".join(sortie)


def detecter_type_round(raison, type_round="R"):
    """DETECTION AUTOMATIQUE du type d inter-round (decision utilisateur
    2026-08-24, etendue modele aero 2026-08-30) : si la raison (normalisee)
    commence par 'INTER-ROUND', 'FIN D INTER-ROUND', 'SIGNALER' ou contient
    ' MISSION-AJOUTER ' (le signalement a ORACLE du modele aero R2), le type
    est IR sans flag manuel. Sinon, garder le type passe (defaut R)."""
    if type_round == "IR":
        return type_round
    raison_haut = (raison or "").strip().upper()
    raison_norm = raison_haut.replace("'", " ").replace("\"", " ")
    if (raison_haut.startswith("INTER-ROUND")
            or raison_norm.startswith("FIN D INTER-ROUND")
            or raison_haut.startswith("SIGNALER")
            or raison_haut.startswith("BESOIN INTER-ROUND")
            or " MISSION-AJOUTER " in " " + raison_norm + " "
            or " INTER-ROUND " in " " + raison_norm + " "):
        return "IR"
    return type_round


def ajouter_historique(timestamp, session, agent, raison, type_round="R", agent_effectif=None, executeur=None):
    """Ajouter une entree dans le fichier historique, max 150.

    agent_effectif : agent affiche dans la colonne Agent (defaut: agent).
    Utilise quand Oracle historise au lieu de l agent (Oracle = le true
    pilote, il apparait dans le tableau).
    executeur : qui execute l action (ex: Oracle). Colonne Executeur.

    Format v0.6.2 timeline :
      ## YYYY-MM-DD
      ### Agent
      - HH:MM | id | TYPE | raison   (TYPE = R round ou IR inter-round)

    La colonne porte l ID LLM (resolu depuis la session via id_lie_a_session,
    repli sur la session si aucun id lie). Le type IR est DETECTE
    AUTOMATIQUEMENT (raison commencant par INTER-ROUND / FIN D INTER-ROUND,
    decision utilisateur 2026-08-24). Aussi met a jour les encarts
    'Activites recentes' PAR SESSION en haut du fichier (header : id).
    """
    if not os.path.isfile(AGENTS_HISTORIQUE):
        print("ERREUR: Le fichier %s n'existe pas" % AGENTS_HISTORIQUE)
        return 1

    type_round = detecter_type_round(raison, type_round)
    identifiant = id_lie_a_session(session) or session
    nouvelle_ligne = composer_bloc_historique(timestamp, identifiant, agent, raison, type_round)

    if not verifier_ascii(nouvelle_ligne):
        print("ERREUR: Caractere non-ASCII detecte dans la raison - ecriture historique REFUSEE")
        return 1

    with io.open(AGENTS_HISTORIQUE, "r", encoding="utf-8", errors="replace") as fh:
        contenu = fh.read()

    # Extraire la date et convertir en JJ/MM/AAAA
    date_raw = (timestamp or "").split(" ")[0] if " " in (timestamp or "") else ""
    if len(date_raw) == 10 and date_raw[4] == "-":
        parts = date_raw.split("-")
        date = "%s/%s/%s" % (parts[2], parts[1], parts[0])
    else:
        date = date_raw
    heure = (timestamp or "").split(" ")[-1] if " " in (timestamp or "") else ""
    agent_titre = (agent_effectif or agent or "Inconnu")

    # 1. Inserer dans le bloc jour/agent (format timeline)
    marqueur_jour = "## %s" % date
    marqueur_agent = "### %s" % agent_titre
   
    if marqueur_jour in contenu:
        # v0.5.21 : borner la recherche du bloc agent A LA SECTION DU JOUR.
        # Avant, contenu.index(marqueur_agent) trouvait le PREMIER '### <agent>'
        # du fichier (souvent dans un jour anterieur) et y inserait l entree
        # (les entrees Cerberus du jour courant tombaient dans le bloc du jour
        # precedent).
        idx_jour = contenu.index(marqueur_jour)
        fin_jour = contenu.find("\n## ", idx_jour + len(marqueur_jour))
        if fin_jour == -1:
            fin_jour = len(contenu)
        section_jour = contenu[idx_jour:fin_jour]
        if marqueur_agent in section_jour:
            idx_agent = idx_jour + section_jour.index(marqueur_agent)
            pos_inser = idx_agent + len(marqueur_agent)
            if pos_inser < len(contenu) and contenu[pos_inser] == "\n":
                pos_inser += 1
            contenu = contenu[:pos_inser] + nouvelle_ligne + contenu[pos_inser:]
        else:
            contenu = contenu[:idx_jour + len(marqueur_jour)] + "\n\n" + marqueur_agent + "\n" + nouvelle_ligne + contenu[idx_jour + len(marqueur_jour):]
    else:
        # v0.5.21 : inserer APRES l encart 'Activites recentes' (jamais entre
        # l en-tete et l encart). Cible : la premiere section jour existante
        # (## JJ/MM/AAAA) ; repli : apres l encart, puis fin de l en-tete.
        m_section = re.search(r"^## \d{2}/\d{2}/\d{4}", contenu, re.MULTILINE)
        if m_section:
            idx_inser = m_section.start()
        else:
            idx_encart = contenu.find("## Activites recentes")
            if idx_encart != -1:
                idx_apres = contenu.find("\n---\n", idx_encart)
                idx_inser = idx_apres + len("\n---\n") if idx_apres != -1 else len(contenu)
            else:
                idx_entete = contenu.find("\n---\n")
                idx_inser = idx_entete + len("\n---\n") if idx_entete != -1 else 0
        nouveau_bloc = "\n" + marqueur_jour + "\n\n" + marqueur_agent + "\n" + nouvelle_ligne
        contenu = contenu[:idx_inser] + nouveau_bloc + contenu[idx_inser:]

    # 2. L encart 'Activites recentes' vit UNIQUEMENT dans
    #    AGENTS-activite-recente.md (decision 2026-08-26 : AGENTS-historique.md
    #    ne contient que le corps chronologique 100 entrees).
    #    (anciennement : maj_encart_activites ecrivait l encart dans
    #    AGENTS-historique.md - SUPPRIME, doublon avec _ecrire_encart_v1)

    with io.open(AGENTS_HISTORIQUE, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(contenu)

    if not verifier_fichier_ascii(AGENTS_HISTORIQUE):
        print("WARNING: Caracteres non-ASCII presents dans %s" % AGENTS_HISTORIQUE)

    # --- v0.8.0 : encart dans AGENTS-activite-recente.md + BDD SQLite ---
    # L encart est desormais dans un fichier separe (50 entrees max, plus
    # fragile que le corps). La chronologie est dans historique.db (7 jours).
    _ecrire_encart_v1(session, heure, agent_titre, identifiant, type_round, raison, executeur=executeur)
    _ecrire_bdd_v1(identifiant, agent_titre, type_round, raison, timestamp)

    print("Historique mis a jour dans %s" % AGENTS_HISTORIQUE)
    return 0


def _construire_encart_v1(corps):
    """Construire l encart 'Activites recentes -- session-admin' UNIQUEMENT
    (frontmatter + tableau au format Grade/Secteur/Debut-Fin), depuis le
    corps chronologique de l historique. Retourne le contenu COMPLET du
    fichier AGENTS-activite-recente.md (migration v0.8.1 : les anciennes
    lignes portent elles aussi les nouvelles colonnes)."""
    mapping = mapper_id_vers_session()
    entrees = []
    agent_courant = "?"
    date_courante = ""
    for ligne in corps.splitlines():
        l = ligne.strip()
        if l.startswith("## ") and not l.startswith("## Activites"):
            date_courante = l[3:].strip()
            agent_courant = "?"
            continue
        if l.startswith("### "):
            agent_courant = l[4:].strip()
            continue
        if l.startswith("- ") and " | " in l:
            parties = l[2:].split(" | ", 3)
            if len(parties) >= 3:
                h = parties[0].strip()
                s = parties[1].strip()
                if len(parties) == 4:
                    t = parties[2].strip()
                    r = parties[3].strip()
                else:
                    t = ""
                    r = parties[2].strip()
                session_entree = mapping.get(s)
                # Historique v1 : l identifiant glm5 est lie a session-admin.
                # Les entrees Oracle serveur sont donc conservees.
                if session_entree != "session-admin" and s != "session-admin":
                    continue
                agent_affiche = "oracle" if "DEMARRAGE SERVEUR" in r else agent_courant
                entrees.append(("%s %s" % (date_courante, h), h, agent_affiche, s, r, t))
    def _cle_tri(entree):
        date, heure = entree[0].split(" ", 1)
        try:
            jj, mm, aaaa = date.split("/")
            return (int(aaaa), int(mm), int(jj), heure)
        except (ValueError, TypeError):
            return (0, 0, 0, heure)

    liste = sorted(entrees, key=_cle_tri, reverse=True)[:50]
    encart = (
        "---\nidentite:\n  nom: \"Activites recentes\"\n"
        "  type: \"tableau\"\n"
        "  description: \"Vue rapide des 50 dernieres actions de la "
        "session-admin (ASCII+LF). Session-freelance : "
        "AGENTS-activite-recente-v2.md (UTF8+CRLF).\"\n"
        "  appartient_a: commun\n  commun: true\n---\n\n"
        "## Activites recentes -- session-admin\n\n"
        + ENTETE_ENCART_V1 + "\n"
        + SEPARATEUR_ENCART_V1 + "\n")
    for _, h, a, s, r, t in liste:
        r_aff = r if len(r) <= 80 else r[:77] + "..."
        r_aff = r_aff.replace("|", "-")
        # FIX 2026-08-29 : les raisons multi-lignes (ex: bloc DEMARRAGE
        # OBLIGATOIRE des tests) cassaient le tableau de l encart. On
        # remplace tout retour a la ligne par un espace.
        r_aff = " ".join(r_aff.split())
        grade = _grade_label(a)
        secteur = _secteur_label(a)
        df = _etat_action(r, a)
        defcon = _lire_defcon_v1()
        encart += "| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |\n" % (
            grade, a, defcon, _executeur_routine(a) or "Oracle", df, secteur, r_aff, h, s, t)
    return encart


def _ecrire_encart_v1(session, heure, agent, identifiant, type_round, raison, executeur=None):
    """Ecrire l encart dans AGENTS-activite-recente.md (50 entrees max,
    raison tronquee a 80 car.). Meme logique que maj_encart_activites mais
    dans un fichier SEPAR (vue rapide, pas le corps chronologique).
    executeur : qui.execute l action (ex: Oracle). Colonne Executeur."""
    mapping = mapper_id_vers_session()
    session_nom = mapping.get(session, session)
    if not session_nom:
        return
    # Raison tronquee pour l encart
    r_aff = raison if len(raison) <= 80 else raison[:77] + "..."
    r_aff = r_aff.replace("|", "-")
    # FIX 2026-08-29 : les raisons multi-lignes cassaient le tableau
    # (les lignes debordaient sur 2 lignes physiques). On aplatit.
    r_aff = " ".join(r_aff.split())
    grade = _grade_label(agent)
    secteur = _secteur_label(agent)
    df = _etat_action(raison, agent)
    exec_aff = executeur or _executeur_routine(agent) or "Oracle"
    defcon = _lire_defcon_v1()
    nouvelle_entree = "| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
        grade, agent, defcon, exec_aff, df, secteur, r_aff, heure,
        identifiant, type_round)
    try:
        if os.path.isfile(AGENTS_ACTIVITE_RECENTE):
            contenu = io.open(AGENTS_ACTIVITE_RECENTE, "r",
                              encoding="utf-8", errors="replace").read()
        else:
            # Creer le fichier v1 (session-admin uniquement - la session
            # freelance a SON fichier AGENTS-activite-recente-v2.md,
            # decision utilisateur 2026-08-26 : chaque session a SES
            # fichiers, plus aucun partage v1/v2)
            contenu = (
                "---\nidentite:\n  type: activite-recente\n"
                "  appartient_a: commun\n  commun: true\n---\n\n"
                "## Activites recentes -- session-admin\n\n"
                + ENTETE_ENCART_V1 + "\n"
                + SEPARATEUR_ENCART_V1 + "\n")
    except OSError:
        return
    lignes = contenu.split("\n")
    # Trouver l encart de la session
    entete_encart = "## Activites recentes -- %s" % session_nom
    zone_debut = 0
    for i, ligne in enumerate(lignes):
        if ligne.strip() == entete_encart:
            zone_debut = i
            break
    # Trouver le tableau (ancien ou nouveau format d entete)
    idx_tableau = _trouver_entete_encart(lignes, zone_debut)
    if idx_tableau == -1:
        return
    # v0.8.1 : migration de l ancien format (| Heure | Agent | id | Type |
    # Raison |) vers le nouveau (Grade/Secteur/Debut-Fin). On REGENERE tout
    # le tableau depuis le corps de l historique pour que les anciennes
    # lignes portent elles aussi les nouvelles colonnes. ATTENTION : on
    # reconstruit UNIQUEMENT l encart (frontmatter + tableau), jamais le
    # corps complet (maj_encart_activites retourne corps+encart - format
    # de l ancien fichier unique - bug corrige v0.8.2 : il ecrasait
    # AGENTS-activite-recente.md avec le corps du journal).
    if "| Grade | Agent |" not in lignes[idx_tableau]:
        try:
            with io.open(AGENTS_HISTORIQUE, "r", encoding="utf-8",
                         errors="replace") as fh:
                corps = fh.read()
            encart = _construire_encart_v1(corps)
            if encart:
                with io.open(AGENTS_ACTIVITE_RECENTE, "w", encoding="utf-8",
                             newline="\n") as fh:
                    fh.write(encart)
                return
        except OSError:
            pass
    # Reconstruire l encart depuis le corps pour que les anciennes entrees
    # portent aussi un executeur (Oracle par defaut). Cette reconstruction
    # evite de laisser des lignes historiques non conformes apres l ajout
    # de la tracabilite du classeur.
    try:
        with io.open(AGENTS_HISTORIQUE, "r", encoding="utf-8",
                     errors="replace") as fh:
            corps = fh.read()
        encart = _construire_encart_v1(corps)
        if encart:
            with io.open(AGENTS_ACTIVITE_RECENTE, "w", encoding="utf-8",
                         newline="\n") as fh:
                fh.write(encart)
            return
    except OSError:
        pass

    # Inserer apres le separateur
    idx_separateur = idx_tableau + 1
    while idx_separateur < len(lignes) and not lignes[idx_separateur].startswith("|---"):
        idx_separateur += 1
    insert_pos = idx_separateur + 1
    lignes.insert(insert_pos, nouvelle_entree)
    # Limiter a 50 entrees
    debut_entrees = insert_pos + 1
    fin_entrees = debut_entrees
    while fin_entrees < len(lignes) and lignes[fin_entrees].startswith("| "):
        fin_entrees += 1
    nb_entrees = fin_entrees - debut_entrees
    if nb_entrees > 50:
        lignes = lignes[:fin_entrees - (nb_entrees - 50)] + lignes[fin_entrees:]
    try:
        io.open(AGENTS_ACTIVITE_RECENTE, "w", encoding="utf-8",
                newline="\n").write("\n".join(lignes))
    except OSError:
        pass


def _ecrire_bdd_v1(identifiant, agent, type_action, raison, timestamp):
    """Ecrire dans la BDD SQLite (historique.db, 7 jours)."""
    try:
        # Import lazy du module BDD
        _bdd_dir = os.path.join("cerveau-projet", "freelance", "tools-commun",
                               "jarvis", "fonctions")
        if _bdd_dir not in sys.path:
            sys.path.insert(0, _bdd_dir)
        import historique_bdd as hb
        # Convertir timestamp v1 ("YYYY-MM-DD HH:MM:SS.ffffff") en ISO
        date_iso = None
        if timestamp:
            date_iso = timestamp.replace(" ", "T", 1)
        # Racine = dossier parent de AGENTS-historique.md
        _racine = os.path.dirname(os.path.abspath(AGENTS_HISTORIQUE))
        hb.ecrire(
            racine=_racine,
            agent=agent,
            llm=identifiant,
            type_action=type_action,
            raison=raison,
            date_iso=date_iso
        )
    except (ImportError, OSError) as exc:
        print("WARNING: BDD historique non disponible: %s" % str(exc)[:60])


def mapper_id_vers_session():
    """Construire le mapping id LLM -> session depuis le classeur-variables
    (lignes profil-session-* : 'session: X / id: Y'). Decision utilisateur
    2026-08-24 : les encarts d activite sont PAR SESSION (session-admin,
    session-freelance...), chaque session ecrit dans SON encart et peut lire
    les autres.

    v0.7.1 (2026-08-24) : supprime le concept d encart 'autre'. Les anciennes
    sessions (session-llm-1, session-llm-2, session-1) sont mappees vers leur
    session nommee (freelance pour la v2/freebuff, admin pour la v1/glm5 et
    l ancienne session-1 de themis). Les entrees dont la session ne matche
    AUCUN mapping ne creent plus d encart : elles sont ignorees (elles restent
    dans le corps de l historique, seuls les encarts ne les affichent pas)."""
    mapping = {
        # Sessions historiques (v0.6.x et avant) -> sessions nommees
        "session-llm-1": "session-freelance",
        "session-llm-2": "session-admin",
        "session-1": "session-admin",
    }
    if os.path.isfile(CLASSEUR_STOCKAGE):
        with io.open(CLASSEUR_STOCKAGE, "r", encoding="utf-8", errors="replace") as fh:
            for ligne in fh:
                if "profil-session-" not in ligne:
                    continue
                ms = re.search(r"session: (session-[A-Za-z0-9_-]+)", ligne)
                mid = re.search(r"id: (\S+)", ligne)
                if ms and mid:
                    mapping[mid.group(1)] = ms.group(1)
    return mapping


def maj_encart_activites(contenu, date, heure, agent, identifiant, raison):
    """Mettre a jour les encarts 'Activites recentes' PAR SESSION en haut du
    fichier (decision utilisateur 2026-08-24).

    Chaque session (session-admin, session-freelance...) possede SON encart
    (les 5 dernieres entrees de SA session), et peut lire les encarts des
    autres sessions pour savoir que les autres travaillent. Le mapping
    id -> session vient du classeur (profil-session-*).
    """
    mapping = mapper_id_vers_session()
    # Extraire toutes les entrees du format timeline avec l agent, la date et l id
    entrees = []
    agent_courant = "?"
    date_courante = ""
    for ligne in contenu.split("\n"):
        l = ligne.strip().rstrip("\\r")
        if l.startswith("## ") and not l.startswith("## Activites"):
            date_courante = l[3:].strip()
        elif l.startswith("### "):
            agent_courant = l[4:].strip()
        elif l.startswith("- ") and " | " in l:
            parties = l[2:].split(" | ", 3)
            if len(parties) >= 3:
                h = parties[0].strip()
                s = parties[1].strip()
                if len(parties) == 4:
                    t = parties[2].strip()
                    r = parties[3].strip()
                else:
                    t = ""
                    r = parties[2].strip()
                # Cle de tri : date + heure (JJ/MM/AAAA HH:MM)
                cle_tri = "%s %s" % (date_courante, h)
                session_entree = mapping.get(s)
                if session_entree is None:
                    # v0.7.1 : plus d encart 'autre' - les entrees non mappees
                    # restent dans le corps de l historique mais ne creent pas
                    # d encart (decision utilisateur 2026-08-24).
                    continue
                entrees.append((cle_tri, h, agent_courant, s, r, t, session_entree))

    # Regrouper par session, trier par date/heure decroissante, garder les 10 plus recentes
    par_session = {}
    for cle_tri, h, a, s, r, t, session_entree in entrees:
        par_session.setdefault(session_entree, []).append((cle_tri, h, a, s, r, t))

    # v0.7.5 : PLUS de '---\n\n' initial dans l encart : le separateur haut
    # est celui du frontmatter (fin de l identite). Avant, le while de
    # remontee mangeait les lignes vides et collait le '---' de l encart a
    # celui du frontmatter -> les tirets grossissaient a chaque execution
    # (bug accumulation, grosse ligne de 1308 tirets observee).
    encart = ""
    sessions_triees = sorted(par_session.keys())
    for session_nom in sessions_triees:
        liste = sorted(par_session[session_nom], key=lambda x: x[0], reverse=True)[:10]
        encart += "## Activites recentes -- %s\n\n" % session_nom
        encart += ENTETE_ENCART_V1 + "\n"
        encart += SEPARATEUR_ENCART_V1 + "\n"
        for _, h, a, s, r, t in liste:
            r_aff = r if len(r) <= 80 else r[:77] + "..."
            r_aff = r_aff.replace("|", "-")
            grade = _grade_label(a)
            secteur = _secteur_label(a)
            df = _etat_action(r, a)
            encart += "| %s | %s | %s | %s | %s | %s | %s | %s |\n" % (
                grade, a, df, secteur, r_aff, h, s, t)
        encart += "\n"
    encart += "---\n"

    # Remplacer l ancien bloc d encarts (s il existe) ou l inserer
    marqueur_debut = "## Activites recentes"
    if marqueur_debut in contenu:
        idx_debut = contenu.index(marqueur_debut)
        # Remonter au tout premier '## Activites recentes' du bloc
        while True:
            prec = contenu.rfind("\n## Activites recentes", 0, idx_debut)
            if prec == -1:
                break
            idx_debut = prec + 1
        # v0.7.5 : NE PAS remonter a travers les lignes vides precedentes :
        # idx_debut pointe sur le '#' de '## Activites recentes' et le
        # frontmatter (--- + ligne vide) reste intact au-dessus.
        # Trouver la fin : le '---' qui suit le dernier tableau du bloc
        idx_fin = contenu.find("\n---\n", idx_debut)
        if idx_fin == -1:
            idx_fin = contenu.find("\n## ", idx_debut + len(marqueur_debut))
        else:
            # v0.7.5 : consommer TOUS les '---' accumules (bug accumulation :
            # l encart finit par '---\n' et idx_fin pointait sur le '\n---\n'
            # trouve -> l ancien separateur restait, un de plus a chaque
            # execution). On avance apres chaque separateur consecutif pour
            # ne garder que celui de l encart.
            idx_fin += len("\n---\n")
            while contenu[idx_fin:idx_fin + len("\n---\n")] == "\n---\n":
                idx_fin += len("\n---\n")
        if idx_fin != -1:
            contenu = contenu[:idx_debut] + encart + contenu[idx_fin:]
        else:
            contenu = contenu[:idx_debut] + encart
    else:
        # Inserer apres le premier ---
        idx = contenu.find("\n---\n")
        if idx != -1:
            contenu = contenu[:idx + 5] + "\n" + encart + contenu[idx + 5:]
        else:
            contenu = encart + contenu

    return contenu


def mettre_a_jour_sessions_connues(contenu):
    """Reconstruire la section '## Sessions connues' d'AGENTS.md a partir du
    classeur-variables (lignes profil-session-*). La section liste toutes les
    sessions existantes (session, id LLM, agent actif, derniere activite) pour
    que chaque LLM sache que les autres existent et voie leur activite en temps
    reel. Retourne le contenu modifie (section remplacee ou inseree)."""
    if not os.path.isfile(CLASSEUR_STOCKAGE):
        return contenu
    lignes = []
    with io.open(CLASSEUR_STOCKAGE, "r", encoding="utf-8", errors="replace") as fh:
        for ligne in fh:
            if "profil-session-" not in ligne:
                continue
            m = re.search(r"session: (session-[A-Za-z0-9_-]+)", ligne)
            if not m:
                continue
            session = m.group(1)
            mid = re.search(r"id: (\S+)", ligne)
            llm_id = mid.group(1) if mid else "-"
            mage = re.search(r"agent: (\S+)", ligne)
            agent = mage.group(1) if mage else "?"
            mdate = re.search(r"date: (\S+ \S+)", ligne)
            date = mdate.group(1) if mdate else "-"
            lignes.append((session, llm_id, agent, date))
    if not lignes:
        return contenu

    def cle_session(entree):
        m = re.search(r"session-llm-(\d+)", entree[0])
        if m:
            return (0, int(m.group(1)))
        m2 = re.search(r"session-(\d+)", entree[0])
        if m2:
            return (1, int(m2.group(1)))
        return (2, 0)

    lignes.sort(key=cle_session)
    table = ("## Sessions connues\n\n"
             "| Session | Nom LLM | Agent actif | Derniere activite |\n"
             "|---|---|---|---|\n")
    for session, llm_id, agent, date in lignes:
        table += "| %s | %s | %s | %s |\n" % (session, llm_id, agent, date)

    # Retirer une section existante (jusqu'a la prochaine section ## OU un
    # marqueur du marbre <!-- MARBRE: --> : les outils ne doivent JAMAIS
    # avaler les bornes des zones protegees - bug detecte par le marbre
    # 2026-08-15 (le DEBUT de la zone constitution a ete mange par cette boucle)
    ls = contenu.split("\n")
    sortie = []
    i = 0
    while i < len(ls):
        if ls[i].strip() == "## Sessions connues":
            i += 1
            while i < len(ls) and not ls[i].startswith("## ") \
                    and not ls[i].startswith("<!-- MARBRE:"):
                i += 1
            continue
        sortie.append(ls[i])
        i += 1
    contenu = "\n".join(sortie)

    # Inserer avant '## Configuration Active' (ou en fin si absente)
    if "## Configuration Active" in contenu:
        contenu = contenu.replace("## Configuration Active",
                                  table + "## Configuration Active", 1)
    else:
        contenu = contenu.rstrip("\n") + "\n\n" + table
    return contenu


def actualiser_sessions_connues():
    """Relire AGENTS.md, reconstruire la section '## Sessions connues' (a partir
    du classeur a jour) et reecrire. A appeler APRES la mise a jour du profil
    session pour que la section reflete l'etat courant."""
    contenu = lire_agents()
    if contenu is None:
        return
    contenu = mettre_a_jour_sessions_connues(contenu)
    ecrire_agents(contenu)


def mettre_a_jour_profil_session(session, agent, llm_id=None):
    """Ecrire ou mettre a jour profil-session-<session> dans le classeur-variables.
    Format : | `profil-session-<session>` | session: <session> [/ id: <llm-id>] / agent: <agent> / date: <AAAA-MM-JJ HH:MM> | activer-agent-principal | <AAAA-MM-JJ> | [OK] |
    REGLE LIAISON ID (v0.3.5) : quand llm_id n'est pas fourni (activer/reactiver),
    PRESERVER l'id deja lie a la session dans la ligne existante -- sinon la liaison
    id<->session posee par sidentifier serait ECRASEE et le prochain sidentifier
    creerait une nouvelle session (sessions fantomes)."""
    fichier = CLASSEUR_STOCKAGE
    if not os.path.isfile(fichier):
        print("WARNING: Fichier classeur %s introuvable - profil session non ecrit" % fichier)
        return 1

    maintenant = datetime.now()
    # v0.7.3 : millisecondes (3 chiffres) au lieu des microsecondes (6 chiffres)
    # le format de largeur '3f' est INVALIDE en Python (ValueError) : troncature
    # [:-3] obligatoire (pattern horloge.py)
    ts = maintenant.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    jour = maintenant.strftime("%Y-%m-%d")
    # REGLE DE DERIVATION (IMMUABLE): id = profil-session- + partie apres le prefixe session-
    id_session = session[len("session-"):] if session.startswith("session-") else session
    prefixe_ligne = "| `profil-session-" + id_session + "`"

    with io.open(fichier, "r", encoding="utf-8", errors="replace") as fh:
        lignes = fh.read().split(chr(10))

    # REGLE LIAISON ID (v0.3.5): preserver l'id existant si non fourni
    if llm_id is None:
        for l in lignes:
            if l.startswith(prefixe_ligne):
                m = re.search(r"id: (\S+)", l)
                if m:
                    llm_id = m.group(1)
                break

    if llm_id:
        nouvelle_ligne = ("| `profil-session-%s` | session: %s / id: %s / agent: %s / date: %s | "
                          "activer-agent-principal | %s | [OK] |") % (id_session, session, llm_id, agent, ts, jour)
    else:
        nouvelle_ligne = ("| `profil-session-%s` | session: %s / agent: %s / date: %s | "
                          "activer-agent-principal | %s | [OK] |") % (id_session, session, agent, ts, jour)

    if not verifier_ascii(nouvelle_ligne):
        print("ERREUR: Caractere non-ASCII dans le profil session - ecriture classeur REFUSEE")
        return 1

    trouve = False
    for i, l in enumerate(lignes):
        if l.startswith(prefixe_ligne):
            lignes[i] = nouvelle_ligne
            trouve = True
            break
    if not trouve:
        idx = -1
        for i, l in enumerate(lignes):
            if l.startswith("| `"):
                idx = i
        if idx >= 0:
            lignes.insert(idx + 1, nouvelle_ligne)
        else:
            lignes.append(nouvelle_ligne)

    if not ecrire_classeur(
            lignes, "profil-session-%s" % id_session,
            "activer-agent-principal", agent, session,
            ancienne_valeur="profil session precedent",
            nouvelle_valeur=nouvelle_ligne,
            raison="Mise a jour du profil de session"):
        print("ERREUR: Ecriture du profil session refusee par la routine du classeur")
        return 1

    print("Profil session mis a jour dans %s : %s (%s)" % (fichier, session, agent))
    return 0


def agent_actif_bloc(contenu, session_id):
    """Retourner l'agent REEL du bloc de session (champ Nom Agent), ou Cerberus
    si le champ est absent. CORRECTION v0.5.1 : sidentifier ecrivait Cerberus
    en dur, ce qui falsifiait le profil classeur quand un AUTRE agent (ex:
    morpheus) etait actif -> double source contradictoire -> l agent s arretait
    au demarrage."""
    for sid, bloc in extraire_blocs_session(contenu):
        if sid == session_id:
            m = re.search(r"\*\*(?:Nom Agent|Nom)\*\* \| ([^|]+)", bloc)
            if m and m.group(1).strip():
                return m.group(1).strip()
            return "Cerberus"
    return "Cerberus"


def normaliser_nom_session(nom_session):
    """Normaliser un nom de session fourni par l utilisateur (decision
    2026-08-24 : sessions NOMMEES admin/freelance au lieu de session-llm-N).
    Accepte 'admin' -> session-admin, 'session-admin' -> session-admin.
    Retourne None si invalide (caracteres non autorises)."""
    if not nom_session:
        return None
    nom = nom_session.strip()
    if nom.startswith("session-"):
        nom = nom[len("session-"):]
    if not re.match(r"^[A-Za-z0-9_-]+$", nom):
        return None
    return "session-" + nom


def sidentifier(llm_id=None, nom_session=None):
    """Creer/choisir la session du LLM (agent principal = Cerberus).
    REGLE UTILISATEUR (mode ID) : chaque LLM possede SON id (donne par
    l'utilisateur au lancement).
    REGLE SESSION NOMMEE (v0.7.0, decision utilisateur 2026-08-24) :
    l utilisateur indique la session au demarrage ('admin' = equipe v1 qui
    gere le cerveau, 'freelance' = equipe v2) : sidentifier <id> <session>.
    La session creee/retrouvee est session-<nom> (ex: session-admin).
    REGLE ALIGNEMENT (v0.4.0) conservee en repli : id llm-N -> session-llm-N
    quand AUCUN nom de session n est fourni (compatibilite heritage).
    SOURCE DOUBLE : l'outil cherche la liaison dans AGENTS.md (champ **Nom LLM**)
    puis dans le classeur (id: <llm-id>). Le LLM peut donc se reconnaitre en
    lisant AGENTS.md.
    - nom_session fourni -> session-<nom> (creee ou retrouvee), id lie
    - id deja lie -> c'est SA session (retrouvee)
    - id inconnu llm-N -> session-llm-N si libre (ou orpheline), sinon prochaine libre
    - sans argument -> compatibilite heritage : prochaine session libre"""
    contenu = lire_agents()
    if contenu is None:
        return 1
    contenu, migre = migrer_si_necessaire(contenu)

    session_explicite = normaliser_nom_session(nom_session)

    if session_explicite:
        # REGLE SESSION NOMMEE : l utilisateur a choisi la session
        id_deja_lie = id_lie_a_session(session_explicite)
        if id_deja_lie is not None and llm_id and id_deja_lie != llm_id.strip():
            print("ATTENTION: %s deja liee a l'id %s - la session reste %s (agent principal : Cerberus)"
                  % (session_explicite, id_deja_lie, session_explicite))
        session = session_explicite
        print("Session %s (demandee par l utilisateur, agent principal : Cerberus)" % session)
    elif llm_id is not None:
        llm_id = llm_id.strip()
        session_liee = trouver_session_par_id(llm_id)
        if session_liee:
            session = session_liee
            agent_actif = agent_actif_bloc(contenu, session)
            print("Session retrouvee pour id %s : %s (agent principal : %s)"
                  % (llm_id, session, agent_actif))
        else:
            # REGLE ALIGNEMENT (v0.4.0) : id llm-N -> session-llm-N
            cible = session_cible_pour_id(llm_id)
            if cible:
                id_deja_lie = id_lie_a_session(cible)
                if id_deja_lie is not None and id_deja_lie != llm_id:
                    # CONFLIT : session-llm-N deja liee a un autre LLM
                    session = "session-llm-1" if migre else trouver_prochaine_session(contenu)
                    print("ATTENTION: %s deja liee a l'id %s - attribution %s (agent principal : Cerberus)"
                          % (cible, id_deja_lie, session))
                else:
                    # Libre ou orpheline (aucun id) -> absorption
                    session = cible
                    print("Nouvelle session pour id %s : %s (alignee sur l'id, agent principal : Cerberus)"
                          % (llm_id, session))
            else:
                session = "session-llm-1" if migre else trouver_prochaine_session(contenu)
                print("Nouvelle session pour id %s : %s (agent principal : Cerberus)"
                      % (llm_id, session))
    else:
        # Sans argument : premier LLM -> llm-1 (via migration), sinon prochaine libre
        session = "session-llm-1" if migre else trouver_prochaine_session(contenu)
        print("Session attribuee : %s (agent principal : Cerberus)" % session)

    if not any(s == session for s, _ in extraire_blocs_session(contenu)):
        contenu = creer_session(contenu, session, llm_id)
        if contenu is None:
            return 1
        ecrire_agents(contenu)
    elif llm_id is not None:
        # Bloc existant : poser/mettre a jour le champ Nom LLM (reconnaissance par lecture)
        contenu = poser_nom_llm_bloc(contenu, session, llm_id)
        ecrire_agents(contenu)

    agent_actif = agent_actif_bloc(contenu, session)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    ajouter_historique(timestamp, session, agent_actif, "Identification LLM - demarrage de session", "R")
    mettre_a_jour_profil_session(session, agent_actif, llm_id)
    actualiser_sessions_connues()
    return 0


CHRONO_OUTIL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                            "..", "chronometrer", "chronometrer-duree",
                            "chronometrer-duree.py")


def appeler_chrono(args):
    """Appelle chronometrer-duree en subprocess (pattern proteger-verrou-marbre).
    Retourne (rc, sortie). En mode test (AGENTS_FILE surcharge), le chrono est
    neutralise : le fichier CHRONOS_FICHIER est surcharge dans un dossier temp."""
    cmd = [sys.executable, CHRONO_OUTIL] + args + ["--confirme-doc"]
    env = dict(os.environ)
    if os.environ.get("AGENTS_FILE"):
        # mode test : chrono isole dans un fichier temporaire par session
        env["CHRONOS_FICHIER"] = os.path.join(
            os.path.dirname(os.environ.get("AGENTS_FILE", "")),
            "chronos-test.jsonl")
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=10,
                           env=env)
        return p.returncode, (p.stdout or "").strip()
    except (OSError, subprocess.TimeoutExpired) as e:
        print("[AVERTISSEMENT] chronometrer-duree injoignable : %s" % e)
        return 1, ""


ANALYSEUR_TOKENS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "..", "..", "analyser", "analyser-tokens",
                                 "analyser-tokens.py")


def appeler_analyser_tokens(args):
    """Appelle analyser-tokens en subprocess (mode machine --snapshot).
    Retourne (rc, sortie). En mode test, TOKENS_SESSION est surcharge pour
    un comportement deterministe (option --tokens-mock)."""
    cmd = [sys.executable, ANALYSEUR_TOKENS] + args
    env = dict(os.environ)
    mock = os.environ.get("TOKENS_MOCK")
    if mock:
        env["TOKENS_SESSION"] = mock
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=10,
                           env=env)
        return p.returncode, (p.stdout or "").strip()
    except (OSError, subprocess.TimeoutExpired) as e:
        print("[AVERTISSEMENT] analyser-tokens injoignable : %s" % e)
        return 1, ""


def snapshot_tokens():
    """Snapshot cumulatif courant des tokens (JSON machine). Retourne dict
    ou None si injoignable. Mode hybride : API (TOKENS_SESSION) si fournie,
    sinon estimation locale par taille des traces."""
    rc, sortie = appeler_analyser_tokens(["--snapshot"])
    if rc != 0 or not sortie:
        return None
    try:
        m = json.loads(sortie.split("\n")[0])
        if isinstance(m, dict):
            return m
    except ValueError:
        pass
    return None


def arreter_chrono_session(session):
    """Arrete le chrono ouvert de la session. Retourne (agent, duree,
    tokens_debut) ou (None, None, None) si aucun chrono actif."""
    rc, sortie = appeler_chrono(["arreter", session])
    if rc != 0 or not sortie or sortie == "AUCUN_CHRONO":
        return None, None, None
    parties = sortie.split("|")
    if len(parties) >= 2:
        # la sortie est 'agent | duree' suivie des MESSAGES POUR L AGENT
        # sur les lignes suivantes : ne garder que la 1re ligne de la duree
        # (sinon les messages parasites sont inseres dans le repere ### de
        # AGENTS-historique -- bug detecte par test-098 via la non-regression
        # Janus 2026-08-19, mission chronometre).
        duree = parties[1].strip().split("\n")[0].strip()
        tokens_debut = None
        if len(parties) >= 3:
            # le 3e champ est le JSON tokens_debut SUIVI des MESSAGES POUR
            # L AGENT : ne garder que la 1re ligne (meme piege que la duree).
            try:
                tokens_debut = json.loads(
                    parties[2].strip().split("\n")[0])
            except ValueError:
                tokens_debut = None
        return parties[0].strip(), duree, tokens_debut
    return None, None, None


def demarrer_chrono_session(session, agent):
    """Demarre le chrono de l agent nouvellement active, avec le snapshot
    tokens de debut (pour la difference par intervention)."""
    snap = snapshot_tokens()
    args = ["demarrer", session, agent]
    if snap:
        args += ["--tokens", json.dumps(snap, ensure_ascii=True)]
    appeler_chrono(args)


def ajouter_duree_repere(agent, duree, conso=None):
    """Ajoute '(duree, tokens: Xk env / Yk recus)' au repere '###' de la
    DERNIERE entree de l agent dans AGENTS-historique. Ne fait rien si
    l agent est inconnu ou si le repere porte deja une duree."""
    if not duree or not os.path.isfile(AGENTS_HISTORIQUE):
        return
    texte_conso = formater_conso_tokens(conso)
    suffixe = " (%s)" % duree
    if texte_conso:
        suffixe = " (%s, %s)" % (duree, texte_conso)
    with io.open(AGENTS_HISTORIQUE, "r", encoding="utf-8",
                 errors="replace") as fh:
        lignes = fh.readlines()
    cible = None
    motif_repere = re.compile(
        r"- <span style=\"color:#[0-9a-f]{6}\">%s</span>" % re.escape(agent))
    for idx, ligne in enumerate(lignes):
        if not ligne.startswith("### <span"):
            continue
        if not motif_repere.search(ligne):
            continue
        cible = idx
        break  # la 1re occurrence = la plus recente (ordre decroissant)
    if cible is None:
        return
    ligne = lignes[cible].rstrip("\n")
    if "(" in ligne and "min" in ligne:
        return  # deja une duree
    lignes[cible] = ligne + suffixe + "\n"
    with io.open(AGENTS_HISTORIQUE, "w", encoding="utf-8", newline="\n") as fh:
        fh.writelines(lignes)


def formater_conso_tokens(conso):
    """Formate la conso tokens pour le repere : '12.4k env / 8.2k recus'.
    Retourne '' si nulle ou absente (parite avec analyser-tokens)."""
    if not conso:
        return ""
    env = int(conso.get("envoyes", 0) or 0)
    rec = int(conso.get("recus", 0) or 0)
    if env == 0 and rec == 0:
        return ""
    def _k(n):
        if n >= 1000:
            return "%.1fk" % (n / 1000.0)
        return str(n)
    return "tokens: %s env / %s recus" % (_k(env), _k(rec))


def conso_tokens_intervention(tokens_debut):
    """Conso de l intervention = snapshot fin - snapshot debut (compteurs
    cumulatifs). Retourne dict {envoyes, recus, fiable} ou None."""
    if not tokens_debut:
        return None
    snap_fin = snapshot_tokens()
    if not snap_fin:
        return None
    try:
        env = max(0, int(snap_fin.get("envoyes", 0))
                  - int(tokens_debut.get("envoyes", 0)))
        rec = max(0, int(snap_fin.get("recus", 0))
                  - int(tokens_debut.get("recus", 0)))
    except (TypeError, ValueError):
        return None
    return {"envoyes": env, "recus": rec,
            "fiable": bool(tokens_debut.get("fiable"))
                       and bool(snap_fin.get("fiable"))}


def _afficher_oracle_inbox(agent):
    """Afficher les messages Oracle non lus d un agent lors de son activation."""
    oracle_inbox = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "..", "oracle", "inbox", "%s.jsonl" % agent)
    if not os.path.isfile(oracle_inbox):
        return
    non_lus = []
    try:
        with io.open(oracle_inbox, "r", encoding="utf-8", errors="replace") as fh:
            for ligne in fh:
                ligne = ligne.strip()
                if not ligne:
                    continue
                try:
                    msg = json.loads(ligne)
                    if not isinstance(msg, dict):
                        continue
                    if not msg.get("lu"):
                        non_lus.append(msg)
                except (ValueError, KeyError):
                    continue
    except OSError:
        return
    if not non_lus:
        return
    print("")
    print("=== MESSAGES ORACLE NON LUS (%d) ===" % len(non_lus))
    for msg in non_lus:
        statut = "[PRIORITE 1]" if msg.get("priorite") == 1 else ""
        print("  [%s] %s -> %s %s" % (msg.get("id", "?"), msg.get("de", "?"), msg.get("vers", "?"), statut))
        print("    Objet: %s" % msg.get("objet", ""))
        corps = msg.get("corps", "")
        if len(corps) > 120:
            corps = corps[:120] + "..."
        print("    Corps: %s" % corps)
    print("  Pour acquitter : oracle.py acquitter %s <id>" % agent)
    print("============================")


def activer_agent(session, agent, raison, mission=None, type_round="R",
                  historiser=True):
    """Activer un agent dans la session (ne touche que son bloc).

    - historiser=True (defaut) : l activation historique l entree (usage
    direct via la CLI, historique CE-ROUND).
    - historiser=False : l appelant (Oracle, vision 2026-08-27) s occupe
      LUI-MEME de l historisation (cmd_activer oracle.py pose DEBUT: pour
      remplir la colonne Debut/Fin). Evite le DOUBLON d entrees quand
      Oracle pilote les activations."""
    if not verifier_ascii(raison):
        print("ERREUR: Caractere non-ASCII detecte dans la raison - activation REFUSEE")
        return 1

    info = get_agent_info(agent)
    if info is None:
        print("ERREUR: Agent inconnu '%s'" % agent)
        return 1

    contenu = lire_agents()
    if contenu is None:
        return 1
    contenu, _ = migrer_si_necessaire(contenu)

    # GARDE-FOU (v0.5.22) : relais de chaine autorise (Pattern 8, decision
    # utilisateur Option A 2026-08-21 : l agent suivant active l agent suivant
    # pour continuer la boucle). Si un agent autre que Cerberus est encore
    # actif dans la session :
    #   - Agent cible = Cerberus (reactivation) : toujours autorise
    #   - Meme agent cible (auto-reactivation) : AVERTISSEMENT, autorise
    #   - Agent different (relais de chaine) : AVERTISSEMENT, AUTORISE
    #     (chaque maillon active le suivant a sa fin de carte - Pattern 8)
    #   - --forcer : option conservee (avertissement forcee, compatibilite)
    agent_actuel = agent_actif_bloc(contenu, session)
    if agent_actuel and agent_actuel.lower() != "cerberus":
        forcer = "--forcer" in sys.argv
        if agent.lower() == "cerberus":
            # Reactivation de Cerberus : toujours autorise
            pass
        elif agent.lower() == agent_actuel.lower():
            # Auto-reactivation : avertissement uniquement
            print("")
            print("=== AVERTISSEMENT GARDE-FOU (agent oublie) ===")
            print("L agent '%s' est encore actif dans %s." % (agent_actuel, session))
            print("Il a probablement oublie sa fin (modele aero R1/R3) : sa fin devait aller vers ORACLE (reactiver-fin --cible oracle).")
            print("Auto-reactivation de '%s' autorisee." % agent)
            print("==============================================")
            print("")
        elif forcer:
            # Activation forcee : avertissement + continuation
            print("")
            print("=== AVERTISSEMENT GARDE-FOU (activation forcee) ===")
            print("L agent '%s' est encore actif dans %s." % (agent_actuel, session))
            print("Activation de '%s' FORCEE (--forcer)." % agent)
            print("Le travail de '%s' risque d etre perdu." % agent_actuel)
            print("===========================================================")
            print("")
        else:
            # RELAIS DE CHAINE : autorise sans avertissement (Pattern 8, v0.5.29).
            # Chaque maillon active le suivant a sa fin de carte : c'est le
            # comportement normal, plus besoin d'avertir.
            pass

    if not any(s == session for s, _ in extraire_blocs_session(contenu)):
        contenu = creer_session(contenu, session)
        if contenu is None:
            return 1

    role, fiche, corrections = info
    date = datetime.now().strftime("%Y-%m-%d")
    # v0.5.4 : ajouter l'instruction de demarrage a la Raison quand un agent
    # (autre que Cerberus) est active - anti-bug d arret a la case c0.
    raison_finale = raison
    if agent.lower() != "cerberus" and "DEMARRAGE" not in raison:
        # v0.5.30 : les agents FREELANCE recoivent le bloc V2 (arbre +
        # jarvis.py), les agents v1 conservent le bloc guider-parcours.
        if "freelance" in fiche:
            raison_finale = raison + "\n\n" + instruction_demarrage_v2(agent)
        else:
            raison_finale = raison + "\n\n" + instruction_demarrage(agent)
    champs = {
        "Nom Agent": agent,
        "Role Agent": role,
        "Derniere mise a jour": date,
        "Fiche": fiche,
        "Corrections": corrections,
        "Active par": "Cerberus (automatique)",
        "Raison": raison_finale,
    }
    # v0.5.16+ : chronometrage + tokens de l intervention - on ferme le
    # chrono de l agent precedent (passage de relais) et on ajoute sa duree
    # ET sa conso tokens (difference debut/fin) au repere de son entree dans
    # l historique, PUIS on ouvre le chrono du nouvel agent (sa propre duree
    # et sa conso seront connues au prochain passage de relais).
    agent_prec, duree_prec, tokens_prec = arreter_chrono_session(session)
    if agent_prec and duree_prec:
        conso_prec = conso_tokens_intervention(tokens_prec)
        ajouter_duree_repere(agent_prec, duree_prec, conso_prec)
    demarrer_chrono_session(session, agent)

    contenu = editer_champs_session(contenu, session, champs)
    ecrire_agents(contenu)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    if historiser:
        ajouter_historique(timestamp, session, agent, raison_finale, type_round)
    mettre_a_jour_profil_session(session, agent)
    actualiser_sessions_connues()
    print("Session %s : agent %s active avec succes" % (session, agent))
    # MESSAGES INFORMATIONNELS (regle immuable v0.3.0) : rappels contextuels
    print("")
    print("=== MESSAGES POUR L AGENT ===")
    print("  > RELEVE MEME ROUND : l agent active (%s) doit enchainer IMMEDIATEMENT (relire SA fiche + SES corrections puis executer sa mission) - ne jamais s arreter apres une activation" % agent)
    print("  > la fin de mission suit SA carte (modele aero R1/R3) : MA FIN va vers ORACLE (python3 cerveau-projet/agents/tools/oracle/oracle.py reactiver-fin <agent> \"<bilan>\" --cible oracle), JAMAIS vers Cerberus ni vers un autre agent. Le PILOTE decide de la suite (largage du maillon suivant) et atterrit sur Cerberus en fin de round avec le bilan consolide.")
    # Oracle v0.1.0 : afficher les messages non lus de l agent
    _afficher_oracle_inbox(agent)
    return 0


def activer_cerberus(session, raison, agent_precedent=None, type_round="R"):
    """Activer Cerberus dans la session (ne touche que son bloc).

    Vision 2026-08-27 : PLUS de 'reactiver', toujours 'activer'.
    Modele aero (2026-08-30, R1/R3) : AUCUN agent n active Cerberus a sa
    fin - la fin de tout agent va vers ORACLE (reactiver-fin <agent>
    --cible oracle). C est le PILOTE (Oracle, l aeroport) qui atterrit sur
    Cerberus via cette fonction quand le ROUND se termine (bilan
    consolide). Le comportement de fin (chrono, duree) etait dans
    reactiver_cerberus ; il est conserve ici sous le seul nom 'activer'.

    agent_precedent : optionnel, deduit de arreter_chrono_session si absent.
    """
    if not verifier_ascii(raison):
        print("ERREUR: Caractere non-ASCII detecte dans la raison - activation REFUSEE")
        return 1

    if not os.path.isfile(CERBERUS_FICHE):
        print("ERREUR: Le fichier %s n'existe pas" % CERBERUS_FICHE)
        return 1

    print("Lecture de %s..." % CERBERUS_FICHE)
    with io.open(CERBERUS_FICHE, "r", encoding="utf-8", errors="replace") as fh:
        fh.read()

    contenu = lire_agents()
    if contenu is None:
        return 1
    contenu, _ = migrer_si_necessaire(contenu)

    if not any(s == session for s, _ in extraire_blocs_session(contenu)):
        contenu = creer_session(contenu, session)
        if contenu is None:
            return 1

    role, fiche, corrections = get_agent_info("cerberus")
    date = datetime.now().strftime("%Y-%m-%d")
    # v0.5.16+ : fin de mission - fermer le chrono de l agent precedent et
    # deduire son nom (agent_precedent optionnel -> agent_prec reel).
    agent_prec, duree_prec, tokens_prec = arreter_chrono_session(session)
    precedent = agent_precedent or agent_prec or "la chaine"
    champs = {
        "Nom Agent": "Cerberus",
        "Role Agent": role,
        "Derniere mise a jour": date,
        "Fiche": fiche,
        "Corrections": corrections,
        "Active par": "%s (retour de mission)" % precedent,
        "Raison": raison,
    }
    if agent_prec and duree_prec:
        conso_prec = conso_tokens_intervention(tokens_prec)
        ajouter_duree_repere(agent_prec, duree_prec, conso_prec)

    contenu = editer_champs_session(contenu, session, champs)
    ecrire_agents(contenu)

    # Colonne Debut/Fin : Cerberus qui reprend = DEBUT de son cycle de
    # coordination (pas FIN), meme si la raison porte le bilan de l agent
    # precedent (ex: 'FIN MISSION VULCAIN : ...'). On prefxe DEBUT pour
    # que la colonne affiche DEBUT (demande utilisateur 2026-08-27).
    # SAUF si la raison commence deja par FIN (retour de mission = FIN).
    r_upper = (raison or "").strip().upper()
    raison_df = raison
    if not r_upper.startswith("DEBUT") and not r_upper.startswith("FIN") and not r_upper.startswith("RETOUR"):
        raison_df = "DEBUT: " + raison

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    ajouter_historique(timestamp, session, "Cerberus", raison_df, type_round, executeur="Oracle")
    mettre_a_jour_profil_session(session, "Cerberus")
    actualiser_sessions_connues()
    print("Session %s : Cerberus reactive avec succes" % session)
    # MESSAGES OBLIGATOIRES (v0.6.2) : forcer Cerberus a suivre sa carte
    print("")
    print("=== INSTRUCTION OBLIGATOIRE ===")
    print("CERBERUS REACTIVE : tu DOIS suivre ta carte de decision.")
    print("")
    # Lancer guider-parcours pour Cerberus
    parcours = "cerveau-projet/agents/cerberus/parcours/parcours-cerberus.json"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tools_dir = os.path.dirname(os.path.dirname(script_dir))
    guider = os.path.join(tools_dir, "guider", "guider-parcours", "guider-parcours.py")
    if os.path.isfile(guider):
        print("LANCE CETTE COMMANDE MAINTENANT :")
        print("")
        print("python3 %s %s --case c0" % (guider, parcours))
        print("")
        print("Puis relis ta fiche et tes corrections avant de continuer.")
    else:
        print("Lance guider-parcours pour ton parcours :")
        print("python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py %s --case c0" % parcours)
    print("")
    print("=== MESSAGES POUR L AGENT ===")
    print("  > RELEVE MEME ROUND : Cerberus doit suivre sa carte IMMEDIATEMENT")
    print("  > le cycle est termine : Cerberus accueille la demande suivante ou relance une mission")
    return 0


def lister_sessions():
    """Lister les sessions et leur agent principal."""
    contenu = lire_agents()
    if contenu is None:
        return 1
    blocs = extraire_blocs_session(contenu)
    if not blocs:
        print("Aucune session LLM enregistree")
        return 0
    for session, bloc in blocs:
        m = re.search(r"\*\*(?:Nom Agent|Nom)\*\* \| ([^|]+)", bloc)
        nom = m.group(1).strip() if m else "?"
        print("%s : %s" % (session, nom))
    return 0


def afficher_aide():
    print("Usage: activer-agent-principal.py <action> [parametres]")
    print("")
    print("Actions disponibles:")
    print("  sidentifier [session]              - Creer/choisir sa session (agent principal = Cerberus)")
    print("  activer <session> <agent> <raison> [mission]  - Activer un agent dans sa session")
    print("                            (agent=cerberus : fin de mission, toujours 'activer' jamais 'reactiver')")
    print("  sessions                           - Lister les sessions et leur agent principal")
    print("  aide                               - Afficher cette aide")
    print("")
    print("Exemples:")
    print("  activer-agent-principal.py sidentifier")
    print("  activer-agent-principal.py sidentifier <id> [session]")
    print("  activer-agent-principal.py sidentifier glm5 admin")
    print("  activer-agent-principal.py sidentifier freebuff freelance")
    print("  activer-agent-principal.py activer session-admin Buffy \"Mission correction\"")
    print("  activer-agent-principal.py activer session-admin cerberus \"Mission terminee\"")


def main(argv):
    if not argv:
        afficher_aide()
        return 0

    # v0.5.30 : --forcer peut etre place n importe ou (garde-fou le detecte
    # via sys.argv). On le retire d argv pour ne pas polluer le parsing
    # positionnel (mission/agent_precedent).
    argv = [a for a in argv if a != "--forcer"]

    # v0.5.24 : extraire --type r|ir (indicateur ROUND/INTER-ROUND, regle R5
    # protocole-fin-mission v0.2.0). Defaut R si absent.
    type_round = "R"
    if "--type" in argv:
        i_type = argv.index("--type")
        if i_type + 1 < len(argv):
            type_round = argv[i_type + 1].upper()
            del argv[i_type:i_type + 2]
        else:
            print("ERREUR: --type attend r ou ir")
            return 1
    if type_round not in ("R", "IR"):
        print("ERREUR: --type attend r ou ir")
        return 1

    action = argv[0]

    if action not in ("aide", "--help", "-h", "--version"):
        verifier_residus_racine()

    if action in ("aide", "--aide", "--help", "-h"):
        afficher_aide()
        return 0

    if action == "--version":
        print("activer-agent-principal v%s (%s)" % (VERSION, STATUT))
        return 0

    if action in ("sidentifier", "identifier", "activer"):
        if not verrouiller_constitution():
            return 1

    if action in ("sidentifier", "identifier"):
        llm_id = argv[1] if len(argv) > 1 else None
        nom_session = argv[2] if len(argv) > 2 else None
        return sidentifier(llm_id, nom_session)

    if action == "sessions":
        return lister_sessions()

    if action == "activer":
        if len(argv) < 4:
            print("ERREUR: Parametres manquants pour l'action 'activer' (session, agent, raison)")
            afficher_aide()
            return 1
        session = argv[1]
        agent = argv[2]
        raison = argv[3]
        mission = argv[4] if len(argv) > 4 else None
        # FIX v0.8.11 (2026-09-02, lecon test-025) : normaliser le nom de
        # session comme sidentifier le fait. Sans normalisation, 'activer
        # admin vulcain' ecrivait un bloc '### Session : admin' (invalide -
        # les sessions NOMMEES sont session-admin/session-freelance) que
        # nettoyer-sessions ne supprimait pas (motif session-*) -> test-025 KO.
        session_normalise = normaliser_nom_session(session) or session
        # Vision 2026-08-27 : PLUS de 'reactiver', toujours 'activer'.
        # Activer Cerberus = fermer/ronde de fin de mission (chrono + bilan).
        # Le 4e argument optionnel (mission) sert d'agent_precedent pour
        # Cerberus (option, deduit du chrono si absent).
        if agent.lower() == "cerberus":
            return activer_cerberus(session_normalise, raison, mission, type_round)
        return activer_agent(session_normalise, agent, raison, mission, type_round)

    print("ERREUR: Action inconnue '%s'" % action)
    afficher_aide()
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
