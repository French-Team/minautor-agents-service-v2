#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
outils-llm/fermer-session.py - FERMETURE EXCLUSIVE D UNE SESSION LLM.

Ferme la session et ETEINT LES SERVEURS PROPREMENT, avec VERIFICATION
qu'ils sont bien fermes. Ni v1, ni v2 : l'outil vit dans outils-llm/ a la
racine (comme demarrer-llm.py / nettoyer-session.py).

  - session-admin     -> eteint les serveurs de la v1 : oracle-server +
                         routines-server v1 (via oracle-demarrage.py arret).
  - session-freelance -> eteint les serveurs de la v2 : daemon routines
                         JARVIS (via jarvis.py arret).

Chaque serveur est VERIFIE apres l'arret : pidfile supprime ET processus
non vivant (sonde OpenProcess sur Windows). Si un serveur refuse de mourir,
l'outil force (SIGTERM puis taskkill /F) et re-verifie. Puis la fermeture
est historisee (encart + corps + BDD de la session).

Sans question : execute et verifie, comme un soldat.

Usage:
    python3 outils-llm/fermer-session.py <id> <session> [--dry-run]

Exemples:
    python3 outils-llm/fermer-session.py glm5 admin        # v1
    python3 outils-llm/fermer-session.py freebuff freelance  # v2

