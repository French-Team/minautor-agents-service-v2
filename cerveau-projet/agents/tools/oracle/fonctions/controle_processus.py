# -*- coding: ascii -*-
# -*- coding: us-ascii -*-
# -*- coding: us-ascii -*-
"""fonctions/controle-processus.py - Controle des processus fantomes v1.

Le systeme v1 doit tourner avec UNE SEULE instance par serveur :
  - oracle-server.py        (hub de coordination)   -> oracle-server.pid
  - routines-server.py v1   (daemon routines v1)    -> routines-server.pid
Lancement suppose : 1 parent de demarrage (oracle-demarrage) qui demarre
exactement ces 2 serveurs => 2 PID residants (le parent s arrete apres
le lancement). Tout processus supplementaire correspondant au meme script
est un PROCESSUS FANTOME.

Ce module LISTE les processus reels par ligne de commande (sans dependance
externe ; wmic/tasklist sont evites au profit de PowerShell uniquement sur
Windows), compare au PID attendu (pid file) et retourne :
  - le processus officiel (celui du pid file, vivant) par serveur
  - les doublons (processus fantomes) : autres instances du meme script
  - les serveurs morts : pid file absent ou PID decede

Lecture seule : ne modifie JAMAIS les processus. La decision d'arreter un
fantome revient a l'appelant (Jamais un auto-kill silencieux ici).
Proprietaire : Oracle (outils v1, session-admin).
Version : 0.1.0
"""

import json
import os
import subprocess
import sys
from pathlib import Path

# Racine du projet (detectee dynamiquement)
_d = os.path.dirname(os.path.abspath(__file__))  # .../oracle/fonctions
_d = os.path.dirname(_d)                          # .../oracle
while not os.path.isfile(os.path.join(_d, "AGENTS.md")):
    _p = os.path.dirname(_d)
    if _p == _d:
        break
    _d = _p
RACINE = Path(_d)
ORACLE_DIR = RACINE / "cerveau-projet" / "agents" / "tools" / "oracle"

VERSION = "0.1.0"

# Signature de chaque serveur v1 : (nom, sous-chaine unique du script,
# nom du pid file). La sous-chaine doit matcher la fin de la ligne de
# commande (chemin relatif ou absolu vers le .py).
SERVEURS = [
    {
        "nom": "oracle-server",
        "script": "oracle-server.py",
        "pid_file": ORACLE_DIR / "oracle-server.pid",
    },
    {
        "nom": "routines-server-v1",
        # Sous-chaine distinctive : la v1 vit dans agents/tools/oracle/
        # (la v2 dans freelance/tools-commun/routines-server/ partage
        # le meme basename routines-server.py).
        "script": "oracle/routines-server.py",
        "pid_file": ORACLE_DIR / "routines-server.pid",
    },
]


def _lister_processus_windows():
    """Lister les processus python (pid, cmdline) via PowerShell.
    Retourne liste de dict {pid:int, cmdline:str}. Vide si indisponible."""
    try:
        script_ps = (
            "Get-CimInstance Win32_Process -Filter \"Name like 'python%'\" | "
            "ForEach-Object { \"$($_.ProcessId)|$($_.CommandLine)\" }"
        )
        p = subprocess.run(
            ["powershell", "-NoProfile", "-Command", script_ps],
            capture_output=True, text=True, timeout=20,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        if p.returncode != 0:
            return []
        resultat = []
        for ligne in p.stdout.splitlines():
            ligne = ligne.strip()
            if not ligne or "|" not in ligne:
                continue
            pid_s, _, cmdline = ligne.partition("|")
            try:
                resultat.append({"pid": int(pid_s), "cmdline": cmdline})
            except ValueError:
                continue
        return resultat
    except (OSError, subprocess.TimeoutExpired):
        return []


def _lister_processus_posix():
    """Listing PID + cmdline sur POSIX via ps (fallback)."""
    try:
        p = subprocess.run(
            ["ps", "-eo", "pid=", "args="],
            capture_output=True, text=True, timeout=20)
        resultat = []
        for ligne in p.stdout.splitlines():
            ligne = ligne.strip()
            parts = ligne.split(None, 1)
            if len(parts) != 2:
                continue
            try:
                resultat.append({"pid": int(parts[0]),
                                 "cmdline": parts[1]})
            except ValueError:
                continue
        return resultat
    except (OSError, subprocess.TimeoutExpired):
        return []


def lister_processus():
    """Tous les processus python reels (pid, cmdline). Plateforme-auto."""
    if os.name == "nt":
        return _lister_processus_windows()
    return _lister_processus_posix()


def _pid_file_valide(pid_file):
    """PID stocke en entiers, vivant ? Retourne int ou None."""
    if not pid_file or not pid_file.is_file():
        return None
    try:
        pid = int(pid_file.read_text(encoding="utf-8").strip())
    except (ValueError, OSError):
        return None
    if os.name == "nt":
        try:
            import ctypes
            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            kernel32 = ctypes.windll.kernel32
            h = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION,
                                     False, pid)
            if h:
                kernel32.CloseHandle(h)
                return pid
            return None
        except Exception:
            return None
    try:
        os.kill(pid, 0)
        return pid
    except OSError:
        return None


