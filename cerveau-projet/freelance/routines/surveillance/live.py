# -*- coding: ascii -*-
# routine : live -- surveillance des activations/desactivations
# d'agents en temps reel.
# Verifie : quels agents sont actifs, si les activations sont recentes,
# si les agents historisent, si les inboxes ne debordent pas.
# Historise UNIQUEMENT quand il y a une anomalie (evenementiel).
import json
import os
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
AGENTS_FILE = RACINE / "AGENTS.md"
JARVIS_DATA = JARVIS_DIR / "jarvis-data.json"

# Seuils
SEUIL_INBOX = 20       # alerte si inbox > 20 messages non-lus
SEUIL_SANS_ACTIVITE = 3600  # 1h sans activite = alerte


def lire_agents_actifs():
    """Lit les agents declares actifs dans AGENTS.md."""
    if not AGENTS_FILE.exists():
        return {}
    contenu = AGENTS_FILE.read_text(encoding="utf-8")
    agents = {}
    bloc_courant = None
    for ligne in contenu.split("\n"):
        if ligne.startswith("| **Agent actif** |"):
            parties = [p.strip() for p in ligne.split("|")]
            if len(parties) >= 3:
                bloc_courant = parties[2]
        elif ligne.startswith("| **Nom LLM** |") and bloc_courant:
            parties = [p.strip() for p in ligne.split("|")]
            if len(parties) >= 3:
                agents[bloc_courant] = parties[2]
                bloc_courant = None
    return agents


def verifier_inbox_agents():
    """Verifie que les inboxes des agents ne debordent pas."""
    inbox_dir = JARVIS_DIR / "inbox"
    if not inbox_dir.exists():
        return True, "Pas d'inbox"
    
    resultats = {}
    for f in inbox_dir.glob("*.jsonl"):
        agent = f.stem
        nb_non_lus = 0
        try:
            for ligne in f.read_text(encoding="utf-8").splitlines():
                if not ligne.strip():
                    continue
                m = json.loads(ligne)
                if not m.get("lu"):
                    nb_non_lus += 1
        except Exception:
            pass
        resultats[agent] = nb_non_lus
    
    debordement = {a: n for a, n in resultats.items() if n > SEUIL_INBOX}
    if debordement:
        msg = ", ".join(f"{a}:{n}" for a, n in debordement.items())
        return False, f"Inbox debordement: {msg}"
    total = sum(resultats.values())
    return True, f"Inbox OK ({len(resultats)} agents, {total} non-lus)"


def verifier_derniere_activite():
    """Verifie que les agents actifs ont eu une activite recente."""
    try:
        _fj = JARVIS_DIR / "fonctions"
        if str(_fj) not in sys.path:
            sys.path.insert(0, str(_fj))
        from historique_bdd import consulter
        entries = consulter(str(RACINE), limite=20)
        if not entries:
            return True, "Pas d'entree dans la BDD"
        
        # Derniere activite par agent
        derniers = {}
        for e in entries:
            agent = e.get("agent", "")
            date = e.get("date_iso", "")
            if agent and date and agent not in derniers:
                try:
                    dt = datetime.strptime(date[:19], "%Y-%m-%dT%H:%M:%S")
                    derniers[agent] = dt
                except ValueError:
                    pass
        
        now = datetime.now()
        inactifs = []
        for agent, dt in derniers.items():
            age = (now - dt).total_seconds()
            if age > SEUIL_SANS_ACTIVITE and agent not in ("sante", "citations", "vigie", "notation", "flux", "harnais"):
                inactifs.append(f"{agent} ({age/60:.0f}min)")
        
        if inactifs:
            return False, f"Agents inactifs: {', '.join(inactifs)}"
        return True, f"Activite OK ({len(derniers)} agents)"
    except Exception as e:
        return True, f"Erreur verification: {e}"


def main():
    """Execution de tous les controles."""
    anomalies = []
    stats = []
    
    # 1. Agents actifs dans AGENTS.md
    agents = lire_agents_actifs()
    stats.append(f"agents_actifs: {len(agents)} ({', '.join(agents.keys())})")
    
    # 2. Inbox
    ok, msg = verifier_inbox_agents()
    stats.append(f"inbox: {msg}")
    if not ok:
        anomalies.append(f"INBOX: {msg}")
    
    # 3. Activite recente
    ok, msg = verifier_derniere_activite()
    stats.append(f"activite: {msg}")
    if not ok:
        anomalies.append(f"ACTIVITE: {msg}")
    
    # Affichage
    print("[AGENTS-REEL] Surveillance des agents:")
    for s in stats:
        print(f"  - {s}")
    
    if anomalies:
        print(f"\n[AGENTS-REEL] {len(anomalies)} anomalie(s):")
        for a in anomalies:
            print(f"  ! {a}")
        try:
            _fo = RACINE / "cerveau-projet" / "freelance" / "tools-commun" \
                / "os_path" / "fonctions"
            _fj = JARVIS_DIR / "fonctions"
            for p in (_fo, _fj):
                if str(p) not in sys.path:
                    sys.path.insert(0, str(p))
            from historique import historiser
            historiser("live",
                       f"{len(anomalies)} anomalie(s): " + "; ".join(anomalies[:3]),
                       "R", session="session-freelance")
            # RETRO-CORRECTION : signaler les debordements inbox
            from corrections import marquer_correction
            for a in anomalies:
                if a.startswith("INBOX:"):
                    # Extraire les agents debordants
                    import re
                    agents_deb = re.findall(r"(\w+):(\d+)", a)
                    for agent, nb in agents_deb:
                        marquer_correction(
                            agent=agent,
                            fichier=str(JARVIS_DIR / "inbox" / f"{agent}.jsonl"),
                            erreur=f"Inbox debordement: {nb} messages non-lus",
                            source="live",
                            session="session-freelance")
        except Exception:
            pass
        return 1
    else:
        print("[AGENTS-REEL] Tous les agents fonctionnent normalement")
        return 0


if __name__ == "__main__":
    sys.exit(main())
