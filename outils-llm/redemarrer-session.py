#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
outils-llm/redemarrer-session.py - REDEMARRAGE EXCLUSIF D UNE SESSION LLM.

Redemarre une session SANS devoir la fermer d'abord (pas besoin de
fermer-session). Cet outil est fait pour UNE situation precise : le flux
est bugge et le LLM a repris la main (ce qui est un probleme). Le
redemarrage sert a REPRENDRE LA MAIN sur le LLM en ayant conscience que
cette reprise est due a un BUG.

Probleme evite : si le redemarrage n etait que la suite de la session qui
a mene au bug, on reviendrait dans la situation precedente. Donc cet outil
DECLENCHE DEFCON 5 (arret total) pour lancer un PROTOCOLE DE SECOURS :
le flux bugge est GELE, la reprise ne peut se faire que par le protocole
(validation des reparations DEFCON 5->4->3->2, decision utilisateur).

Ce que l outil fait (dans l ordre) :
  1. Verifier/reparer les serveurs de la session SANS fermer (un serveur
     tombe est relance par SA commande de demarrage).
  2. Declarer DEFCON 5 (arret total) avec la raison du bug :
       v1 -> oracle.py defcon-declarer ; v2 -> jarvis.py stop-dev.
  3. Reprendre la main sur le LLM : l agent actif de la session redevient
     le point d entree (v1 -> cerberus, v2 -> stark) via
     activer-agent-principal activer --forcer (outrepasse le garde-fou :
     c est le but d une reprise apres bug). L ACTIVATION historise la
     reprise (voie officielle, bon format) : on n ecrit JAMAIS en plus
     (ecriture maison = ancien format + doublon dans l encart).

Sans question : execute, comme un soldat.

