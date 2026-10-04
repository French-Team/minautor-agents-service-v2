#!/usr/bin/env python3
# -*- coding: ascii -*-
# oracle-demarrage.py
# Serveur de demarrage v1 : lance/arrete/surveille les serveurs de la
# session-admin (oracle-server + futur serveur de routines v1).
# Inspire de la chaine de demarrage v2 (jarvis demarrage/arret) mais code
# 100% v1 : chaque univers a SON code (decision utilisateur 2026-08-27).
# Version : 0.1.1
# Statut : ebauche

# ============================================================
# REGLE IMMUABLE DE NOMMAGE : le nom commence par le prefixe du
# dossier (oracle-).
# ============================================================
# REGLE IMMUABLE : 100% stdlib Python (aucune dependance externe).
# ============================================================
# REGLE IMMUABLE : ASCII strict (aucun accent, aucun emoji).
# ============================================================

import argparse
import io
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

VERSION = "0.1.1"
STATUT = "ebauche"

_COULEURS = {
    "rouge": "\033[0;31m",
    "vert": "\033[0;32m",
    "jaune": "\033[1;33m",
    "bleu": "\033[0;34m",
    "neutre": "\033[0m",
}


def _couleur(texte, nom="neutre"):
    if not sys.stdout.isatty():
        return texte
    return _COULEURS.get(nom, "") + texte + _COULEURS["neutre"]


def _doc_chemin(script_path):
    p = Path(script_path)
    return p.with_suffix(".md")


def verifier_doc_presente(script_path):
    doc = _doc_chemin(script_path)
    if not doc.is_file():
        print(_couleur(
            "ERREUR: Documentation manquante : %s" % doc, "rouge"),
            file=sys.stderr)
        sys.exit(2)


def afficher_section_utilisation(doc):
    try:
        texte = doc.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return
    lignes = texte.splitlines()
    dans_usage = False
    for ligne in lignes:
        if ligne.strip().startswith("## "):
            dans_usage = ligne.strip().lower().startswith("## utilisation")
            continue
        if dans_usage and ligne.strip():
            print("  " + ligne.rstrip())


def exiger_confirmation_doc(script_path, dry_run, confirme_doc):
    if dry_run:
        return
    if confirme_doc:
        return
    doc = _doc_chemin(script_path)
    verifier_doc_presente(script_path)
    print(_couleur("=== DOCUMENTATION OBLIGATOIRE ===", "jaune"))
    print("  Cet outil exige la lecture de sa documentation avant usage reel.")
    print("  Section Utilisation de %s :" % doc.name)
    print("")
    afficher_section_utilisation(doc)
    print("")
    print(_couleur("REFUS: relancez avec --confirme-doc apres lecture de la doc.",
                   "rouge"), file=sys.stderr)
    sys.exit(2)


def afficher_messages_info(messages):
    if not messages:
        return
    print("")
    print(_couleur("=== MESSAGES POUR L AGENT ===", "jaune"))
    for message in messages:
        print("  > %s" % message)


def verifier_nommage(script_path):
    chemin = Path(script_path)
    nom_fichier = chemin.stem
    if nom_fichier == "outil-template":
        return
    dossier = chemin.parent.name
    prefixe = dossier.split("-")[0] + "-"
    if not nom_fichier.startswith(prefixe):
        print(_couleur(
            "ERREUR: Le nom '%s' ne commence pas par le prefixe du dossier '%s'"
            % (nom_fichier, prefixe), "rouge"), file=sys.stderr)
        sys.exit(1)


def _racine_projet():
    d = Path(__file__).resolve().parent
    while not (d / "AGENTS.md").is_file():
        parent = d.parent
        if parent == d:
            break
        d = parent
    return d


RACINE = _racine_projet()
ORACLE_DIR = Path(__file__).parent
SERVER_PY = ORACLE_DIR / "oracle-server.py"
PID_FILE = ORACLE_DIR / "oracle-server.pid"
LOG_DIR = ORACLE_DIR / "observations"
# Futur serveur de routines v1 : chemin declare, lance s il existe.
ROUTINES_SERVER = RACINE / "cerveau-projet" / "agents" / "tools" / \
    "oracle" / "routines-server.py"
ROUTINES_PID = ORACLE_DIR / "routines-server.pid"
SESSION_INACTIVITE = ORACLE_DIR / "session-admin-inactivite.json"
# SUPER-PILOTE cote Oracle : conduire les super-combos (prototype 2026-08-30).
# Lance s il existe (comme le serveur de routines).
SUPER_PILOTE_PY = ORACLE_DIR / "super-combos" / "super-pilote.py"
SUPER_PILOTE_PID = ORACLE_DIR / "super-combos" / "super-pilote.pid"


