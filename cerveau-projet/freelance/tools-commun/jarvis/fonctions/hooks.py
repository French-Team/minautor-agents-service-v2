# -*- coding: ascii -*-
"""fonctions/hooks.py - UNE tache : piloter le serveur de routines EDITH
(demarrage / arret / etat). Protocole 16 volet 4."""

import os
import signal
import subprocess
import sys
from pathlib import Path

from racine import trouver_racine

RACINE = Path(trouver_racine(__file__))
SERVEUR = RACINE / "cerveau-projet" / "freelance" / "tools-commun" / \
    "routines-server" / "routines-server.py"
PID_FILE = Path(__file__).parent.parent / "routines-server.pid"


def _pid_actuel():
    """PID stocke s'il correspond a un processus vivant, sinon None.
    WINDOWS : os.kill(pid, 0) ne TESTE pas - il TERMINE le processus
    (TerminateProcess). La sonde passe donc par OpenProcess."""
    if not PID_FILE.exists():
        return None
    try:
        pid = int(PID_FILE.read_text(encoding="utf-8").strip())
    except ValueError:
        return None
    if hasattr(os, "name") and os.name == "nt":
        import ctypes
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        kernel32 = ctypes.windll.kernel32
        h = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION,
                                 False, pid)
        if h:
            kernel32.CloseHandle(h)
            return pid
        PID_FILE.unlink(missing_ok=True)
        return None
    try:
        os.kill(pid, 0)  # POSIX : signal 0 = sondes sans tuer
        return pid
    except OSError:
        PID_FILE.unlink(missing_ok=True)
        return None


def _executer_routines_manifest(cle):
    """Executer les scripts declares dans routines_demarrage / routines_arret
    du manifest (D15). Tolerant : une routine qui plante ne bloque pas le
    demarrage/arret. Les routines sont des elements surveilles (grade),
    elles historisent sous leur propre nom (ex: integrite, orphelins)."""
    import json
    try:
        manifest = json.loads(
            (RACINE / "cerveau-projet" / "freelance" / "routines" /
             "manifest.json").read_text(encoding="utf-8"))
        base = RACINE / "cerveau-projet" / "freelance" / "routines"
        for r in manifest.get(cle, []):
            if not r.get("actif", True):
                continue
            script = base / r.get("script", "")
            if script.is_file():
                try:
                    subprocess.run([sys.executable, str(script)],
                                   timeout=120)
                except Exception as e:
                    print("[JARVIS] routine %s (%s) : %s"
                          % (r.get("nom"), script.name, e))
    except Exception as e:
        print("[JARVIS] routines %s : %s" % (cle, e))


def routines_demarrer():
    pid = _pid_actuel()
    if pid:
        print(f"[JARVIS] Serveur de routines DEJA EN MARCHE (pid {pid}).")
        return 0
    # Routines de DEMARRAGE (ex: integrite) : verifier avant de lancer.
    _executer_routines_manifest("routines_demarrage")
    # v0.9.1 : DETACHED_PROCESS - le serveur SURVIT a la fermeture de la
    # console parente. Sorties vers un fichier de log (un crash doit etre
    # VISIBLE, jamais avale par DEVNULL).
    log_dir = RACINE / "cerveau-projet" / "freelance" / "tools-commun" / \
        "routines-server" / "observations"
    log_dir.mkdir(parents=True, exist_ok=True)
    log = open(log_dir / "serveur-log.txt", "a", encoding="utf-8")
    flags = 0
    if hasattr(subprocess, "CREATE_NEW_PROCESS_GROUP"):
        flags |= subprocess.CREATE_NEW_PROCESS_GROUP
    if hasattr(subprocess, "DETACHED_PROCESS"):
        flags |= subprocess.DETACHED_PROCESS
    process = subprocess.Popen(
        [sys.executable, str(SERVEUR), "--boucle"],
        creationflags=flags, stdout=log, stderr=log,
        stdin=subprocess.DEVNULL, close_fds=True)
    PID_FILE.write_text(str(process.pid), encoding="utf-8")
    print(f"[JARVIS] Serveur de routines DEMARRE (pid {process.pid}, "
          f"detache). Log: observations/serveur-log.txt")
    return 0


def routines_arreter():
    pid = _pid_actuel()
    if not pid:
        print("[JARVIS] Serveur de routines deja arrete.")
        return 0
    # Routines d'ARRET (ex: orphelins) : detecter avant de couper.
    _executer_routines_manifest("routines_arret")
    try:
        os.kill(pid, signal.SIGTERM)
        print(f"[JARVIS] Serveur de routines ARRETE (pid {pid}).")
    except OSError as e:
        print(f"[JARVIS] ERREUR d'arret: {e}")
        return 1
    finally:
        PID_FILE.unlink(missing_ok=True)
    return 0


def routines_etat():
    pid = _pid_actuel()
    if pid:
        print(f"[JARVIS] Serveur de routines EN MARCHE (pid {pid}).")
    else:
        print("[JARVIS] Serveur de routines ARRETE.")
    return 0
