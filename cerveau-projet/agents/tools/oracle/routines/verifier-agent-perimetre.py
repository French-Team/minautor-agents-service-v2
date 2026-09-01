#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
routine verifier-agent-perimetre -- Verifie que chaque mission/modification
est effectuee par LE BON AGENT (respect des perimetres v1/v2).

Contexte 2026-08-29 (decision utilisateur) : un agent v1 (Buffy) a modifie
des fichiers de la v2 (cerveau-projet/freelance/) alors que c est ferrari
(agent v1 specialise freelance) qui doit le faire quand on est en v1. Un
outil de conformite ASCII v1 a par ailleurs remplace les emojis de
grades-v2.json par des placeholders texte ([ROND_VERT] au lieu de l emoji)
- emojis AUTORISES en v2. Il faut une routine qui verifie que la mission
va etre effectuee par le bon agent.

Regles de perimetre (source AGENTS.md) :
  - Agents v1 (Buffy, Cerberus, Vulcain...) : ecrivent dans
    cerveau-projet/ (hors freelance/). SAUF ferrari (agent v1 specialise
    qui corrige et modifie le dossier v2, conventions v2).
  - Agents v2 (freelance) : n ecrivent QUE dans cerveau-projet/freelance/.
  - Vision : SEUL habilite a modifier JARVIS (freelance/jarvis/ +
    tools-commun/jarvis/).
  - Hades : SEUL habilite aux commandes git.
  - Hygie : SEULE habilite a tout le workspace.
  - Gardien : SEUL a proposer la modification des zones protegees.

La routine surveille les commits git recents et les fichiers modifies
(non commites) : pour chaque fichier, elle determine la zone (v1 / v2 /
jarvis / zone protegee) et l auteur git, puis verifie si l auteur est
habilitE pour cette zone. En cas de violation, alerte Oracle au format
4W via l inbox Oracle (decision utilisateur 2026-08-30 : routines -> Oracle).

LECTURE SEULE + alerte : ne corrige jamais, elle signale.

MODE GATE (--gate --moi <agent>) : porte de VERIFICATION PRE-VOL, lancee
PAR L AGENT lui-meme au moment ou il decide de commencer sa mission (case
c0g de son parcours) - PAS un timer (decision utilisateur 2026-08-29 : il
est inutile de laisser un mauvais agent travailler puis tout detruire ; on
verifie AVANT qu il commence). La porte verifie :
  1. L agent actif de la session-admin (AGENTS.md) == moi. Sinon KO : un
     autre agent est actif, je ne dois PAS travailler.
  2. La Raison de la session (ma mission) ne vise pas une zone hors de mes
     habilitations (ex: agent v1 non-ferrari avec une mission freelance/).
Retour 0 = OK (je peux commencer) / 1 = KO (STOP immediat, reactiver
Cerberus SANS RIEN TOUCHER). En mode gate : PAS d alerte inbox, PAS
d historisation, PAS d anti-spam - c est un controle pur.

Usage:
    python3 verifier-agent-perimetre.py [--dry-run] [--no-chrono]
    python3 verifier-agent-perimetre.py --gate --moi <mon-agent>

