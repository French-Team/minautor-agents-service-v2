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
from datetime import datetime
from pathlib import Path

VERSION = "0.2.0"

_ORACLE_DIR = Path(__file__).parent
ROUTINES_DIR = _ORACLE_DIR / "routines"
MANIFEST = ROUTINES_DIR / "manifest.json"
ETAT = ROUTINES_DIR / "etat-executions.json"
PID_FILE = _ORACLE_DIR / "routines-server.pid"


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
    """Un tic du daemon : executer les routines dont l intervalle est
    ecoule. Tolerant : une erreur ne tue jamais le daemon."""
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
        derniere = etat.get(nom, "")
        if not derniere or secondes_ecoulees(derniere) >= intervalle:
            try:
                if executer_routine(routine):
                    etat[nom] = maintenant
            except Exception as exc:
                print("[ROUTINES-SERVER] ERREUR routine '%s' : %s"
                      % (nom, exc), flush=True)
    sauver_etat(etat)


def boucler(intervalle_secondes):
    """Boucle residente du daemon v1 : tic toutes les N secondes.
    Le processus tourne en permanence (lance par oracle-demarrage)."""
    try:
        PID_FILE.write_text(str(os.getpid()), encoding="utf-8")
    except OSError:
        pass
    print("[ROUTINES-SERVER] daemon lance (tic toutes les %ds, pid %d)"
          % (intervalle_secondes, os.getpid()), flush=True)
    try:
        while True:
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