Options : --help/-h, --version, --dry-run (simule sans rien arreter).
"""

import os
import signal
import subprocess
import sys
import time
from pathlib import Path

VERSION = "0.1.1"
RACINE = Path(__file__).resolve().parent.parent

# Serveurs de la v1 (session-admin) : pidfiles geres par oracle-demarrage.
ORACLE_DIR = RACINE / "cerveau-projet" / "agents" / "tools" / "oracle"
PID_ORACLE = ORACLE_DIR / "oracle-server.pid"
PID_ROUTINES_V1 = ORACLE_DIR / "routines-server.pid"
PID_SUPER_PILOTE = ORACLE_DIR / "super-combos" / "super-pilote.pid"
ORACLE_DEMARRAGE = ORACLE_DIR / "oracle-demarrage.py"

# Serveurs de la v2 (session-freelance) : daemon routines JARVIS.
JARVIS_DIR = RACINE / "cerveau-projet" / "freelance" / "tools-commun" / "jarvis"
PID_ROUTINES_V2 = JARVIS_DIR / "routines-server.pid"
JARVIS_PY = JARVIS_DIR / "jarvis.py"


# ----------------------------------------------------------- verification

def _probe_pid(pid):
    """Le processus <pid> est-il vivant ? (sonde Windows-safe : OpenProcess
    ne TERMINE pas, contrairement a os.kill(pid, 0) sur Windows)."""
    if not pid:
        return False
    if os.name == "nt":
        import ctypes
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        kernel32 = ctypes.windll.kernel32
        h = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if h:
            kernel32.CloseHandle(h)
            return True
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def _lire_pid(pid_file):
    if not pid_file.exists():
        return None
    try:
        return int(pid_file.read_text(encoding="utf-8").strip())
    except (ValueError, OSError):
        return None


def _etat_serveur(pid_file):
    """Etat d un serveur : (pid_avant, ferme_bool, detail)."""
    pid = _lire_pid(pid_file)
    if pid is None:
        return None, True, "pidfile absent (deja arrete)"
    vivant = _probe_pid(pid)
    if not vivant:
        return pid, True, "pid %d : processus non vivant (pidfile restant a nettoyer)" % pid
    return pid, False, "pid %d : ENCORE ACTIF" % pid


def _forcer_arret(pid, nom):
    """Arret force : SIGTERM puis taskkill /F si besoin. Retour (ok, msg)."""
    if not pid:
        return True, "rien a forcer"
    try:
        os.kill(pid, signal.SIGTERM)
    except OSError as exc:
        return False, "SIGTERM echoue (%s)" % exc
    time.sleep(1)
    if not _probe_pid(pid):
        return True, "pid %d arrete par SIGTERM" % pid
    # Windows : force
    try:
        subprocess.run(["taskkill", "/F", "/PID", str(pid)],
                       capture_output=True, text=True, timeout=15)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, "taskkill /F echoue (%s)" % exc
    time.sleep(1)
    if not _probe_pid(pid):
        return True, "pid %d arrete par taskkill /F" % pid
    return False, "pid %d REFUSE de mourir" % pid


def _nettoyer_pidfile(pid_file):
    try:
        pid_file.unlink(missing_ok=True)
    except OSError:
        pass


# ------------------------------------------------------------ arret v1/v2

def _arreter_v1(dry_run):
    """Eteindre oracle-server + routines-server v1. Retour (rapports,
    force_utilise) : force_utilise=True si au moins un serveur a exige un
    arret force (l arret propre n a donc PAS historise "Arret propre")."""
    print("=== ARRET SERVEURS V1 (session-admin) ===")
    rapports = []
    force_utilise = False
    cibles = [("oracle-server", PID_ORACLE), ("routines-server v1", PID_ROUTINES_V1),
              ("super-pilote", PID_SUPER_PILOTE)]
    pid_avant = {nom: _lire_pid(pf) for nom, pf in cibles}
    if dry_run:
        for nom, pf in cibles:
            pid, ferme, detail = _etat_serveur(pf)
            rapports.append((nom, ferme, "[dry-run] " + detail))
        return rapports, force_utilise
    # Arret propre via oracle-demarrage.py. L outil de demarrage peut
    # rencontrer un daemon deja sorti; la verification ci-dessous nettoie
    # alors son pidfile. Les trois cibles sont toujours controlees.
    cmd = [sys.executable, str(ORACLE_DEMARRAGE), "--confirme-doc", "arret"]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60,
                           cwd=str(RACINE))
        for ligne in (r.stdout or "").splitlines():
            print("  [oracle-demarrage] %s" % ligne.strip())
        if r.returncode != 0 and r.stderr:
            print("  [oracle-demarrage-err] %s" % (r.stderr or "")[-500:])
    except (OSError, subprocess.TimeoutExpired) as exc:
        print("  [oracle-demarrage] ERREUR : %s" % exc)
    time.sleep(1)
    for nom, pf in cibles:
        pid, ferme, detail = _etat_serveur(pf)
        if not ferme:
            # arret force
            force_utilise = True
            ok, msg = _forcer_arret(pid, nom)
            _nettoyer_pidfile(pf)
            detail = "force : %s" % msg
            ferme = ok
        elif pid is not None:
            _nettoyer_pidfile(pf)
            detail += " -> pidfile nettoye"
        rapports.append((nom, ferme, detail))
    return rapports, force_utilise


def _arreter_v2(dry_run):
    """Eteindre le daemon routines JARVIS (v2). Retour (rapports,
    force_utilise) : force_utilise=True si le daemon a exige un arret force."""
    print("=== ARRET SERVEURS V2 (session-freelance) ===")
    rapports = []
    force_utilise = False
    cibles = [("routines-server v2 (JARVIS)", PID_ROUTINES_V2)]
    if dry_run:
        for nom, pf in cibles:
            pid, ferme, detail = _etat_serveur(pf)
            rapports.append((nom, ferme, "[dry-run] " + detail))
        return rapports, force_utilise
    # arret propre via jarvis.py arret (resume + daemon routines)
    cmd = [sys.executable, str(JARVIS_PY), "arret", "--session", "session-freelance"]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60,
                           cwd=str(RACINE))
        for ligne in (r.stdout or "").splitlines():
            print("  [jarvis] %s" % ligne.strip())
        if r.returncode != 0 and r.stderr:
            print("  [jarvis-err] %s" % (r.stderr or "")[-500:])
    except (OSError, subprocess.TimeoutExpired) as exc:
        print("  [jarvis] ERREUR : %s" % exc)
    time.sleep(1)
    for nom, pf in cibles:
        pid, ferme, detail = _etat_serveur(pf)
        if not ferme:
            force_utilise = True
            ok, msg = _forcer_arret(pid, nom)
            _nettoyer_pidfile(pf)
            detail = "force : %s" % msg
            ferme = ok
        elif pid is not None:
            _nettoyer_pidfile(pf)
            detail += " -> pidfile nettoye"
        rapports.append((nom, ferme, detail))
    return rapports, force_utilise


# ------------------------------------------------------------ historisation

def _historiser_officiel(raison, session):
    """Historiser la fermeture via la voie OFFICIELLE de la session (jamais
    d'ecriture maison : l encart doit garder SON format et la raison son
    etat). v1 -> oracle.py historiser ; v2 -> jarvis.py historiser.
    N est appele QUE quand l arret propre n a pas pu historiser (arret
    force) : en arret propre, oracle-demarrage/jarvis historisent DEJA
    (ecrire en plus = doublon dans l encart).
    Retour: True si historise, False sinon."""
    if session == "session-admin":
        cmd = [sys.executable, str(ORACLE_DIR / "oracle.py"), "historiser",
               "systeme", raison]
    else:
        cmd = [sys.executable, str(JARVIS_PY), "historiser",
               "--agent", "systeme", "--raison", raison,
               "--session", "session-freelance"]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60,
                           cwd=str(RACINE))
        for ligne in (r.stdout or "").splitlines():
            if ligne.strip():
                print("  [historiser] %s" % ligne.strip())
        if r.returncode != 0 and r.stderr:
            print("  [historiser-err] %s" % (r.stderr or "")[-400:])
        return r.returncode == 0
    except (OSError, subprocess.TimeoutExpired) as exc:
        print("  [historiser] ERREUR : %s" % exc)
        return False


# ------------------------------------------------------------------- main

def fermer(llm_id, session, dry_run=False):
    print("=== FERMETURE SESSION (outils-llm/fermer-session.py v%s) ===" % VERSION)
    print("  id      : %s" % llm_id)
    print("  session : %s" % session)
    if dry_run:
        print("  MODE    : --dry-run (simulation, AUCUN serveur arrete)")
    print()

    if session == "session-admin":
        rapports, force_utilise = _arreter_v1(dry_run)
    elif session == "session-freelance":
        rapports, force_utilise = _arreter_v2(dry_run)
    else:
        print("ERREUR: session invalide '%s'" % session)
        return 1

    print()
    print("=== VERIFICATION (serveurs bien fermes ?) ===")
    tous_fermes = True
    for nom, ferme, detail in rapports:
        statut = "ARRETE" if ferme else "ENCORE ACTIF"
        if not ferme:
            tous_fermes = False
        print("  %-28s : %-13s (%s)" % (nom, statut, detail))
    print()
    if dry_run:
        print("=== DRY-RUN TERMINE : rien n a ete arrete (verification seule) ===")
        return 0 if tous_fermes else 2

    if not tous_fermes:
        print("=== ERREUR : au moins un serveur refuse de s arreter. ===")
        print("    Verifiez manuellement les processus (tasklist | grep python).")
        print("    La session n est PAS fermee proprement.")
        return 1

    # Historisation : JAMAIS en double. En arret propre, oracle-demarrage /
    # jarvis ont DEJA historise leur arret (voie officielle, bon format).
    # On n historise ici QUE si un arret force a contourne cette ecriture.
    if force_utilise:
        raison = "FERMETURE SESSION (arret force) : serveurs %s eteints et verifies" \
                 % ("v1" if session == "session-admin" else "v2")
        if _historiser_officiel(raison, session):
            print("  [HISTORISATION] fermeture (arret force) tracee via la voie officielle.")
        else:
            print("  [HISTORISATION] ECHEC de la trace officielle - voir messages ci-dessus.")
    else:
        print("  [HISTORISATION] deja historise par %s (Arret propre) - pas de doublon."
              % ("oracle-demarrage" if session == "session-admin" else "jarvis"))
    print()
    print("=== FERMETURE TERMINEE : serveurs eteints et verifies ===")
    print("    La session est recoverable par : outils-llm/demarrer-llm.py %s %s"
          % (llm_id, "admin" if session == "session-admin" else "freelance"))
    return 0


def afficher_aide():
    print("usage: fermer-session.py <id> <session> [--dry-run]")
    print()
    print("FERMETURE EXCLUSIVE D UNE SESSION LLM - outils-llm/")
    print("Eteint les serveurs proprement AVEC verification qu'ils sont bien")
    print("fermes (pidfile supprime + processus non vivant).")
    print("  session-admin     -> serveurs v1 (oracle-server + routines-server v1)")
    print("  session-freelance -> serveurs v2 (daemon routines JARVIS)")
    print()
    print("exemples :")
    print("  python3 outils-llm/fermer-session.py glm5 admin")
    print("  python3 outils-llm/fermer-session.py freebuff freelance")
    print("  python3 outils-llm/fermer-session.py glm5 admin --dry-run")
    print()
    print("options :")
    print("  --help, -h   Afficher cette aide")
    print("  --version    Afficher la version")
    print("  --dry-run    Simuler sans arreter (verification seule)")


def main(argv):
    dry_run = "--dry-run" in argv
    argv = [a for a in argv if a != "--dry-run"]
    if argv and argv[0] in ("--help", "-h", "aide"):
        afficher_aide()
        return 0
    if argv and argv[0] == "--version":
        print("fermer-session v%s" % VERSION)
        return 0
    if not argv or len(argv) < 2:
        print("ERREUR: id et session obligatoires (ex: fermer-session.py glm5 admin)")
        afficher_aide()
        return 1
    llm_id = argv[0]
    session = argv[1]
    if session in ("admin", "freelance"):
        session = "session-" + session
    if not session.startswith("session-"):
        print("ERREUR: session invalide '%s' (admin ou freelance attendu)" % argv[1])
        return 1
    return fermer(llm_id, session, dry_run=dry_run)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