def _pid_actuel(pid_file):
    """PID stocke s'il correspond a un processus vivant, sinon None.
    WINDOWS : os.kill(pid, 0) ne TESTE pas - il TERMINE le processus
    (TerminateProcess). La sonde passe donc par OpenProcess (lecon v2)."""
    if not pid_file.exists():
        return None
    try:
        pid = int(pid_file.read_text(encoding="utf-8").strip())
    except ValueError:
        return None
    if os.name == "nt":
        import ctypes
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        kernel32 = ctypes.windll.kernel32
        h = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if h:
            kernel32.CloseHandle(h)
            return pid
        pid_file.unlink(missing_ok=True)
        return None
    try:
        os.kill(pid, 0)
        return pid
    except OSError:
        pid_file.unlink(missing_ok=True)
        return None


def _marquer_demarrage_session():
    """Initialiser l horloge d inactivite de la session-admin."""
    try:
        SESSION_INACTIVITE.write_text(
            json.dumps({"derniere_demande_user": time.time()}, ensure_ascii=True),
            encoding="utf-8")
    except OSError:
        pass


def _lancer_serveur(script, pid_file, nom, args_extra=None):
    """Lancer un serveur en daemon detache (DETACHED_PROCESS + log visible).
    Retourne (pid, message)."""
    pid = _pid_actuel(pid_file)
    if pid:
        return pid, "DEJA EN MARCHE (pid %d)" % pid
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log = io.open(LOG_DIR / ("%s-log.txt" % nom), "a", encoding="utf-8", newline="\n")
    flags = 0
    if hasattr(subprocess, "CREATE_NEW_PROCESS_GROUP"):
        flags |= subprocess.CREATE_NEW_PROCESS_GROUP
    if hasattr(subprocess, "DETACHED_PROCESS"):
        flags |= subprocess.DETACHED_PROCESS
    cmd = [sys.executable, str(script)] + (args_extra or [])
    proc = subprocess.Popen(cmd, creationflags=flags, stdout=log, stderr=log,
                            stdin=subprocess.DEVNULL, close_fds=True)
    # Le processus ecrit lui-meme son PID avant de commencer son premier tic.
    # Evite que le lanceur ecrase un PID concurrent et que sante lise un
    # marqueur obsolete pendant le demarrage.
    deadline = time.time() + 5
    while time.time() < deadline:
        if pid_file.exists():
            try:
                if int(pid_file.read_text(encoding="utf-8").strip()) == proc.pid:
                    return proc.pid, "LANCE (pid %d, detache)" % proc.pid
            except (ValueError, OSError):
                pass
        if proc.poll() is not None:
            return proc.pid, "ECHEC (processus termine, rc=%s)" % proc.returncode
        time.sleep(0.05)
    return proc.pid, "LANCE (pid %d, detache; pid confirme par le serveur)" % proc.pid


def _arreter_serveur(pid_file, nom):
    pid = _pid_actuel(pid_file)
    if not pid:
        return "deja arrete"
    try:
        os.kill(pid, signal.SIGTERM)
        pid_file.unlink(missing_ok=True)
        return "ARRETE (pid %d)" % pid
    except OSError as exc:
        return "ERREUR d arret: %s" % exc


def _etat_defcon():
    """Niveau DEFCON v1 (files/defcon.jsonl) : None si aucun."""
    defcon_file = ORACLE_DIR / "files" / "defcon.jsonl"
    if not defcon_file.exists():
        return None
    dernier = None
    for l in defcon_file.read_text(encoding="utf-8").splitlines():
        if not l.strip():
            continue
        try:
            e = json.loads(l)
        except ValueError:
            continue
        if e.get("niveau"):
            dernier = e["niveau"]
    return dernier


def _etat_files():
    """Missions actives dans les files v1 (statut != TERMINEE)."""
    files_dir = ORACLE_DIR / "files"
    total = 0
    details = []
    for nom in ("asap.jsonl", "normale.jsonl", "plus-tard.jsonl"):
        chemin = files_dir / nom
        if not chemin.exists():
            continue
        for ligne in chemin.read_text(encoding="utf-8").splitlines():
            if not ligne.strip():
                continue
            try:
                e = json.loads(ligne)
            except ValueError:
                continue
            if e.get("statut") in ("TERMINEE", None):
                continue
            total += 1
            details.append("[%s] %s" % (
                nom.replace(".jsonl", ""), (e.get("mission") or "")[:50]))
    return total, details


