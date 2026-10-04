# -*- coding: ascii -*-
"""fonctions/harnais_oracle.py - Harnais de surveillance des agents v1.

Surveille l'etat de la coordination v1 et signale chaque ecart :
  - message_non_lu : un message P1 reste non lu depuis N jours
  - agent_inactif : un agent n'a plus d'activite depuis N jours
  - mission_abandonnee : une mission EN_ATTENTE depuis N jours
  - defcon_gele : DEFCON 5 declare mais pas descendu depuis N jours

Le harnais ne modifie JAMAIS le fonctionnement : il DETECTE et SIGNALE.
Lecture seule des fichiers Oracle + ecriture d'une alerte dans
l inbox de cerberus (le coordinateur).
"""

import json
import os
from datetime import datetime, timezone, timedelta

# Chemin relatif : fonctions/ -> oracle/
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INBOX_DIR = os.path.join(BASE, "inbox")
OUTBOX_DIR = os.path.join(BASE, "outbox")
FILES_DIR = os.path.join(BASE, "files")
DATA_FILE = os.path.join(BASE, "oracle-data.json")

VERSION = "0.1.0"

SEUILS = {
    "message_non_lu_jours": 2,
    "agent_inactif_jours": 7,
    "mission_abandonnee_jours": 7,
    "defcon_gele_jours": 3,
}


def charger_agents():
    """Liste des agents depuis oracle-data.json."""
    try:
        with open(DATA_FILE, encoding="utf-8") as f:
            return json.load(f).get("agents", [])
    except (OSError, ValueError):
        return []


def _lire_jsonl(chemin):
    """Lire un fichier JSONL : [(contenu_brut, dict_ou_None), ...]."""
    if not os.path.isfile(chemin):
        return []
    lignes = []
    with open(chemin, encoding="utf-8", errors="replace") as fh:
        for ligne in fh:
            brut = ligne.strip()
            if not brut:
                continue
            try:
                lignes.append((brut, json.loads(brut)))
            except ValueError:
                lignes.append((brut, None))
    return lignes


