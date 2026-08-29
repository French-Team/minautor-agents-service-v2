#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
routine verifier-statuts -- Verifier la colonne Etat et informer Oracle (v1).

Decision utilisateur 2026-08-29 : une routine doit lire les etats (colonne
Etat de l encart v1), informer oracle qui avise en fonction de l etat.
Ici, l etat qui requiert une action est URGENT : on ESCALADE le DEFCON
vers 4 (VALIDATION DES REPARATIONS) et on depose la mission prioritaire.

La routine agit via la CLI OFFICIELLE `oracle.py` (pattern des routines
v1) - c est Oracle qui avise, la routine est son oeil de surveillance.

Actes sur un NOUVEL etat URGENT :
  1. defcon-escaler 4 (degradation : URGENT -> DEFCON 4). No-op si deja
     au niveau cible ou superieur (defcon.py gere la transition legale).
  2. mission-ajouter --file asap (mission prioritaire) pour la source.
  3. Si un ROUND est EN COURS (agent actif != cerberus) : mettre la
     mission courante en attente (file-attente v1) + instruction
     INTER-ROUND a l agent actif (activer l agent habilite --type ir puis
     reprendre) - transposition de la v2 (activation reelle + mise en
     attente dans une file).

Anti-inondation : on agit UNE SEULE FOIS par entree URGENT (cle
heure|agent, persiste dans routines/data/etat-statuts.json). La trace d
 informat ion est NEUTRE (etat AUTO) pour ne jamais cacher de nouveau
 URGENT.

DEFCON 2 = niveau normal (REPRISE TOTALE, protocole 15 v2). URGENT monte
vers 4 ; la descente (reparations validees) reste faite par
`oracle.py defcon-changer 4 3` puis `3 2`.

Usage:
    python3 verifier-statuts.py [--dry-run]

Retour: 0 si ok, 1 si erreur.
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

VERSION = "0.1.0"

_DOSSIER = os.path.dirname(os.path.abspath(__file__))
ORACLE_DIR = Path(_DOSSIER).parent
INBOX_DIR = ORACLE_DIR / "inbox"
DATA_DIR = Path(_DOSSIER) / "data"
ETAT_STATUTS = DATA_DIR / "etat-statuts.json"

# Sources de surveillance dont un etat URGENT signale une VRAIE anomalie.
SURVEILLANCE = {"encart", "sante", "flux", "live", "vigie-round",
                "vigie-perimetre", "verifier-agent-perimetre"}
# Marqueurs d urgence reelle (les messages neutres type "Demarrage ...
# DEFCON=3" ne doivent PAS declencher d actes).
MARQUEURS_URGENCE = ("ANOMALIE", "NON-ACQUITTE", "DEBORDEMENT", "FANTOME",
                     "VIOLATION", "SERVEUR MORT", "PIDFILE", "DEFCON 5",
                     "DEFCON GELE")


def _est_urgence_reelle(agent, raison):
    """Vrai si l entree URGENT signale une vraie anomalie (et pas une
    trame neutre coloree par un mot-cle, ex: Demarrage ... DEFCON=3)."""
    if (agent or "").lower() in SURVEILLANCE:
        return True
    return any(m in (raison or "").upper() for m in MARQUEURS_URGENCE)


def _racine_projet():
    racine = Path(_DOSSIER)
    while not (racine / "AGENTS-historique.md").is_file():
        if racine.parent == racine:
            return Path.cwd()
        racine = racine.parent
    return racine


def _historiser_agent(agent, raison, type_action="R"):
    """Helper d historisation (meme que flux.py/sante.py). Chemins ABSOLUS."""
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


def _lire_urgents():
    """Lire l encart v1 et renvoyer [(heure, agent, raison)] pour les
    entrees dont la colonne Etat == URGENT. Colonnes :
    Grade | Agent | Executeur | Etat | Secteur | Raison | Heure | id | Type."""
    racine = _racine_projet()
    encart = racine / "AGENTS-activite-recente.md"
    if not encart.is_file():
        return []
    resultats = []
    for ligne in encart.read_text(encoding="utf-8",
                                  errors="replace").split("\n"):
        if not ligne.strip().startswith("| ") or "|---" in ligne \
                or "| Grade |" in ligne:
            continue
        cols = [c.strip() for c in ligne.split("|")]
        # cols = ['', Grade, Agent, Executeur, Etat, Secteur, Raison, Heure, id, Type, '']
        if len(cols) < 9:
            continue
        if cols[4] == "URGENT":
            resultats.append((cols[7], cols[2], cols[6]))
    return resultats


