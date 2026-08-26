# -*- coding: ascii -*-
"""fonctions/etat.py - module du combo ETAT."""
import re
from datetime import datetime
from lib_lecture import lire_texte, lire_jsonl, dernieres_lignes
from commun import AGENTS_CONNUS


def combo_etat(besoin):
    """v0.2.0 : temps 2 REEL - etat verifie du systeme."""
    sessions = []
    contenu = lire_texte("AGENTS.md")
    if contenu:
        blocs = re.split(r"(?=### Session : )", contenu)
        for bloc in blocs:
            m = re.search(r"### Session : (\S+)", bloc)
            if not m:
                continue
            nom_llm = re.search(r"\*\*Nom LLM\*\* \| (.+?) \|", bloc)
            agent = re.search(r"\*\*Nom Agent\*\* \| (.+?) \|", bloc)
            date = re.search(r"\*\*Derniere mise a jour\*\* \| (.+?) \|", bloc)
            sessions.append({
                "session": m.group(1),
                "llm": nom_llm.group(1).strip() if nom_llm else "?",
                "agent_actif": agent.group(1).strip() if agent else "?",
                "maj": date.group(1).strip() if date else "?",
            })
    # Corps v2 (decision 2026-08-26 : fichiers separes par session,
    # la v2 lit AGENTS-historique-v2.md)
    activite = dernieres_lignes("AGENTS-historique-v2.md", 20)
    bloques = []
    for nom in AGENTS_CONNUS:
        for msg in lire_jsonl(
                "cerveau-projet/freelance/tools-commun/jarvis/inbox/%s.jsonl" % nom):
            if not msg.get("lu") and msg.get("priorite") == 1:
                bloques.append({"agent": nom, "id": msg.get("id"),
                                "objet": msg.get("objet")})
    return {
        "combo": "ETAT",
        "besoin": besoin,
        "statut": "OK",
        "sessions": sessions,
        "activite_recente": activite,
        "agents_bloques_P1": bloques,
        "date": datetime.now().isoformat(timespec="seconds"),
    }