def verifier(seuils=None):
    """Scan complet : retourne la liste des ecarts detectes."""
    seuils = seuils or SEUILS
    ecarts = []
    maintenant = datetime.now(timezone.utc).replace(tzinfo=None)

    # 1. message_non_lu : P1 non lu depuis N jours
    for nom_fichier in sorted(os.listdir(INBOX_DIR)) if os.path.isdir(INBOX_DIR) else []:
        if not nom_fichier.endswith(".jsonl"):
            continue
        chemin = os.path.join(INBOX_DIR, nom_fichier)
        for _, msg in _lire_jsonl(chemin):
            if not isinstance(msg, dict) or msg.get("lu"):
                continue
            if msg.get("priorite") != 1:
                continue
            try:
                d = datetime.strptime(str(msg.get("date", ""))[:19],
                                      "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                continue
            age = (maintenant - d).days
            if age >= seuils.get("message_non_lu_jours", 2):
                ecarts.append({
                    "type": "message_non_lu",
                    "message": f"message P1 non lu depuis {age} jour(s) "
                               f"pour {nom_fichier[:-6]} (id {msg.get('id')})",
                    "agent": nom_fichier[:-6],
                })

    # 2. agent_inactif : fiche/corrections existent mais aucun message recent
    agents = charger_agents()
    for a in agents:
        nom = a.get("nom", "?")
        # Dernier message dans inbox ou outbox
        dernier = None
        for dossier in (INBOX_DIR, OUTBOX_DIR):
            if not os.path.isdir(dossier):
                continue
            chemin = os.path.join(dossier, f"{nom}.jsonl")
            for _, msg in _lire_jsonl(chemin):
                if not isinstance(msg, dict):
                    continue
                try:
                    d = datetime.strptime(str(msg.get("date", ""))[:19],
                                          "%Y-%m-%dT%H:%M:%S")
                except ValueError:
                    continue
                if dernier is None or d > dernier:
                    dernier = d
        if dernier is None:
            continue  # jamais de message = pas encore utilise
        age = (maintenant - dernier).days
        if age >= seuils.get("agent_inactif_jours", 7):
            ecarts.append({
                "type": "agent_inactif",
                "message": f"agent {nom} inactif depuis {age} jour(s) "
                           f"(dernier message {dernier.strftime('%d/%m')})",
                "agent": nom,
            })

    # 3. mission_abandonnee : EN_ATTENTE depuis N jours
    for nom_fichier in sorted(os.listdir(FILES_DIR)) if os.path.isdir(FILES_DIR) else []:
        if nom_fichier == "defcon.jsonl" or not nom_fichier.endswith(".jsonl"):
            continue
        chemin = os.path.join(FILES_DIR, nom_fichier)
        for _, m in _lire_jsonl(chemin):
            if m is None or m.get("statut") != "EN_ATTENTE":
                continue
            try:
                d = datetime.strptime(str(m.get("date", ""))[:10], "%Y-%m-%d")
            except ValueError:
                continue
            age = (maintenant - d).days
            if age >= seuils.get("mission_abandonnee_jours", 7):
                ecarts.append({
                    "type": "mission_abandonnee",
                    "message": f"mission en attente depuis {age} jour(s) "
                               f"({m.get('id')}) : {m.get('mission', '')[:40]}",
                    "agent": m.get("agent", "?"),
                })

    # 4. defcon_gele : DEFCON 5 non descendu depuis N jours
    defcon_file = os.path.join(FILES_DIR, "defcon.jsonl")
    if os.path.isfile(defcon_file):
        dernier_defcon = None
        for _, e in _lire_jsonl(defcon_file):
            if e is None or e.get("niveau") is None:
                continue
            try:
                d = datetime.strptime(str(e.get("date", ""))[:19],
                                      "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                continue
            if dernier_defcon is None or d > dernier_defcon[0]:
                dernier_defcon = (d, e.get("niveau"))
        if dernier_defcon and dernier_defcon[1] == 5:
            age = (maintenant - dernier_defcon[0]).days
            if age >= seuils.get("defcon_gele_jours", 3):
                ecarts.append({
                    "type": "defcon_gele",
                    "message": f"DEFCON 5 non descendu depuis {age} jour(s) "
                               f"(validation des reparations attendue)",
                    "agent": "oracle",
                })

    return ecarts


def signaler(ecarts):
    """Ecrire une alerte dans l inbox de cerberus."""
    if not ecarts:
        return
    message = {
        "id": f"harnais-{datetime.now().strftime('%H%M%S')}",
        "de": "oracle-harnais",
        "vers": "cerberus",
        "priorite": 1,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "objet": f"[HARNAIS-ORACLE] {len(ecarts)} ecart(s) detecte(s)",
        "corps": "\n".join(f"- [{e['type']}] {e['message']}" for e in ecarts),
        "lu": False,
        "accuse": False,
        "type": "harnais-oracle",
    }
    cible = os.path.join(INBOX_DIR, "cerberus.jsonl")
    with open(cible, "a", encoding="utf-8") as f:
        f.write(json.dumps(message, ensure_ascii=False) + "\n")
    return message


def cmd_harnais(args):
    """CLI : verifier + signaler."""
    ecarts = verifier()
    if not ecarts:
        print("[HARNAIS-ORACLE] Aucun ecart - la v1 se comporte bien.")
        return
    print(f"[HARNAIS-ORACLE] {len(ecarts)} ecart(s) detecte(s):")
    for e in ecarts:
        print(f"  - [{e['type']}] {e['message']}")
    # Signaler a cerberus
    msg = signaler(ecarts)
    if msg:
        print(f"[HARNAIS-ORACLE] Alerte envoyee a cerberus ({msg['id']})")