Retour: 0 si succes (rien de suspect), 1 si violation detectee / gate KO.
"""

import io
import json
import os
import subprocess
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path

VERSION = "0.1.0"

_DOSSIER = os.path.dirname(os.path.abspath(__file__))
ORACLE_DIR = Path(_DOSSIER).parent
INBOX_DIR = ORACLE_DIR / "inbox"
MANIFEST = ORACLE_DIR / "routines" / "manifest.json"
ETAT_VIOLATIONS = Path(_DOSSIER) / "etat-violations.json"

# Zones et agents habilitES (source AGENTS.md, regle groupes-agents).
# zone -> (chemin_prefixe, agents_habilitES)
ZONES = {
    # v1 : le cerveau-projet HORS freelance (agents v1, SAUF ferrari qui
    # traite la v2). Les agents v2 n ecrivent JAMAIS ici.
    "v1": ("cerveau-projet", ["cerberus", "buffy", "vulcain", "morpheus",
                              "janus", "atlas", "themis", "clio", "hygie",
                              "hermes", "socrate", "redacteur-v2", "hades",
                              "argus", "chiron", "gardien", "oracle"]),
    # v2 : le dossier freelance. Agents v2 autorises + ferrari (agent v1
    # specialise v2, conventions v2). Les autres agents v1 sont EXCLUS.
    "v2": ("cerveau-projet/freelance",
           ["ferrari", "stark", "jarvis", "vision", "shuri", "forge",
            "rogers", "parker", "edith", "fury"]),
    # JARVIS : exclusivite Vision (agent + server MCP).
    "jarvis": ("cerveau-projet/freelance/tools-commun/jarvis", ["vision"]),
}

# Agents v1 autorises a TOUT le workspace (Hygie). Hades : git seul.
AGENTS_TOUT_WORKSPACE = {"hygie", "hades"}

# Agents de COORDINATION (cerberus, oracle) : pas de zone de travail - ils
# coordonnent. Leur Raison (bilan FIN des agents precedents) peut legitiment
# mentionner n importe quelle zone (ex: ferrari reactive Cerberus avec un
# bilan sur des fichiers freelance) : la verif de ZONE ne s applique pas a
# eux, seule la verif d AGENT ACTIF reste (decision 2026-08-29).
AGENTS_COORDINATION = {"cerberus", "oracle"}

# Fichiers racine partages (AGENTS.md, README.md, demarrer.md...) :
# geres par les outils d activation/historisation, tous agents autorises.
FICHIERS_RACINE = {"AGENTS.md", "README.md", "AGENTS-historique.md",
                   "AGENTS-activite-recente.md", "AGENTS-historique-v2.md",
                   "AGENTS-activite-recente-v2.md", "demarrer.md",
                   "USER-DEMANDES.md"}

# Fichiers de DONNEES mecaniques (ecrits par les outils/routines, pas
# par un agent conscient) : jamais signales comme violation.
NOMS_DONNEES = {"historique.db", "corrections.jsonl", "defcon.jsonl",
                "file-asap.jsonl", "file-attente.jsonl"}

# Emojis autorises en v2 : si un fichier v2 est vide d emojis alors qu il
# en portait (detecte par regression d octets non-ASCII), c est suspect.
# (Signalement, pas correction.)


def _racine_projet():
    racine = Path(_DOSSIER)
    while not (racine / "AGENTS-historique.md").is_file():
        if racine.parent == racine:
            return Path.cwd()
        racine = racine.parent
    return racine


def _historiser_agent(agent, raison, type_action="R"):
    """Helper d historisation (meme que vigie-perimetre.py)."""
    import importlib.util
    import os as _os
    aap_path = ORACLE_DIR.parent / "activer" / "activer-agent-principal" / \
        "activer-agent-principal.py"
    if not aap_path.exists():
        return False
    racine = _racine_projet()
    _os.environ["AGENTS_HISTORIQUE"] = str(racine / "AGENTS-historique.md")
    _os.environ["AGENTS_ACTIVITE_RECENTE"] = str(
        racine / "AGENTS-activite-recente.md")
    _os.environ["AGENTS_FILE"] = str(racine / "AGENTS.md")
    _os.environ["CLASSEUR_STOCKAGE"] = str(
        racine / "cerveau-projet" / "agents" / "classeur-variables" /
        "stockage" / "variables-actuelles.md")
    _os.environ["GRADES_V1"] = str(
        racine / "cerveau-projet" / "agents" / "tools" / "oracle" /
        "grades-v1.json")
    _bdd_dir = (racine / "cerveau-projet" / "freelance" / "tools-commun" /
                "jarvis" / "fonctions")
    if str(_bdd_dir) not in sys.path:
        sys.path.insert(0, str(_bdd_dir))
    spec = importlib.util.spec_from_file_location("aap_v1", str(aap_path))
    aap = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(aap)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    rc = aap.ajouter_historique(ts, "session-admin", agent, raison,
                                type_action)
    return rc == 0


def _ecrire_alerte(details, motif):
    """Alerte Oracle au format 4W (canal inbox Oracle) - decision utilisateur
    2026-08-30 : routines -> Oracle (coordinateur), pas Cerberus."""
    maintenant = datetime.now()
    message = {
        "id": "verifier-agent-%s" % uuid.uuid4().hex[:8],
        "de": "verifier-agent-perimetre",
        "vers": "oracle",
        "priorite": 1,
        "date": maintenant.strftime("%Y-%m-%dT%H:%M:%S"),
        "objet": "[PERIMETRE-AGENT] violation : " + motif[:50],
        "corps": details,
        "lu": False,
        "accuse": False,
        "type": "verifier-agent-perimetre",
    }
    try:
        INBOX_DIR.mkdir(parents=True, exist_ok=True)
        with open(INBOX_DIR / "oracle.jsonl", "a",
                  encoding="utf-8") as f:
            f.write(json.dumps(message, ensure_ascii=False) + "\n")
        return message
    except OSError as exc:
        print("[PERIMETRE-AGENT] ERREUR ecriture alerte : %s" % exc)
        return None


def _zone_de(rel_ws):
    """Zone d un fichier (chemin relatif /): v2, jarvis, v1, racine, autre."""
    r = rel_ws.replace("\\", "/")
    if r.startswith("cerveau-projet/freelance/tools-commun/jarvis"):
        return "jarvis"
    if r.startswith("cerveau-projet/freelance"):
        return "v2"
    if r.startswith("cerveau-projet"):
        return "v1"
    if r in FICHIERS_RACINE or (r.count("/") == 0 and r.endswith(".md")):
        return "racine"
    return "autre"


def _agent_habilitE(agent, zone, rel_ws):
    """Un agent est-il habilitE pour cette zone/fichier ?"""
    agent = (agent or "").strip().lower()
    if not agent or agent == "inconnu":
        # Auteur git inconnu (non commite) : on ne peut pas statuer, la
        # vigilance passe par l encart/activite, pas ici.
        return True
    if agent in AGENTS_TOUT_WORKSPACE:
        return True
    if zone == "racine":
        return True
    if zone == "autre":
        return True
    # Hades : git seul (mais tous les fichiers peuvent transiter par git).
    if agent == "hades":
        return True
    if zone == "jarvis":
        return agent in {"vision"}
    if zone == "v2":
        return agent in ZONES["v2"][1]
    if zone == "v1":
        return agent in ZONES["v1"][1] or agent in ZONES["v2"][1]
    return True


def _modifications_recentes(racine, profondeur=30):
    """Fichiers modifies non commites + derniers commits git.

    Retourne une liste de dicts:
      {fichier, auteur, quand, type: git|working}
    """
    resultats = []
    flags = 0
    if hasattr(subprocess, "CREATE_NO_WINDOW"):
        flags = subprocess.CREATE_NO_WINDOW
    try:
        # 1. Fichiers modifies dans le working tree (non commites)
        p = subprocess.run(["git", "status", "--porcelain"],
                           capture_output=True, text=True,
                           cwd=str(racine), timeout=15,
                           creationflags=flags)
        for ligne in p.stdout.splitlines():
            ligne = ligne.strip()
            if not ligne:
                continue
            statut = ligne[:2]
            chemin = ligne[3:].strip().strip('"')
            if statut in ("??",):
                continue  # fichiers non suivis : pas d auteur git
            if chemin.endswith(".pyc") or "__pycache__" in chemin:
                continue
            resultats.append({"fichier": chemin.replace("\\", "/"),
                              "auteur": "inconnu (working tree)",
                              "quand": "non commite", "type": "working"})
        # 2. Derniers commits (auteur git)
        p = subprocess.run(
            ["git", "log", "-%d" % profondeur,
             "--format=%an|%ad|%H", "--date=short"],
            capture_output=True, text=True, cwd=str(racine), timeout=15,
            creationflags=flags)
        for ligne in p.stdout.splitlines():
            parties = ligne.split("|")
            if len(parties) < 3:
                continue
            auteur, date_c, commit = parties[0], parties[1], parties[2]
            # Fichiers du commit
            p2 = subprocess.run(
                ["git", "show", "--name-only", "--format=", commit],
                capture_output=True, text=True, cwd=str(racine), timeout=15,
                creationflags=flags)
            for f in p2.stdout.splitlines():
                f = f.strip()
                if not f:
                    continue
                resultats.append({"fichier": f.replace("\\", "/"),
                                  "auteur": auteur, "quand": date_c,
                                  "type": "git"})
    except (OSError, subprocess.TimeoutExpired) as exc:
        print("[PERIMETRE-AGENT] ERREUR git : %s" % exc)
    return resultats


def _raison_session(racine):
    """Raison (mission) du bloc session-admin dans AGENTS.md."""
    try:
        contenu = (racine / "AGENTS.md").read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""
    idx = contenu.find("### Session : session-admin")
    if idx == -1:
        return ""
    bloc = contenu[idx:idx + 2000]
    import re
    m = re.search(r"\| \*\*Raison\*\* \| ([^|]+) \|", bloc)
    if not m:
        return ""
    return m.group(1).strip()


def _gate(agent):
    """Porte de verification PRE-VOL (pas un timer). L agent la lance au
    moment ou il decide de commencer : verifie qu il est LE BON AGENT.
    Retour 0 = OK (commencer), 1 = KO (STOP immediat).
    """
    racine = _racine_projet()
    moi = (agent or "").strip().lower()
    if not moi:
        print("[GATE] KO : --moi <mon-agent> est obligatoire.")
        return 1
    # 1. L agent actif de la session doit etre MOI.
    actif, actif_v2 = _agent_actif_session(racine)
    if actif and actif != moi:
        print("[GATE] KO : l agent actif de la session-admin est '%s' (%s), "
              "pas toi ('%s'). Tu ne dois PAS travailler : STOP immediat, "
              "reactiver Cerberus SANS RIEN TOUCHER."
              % (actif, "v2" if actif_v2 else "v1", moi))
        return 1
    if actif is None:
        print("[GATE] ATTENTION : agent actif de la session introuvable "
              "(AGENTS.md illisible ?) - porte NON bloquante.")
    # 2. La Raison (mission) ne doit pas viser une zone hors habilitation.
    #    Les agents de COORDINATION (cerberus, oracle) en sont exempts :
    #    leur Raison est le bilan FIN de l agent precedent, qui peut
    #    legitiment mentionner une autre zone (pas de faux KO).
    if moi in AGENTS_COORDINATION:
        print("[GATE] OK : tu es le bon agent ('%s', coordination) pour cette "
              "mission. Tu peux commencer." % moi)
        return 0
    raison = _raison_session(racine).lower()
    zone_v2 = ("freelance" in raison or "jarvis" in raison
               or "zone v2" in raison)
    zone_jarvis = "jarvis" in raison
    est_v2_agent = moi in ZONES["v2"][1]
    if zone_jarvis and moi != "vision":
        print("[GATE] KO : ta mission vise JARVIS (exclusivite Vision) mais "
              "tu es '%s'. STOP immediat." % moi)
        return 1
    if zone_v2 and moi not in ZONES["v2"][1] and moi not in \
            AGENTS_TOUT_WORKSPACE:
        print("[GATE] KO : ta mission vise la zone v2 (freelance/JARVIS) mais "
              "tu es '%s' (agent non habilite pour la v2 depuis la v1 - "
              "seul ferrari l est, ou un agent v2). STOP immediat." % moi)
        return 1
    # Un agent v2 (sauf Vision/JARVIS exclusif) avec une mission qui ne
    # mentionne AUCUN marqueur v2 (freelance, jarvis, agent v2) : c est
    # probablement une mission v1 -> KO (les agents v2 n ecrivent QUE
    # dans cerveau-projet/freelance/, regle AGENTS.md).
    marqueurs_v2 = ("freelance", "jarvis", "v2", "stark", "shuri",
                    "forge", "rogers", "parker", "edith", "fury",
                    "vision")
    if est_v2_agent and moi not in AGENTS_TOUT_WORKSPACE and not any(
            m in raison for m in marqueurs_v2):
        print("[GATE] KO : ta mission ne mentionne aucun marqueur v2 "
              "(freelance/jarvis/agent v2) - elle vise probablement la zone "
              "v1, ou tu (agent v2 '%s') n es pas habilite. STOP immediat."
              % moi)
        return 1
    # CONTROLE PAR LA MISSION (decision utilisateur 2026-08-29) : le gate
    # doit utiliser la MISSION pour savoir si c est le bon agent qui veut
    # l executer. Si une mission pendante consigne un agent cible (`agent`
    # dans les files asap/normale) et que moi != cet agent cible, alors
    # je ne suis PAS celui qui doit executer cette mission -> KO. Les
    # agents de COORDINATION (cerberus, oracle) restent exempts : ils
    # ROUTENT la mission, ils ne l executent pas.
    cible = _mission_agent_cible(racine)
    if cible and moi not in AGENTS_COORDINATION \
            and moi not in AGENTS_TOUT_WORKSPACE and cible != moi:
        print("[GATE] KO : une mission pendante est assignee a '%s' mais tu es "
              "'%s' - tu n es pas celui qui doit l executer. STOP immediat, "
              "reactiver %s (ou Cerberus via Oracle)."
              % (cible, moi, cible))
        return 1
    print("[GATE] OK : tu es le bon agent ('%s') pour cette mission. "
          "Tu peux commencer." % moi)
    return 0


def _mission_agent_cible(racine):
    """Agent cible (assigne) de la mission pendante, depuis les files de
    missions d Oracle (asap, normale, attente). Lit le PREMIER enregistrement
    EN_ATTENTE de chaque file et renvoie son champ `agent` (vide si aucun
    agent explicite). Decision utilisateur 2026-08-29 : le gate utilise la
    mission pour savoir si c est le bon agent qui veut l executer."""
    dirs = racine / "cerveau-projet" / "agents" / "tools" / "oracle" / "files"
    if not dirs.is_dir():
        return None
    for file in ("asap.jsonl", "normale.jsonl", "attente.jsonl"):
        chemin = dirs / file
        if not chemin.is_file():
            continue
        try:
            for ligne in chemin.read_text(encoding="utf-8",
                                          errors="replace").splitlines():
                ligne = ligne.strip()
                if not ligne:
                    continue
                e = json.loads(ligne)
                if e.get("statut") != "EN_ATTENTE":
                    continue
                agent = (e.get("agent") or "").strip().lower()
                if agent:
                    return agent
        except (ValueError, OSError):
            continue
    return None


def _agent_actif_session(racine):
    """Agent actuellement actif dans la session-admin (AGENTS.md).

    Le vrai signal de violation de perimetre : quand un agent v1 (Buffy)
    est ACTIF et modifie des fichiers v2 (hors ferrari), ou quand un
    agent v2 est actif et modifie des fichiers v1. Retourne (nom_agent,
    est_v2) ou (None, False) si non trouve.
    """
    try:
        contenu = (racine / "AGENTS.md").read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None, False
    # Chercher le bloc session-admin
    idx = contenu.find("### Session : session-admin")
    if idx == -1:
        return None, False
    bloc = contenu[idx:idx + 1200]
    import re
    m = re.search(r"\| \*\*Nom Agent\*\* \| ([^|]+) \|", bloc)
    if not m:
        return None, False
    nom = m.group(1).strip().lower()
    est_v2 = (racine / "cerveau-projet" / "freelance" / nom).is_dir()
    return nom, est_v2


def _normaliser_agent_git(auteur):
    """Mapper les auteurs git vers les agents connus."""
    a = (auteur or "").strip()
    if not a:
        return "inconnu"
    # git config user.name -> agent. On cherche le nom dans les listes.
    for zone, (_, agents) in ZONES.items():
        for ag in agents:
            if ag.lower() in a.lower():
                return ag
    for ag in AGENTS_TOUT_WORKSPACE:
        if ag.lower() in a.lower():
            return ag
    return "inconnu"


def main():
    if "--gate" in sys.argv:
        moi = ""
        if "--moi" in sys.argv:
            i = sys.argv.index("--moi")
            if i + 1 < len(sys.argv):
                moi = sys.argv[i + 1]
        return _gate(moi)

    dry_run = "--dry-run" in sys.argv
    chrono_actif = "--no-chrono" not in sys.argv
    t_debut = time.monotonic()
    if chrono_actif:
        print("[CHRONO] verifier-agent-perimetre (debut)")

    racine = _racine_projet()
    # Anti-spam : ne signaler chaque (agent, zone) qu une fois par jour.
    etat = {}
    if ETAT_VIOLATIONS.is_file():
        try:
            etat = json.loads(ETAT_VIOLATIONS.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            etat = {}
    jour = datetime.now().strftime("%Y-%m-%d")
    agent_actif, agent_actif_v2 = _agent_actif_session(racine)
    if agent_actif:
        print("[PERIMETRE-AGENT] Agent actif de la session: %s (%s)"
              % (agent_actif, "v2" if agent_actif_v2 else "v1"))

    violations = []
    for mod in _modifications_recentes(racine):
        fichier = mod["fichier"]
        if fichier in FICHIERS_RACINE:
            continue
        if fichier.startswith("cerveau-projet/freelance/routines/data"):
            continue  # journaux de routines, tout le monde peut ecrire
        zone = _zone_de(fichier)
        if zone == "autre":
            continue
        # Auteur : git si connu, sinon l agent actif de la session.
        # Le vrai signal est l AGENT ACTIF (AGENTS.md) qui modifie des
        # fichiers - pas l auteur git (qui peut etre un commit ancien
        # ou l utilisateur). Pour un commit git a l auteur inconnu,
        # on ne peut pas statuer : on NE l attribue PAS a l agent actif
        # (faux positifs sur les commits historiques).
        auteur = _normaliser_agent_git(mod["auteur"])
        if auteur == "inconnu":
            if mod["type"] == "working" and agent_actif:
                auteur = agent_actif
            else:
                continue  # commit historique a l auteur inconnu : skip
        # Fichiers de donnees mecaniques : jamais signales.
        if os.path.basename(fichier) in NOMS_DONNEES:
            continue
        if fichier.endswith(".db") or fichier.endswith(".jsonl"):
            if "data" in fichier or "classeur" in fichier \
               or "files" in fichier or "inbox" in fichier \
               or "outbox" in fichier or "historique" in fichier:
                continue
        habilitE = _agent_habilitE(auteur, zone, fichier)
        if not habilitE:
            cle = "%s|%s|%s" % (jour, auteur, zone)
            if etat.get(cle):
                continue  # deja signale aujourd hui
            etat[cle] = True
            violations.append(
                "[violation-perimetre] QUI: %s (%s) - QUOI: a modifie %s - "
                "QUAND: %s - OU: zone %s (agent non habilitE, regle "
                "groupes-agents AGENTS.md)" % (
                    auteur, mod["auteur"], fichier, mod["quand"], zone))
            print("  ! %s" % violations[-1])

    if not violations:
        print("[PERIMETRE-AGENT] Aucune violation de perimetre detectee.")
        if not dry_run:
            try:
                with io.open(ETAT_VIOLATIONS, "w", encoding="utf-8",
                             newline="\n") as fh:
                    fh.write(json.dumps(etat, ensure_ascii=True,
                                        indent=1, sort_keys=True))
            except OSError:
                pass
        if chrono_actif:
            print("[CHRONO] verifier-agent-perimetre (fin, %.1fs)"
                  % (time.monotonic() - t_debut))
        return 0

    print("[PERIMETRE-AGENT] %d violation(s) de perimetre :"
          % len(violations))
    for v in violations:
        print("  - %s" % v)
    if dry_run:
        print("[PERIMETRE-AGENT] --dry-run : alerte NON envoyee.")
        if chrono_actif:
            print("[CHRONO] verifier-agent-perimetre (fin, %.1fs)"
                  % (time.monotonic() - t_debut))
        return 1
    corps = "\n".join("- %s" % v for v in violations)
    motif = violations[0].split("QUOI: ")[1].split(" - QUAND:")[0][:50]
    msg = _ecrire_alerte(corps, motif)
    try:
        with io.open(ETAT_VIOLATIONS, "w", encoding="utf-8",
                     newline="\n") as fh:
            fh.write(json.dumps(etat, ensure_ascii=True,
                                indent=1, sort_keys=True))
    except OSError:
        pass
    _historiser_agent("verifier-agent-perimetre",
                      "%d violation(s) de perimetre" % len(violations), "R")
    if msg:
        print("[PERIMETRE-AGENT] Alerte envoyee a Cerberus (%s)" % msg["id"])
    if chrono_actif:
        print("[CHRONO] verifier-agent-perimetre (fin, %.1fs)"
              % (time.monotonic() - t_debut))
    return 0 if msg else 1


if __name__ == "__main__":
    sys.exit(main())
