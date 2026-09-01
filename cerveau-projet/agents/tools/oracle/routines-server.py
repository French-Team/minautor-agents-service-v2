#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
routines-server.py -- DAEMON RESIDENT des routines v1 (session-admin).

Equivalent v1 du routines-server v2 (decision utilisateur 2026-08-27 :
on s inspire de la v2 mais on ne recupere pas son code - 2 univers
distincts). Le daemon tick les routines du manifest en boucle,
independamment des invocations ponctuelles des outils v1.

Lance par oracle-demarrage.py demarrage (detache, survit a la console) ;
arrete par oracle-demarrage.py arret.

Usage:
    python3 routines-server.py --boucle [--intervalle N]

Boucle : toutes les N secondes (defaut 30), executer les routines du
manifest dont l intervalle est ecoule. L etat de la derniere execution
est conserve dans routines/etat-executions.json (persistant entre les
tic et les redemarrages du daemon).

Proprietaire : Vulcain (outils v1)
Version : 0.2.0
Statut : ebauche
"""

import io
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

VERSION = "0.2.1"

_ORACLE_DIR = Path(__file__).parent
ROUTINES_DIR = _ORACLE_DIR / "routines"
MANIFEST = ROUTINES_DIR / "manifest.json"
ETAT = ROUTINES_DIR / "etat-executions.json"
PID_FILE = _ORACLE_DIR / "routines-server.pid"
# Production: arret apres 30 minutes d inactivite du dernier agent actif.
INACTIVITE_MAX_SECONDES = 30 * 60
INACTIVITE_ETAT = _ORACLE_DIR / "session-admin-inactivite.json"
AGENTS_FILE = _ORACLE_DIR.parents[2] / "AGENTS.md"


def _maintenant_iso():
    """Horodatage ISO local (AAAA-MM-JJTHH:MM:SS)."""
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def charger_etat():
    if ETAT.exists():
        try:
            return json.loads(ETAT.read_text(encoding="utf-8"))
        except ValueError:
            return {}
    return {}


def sauver_etat(etat):
    ROUTINES_DIR.mkdir(parents=True, exist_ok=True)
    with io.open(ETAT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(etat, ensure_ascii=True))


def secondes_ecoulees(iso_derniere):
    """Secondes ecoulees depuis un horodatage ISO. Tolerant : si
    illisible, on considere 'longtemps' (la routine s execute)."""
    try:
        derniere = datetime.strptime(iso_derniere, "%Y-%m-%dT%H:%M:%S")
        return (datetime.now() - derniere).total_seconds()
    except (ValueError, TypeError):
        return 10 ** 9


def charger_manifest():
    if not MANIFEST.is_file():
        return []
    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        return data.get("routines_surveillance", [])
    except ValueError:
        return []


def executer_routine(routine):
    """Executer une routine du manifest (script enfant, timeout 60s).
    Le script est cherche dans routines/ (chemin relatif au manifest)."""
    nom = routine.get("nom", "?")
    script = ROUTINES_DIR / routine.get("script", "")
    if not script.is_file():
        print("[ROUTINES-SERVER] routine '%s' : script introuvable %s"
              % (nom, script), flush=True)
        return False
    try:
        # CREATE_NO_WINDOW (Windows) : aucune fenetre cmd qui clignote
        # quand une routine est lancee depuis le daemon (meme principe
        # que la v2 fonctions/routines.py). 0 sur POSIX = inoffensif.
        flags_no_window = 0
        if hasattr(subprocess, "CREATE_NO_WINDOW"):
            flags_no_window = subprocess.CREATE_NO_WINDOW
        proc = subprocess.run(
            [sys.executable, str(script)],
            timeout=60, capture_output=True, text=True,
            cwd=str(ROUTINES_DIR), creationflags=flags_no_window)
        if proc.returncode == 0:
            sortie = (proc.stdout or "").strip().splitlines()
            if sortie:
                print("[ROUTINES-SERVER] %s : %s" % (nom, sortie[-1]),
                      flush=True)
            return True
        print("[ROUTINES-SERVER] routine '%s' : echec rc=%d : %s"
              % (nom, proc.returncode, (proc.stderr or "").strip()[:120]),
              flush=True)
        return False
    except subprocess.TimeoutExpired:
        print("[ROUTINES-SERVER] routine '%s' : timeout 60s" % nom,
              flush=True)
        return False


def tic():
    """Un tic du daemon : executer les routines dont la prochaine execution
    est atteinte. Tolerant : une erreur ne tue jamais le daemon.

    Chaque routine utilise uniquement son intervalle fixe declare dans
    manifest.json. Aucun decalage aleatoire n est ajoute."""
    routines = charger_manifest()
    if not routines:
        return
    etat = charger_etat()
    maintenant = _maintenant_iso()
    for routine in routines:
        nom = routine.get("nom", "?")
        if not routine.get("actif", True):
            continue
        intervalle = int(routine.get("intervalles_secondes", 300))
        prochaine = etat.get(nom, "")
        # L etat stocke la prochaine execution selon l intervalle fixe.
        echu = False
        if not prochaine:
            echu = True
        else:
            secondes = secondes_ecoulees(prochaine)
            # date passee ou egale a maintenant -> echu ; date future -> attendre.
            echu = secondes >= 0
        if echu:
            try:
                if executer_routine(routine):
                    # Prochaine execution : intervalle fixe, sans jitter.
                    dproch = datetime.now() + timedelta(seconds=intervalle)
                    etat[nom] = dproch.strftime("%Y-%m-%dT%H:%M:%S")
            except Exception as exc:
                print("[ROUTINES-SERVER] ERREUR routine '%s' : %s"
                      % (nom, exc), flush=True)
    sauver_etat(etat)


def _historiser_demarrage():
    try:
        oracle_cli = _ORACLE_DIR / "oracle.py"
        subprocess.run([sys.executable, str(oracle_cli), "historiser", "routines-server",
                        "DEMARRAGE SERVEUR: routines-server actif pid=%d" % os.getpid()],
                       timeout=30, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass


def _dernier_agent_actif():
    try:
        texte = AGENTS_FILE.read_text(encoding="utf-8")
    except OSError:
        return "cerberus"
    actif = None
    dans_session = False
    for ligne in texte.splitlines():
        if ligne.startswith("### Session :"):
            dans_session = "session-admin" in ligne.lower()
        elif dans_session and ligne.startswith("| **Agent actif** |"):
            actif = ligne.split("|", 2)[1].strip(" *")
            break
    return actif or "cerberus"


def _dernier_agent_a_agit():
    try:
        activite = AGENTS_FILE.parent / "AGENTS-activite-recente.md"
        lignes = activite.read_text(encoding="utf-8").splitlines()
    except OSError:
        return time.time()
    agent = _dernier_agent_actif().lower()
    for ligne in lignes:
        if not ligne.startswith("| ") or "| Grade |" in ligne or "|---" in ligne:
            continue
        c = [x.strip() for x in ligne.split("|")]
        if len(c) >= 9 and c[2].lower() == agent:
            try:
                return datetime.now().replace(hour=int(c[8][0:2]), minute=int(c[8][3:5]), second=int(c[8][6:8]), microsecond=0).timestamp()
            except (ValueError, IndexError):
                return time.time()
    return time.time()


def _demande_user_recente():
    try:
        data = json.loads(INACTIVITE_ETAT.read_text(encoding="utf-8"))
        return float(data.get("derniere_demande_user", 0))
    except (OSError, ValueError, TypeError):
        return time.time()


def _arret_inactivite():
    if time.time() - _dernier_agent_a_agit() < INACTIVITE_MAX_SECONDES:
        return False
    try:
        oracle_cli = _ORACLE_DIR / "oracle.py"
        subprocess.run([sys.executable, str(oracle_cli), "historiser", "oracle",
                        "ARRET AUTO: dernier agent actif inactif >= 30 min"],
                       timeout=30, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass
    # routines-server ne tue pas son parent: Oracle orchestre l arret global.
    # Il supprime uniquement son propre marqueur et termine proprement.
    try:
        PID_FILE.unlink()
    except OSError:
        pass
    print("[ROUTINES-SERVER] arret automatique: dernier agent actif inactif >= 30 min", flush=True)
    return True


def boucler(intervalle_secondes):
    """Boucle residente avec arret apres 30 min sans demande utilisateur."""
    try:
        PID_FILE.write_text(str(os.getpid()), encoding="utf-8")
    except OSError:
        pass
    print("[ROUTINES-SERVER] DEMARRAGE SERVEUR: daemon lance (tic toutes les %ds, pid %d)"
          % (intervalle_secondes, os.getpid()), flush=True)
    _historiser_demarrage()
    try:
        while True:
            if _arret_inactivite():
                return
            try:
                tic()
            except Exception as exc:
                print("[ROUTINES-SERVER] ERREUR tic : %s" % exc, flush=True)
            time.sleep(intervalle_secondes)
    finally:
        try:
            PID_FILE.unlink()
        except OSError:
            pass


def main():
    if "--boucle" not in sys.argv:
        print("usage : python3 routines-server.py --boucle [--intervalle N]")
        return 2
    intervalle = 30
    if "--intervalle" in sys.argv:
        try:
            intervalle = int(sys.argv[sys.argv.index("--intervalle") + 1])
        except (ValueError, IndexError):
            pass
    boucler(intervalle)
    return 0


if __name__ == "__main__":
    sys.exit(main())