def _matche_script(cmdline, script):
    """True si la ligne de commande reference le script serveur.
    Normalise les separations de chemin (\\ -> /) puis cherche la
    sous-chaine distinctive du script. Pour oracle-server on cherche le
    nom du .py ; pour la v1 routines on cherche le chemin relatif as
    discriminant (evite le partage de basename avec la v2)."""
    if not cmdline:
        return False
    norm = cmdline.replace('\\', '/')
    motif = script
    if script == 'oracle-server.py':
        # uniquement par nom de fichier (aucune v2 oracle-server)
        return script in norm
    return script in norm


def verifier():
    """Controle complet des processus v1.
    Retourne resume dict :
      {
        "serveurs": [ {nom, pid_officiel, doublons:[pid...], mort:bool} ],
        "fantomes_totaux": int,
        "total_processus_python": int,
        "ok": bool   # True si 1 instance par serveur, aucun fantome,
                     # aucun serveur mort
      }
    """
    processus = lister_processus()
    resume = {
        "serveurs": [],
        "fantomes_totaux": 0,
        "total_processus_python": len(processus),
        "ok": True,
        "erreurs_listing": not processus and os.name == "nt",
    }
    # NB (correction 2026-08-29) : AUCUNE auto-exclusion par pid.
    # Le harnais est execute DANS le daemon oracle-server (meme pid) :
    # exclure os.getpid() retirait l instance officielle du daemon lui-
    # meme -> faux positif 'SERVEUR MORT' a chaque tic (18 alertes
    # [FANTOMES] spammees). Le matcher par ligne de commande suffit :
    # une invocation CLI (oracle.py controle-processus) ne matche jamais
    # un script serveur (oracle-server.py / routines-server.py).
    for s in SERVEURS:
        script = s["script"]
        nom = s["nom"]
        pid_officiel = _pid_file_valide(s["pid_file"])
        # Toutes les instances reelles du script
        instances = [p["pid"] for p in processus
                     if _matche_script(p.get("cmdline", ""), script)]
        # Le serveur est MORT s il n existe AUCUNE instance reelle.
        mort = not instances
        doublons = []
        if instances and pid_officiel in instances:
            instances.remove(pid_officiel)
        # Reste apres le PID officiel = processus fantomes (doublons)
        doublons = sorted(instances)
        if mort or doublons:
            resume["ok"] = False
        resume["serveurs"].append({
            "nom": nom,
            "pid_officiel": pid_officiel,
            "doublons": doublons,
            "mort": mort,
        })
        resume["fantomes_totaux"] += len(doublons)
    return resume


def formatter(resume):
    """Representation lisible du controle."""
    lignes = ["=== CONTROLE PROCESSUS v1 (Oracle) ==="]
    lignes.append("  Processus python reels : %d"
                  % resume["total_processus_python"])
    for s in resume["serveurs"]:
        statut = "OK" if not s["mort"] and not s["doublons"] else "PROBLEME"
        seg = "  [%s] %s : pid officiel=%s" % (
            statut, s["nom"],
            s["pid_officiel"] or "ABSENT")
        if s["mort"]:
            seg += " | SERVEUR MORT (aucune instance)"
        if s["doublons"]:
            seg += " | FANTOMES: " + ",".join(str(p) for p in s["doublons"])
        lignes.append(seg)
    if resume["fantomes_totaux"]:
        lignes.append("  !! %d processus fantome(s) detecte(s)"
                      % resume["fantomes_totaux"])
    elif dict_get(resume, "ok"):
        lignes.append("  Aucun processus fantome - 1 instance par serveur.")
    return "\n".join(lignes)


def dict_get(d, k, default=None):
    return d.get(k, default) if isinstance(d, dict) else default


if __name__ == "__main__":
    r = verifier()
    print(formatter(r))
    sys.exit(0 if r.get("ok", False) else 1)