Usage:
    python3 outils-llm/redemarrer-session.py <id> <session> [--raison \"...\"] [--dry-run]

Exemples:
    python3 outils-llm/redemarrer-session.py glm5 admin --raison \"flux casse, LLM a repris la main\"
    python3 outils-llm/redemarrer-session.py freebuff freelance

Options : --help/-h, --version, --raison <texte>, --dry-run (simule sans rien faire).
"""

import os
import signal
import subprocess
import sys
import time
from pathlib import Path

VERSION = "0.1.1"
RACINE = Path(__file__).resolve().parent.parent

# Serveurs de la v1 (session-admin).
ORACLE_DIR = RACINE / "cerveau-projet" / "agents" / "tools" / "oracle"
PID_ORACLE = ORACLE_DIR / "oracle-server.pid"
PID_ROUTINES_V1 = ORACLE_DIR / "routines-server.pid"
ORACLE_DEMARRAGE = ORACLE_DIR / "oracle-demarrage.py"
ORACLE_PY = ORACLE_DIR / "oracle.py"

# Serveurs de la v2 (session-freelance) : daemon routines JARVIS.
JARVIS_DIR = RACINE / "cerveau-projet" / "freelance" / "tools-commun" / "jarvis"
PID_ROUTINES_V2 = JARVIS_DIR / "routines-server.pid"
JARVIS_PY = JARVIS_DIR / "jarvis.py"

ACTIVER_PRINCIPAL = RACINE / "cerveau-projet" / "agents" / "tools" / "activer" / \
    "activer-agent-principal" / "activer-agent-principal.py"

# Point d entree par session (qui reprend la main sur le LLM).
ENTREE_PAR_SESSION = {"session-admin": "cerberus", "session-freelance": "stark"}

RAISON_DEFAUT = ("reprise apres bug : le flux etait casse et le LLM a repris "
                 "la main - redemarrage avec DEFCON 5 (protocole de secours)")


# ------------------------------------------------------------ utils texte

def tronquer(texte, n=80):
    return texte if len(texte) <= n else texte[:n] + "..."


# ----------------------------------------------------------- verification

def _probe_pid(pid):
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


def _serveur_en_marche(pid_file):
    pid = _lire_pid(pid_file)
    if pid is None:
        return False, None
    return _probe_pid(pid), pid


# ------------------------------------------------------------ serveurs

def _reparer_serveurs_v1(dry_run):
    """Verifier oracle + routines v1 ; relancer ceux qui sont tombes."""
    print("[1/3] Serveurs v1 (verifier/reparer SANS fermer la session)")
    cibles = [("oracle-server", PID_ORACLE), ("routines-server v1", PID_ROUTINES_V1)]
    a_relancer = []
    for nom, pf in cibles:
        en_marche, pid = _serveur_en_marche(pf)
        if en_marche:
            print("  %-20s : EN MARCHE (pid %d)" % (nom, pid))
        else:
            a_relancer.append(nom)
            print("  %-20s : EN PANNE (pidfile %s)" % (nom, "absent" if pid is None else "pid %d mort" % pid))
    if not a_relancer:
        print("  -> serveurs v1 tous operationnels (aucune reparation).")
        return True
    if dry_run:
        print("  -> [dry-run] serait relances : %s" % ", ".join(a_relancer))
        return True
    print("  -> relance via oracle-demarrage demarrage...")
    cmd = [sys.executable, str(ORACLE_DEMARRAGE), "--confirme-doc", "demarrage"]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=90,
                           cwd=str(RACINE))
        for ligne in (r.stdout or "").splitlines():
            print("  [oracle-demarrage] %s" % ligne.strip())
    except (OSError, subprocess.TimeoutExpired) as exc:
        print("  [oracle-demarrage] ERREUR : %s" % exc)
    time.sleep(1)
    tous_ok = True
    for nom, pf in cibles:
        en_marche, pid = _serveur_en_marche(pf)
        statut = "EN MARCHE (pid %d)" % pid if en_marche else "ENCORE EN PANNE"
        if not en_marche:
            tous_ok = False
        print("  %-20s : %s" % (nom, statut))
    return tous_ok


def _reparer_serveurs_v2(dry_run):
    """Verifier le daemon routines JARVIS ; le relancer s il est tombe."""
    print("[1/3] Serveurs v2 (verifier/reparer SANS fermer la session)")
    en_marche, pid = _serveur_en_marche(PID_ROUTINES_V2)
    if en_marche:
        print("  %-20s : EN MARCHE (pid %d)" % ("routines JARVIS", pid))
        print("  -> serveurs v2 operationnels (aucune reparation).")
        return True
    print("  %-20s : EN PANNE" % "routines JARVIS")
    if dry_run:
        print("  -> [dry-run] serait relance via jarvis.py demarrage.")
        return True
    print("  -> relance via jarvis.py demarrage...")
    cmd = [sys.executable, str(JARVIS_PY), "demarrage", "--session", "session-freelance"]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=90,
                           cwd=str(RACINE))
        for ligne in (r.stdout or "").splitlines():
            if "DEMARRE" in ligne or "DEJA" in ligne or "OPERATIONNEL" in ligne or "[1/4]" in ligne or "[4/4]" in ligne:
                print("  [jarvis] %s" % ligne.strip())
    except (OSError, subprocess.TimeoutExpired) as exc:
        print("  [jarvis] ERREUR : %s" % exc)
    time.sleep(1)
    en_marche, pid = _serveur_en_marche(PID_ROUTINES_V2)
    print("  %-20s : %s" % ("routines JARVIS",
                            "EN MARCHE (pid %d)" % pid if en_marche else "ENCORE EN PANNE"))
    return en_marche


# ------------------------------------------------------------- DEFCON 5

def _declarer_defcon5(session, raison, dry_run):
    """DEFCON 5 (arret total) - le flux bugge est gele."""
    print("[2/3] DEFCON 5 - ARRET TOTAL (protocole de secours)")
    if dry_run:
        print("  -> [dry-run] DEFCON 5 serait declare (raison : %s...)" % tronquer(raison, 60))
        return True
    if session == "session-admin":
        cmd = [sys.executable, str(ORACLE_PY), "defcon-declarer", raison]
    else:
        cmd = [sys.executable, str(JARVIS_PY), "stop-dev", "--raison", raison]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60,
                           cwd=str(RACINE))
        for ligne in (r.stdout or "").splitlines():
            print("  [defcon] %s" % ligne.strip())
        if r.returncode != 0 and r.stderr:
            print("  [defcon-err] %s" % (r.stderr or "")[-400:])
        if r.returncode == 0:
            print("  -> DEFCON 5 DECLARE : dev GELE, reprise par protocole de secours uniquement.")
            return True
        return False
    except (OSError, subprocess.TimeoutExpired) as exc:
        print("  [defcon] ERREUR : %s" % exc)
        return False


# ------------------------------------------------------- reprise de main

def _reprendre_main(session, raison, dry_run):
    """L agent actif redevient le point d entree (cerberus/stark) - le LLM
    reprend le flux correctement. --forcer : outrepasse le garde-fou de
    double activation (c est le but d une reprise apres bug)."""
    entree = ENTREE_PAR_SESSION[session]
    print("[3/3] Reprendre la main sur le LLM (agent actif -> %s)" % entree)
    if dry_run:
        print("  -> [dry-run] activer %s avec --forcer (raison : %s...)"
              % (entree, tronquer(raison, 60)))
        return True
    # --forcer est un flag GLOBAL lu dans sys.argv : place en fin de ligne.
    # activer-agent-principal v0.8.5 le retire d argv avant le parsing
    # positionnel -> ni session, ni mission ne sont pollues.
    cmd = [sys.executable, str(ACTIVER_PRINCIPAL), "activer", session, entree,
           raison, "--forcer"]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60,
                           cwd=str(RACINE))
        for ligne in (r.stdout or "").splitlines():
            if ligne.strip():
                print("  [activer] %s" % ligne.strip())
        if r.returncode != 0 and r.stderr:
            print("  [activer-err] %s" % (r.stderr or "")[-400:])
        return r.returncode == 0
    except (OSError, subprocess.TimeoutExpired) as exc:
        print("  [activer] ERREUR : %s" % exc)
        return False


# ------------------------------------------------------------------- main

def redemarrer(llm_id, session, raison, dry_run=False):
    print("=== REDEMARRAGE SESSION (outils-llm/redemarrer-session.py v%s) ===" % VERSION)
    print("  id      : %s" % llm_id)
    print("  session : %s" % session)
    print("  cause   : BUG (le LLM a repris la main - probleme)")
    print("  raison  : %s" % raison)
    if dry_run:
        print("  MODE    : --dry-run (simulation, AUCUN effet)")
    print()

    # 1. Serveurs (verifier/reparer, sans fermer)
    if session == "session-admin":
        ok_serveurs = _reparer_serveurs_v1(dry_run)
    else:
        ok_serveurs = _reparer_serveurs_v2(dry_run)
    print()

    # 2. DEFCON 5 (arret total)
    raison_defcon = "REDEMARRAGE APRES BUG : %s" % raison
    ok_defcon = _declarer_defcon5(session, raison_defcon, dry_run)
    print()

    # 3. Reprendre la main sur le LLM
    raison_act = ("REDEMARRAGE APRES BUG (DEFCON 5 declare) : %s - NE PAS "
                  "reprendre le flux bugge, lancer le protocole de secours "
                  "(diagnostic du bug, reparations, DEFCON 5->4->3->2 avec "
                  "decision utilisateur)" % raison)
    ok_main = _reprendre_main(session, raison_act, dry_run)
    print()

    if not (ok_serveurs and ok_defcon and ok_main):
        print("=== ERREUR : le redemarrage n est pas complet. ===")
        print("    Serveurs ok=%s | DEFCON 5 ok=%s | Reprise main ok=%s"
              % (ok_serveurs, ok_defcon, ok_main))
        return 1

    print("=== REDEMARRAGE TERMINE (reprise apres BUG) ===")
    print("  DEFCON 5 = ARRET TOTAL : le flux bugge est GELE.")
    print("  Le LLM ne doit PAS continuer la session precedente.")
    print()
    print("  PROTOCOLE DE SECOURS (reprise uniquement par ici) :")
    print("   1. %s lance le DIAGNOSTIC du bug (jamais la suite du flux bugge)."
          % ENTREE_PAR_SESSION[session].capitalize())
    print("   2. Reparations validees -> DEFCON 4 : oracle.py defcon-changer"
          " (v1) / jarvis.py defcon-changer (v2)")
    print("   3. Reprise surveillee   -> DEFCON 3")
    print("   4. Reprise totale       -> DEFCON 2")
    print("  Chaque descente de DEFCON exige la DECISION EXPLICITE de"
          " l utilisateur.")
    print()
    print("  Reprise de session : outils-llm/demarrer-llm.py %s %s"
          % (llm_id, "admin" if session == "session-admin" else "freelance"))
    return 0


def afficher_aide():
    print("usage: redemarrer-session.py <id> <session> [--raison \"...\"] [--dry-run]")
    print()
    print("REDEMARRAGE EXCLUSIF D UNE SESSION LLM (reprise apres BUG) - outils-llm/")
    print("A utiliser quand le flux est bugge et que le LLM a repris la main.")
    print("Redemarre SANS fermer la session :")
    print("  1. verifie/reparent les serveurs (sans fermer)")
    print("  2. declare DEFCON 5 (arret total - le flux bugge est gele)")
    print("  3. reprend la main sur le LLM (agent actif -> cerberus/stark)")
    print("  4. historise le redemarrage")
    print("La reprise se fait par le PROTOCOLE DE SECOURS (DEFCON 5->4->3->2,")
    print("decision utilisateur a chaque etape).")
    print()
    print("exemples :")
    print("  python3 outils-llm/redemarrer-session.py glm5 admin")
    print("  python3 outils-llm/redemarrer-session.py freebuff freelance --raison \"flux casse\"")
    print("  python3 outils-llm/redemarrer-session.py glm5 admin --dry-run")
    print()
    print("options :")
    print("  --help, -h       Afficher cette aide")
    print("  --version        Afficher la version")
    print("  --raison <texte> Raison du bug (obligatoire pour l audit)")
    print("  --dry-run        Simuler sans rien faire")


def main(argv):
    dry_run = "--dry-run" in argv
    argv = [a for a in argv if a != "--dry-run"]
    raison = RAISON_DEFAUT
    if "--raison" in argv:
        i = argv.index("--raison")
        if i + 1 < len(argv):
            raison = argv[i + 1]
            del argv[i:i + 2]
        else:
            print("ERREUR: --raison attend un texte")
            return 1
    if argv and argv[0] in ("--help", "-h", "aide"):
        afficher_aide()
        return 0
    if argv and argv[0] == "--version":
        print("redemarrer-session v%s" % VERSION)
        return 0
    if not argv or len(argv) < 2:
        print("ERREUR: id et session obligatoires (ex: redemarrer-session.py glm5 admin)")
        afficher_aide()
        return 1
    llm_id = argv[0]
    session = argv[1]
    if session in ("admin", "freelance"):
        session = "session-" + session
    if not session.startswith("session-"):
        print("ERREUR: session invalide '%s' (admin ou freelance attendu)" % argv[1])
        return 1
    return redemarrer(llm_id, session, raison, dry_run=dry_run)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
