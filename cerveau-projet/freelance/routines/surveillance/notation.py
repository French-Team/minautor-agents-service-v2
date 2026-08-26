# -*- coding: ascii -*-
# routine : notation -- depose une demande d'evaluation periodique des
# agents (ex-evaluer-agents, renommee 2026-08-26 : nom simple qui
# exprime ce qu'elle est).
import json
import os
import sys
import uuid
from datetime import datetime, timezone

from pathlib import Path

# P10 : racine DETECTEE en remontant jusqu'a AGENTS.md (jamais compte)
_d = os.path.dirname(os.path.abspath(__file__))
while not os.path.isfile(os.path.join(_d, "AGENTS.md")):
    _p = os.path.dirname(_d)
    if _p == _d:
        break
    _d = _p
RACINE = Path(_d)
JARVIS_DIR = RACINE / "cerveau-projet" / "freelance" / "tools-commun" / "jarvis"


def observations_recentes():
    obs_dir = Path(RACINE, "cerveau-projet", "freelance", "tools-commun",
                   "routines-server", "observations")
    if not obs_dir.exists():
        return ["(aucune observation)"]
    fichiers = sorted(obs_dir.glob("*.md"))[-5:]
    return [f.name for f in fichiers] or ["(aucune observation)"]


def demande_deja_en_attente():
    """True si une demande d'evaluation attend deja :
    - NON-LUE dans l'inbox de jarvis (anti-inondation d'origine), OU
    - DEPOSEE il y a moins de 10 min dans outbox/edith (v0.2.0 : le
      relais marque le hub 'lu' des transmission - sans ce second
      test, chaque tic redeposait une evaluation deja transmise a
      stark et personne ne la consomme hors session : 1 spam / 10 min).
    """
    inbox = JARVIS_DIR / "inbox" / "jarvis.jsonl"
    if inbox.exists():
        with open(inbox, encoding="utf-8") as f:
            for ligne in f:
                if not ligne.strip():
                    continue
                try:
                    m = json.loads(ligne)
                except ValueError:
                    continue
                if not m.get("lu") and \
                        "[EDITH-EVALUATION]" in str(m.get("objet", "")):
                    return True
    return depot_recent()


def depot_recent(secondes=600):
    """True si une evaluation a ete deposee il y a moins de <secondes>."""
    from datetime import datetime, timedelta
    outbox = JARVIS_DIR / "outbox" / "edith.jsonl"
    if not outbox.exists():
        return False
    borne = datetime.now(timezone.utc).replace(tzinfo=None) \
        - timedelta(seconds=secondes)
    with open(outbox, encoding="utf-8") as f:
        for ligne in reversed(f.readlines()):
            if not ligne.strip():
                continue
            try:
                m = json.loads(ligne)
            except ValueError:
                continue
            if "[EDITH-EVALUATION]" not in str(m.get("objet", "")):
                continue
            try:
                d = datetime.strptime(str(m.get("date", ""))[:19],
                                      "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                continue
            return d >= borne
    return False


def main():
    if demande_deja_en_attente():
        print("[ROUTINE] Demande d'evaluation deja en attente - rien depose.")
        return 0
    msg = {
        "id": str(uuid.uuid4())[:8],
        "de": "edith", "vers": "jarvis", "priorite": 2,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "objet": "[EDITH-EVALUATION] demande activation EDITH : cycle "
                  "periodique d'evaluation des agents",
        "corps": (
            "DEMANDE D'ACTIVATION EDITH (protocole 17, routine 5 min - "
            "manifest 300s, reduite pour les essais 2026-08-26). EDITH doit etre "
            "activee pour poser le "
            "QUESTIONNAIRE STANDARD aux agents actifs, attribuer les +/- "
            "et transmettre son rapport a JARVIS pour application via "
            "rating-agents.\nObservations recentes du serveur : "
            + ", ".join(observations_recentes())
        ),
        "lu": False, "accuse": False,
    }
    jarvis_inbox = JARVIS_DIR / "inbox" / "jarvis.jsonl"
    jarvis_outbox = JARVIS_DIR / "outbox" / "edith.jsonl"
    for cible in (jarvis_inbox, jarvis_outbox):
        cible.parent.mkdir(parents=True, exist_ok=True)
        with open(cible, "a", encoding="utf-8") as f:
            f.write(json.dumps(msg, ensure_ascii=False) + "\n")
    # Tracabilite : le depot apparait dans les activites recentes
    try:
        _fo = Path(RACINE, "cerveau-projet", "freelance", "tools-commun",
                   "os_path", "fonctions")
        _fj = JARVIS_DIR / "fonctions"
        for p in (_fo, _fj):
            if str(p) not in sys.path:
                sys.path.insert(0, str(p))
        from historique import historiser
        # trace sous le nom de la routine notation (decision utilisateur
        # 2026-08-26 : les routines sont des elements surveilles avec
        # LEUR propre nom/grade - la couleur rouge G4 s'affiche).
        historiser("notation",
                   "Depose demande d'evaluation periodique des agents",
                   "R", session="session-freelance")
    except Exception:
        pass
    print("[ROUTINE] Demande d'evaluation deposee dans l'inbox de jarvis.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