def _lire_manquante():
    if ETAT_STATUTS.is_file():
        try:
            return json.loads(ETAT_STATUTS.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            return {}
    return {}


def _sauver_manquante(manquante):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ETAT_STATUTS.write_text(
        json.dumps(manquante, ensure_ascii=False, indent=1), encoding="utf-8")


def _agent_actif():
    """(agent, date) de la session depuis le classeur, ou (None, None)."""
    racine = _racine_projet()
    classeur = racine / "cerveau-projet" / "agents" / "classeur-variables" / \
        "stockage" / "variables-actuelles.md"
    try:
        contenu = classeur.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return (None, None)
    for ligne in contenu.split("\n"):
        if "profil-session-admin" not in ligne:
            continue
        agent = None
        date = None
        for partie in ligne.split("/"):
            p = partie.strip()
            if p.startswith("agent:"):
                agent = p.split(":", 1)[1].strip()
            elif p.startswith("date:"):
                date = p.split(":", 1)[1].strip()
        return agent, date
    return (None, None)


def _oracle(*args):
    """Executer oracle.py <args> en sous-processus (cwd = racine)."""
    oracle_cli = ORACLE_DIR / "oracle.py"
    try:
        r = subprocess.run([sys.executable, str(oracle_cli)] + list(args),
                           capture_output=True, text=True, timeout=30,
                           cwd=str(_racine_projet()))
        lignes = [l for l in (r.stdout or "").splitlines() if l.strip()]
        return r.returncode == 0, lignes
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, ["ERREUR oracle: %s" % exc]


def _alerte_inbox(agent, objet, corps, type_msg):
    """Deposer une alerte P1 dans inbox/<agent>.jsonl."""
    maintenant = datetime.now()
    message = {
        "id": "verifier-statuts-%s" % maintenant.strftime("%H%M%S"),
        "de": "oracle", "vers": agent, "priorite": 1,
        "date": maintenant.strftime("%Y-%m-%dT%H:%M:%S"),
        "objet": objet, "corps": corps,
        "lu": False, "accuse": False, "type": type_msg,
    }
    try:
        INBOX_DIR.mkdir(parents=True, exist_ok=True)
        with open(INBOX_DIR / ("%s.jsonl" % agent), "a", encoding="utf-8") as f:
            f.write(json.dumps(message, ensure_ascii=False) + "\n")
        return True
    except OSError:
        return False


def _mettre_en_attente(agent):
    """Mettre la mission PRISE de l agent en attente dans la file attente."""
    chemin = ORACLE_DIR / "files" / "asap.jsonl"
    if not chemin.is_file():
        return None
    lignes = [l.strip() for l in chemin.read_text(encoding="utf-8",
                                                  errors="replace").splitlines()
              if l.strip()]
    modif = False
    for i, l in enumerate(lignes):
        try:
            e = json.loads(l)
        except ValueError:
            continue
        if e.get("statut") == "PRISE" and (not agent or e.get("agent") == agent):
            e["statut"] = "EN_ATTENTE"
            lignes[i] = json.dumps(e, ensure_ascii=False)
            modif = True
            break
    if not modif:
        return None
    with open(chemin, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes) + "\n")
    return True


def main():
    dry_run = "--dry-run" in sys.argv
    urgents = _lire_urgents()
    manquante = _lire_manquante()

    nouveaux = []
    for heure, agent, raison in urgents:
        if not _est_urgence_reelle(agent, raison):
            continue
        cle = "%s|%s|%s" % (heure, agent, raison[:40])
        if cle not in manquante:
            nouveaux.append((cle, heure, agent, raison))
            manquante[cle] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    if not nouveaux:
        print("[VERIFIER-STATUTS] Inchange : %d URGENT (dernieres %d gerees, "
              "rien de nouveau)" % (len(urgents), len(manquante)))
        return 0

    nb = len(nouveaux)
    print("[VERIFIER-STATUTS] %d nouvel(s) etat(s) URGENT detecte(s)" % nb)
    for cle, heure, agent, raison in nouveaux:
        print("  - %s | %s | %s" % (heure, agent, raison[:70]))

    if dry_run:
        print("[VERIFIER-STATUTS] --dry-run : rien n est declenche "
              "(escalade DEFCON 4 + mission asap + IR si round en cours).")
        return 0

    # 1. Escalade DEFCON 4 (degradation) - via la CLI officielle.
    premier = nouveaux[0]
    ok, lignes = _oracle("defcon-escaler", "4",
                         "URGENT via verifier-statuts: %s" % premier[3][:90])
    print("  [defcon-escaler] " + " / ".join(lignes[:3]) + " (ok=%s)" % ok)

    # 2. Mission prioritaire (asap) pour chacune, porteuse de l info.
    for cle, heure, agent, raison in nouveaux:
        _oracle("mission-ajouter", "--file", "asap", "--agent", agent or "oracle",
                "ETAT URGENT: %s (source %s, %s)" % (raison[:140], agent, heure))

    # 3. Round en cours -> inter-round (transposition v2).
    agent_actif, date_actif = _agent_actif()
    round_en_cours = bool(agent_actif) and agent_actif.lower() != "cerberus"
    if round_en_cours:
        okm = _mettre_en_attente(agent_actif)
        _oracle("mission-ajouter", "--file", "attente", "--agent", agent_actif,
                "MISE EN ATTENTE (inter-round URGENT) : %s" % premier[3][:120])
        # Instruction IR reelle a l agent actif : activer l agent habilite.
        _alerte_inbox(
            agent_actif,
            "[INTER-ROUND] etat URGENT detecte - traite en inter-round",
            "Un etat URGENT (voir encart) exige une action prioritaire. "
            "DEFCON monte vers 4. Ta mission est mise en attente (file "
            "attente). A ta prochaine case : ACTIVE l agent habilite pour "
            "l URGENT avec --type ir (inter-round), puis reprends ta mission "
            "depuis la file attente.",
            "inter-round")
        print("  [inter-round] round en cours (%s) : mission mise en "
              "attente + instruction IR envoyee" % agent_actif)

    # 4. Informer Cerberus + trace neutre dans l encart (etat AUTO).
    _alerte_inbox(
        "cerberus", "[URGENT] %d etat(s) URGENT traite(s) -> DEFCON 4 + mission asap" % nb,
        "La routine verifier-statuts a escalade le DEFCON vers 4 et depose "
        "les missions asap pour %d etat(s) URGENT."
        % nb + (" Un round etant en cours, une instruction inter-round a ete "
                "envoyee a l agent actif." if round_en_cours else ""),
        "statuts")
    _historiser_agent(
        "verifier-statuts",
        "Relais Oracle : %d etat(s) requerrant action, escalade + mission "
        "placee%s" % (nb, " + inter-round" if round_en_cours else ""), "R")
    # Persister l anti-inondation APRES les actions (dry-run ne persiste pas).
    _sauver_manquante(manquante)
    return 0


if __name__ == "__main__":
    sys.exit(main())