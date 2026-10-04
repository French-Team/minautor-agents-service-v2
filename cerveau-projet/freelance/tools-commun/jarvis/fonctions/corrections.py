# -*- coding: utf-8 -*-
"""
fonctions/corrections.py v0.1.0 - Systeme de retro-correction automatique.

Quand une routine de surveillance detecte une erreur pre-existante
(fichier d un agent contient une incoherence), elle ecrit dans
corrections.jsonl. JARVIS traite cette file EN PRIORITE avant toute
autre mission.

Protocole :
  1. Routine detecte erreur -> marquer_correction()
  2. JARVIS (tic ou debut de mission) -> traiter_corrections()
  3. Si corrections en attente :
     a. Mettre la mission principale EN PAUSE (si elle existe)
     b. Activer l agent proprietaire du fichier
     c. Agent corrige -> revient a JARVIS
     d. JARVIS DEPAUSE la mission principale
  4. Si correction echoue -> compteur d echecs, alerte si > seuil

L utilisateur n est JAMAIS mele a ce processus.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

FILES_DIR = Path(__file__).parent.parent / "files"
CORRECTIONS_FILE = FILES_DIR / "corrections.jsonl"
CORRECTIONS_EN_COURS = FILES_DIR / "corrections-en-cours.json"

# Seuils
MAX_ECHECS_PAR_AGENT = 3  # apres 3 echecs, on alerte
MAX_CASCADE = 5  # max de corrections en cascade


def _lire_corrections():
    """Lire toutes les corrections de la file."""
    if not CORRECTIONS_FILE.exists():
        return []
    corrections = []
    for line in CORRECTIONS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            corrections.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return corrections


def _ecrire_corrections(corrections):
    """Ecrire la liste des corrections dans le fichier."""
    CORRECTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CORRECTIONS_FILE, "w", encoding="utf-8") as f:
        for c in corrections:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")


def marquer_correction(agent, fichier, erreur, source="routine",
                       session="session-freelance"):
    """Ajouter une erreur detectee dans la file de corrections.

    Args:
        agent: nom de l agent proprietaire du fichier
        fichier: chemin du fichier en erreur
        erreur: description de l erreur
        source: qui a detecte (nom de la routine)
        session: session concernee
    """
    correction = {
        "id": datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S.") +
              datetime.now().strftime("%f")[:6],
        "agent": agent,
        "fichier": str(fichier),
        "erreur": erreur,
        "source": source,
        "session": session,
        "date_detection": datetime.now(timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%S"),
        "statut": "EN_ATTENTE",  # EN_ATTENTE -> EN_COURS -> CORRIGEE / ECHEC
        "echecs": 0,
        "cascade": 0,
    }
    with open(CORRECTIONS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(correction, ensure_ascii=False) + "\n")
    print(f"[CORRECTION] Erreur detectee pour {agent}: {erreur[:60]}")
    print(f"  Fichier: {fichier}")
    print(f"  Source: {source}")
    return correction["id"]


def traiter_corrections(session="session-freelance"):
    """Traiter les corrections en attente (PRIORITAIRE).

    Retourne True si des corrections ont ete traitees, False sinon.
    Appele par JARVIS a chaque tic et au debut de chaque mission.
    """
    corrections = _lire_corrections()
    en_attente = [c for c in corrections if c.get("statut") == "EN_ATTENTE"]

    if not en_attente:
        return False

    # Trier par date (plus ancien d abord)
    en_attente.sort(key=lambda c: c.get("date_detection", ""))

    print(f"[CORRECTIONS] {len(en_attente)} correction(s) en attente :")
    for c in en_attente:
        print(f"  [{c['id']}] {c['agent']}: {c['erreur'][:60]}")

    # Prendre la premiere correction
    correction = en_attente[0]
    correction["statut"] = "EN_COURS"
    correction["date_debut"] = datetime.now(timezone.utc).strftime(
        "%Y-%m-%dT%H%M:%S")

    # Sauvegarder l etat en cours
    _sauvegarder_en_cours(correction)
    _ecrire_corrections(corrections)

    print(f"\n[CORRECTIONS] TRAITEMENT : {correction['agent']}")
    print(f"  Fichier: {correction['fichier']}")
    print(f"  Erreur: {correction['erreur']}")
    print(f"  -> Activation de {correction['agent']} pour correction")

    return True


def terminer_correction(correction_id, succes=True):
    """Marquer une correction comme terminee.

    Args:
        correction_id: id de la correction
        succes: True si corrigee, False si echec
    """
    corrections = _lire_corrections()
    for c in corrections:
        if c.get("id") == correction_id:
            if succes:
                c["statut"] = "CORRIGEE"
                c["date_fin"] = datetime.now(timezone.utc).strftime(
                    "%Y-%m-%dT%H%M:%S")
                print(f"[CORRECTION] {c['agent']}: CORRIGEE")
            else:
                c["echecs"] = c.get("echecs", 0) + 1
                if c["echecs"] >= MAX_ECHECS_PAR_AGENT:
                    c["statut"] = "ALERTE"
                    print(f"[CORRECTION] {c['agent']}: ECHEC x{c['echecs']}"
                          f" -> ALERTE (seuil atteint)")
                else:
                    c["statut"] = "EN_ATTENTE"
                    print(f"[CORRECTION] {c['agent']}: ECHEC x{c['echecs']}"
                          f" -> remise en attente")
            break
    _ecrire_corrections(corrections)
    _supprimer_en_cours()


def annuler_corrections_agent(agent):
    """Annuler toutes les corrections en attente pour un agent.
    Utile si l agent est deja en train de corriger."""
    corrections = _lire_corrections()
    annulees = 0
    for c in corrections:
        if (c.get("agent") == agent and
                c.get("statut") in ("EN_ATTENTE", "EN_COURS")):
            c["statut"] = "ANNULEE"
            annulees += 1
    if annulees:
        _ecrire_corrections(corrections)
        print(f"[CORRECTIONS] {annulees} correction(s) annulee(s)"
              f" pour {agent}")
    return annulees


def lister_corrections():
    """Lister toutes les corrections (pour le statut)."""
    corrections = _lire_corrections()
    if not corrections:
        print("[CORRECTIONS] Aucune correction enregistree.")
        return
    stats = {}
    for c in corrections:
        s = c.get("statut", "INCONNU")
        stats[s] = stats.get(s, 0) + 1
    print(f"[CORRECTIONS] {len(corrections)} correction(s) :")
    for s, n in stats.items():
        print(f"  {s}: {n}")
    en_attente = [c for c in corrections if c.get("statut") == "EN_ATTENTE"]
    if en_attente:
        print(f"\n  En attente :")
        for c in en_attente:
            print(f"    [{c['id']}] {c['agent']}: {c['erreur'][:50]}")


def a_corrections_en_attente():
    """Verifier s il y a des corrections en attente."""
    corrections = _lire_corrections()
    return any(c.get("statut") == "EN_ATTENTE" for c in corrections)


def get_correction_en_cours():
    """Recuperer la correction en cours de traitement."""
    if not CORRECTIONS_EN_COURS.exists():
        return None
    try:
        return json.loads(CORRECTIONS_EN_COURS.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _sauvegarder_en_cours(correction):
    """Sauvegarder la correction en cours."""
    CORRECTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    CORRECTIONS_EN_COURS.write_text(
        json.dumps(correction, ensure_ascii=False, indent=2),
        encoding="utf-8")


def _supprimer_en_cours():
    """Supprimer le fichier de correction en cours."""
    if CORRECTIONS_EN_COURS.exists():
        CORRECTIONS_EN_COURS.unlink()


def nettoyer_corrections():
    """Supprimer les corrections terminees (> 7 jours)."""
    corrections = _lire_corrections()
    seuil = datetime.now(timezone.utc).timestamp() - 7 * 86400
    avant = len(corrections)
    conservees = []
    for c in corrections:
        date_str = c.get("date_detection", "")
        try:
            ts = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            if ts.timestamp() > seuil or c.get("statut") not in (
                    "CORRIGEE", "ANNULEE"):
                conservees.append(c)
        except ValueError:
            conservees.append(c)
    apres = len(conservees)
    if avant != apres:
        _ecrire_corrections(conservees)
        print(f"[CORRECTIONS] {avant - apres} ancienne(s) correction(s)"
              f" supprimee(s)")
    return avant - apres
