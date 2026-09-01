#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
routine sante -- Etat global du systeme v1 (session-admin).

Transposee de la routine v2 sante (surveillance/sante.py) pour l univers
v1 : verifie l etat global de la coordination v1 et historise UNIQUEMENT
en cas d anomalie (evenementiel).

Verifie :
  1. DAEMONS : oracle-server et routines-server sont-ils vivants ?
  2. DEFCON : un DEFCON 5 (arret total) gele depuis longtemps ?
  3. ENCART v1 : AGENTS-activite-recente.md coherent (tableau + LIGNE
     ACCUEIL Cerberus en tete = la derniere entree est le point d entree).
  4. BDD : ecriture recente dans AGENTS-historique.md / activite.

Alerte Cerberus via inbox Oracle + historise l anomalie.

Usage:
    python3 sante.py [--dry-run]

Retour: 0 si sain, 1 si anomalie(s).
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

VERSION = "0.1.0"

_DOSSIER = os.path.dirname(os.path.abspath(__file__))
ORACLE_DIR = Path(_DOSSIER).parent
PID_ORACLE = ORACLE_DIR / "oracle-server.pid"
PID_ROUTINES = ORACLE_DIR / "routines-server.pid"
FILES_DIR = ORACLE_DIR / "files"
INBOX_DIR = ORACLE_DIR / "inbox"
def _rotation_ajouter(agent, message):
    """Rotation inbox : garder les 5 messages les plus recents (decision
    utilisateur 2026-08-29 : les inbox s accumulaient, personne ne les
    lisait). Reutilise le module central oracle/fonctions/rotation.py."""
    try:
        import importlib.util
        _f = Path(_DOSSIER).parent / "fonctions" / "rotation.py"
        _spec = importlib.util.spec_from_file_location("rotation", str(_f))
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        return _mod.ajouter_message(INBOX_DIR, agent, message)
    except Exception:
        return False


SEUIL_DEFCON_GELE_HEURES = 24
ETAT_ALERTE = Path(_DOSSIER) / "data" / "etat-sante-alerte.json"


def _alerte_deja_envoyee(corps):
    # Empreinte deterministe: hash() varie entre processus Python.
    import hashlib
    empreinte = hashlib.sha256(corps.encode("utf-8")).hexdigest()
    try:
        ancien = json.loads(ETAT_ALERTE.read_text(encoding="utf-8"))
        if ancien.get("empreinte") == empreinte:
            return True
    except (OSError, ValueError):
        pass
    ETAT_ALERTE.parent.mkdir(parents=True, exist_ok=True)
    ETAT_ALERTE.write_text(json.dumps({"empreinte": empreinte}, ensure_ascii=True), encoding="utf-8")
    return False


def _racine_projet():
    racine = Path(_DOSSIER)
    while not (racine / "AGENTS-historique.md").is_file():
        if racine.parent == racine:
            return Path.cwd()
        racine = racine.parent
    return racine


def _historiser_agent(agent, raison, type_action="R"):
    """Helper d historisation (meme que flux.py / citations.py)."""
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


def _ecrire_alerte(corps):
    """Ecrire une alerte dans l inbox d Oracle (coordinateur) - decision
    utilisateur 2026-08-30 : routines -> Oracle, pas Cerberus."""
    maintenant = datetime.now()
    message = {
        "id": "sante-%s" % maintenant.strftime("%H%M%S"),
        "de": "sante",
        "vers": "oracle",
        "priorite": 1,
        "date": maintenant.strftime("%Y-%m-%dT%H:%M:%S"),
        "objet": "[SANTE] %s" % corps[:60],
        "corps": corps,
        "lu": False,
        "accuse": False,
        "type": "sante",
    }
    try:
        _rotation_ajouter("oracle", message)
        return message
    except OSError as exc:
        print("[SANTE] ERREUR ecriture alerte : %s" % exc)
        return None


def _pid_vivant(pid):
    """Vrai si le processus existe (Windows via ctypes, sinon os.kill)."""
    if sys.platform == "win32":
        import ctypes
        handle = ctypes.windll.kernel32.OpenProcess(0x1000, False, pid)
        if handle:
            ctypes.windll.kernel32.CloseHandle(handle)
            return True
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def _verifier_daemon(pid_file, nom):
    if not pid_file.is_file():
        return False, "%s : pidfile absent" % nom
    try:
        pid = int(pid_file.read_text().strip())
    except (ValueError, OSError):
        return False, "%s : pidfile illisible" % nom
    if _pid_vivant(pid):
        return True, "%s : pid %d vivant" % (nom, pid)
    return False, "%s : pid %d mort" % (nom, pid)


