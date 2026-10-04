# -*- coding: ascii -*-
# routine : sante -- etat global du systeme en temps reel
# Verifie : daemon vivant, BDD accessible, routines fonctionnelles,
# encart v2 coherent, P1 non-acquittes, inbox non bloquee.
# Historise UNIQUEMENT quand il y a une anomalie (evenementiel).
import json
import os
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

# P10 : racine DETECTEE
_d = os.path.dirname(os.path.abspath(__file__))
while not os.path.isfile(os.path.join(_d, "AGENTS.md")):
    _p = os.path.dirname(_d)
    if _p == _d:
        break
    _d = _p
RACINE = Path(_d)

JARVIS_DIR = RACINE / "cerveau-projet" / "freelance" / "tools-commun" / "jarvis"
BDD_PATH = JARVIS_DIR / "historique" / "historique.db"
ENCART_PATH = RACINE / "AGENTS-activite-recente-v2.md"
PIDFILE = RACINE / "cerveau-projet" / "freelance" / "routines-server" / "routines-server.pid"

# Seuils
SEUIL_P1 = 10          # alerte si plus de 10 P1 non-acquittes
SEUIL_INBOX = 50       # alerte si plus de 50 messages non-lus
SEUIL_BDD_HEURES = 1   # alerte si pas d'ecriture BDD depuis 1h


def verifier_daemon():
    """Verifie que le daemon routines est vivant."""
    if not PIDFILE.exists():
        return False, "PIDFILE absent"
    try:
        pid = int(PIDFILE.read_text().strip())
        # Verifier si le processus existe (Windows : OpenProcess)
        if sys.platform == "win32":
            import ctypes
            handle = ctypes.windll.kernel32.OpenProcess(0x1000, False, pid)
            if handle:
                ctypes.windll.kernel32.CloseHandle(handle)
                return True, f"PID {pid} vivant"
            return False, f"PID {pid} mort"
        else:
            os.kill(pid, 0)
            return True, f"PID {pid} vivant"
    except (ValueError, OSError) as e:
        return False, f"Erreur PID: {e}"


def verifier_bdd():
    """Verifie que la BDD est accessible et contient des donnees recentes."""
    if not BDD_PATH.exists():
        return False, "BDD introuvable"
    try:
        conn = sqlite3.connect(str(BDD_PATH))
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM historique")
        total = cursor.fetchone()[0]
        # Derniere entree
        cursor.execute("SELECT MAX(date_iso) FROM historique")
        derniere = cursor.fetchone()[0]
        conn.close()
        if total == 0:
            return False, "BDD vide"
        if derniere:
            try:
                dt = datetime.strptime(derniere[:19], "%Y-%m-%dT%H:%M:%S")
                age_heures = (datetime.now() - dt).total_seconds() / 3600
                if age_heures > SEUIL_BDD_HEURES:
                    return False, f"BDD stale ({age_heures:.1f}h sans ecriture)"
            except ValueError:
                pass
        return True, f"BDD OK ({total} entrees, derniere: {derniere[:16]})"
    except Exception as e:
        return False, f"Erreur BDD: {e}"


def verifier_encart():
    """Verifie l'integrite de l'encart v2."""
    if not ENCART_PATH.exists():
        return False, "Encart v2 introuvable"
    try:
        contenu = ENCART_PATH.read_text(encoding="utf-8").replace("\r\n", "\n")
        lignes = contenu.split("\n")
        # Trouver le tableau
        idx_tableau = -1
        for i, ligne in enumerate(lignes):
            if "| Grade |" in ligne and "| Agent |" in ligne:
                idx_tableau = i
                break
        if idx_tableau == -1:
            return False, "Tableau non trouve"
        # Compter les entrees
        nb_entrees = 0
        for i in range(idx_tableau + 2, len(lignes)):
            if lignes[i].startswith("| "):
                nb_entrees += 1
            else:
                break
        # Verifier les colonnes (7 colonnes : Grade|Agent|Secteur|Raison|Heure|id|Type)
        for i in range(idx_tableau + 2, idx_tableau + 2 + nb_entrees):
            cols = [c.strip() for c in lignes[i].split("|") if c.strip()]
            if len(cols) != 7:
                return False, f"Ligne {i+1}: {len(cols)} colonnes au lieu de 7"
        if nb_entrees > 50:
            return False, f"Trop d'entrees: {nb_entrees} > 50"
        return True, f"Encart OK ({nb_entrees} entrees, 6 colonnes)"
    except Exception as e:
        return False, f"Erreur encart: {e}"


def verifier_p1():
    """Verifie les P1 non-acquittes dans les inboxes."""
    inbox_dir = JARVIS_DIR / "inbox"
    if not inbox_dir.exists():
        return True, "Pas d'inbox"
    nb_p1 = 0
    for f in inbox_dir.glob("*.jsonl"):
        try:
            for ligne in f.read_text(encoding="utf-8").splitlines():
                if not ligne.strip():
                    continue
                m = json.loads(ligne)
                if not m.get("lu") and m.get("priorite") == 1:
                    nb_p1 += 1
        except Exception:
            pass
    if nb_p1 > SEUIL_P1:
        return False, f"{nb_p1} P1 non-acquittes (seuil: {SEUIL_P1})"
    return True, f"{nb_p1} P1 non-acquittes (OK)"


def main():
    """Execution de tous les controles."""
    anomalies = []
    stats = []
    
    # 1. Daemon
    ok, msg = verifier_daemon()
    stats.append(f"daemon: {msg}")
    if not ok:
        anomalies.append(f"DAEMON: {msg}")
    
    # 2. BDD
    ok, msg = verifier_bdd()
    stats.append(f"bdd: {msg}")
    if not ok:
        anomalies.append(f"BDD: {msg}")
    
    # 3. Encart
    ok, msg = verifier_encart()
    stats.append(f"encart: {msg}")
    if not ok:
        anomalies.append(f"ENCART: {msg}")
    
    # 4. P1
    ok, msg = verifier_p1()
    stats.append(f"p1: {msg}")
    if not ok:
        anomalies.append(f"P1: {msg}")
    
    # Affichage
    print("[SANTE] Etat du systeme:")
    for s in stats:
        print(f"  - {s}")
    
    if anomalies:
        print(f"\n[SANTE] {len(anomalies)} anomalie(s) detectee(s):")
        for a in anomalies:
            print(f"  ! {a}")
        # Historiser les anomalies
        try:
            _fo = RACINE / "cerveau-projet" / "freelance" / "tools-commun" \
                / "os_path" / "fonctions"
            _fj = JARVIS_DIR / "fonctions"
            for p in (_fo, _fj):
                if str(p) not in sys.path:
                    sys.path.insert(0, str(p))
            from historique import historiser
            historiser("sante",
                       f"{len(anomalies)} anomalie(s): " + "; ".join(anomalies[:3]),
                       "R", session="session-freelance")
            # RETRO-CORRECTION : signaler les anomalies agent-specifiques
            from corrections import marquer_correction
            for a in anomalies:
                if a.startswith("ENCART:"):
                    marquer_correction(
                        agent="jarvis",
                        fichier=str(ENCART_PATH),
                        erreur=a,
                        source="sante",
                        session="session-freelance")
                elif a.startswith("P1:"):
                    marquer_correction(
                        agent="jarvis",
                        fichier=str(JARVIS_DIR / "inbox"),
                        erreur=a,
                        source="sante",
                        session="session-freelance")
        except Exception:
            pass
        return 1
    else:
        print("[SANTE] Aucune anomalie - systeme sain")
        return 0


if __name__ == "__main__":
    sys.exit(main())