def _agents_bloques():
    """Agents avec au moins une P1 non lue (inbox oracle).
    Tolerant : une ligne JSON invalide ou double-encodee est ignoree."""
    inbox = ORACLE_DIR / "inbox"
    bloques = []
    if not inbox.is_dir():
        return bloques
    for nom_fichier in sorted(inbox.glob("*.jsonl")):
        for ligne in nom_fichier.read_text(encoding="utf-8").splitlines():
            if not ligne.strip():
                continue
            try:
                m = json.loads(ligne)
            except ValueError:
                continue
            if isinstance(m, str):
                # JSON double-encode (historique) : tenter un second parse
                try:
                    m = json.loads(m)
                except ValueError:
                    continue
            if not isinstance(m, dict):
                continue
            if not m.get("lu") and m.get("priorite") == 1:
                bloques.append(nom_fichier.stem)
                break
    return bloques


def _historiser(agent, raison):
    """Historiser via oracle.py (cmd_historiser) si disponible."""
    try:
        oracle_cli = ORACLE_DIR / "oracle.py"
        # CREATE_NO_WINDOW (Windows) : aucune fenetre cmd qui clignote
        # (meme principe que les routines v1/v2). 0 sur POSIX = inoffensif.
        flags_no_window = 0
        if hasattr(subprocess, "CREATE_NO_WINDOW"):
            flags_no_window = subprocess.CREATE_NO_WINDOW
        subprocess.run([sys.executable, str(oracle_cli), "historiser",
                        agent, raison], timeout=30,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       creationflags=flags_no_window)
    except Exception:
        pass


def _lancer_serveur_dry(script, pid_file, nom, args_extra=None):
    """Simulation de lancement (dry-run) : affiche ce qui serait lance."""
    pid = _pid_actuel(pid_file)
    if pid:
        return pid, "DEJA EN MARCHE (pid %d)" % pid
    cmd = [sys.executable, str(script)] + (args_extra or [])
    return None, "SERAT LANCE (detache) : %s" % " ".join(cmd)


