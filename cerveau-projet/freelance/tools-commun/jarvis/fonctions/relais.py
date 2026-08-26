# -*- coding: ascii -*-
"""fonctions/relais.py - UNE tache : POUSSE vers stark les messages du
hub qui lui sont destines (decision utilisateur 2026-08-25).

Avant : EDITH deposait dans le hub (inbox/jarvis.jsonl) et le message
y dormait jusqu'a ce que quelqu'un vienne le lire. Desormais : a chaque
invocation de jarvis ET a chaque tic du daemon, JARVIS TRANSMET lui-
meme les messages non-lus du hub a stark :
  - copie dans inbox/stark.jsonl : de=jarvis, corps prefixe
    "[RELAI - de <expediteur>, id original <id>]"
  - message du hub marque lu (transmis = traite par le routeur)
  - historisation.

Les messages d'activation (type activation) ne sont PAS relaires ici :
ils suivent deja le chainage activer. Le relais ne s'auto-declenche pas
sur ses propres messages (de=jarvis).
"""

import json
import os
import sys
from pathlib import Path

_sys_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "..", "os_path", "fonctions")
sys.path.insert(0, _sys_dir)
from racine import trouver_racine  # noqa: E402

RACINE = Path(trouver_racine(__file__))
JARVIS_DIR = RACINE / "cerveau-projet" / "freelance" / "tools-commun" / "jarvis"

VERSION = "0.1.0"


def relayer_vers_stark():
    """Transmettre les messages hub non-lus (hors activations) a stark.
    Retourne le nombre de messages relais."""
    hub = JARVIS_DIR / "inbox" / "jarvis.jsonl"
    if not hub.exists():
        return 0
    try:
        lignes = hub.read_text(encoding="utf-8").splitlines()
    except OSError:
        return 0
    messages = []
    for ligne in lignes:
        if not ligne.strip():
            continue
        try:
            m = json.loads(ligne)
        except ValueError:
            continue
        if not m.get("lu") and m.get("type") != "activation" \
                and str(m.get("vers", "")) == "jarvis" \
                and str(m.get("de", "")) != "jarvis":
            messages.append(m)
    if not messages:
        return 0
    import uuid
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    nouveaux_lignes = []
    ids_hub_lus = {m.get("id") for m in messages}
    for ligne in lignes:
        if not ligne.strip():
            nouveaux_lignes.append(ligne)
            continue
        try:
            m = json.loads(ligne)
        except ValueError:
            nouveaux_lignes.append(ligne)
            continue
        # marque lu dans le hub : transmis par le routeur
        if m.get("id") in ids_hub_lus and not m.get("lu"):
            m["lu"] = True
            m["accuse"] = True
        nouveaux_lignes.append(json.dumps(m, ensure_ascii=False))
    hub.write_text("\n".join(nouveaux_lignes) + "\n", encoding="utf-8")

    from historique import historiser, session_courante
    session = session_courante()
    for m in messages:
        copie = {
            "id": str(uuid.uuid4())[:8],
            # destination FIXE du relai : decision utilisateur - jarvis
            # transmet les demandes d'EDITH au coordinateur.
            "de": "jarvis", "vers": "stark",  # destination fixe (decision)
            "priorite": int(m.get("priorite", 3)),
            "date": now,
            "objet": "[RELAI] %s" % str(m.get("objet", ""))[:70],
            "corps": ("[RELAI JARVIS - de %s, id original %s]\n%s"
                      % (m.get("de"), m.get("id"),
                         str(m.get("corps", "")))),
            "lu": False, "accuse": False,
        }
        inbox_stark = JARVIS_DIR / "inbox" / "stark.jsonl"
        outbox_jarvis = JARVIS_DIR / "outbox" / "jarvis.jsonl"
        # outbox/jarvis = TRACE cote expediteur (jamais a lire)
        trace = dict(copie)
        trace["lu"] = True
        trace["accuse"] = True
        for cible, ecrit in ((inbox_stark, copie),
                             (outbox_jarvis, trace)):
            with open(cible, "a", encoding="utf-8") as f:
                f.write(json.dumps(ecrit, ensure_ascii=False) + "\n")
        historiser("jarvis", "Relai vers stark : %s (id original %s)"
                   % (str(m.get("objet", ""))[:50], m.get("id")),
                   session=session)
    return len(messages)


def cmd_relayer(args=None):
    n = relayer_vers_stark()
    print("[JARVIS] Relai : %d message(s) du hub transmis a stark."
          % n if n else "[JARVIS] Relai : rien a transmettre.")