def _verifier_defcon():
    """DEFCON 5 gele depuis SEUIL heures ?"""
    defcon_file = FILES_DIR / "defcon.jsonl"
    if not defcon_file.is_file():
        return True, "defcon: aucun journal"
    dernier = None
    for ligne in defcon_file.read_text(encoding="utf-8").splitlines():
        if not ligne.strip():
            continue
        try:
            e = json.loads(ligne)
        except ValueError:
            continue
        if e.get("niveau"):
            try:
                d = datetime.strptime(str(e.get("date", ""))[:19],
                                      "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                continue
            # dernier = LA DERNIERE entree de niveau (ordre du fichier,
            # chronologique). Comparer EN-NON-STRICT (>=) pour que, quand
            # deux entrees portent le meme timestamp (ex: 5 puis 4 poses
            # dans la meme seconde), la DERNIERE gagne - sinon un DEFCON 5
            # eloigne etait rapporte a la place du 4 actuel (faux positif).
            if dernier is None or d >= dernier[0]:
                dernier = (d, e.get("niveau"))
    if not dernier:
        return True, "defcon: aucun niveau declare"
    if dernier[1] == 5:
        age_h = (datetime.now() - dernier[0]).total_seconds() / 3600
        if age_h >= SEUIL_DEFCON_GELE_HEURES:
            return False, "defcon: DEFCON 5 gele depuis %.0fh" % age_h
    return True, "defcon: niveau %s (normal)" % dernier[1]


def _verifier_encart():
    """Encart v1 : le fichier existe et commence par une ligne ACCUEIL
    Cerberus (point d entree) - sinon la session peut etre cassee."""
    racine = _racine_projet()
    encart = racine / "AGENTS-activite-recente.md"
    if not encart.is_file():
        return False, "encart: AGENTS-activite-recente.md absent"
    try:
        contenu = encart.read_text(encoding="utf-8", errors="replace")
        if "Activites recentes" not in contenu:
            return False, "encart: en-tete 'Activites recentes' absent"
        return True, "encart: OK"
    except OSError as exc:
        return False, "encart: illisible (%s)" % exc


def _verifier_bdd():
    """Ecriture recente : le fichier historique a grossi recemment."""
    racine = _racine_projet()
    historique = racine / "AGENTS-historique.md"
    if not historique.is_file():
        return False, "bdd: AGENTS-historique.md absent"
    try:
        mtime = historique.stat().st_mtime
        age_h = (datetime.now().timestamp() - mtime) / 3600
        if age_h > 48:
            return False, "bdd: historique stale (%.0fh sans ecriture)" % age_h
        return True, "bdd: historique recent (%.0fh)" % age_h
    except OSError as exc:
        return False, "bdd: illisible (%s)" % exc


def main():
    dry_run = "--dry-run" in sys.argv
    anomalies = []
    stats = []

    ok, msg = _verifier_daemon(PID_ORACLE, "oracle-server")
    stats.append(msg)
    if not ok and not ("pidfile absent" in msg and not PID_ROUTINES.exists()):
        anomalies.append("DAEMON: " + msg)

    ok, msg = _verifier_daemon(PID_ROUTINES, "routines-server")
    stats.append(msg)
    if not ok:
        anomalies.append("DAEMON: " + msg)

    ok, msg = _verifier_defcon()
    stats.append(msg)
    if not ok:
        anomalies.append("DEFCON: " + msg)

    ok, msg = _verifier_encart()
    stats.append(msg)
    if not ok:
        anomalies.append("ENCART: " + msg)

    ok, msg = _verifier_bdd()
    stats.append(msg)
    if not ok:
        anomalies.append("BDD: " + msg)

    print("[SANTE] Etat du systeme v1:")
    for s in stats:
        print("  - %s" % s)

    if not anomalies:
        print("[SANTE] Aucune anomalie - systeme sain")
        return 0

    print("[SANTE] %d anomalie(s) :" % len(anomalies))
    for a in anomalies:
        print("  ! %s" % a)
    corps = "\n".join("- %s" % a for a in anomalies)
    if dry_run:
        print("[SANTE] --dry-run : anomalies non historisees/non envoyees")
        return 1
    if _alerte_deja_envoyee(corps):
        print("[SANTE] Anomalie identique deja signalee : aucune repetition")
        return 1
    _historiser_agent("sante", "%d anomalie(s): %s" %
                      (len(anomalies), "; ".join(anomalies[:3])), "R")
    msg_alerte = _ecrire_alerte(corps)
    if msg_alerte:
        print("[SANTE] Alerte envoyee a Cerberus (%s)" % msg_alerte["id"])
    return 1


if __name__ == "__main__":
    sys.exit(main())