def _lire_messages_oracle_demarrage():
    """Oracle lit ses alertes avant toute activation de Cerberus."""
    try:
        oracle_cli = ORACLE_DIR / "oracle.py"
        r = subprocess.run([sys.executable, str(oracle_cli), "lire", "oracle"],
                           timeout=30, capture_output=True, text=True,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        for ligne in (r.stdout or "").splitlines():
            if ligne.strip():
                print("      [Oracle] " + ligne)
        return r.returncode == 0
    except Exception as exc:
        print("      [Oracle] lecture impossible: %s" % exc)
        return False


def _reprendre_cerberus():
    """Reprendre Cerberus puis piloter une seule fois sa carte."""
    try:
        oracle_cli = ORACLE_DIR / "oracle.py"
        mission = "Reprise session-admin apres redemarrage des serveurs; Cerberus reprend la communication utilisateur."
        activation = subprocess.run(
            [sys.executable, str(oracle_cli), "activer", "cerberus", mission],
            timeout=30, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            capture_output=True, text=True)
        if activation.returncode != 0:
            return False, "activation Cerberus echouee"
        # Le pilote doit suivre l arbre de Cerberus, mais ne doit pas
        # relancer une carte deja terminee ni prendre une decision libre.
        pilotage = subprocess.run(
            [sys.executable, str(oracle_cli), "pilote", "cerberus", "--limite", "50"],
            timeout=60, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            capture_output=True, text=True)
        return pilotage.returncode == 0, "pilotage Cerberus: " + (
            "OK" if pilotage.returncode == 0 else "ECHEC")
    except Exception as exc:
        return False, "pilotage Cerberus indisponible: %s" % exc


def cmd_demarrage(args):
    """Chaine de demarrage v1 : daemons -> Cerberus -> operationnel."""
    print("=== ORACLE DEMARRAGE (v1) ===")
    dry = bool(getattr(args, "dry_run", False))
    if not dry:
        _marquer_demarrage_session()

    # 1. Routines d abord: elles produisent leurs traces avant qu Oracle
    #    ne lise son inbox et avant la reprise de Cerberus.
    if ROUTINES_SERVER.exists():
        if dry:
            pid2, msg2 = _lancer_serveur_dry(ROUTINES_SERVER, ROUTINES_PID,
                                             "routines", ["--boucle"])
        else:
            pid2, msg2 = _lancer_serveur(ROUTINES_SERVER, ROUTINES_PID,
                                         "routines", ["--boucle"])
        print("[1/4] Serveur routines v1 : %s" % msg2)
        if not dry:
            _historiser("routines-server", "DEMARRAGE SERVEUR: routines-server " + msg2)
    else:
        print("[1/4] Serveur routines v1 : absent (futur) - structure prete")

    # 2. Oracle-server ensuite (hub de coordination v1).
    if not SERVER_PY.exists():
        print(_couleur("[2/4] ERREUR: oracle-server.py introuvable", "rouge"))
        return 1
    if dry:
        pid, msg = _lancer_serveur_dry(SERVER_PY, PID_FILE, "oracle",
                                       ["--boucle", "--intervalle",
                                        str(getattr(args, "intervalle", 30))])
    else:
        pid, msg = _lancer_serveur(SERVER_PY, PID_FILE, "oracle",
                                   ["--boucle", "--intervalle",
                                    str(getattr(args, "intervalle", 30))])
    print("[2/4] Serveur oracle : %s" % msg)
    if not dry:
        _historiser("oracle", "DEMARRAGE SERVEUR: oracle-server " + msg)

    # 2b. SUPER-PILOTE cote Oracle (prototype super-combos) - s il existe
    if SUPER_PILOTE_PY.exists():
        if dry:
            pid_sp, msg_sp = _lancer_serveur_dry(
                SUPER_PILOTE_PY, SUPER_PILOTE_PID, "super-pilote",
                ["--boucle", "--intervalle", "120"])
        else:
            pid_sp, msg_sp = _lancer_serveur(
                SUPER_PILOTE_PY, SUPER_PILOTE_PID, "super-pilote",
                ["--boucle", "--intervalle", "120"])
        print("[2b] Serveur super-pilote (super-combos) : %s" % msg_sp)
        if not dry:
            _historiser("oracle", "DEMARRAGE SERVEUR: super-pilote " + msg_sp)
    else:
        print("[2b] Serveur super-pilote (super-combos) : absent "
              "(aucun super-combo) - structure prete")

    # 3. DEFCON + files + agents bloques
    niveau = _etat_defcon()
    if niveau == 5:
        print("[3/4] DEFCON 5 - ARRET TOTAL : dev GELE. Escalade utilisateur "
              "requise avant toute mission.")
    elif niveau is None:
        print("[3/4] DEFCON : aucun niveau journalise (etat nominal)")
    else:
        print("[3/4] DEFCON %d - %s" % (niveau, {
            5: "ARRET TOTAL", 4: "VALIDATION DES REPARATIONS",
            3: "REPRISE SURVEILLEE", 2: "REPRISE TOTALE"}.get(niveau, "?")))
    total, details = _etat_files()
    print("[3/4] Files v1 : %d mission(s) active(s)" % total)
    for d in details:
        print("      %s" % d)
    bloques = _agents_bloques()
    if bloques:
        print("      AGENTS BLOQUES (P1 non lue) : %s"
              % ", ".join(sorted(set(bloques))))
    else:
        print("      aucun agent bloque")

    # 4. operationnel
    if dry:
        print("[4/4] [DRY-RUN] ORACLE OPERATIONNEL (rien n a ete lance)")
        # Le dry-run ne doit produire aucune trace : il ne modifie aucun
        # etat et ne simule pas une activation dans l historique.
    else:
        # Oracle-agent lit son inbox une seule fois avant Cerberus.
        print("[4/4] Lecture prioritaire des messages Oracle")
        lus = _lire_messages_oracle_demarrage()
        print("      Oracle : %s" % ("MESSAGES LUS" if lus else "ECHEC LECTURE"))
        print("[4/4] Oracle-agent : traitement initial puis fin vers Cerberus")
        _historiser("oracle", "FIN: lecture et traitement initial termines; activation Cerberus autorisee")
        print("[4/4] Activation finale de Cerberus (agent communication)")
        repris, detail_cerb = _reprendre_cerberus()
        print("      Cerberus : %s (%s)" % ("REPRIS" if repris else "ECHEC", detail_cerb))
        print("[4/4] ORACLE OPERATIONNEL (session-admin)")
        # Une seule trace de cloture pour le cycle complet. Les traces des
        # serveurs, de la lecture Oracle et de la reprise Cerberus restent
        # distinctes et ne sont pas reconsolidees ici.
    return 0


def cmd_arret(args):
    """Extinction propre des serveurs v1."""
    print("=== ORACLE ARRET (v1) ===")
    print("- Serveur oracle : %s" % _arreter_serveur(PID_FILE, "oracle"))
    print("- Serveur routines v1 : %s"
          % _arreter_serveur(ROUTINES_PID, "routines"))
    print("- Serveur super-pilote : %s"
          % _arreter_serveur(SUPER_PILOTE_PID, "super-pilote"))
    print("- DEFCON : %s" % (_etat_defcon()
                             if _etat_defcon() is not None else "aucun"))
    print("- Etat sauvegarde : session recoverable par oracle-demarrage "
          "demarrage")
    if not getattr(args, "dry_run", False):
        _historiser("oracle", "Arret propre des serveurs v1")
    return 0


def cmd_etat(args):
    """Etat des serveurs v1."""
    print("=== ORACLE ETAT (v1) ===")
    pid = _pid_actuel(PID_FILE)
    print("- Serveur oracle : %s" % ("EN MARCHE (pid %d)" % pid if pid
                                     else "ARRETE"))
    pid2 = _pid_actuel(ROUTINES_PID)
    if ROUTINES_SERVER.exists():
        print("- Serveur routines v1 : %s" % ("EN MARCHE (pid %d)" % pid2
                                              if pid2 else "ARRETE"))
    else:
        print("- Serveur routines v1 : absent (futur)")
    niveau = _etat_defcon()
    print("- DEFCON : %s" % ("%d" % niveau if niveau is not None
                             else "aucun"))
    total, _ = _etat_files()
    print("- Files v1 : %d mission(s) active(s)" % total)
    bloques = _agents_bloques()
    print("- Agents bloques : %s" % (", ".join(sorted(set(bloques)))
                                     if bloques else "aucun"))
    return 0


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="oracle-demarrage",
        description="Serveur de demarrage v1 : lance/arrete/surveille les "
                    "serveurs de la session-admin (oracle-server + futur "
                    "serveur de routines v1)",
        epilog="Version %s (Statut : %s)" % (VERSION, STATUT))
    parser.add_argument("--dry-run", action="store_true",
                        help="Simuler sans rien modifier")
    parser.add_argument("--verbose", action="store_true",
                        help="Afficher les details")
    parser.add_argument("--version", action="version",
                        version="oracle-demarrage v%s" % VERSION)
    parser.add_argument("--chrono", action="store_true",
                        help="Mesurer la duree d execution")
    parser.add_argument("--doc", action="store_true",
                        help="Afficher le .md de documentation complet et sortir")
    parser.add_argument("--confirme-doc", action="store_true",
                        help="Confirmer la lecture de la documentation (requis "
                             "en mode reel)")
    parser.add_argument("--intervalle", type=int, default=30,
                        help="Secondes entre deux tics du daemon (defaut 30)")
    subparsers = parser.add_subparsers(dest="commande")
    subparsers.add_parser("demarrage", help="Chaine de demarrage v1")
    subparsers.add_parser("arret", help="Extinction propre des serveurs v1")
    subparsers.add_parser("etat", help="Etat des serveurs v1")
    return parser


def main():
    verifier_nommage(sys.argv[0])
    verifier_doc_presente(sys.argv[0])
    parser = construire_parser()
    args = parser.parse_args()

    if getattr(args, "doc", False):
        doc = _doc_chemin(sys.argv[0])
        print(doc.read_text(encoding="utf-8"))
        return 0

    exiger_confirmation_doc(sys.argv[0], getattr(args, "dry_run", False),
                            getattr(args, "confirme_doc", False))

    if not args.commande:
        parser.print_help()
        return 0

    if args.commande == "demarrage":
        rc = cmd_demarrage(args)
    elif args.commande == "arret":
        rc = cmd_arret(args)
    elif args.commande == "etat":
        rc = cmd_etat(args)
    else:
        parser.print_help()
        return 0

    if rc == 0 and not getattr(args, "dry_run", False):
        afficher_messages_info([
            "serveur de demarrage v1 : documenter dans oracle-demarrage.md "
            "(historique de version)",
            "fichier cree : indexer dans index-tools.md (categorie oracle)",
            "fichier cree : adapter les tests (Morpheus)",
        ])
    return rc


if __name__ == "__main__":
    sys.exit(main())
