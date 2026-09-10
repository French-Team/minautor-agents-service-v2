"""Fonctions communes de la routine suivi-sync.

Lecture de l'inbox, synchronisation vers suivi-optimus (append-only,
pas de duplication si l'entree existe deja dans le suivi).
"""
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

from constants import (
    CHEMIN_INBOX,
    REPERTOIRE_OUTIL_SUIVI,
    TYPES_INTERESSANTS,
    ENCODAGE,
)


def lire_inbox():
    """Retourne la liste des evenements de l'inbox (liste de dicts)."""
    if not CHEMIN_INBOX.exists():
        return []
    try:
        lignes = CHEMIN_INBOX.read_text(encoding=ENCODAGE).splitlines()
    except OSError:
        return []
    evenements = []
    for ligne in lignes:
        ligne = ligne.strip()
        if not ligne:
            continue
        try:
            evenements.append(json.loads(ligne))
        except json.JSONDecodeError:
            continue
    return evenements


def dernier_date_suivi():
    """Retourne la date du dernier evenement dans le suivi-optimus, ou None."""
    chemin_suivi = REPERTOIRE_OUTIL_SUIVI.parent.parent / "suivi-optimus.jsonl"
    if not chemin_suivi.exists():
        return None
    try:
        lignes = chemin_suivi.read_text(encoding=ENCODAGE).splitlines()
    except OSError:
        return None
    for ligne in reversed(lignes):
        ligne = ligne.strip()
        if not ligne:
            continue
        try:
            d = json.loads(ligne)
            return d.get("date", "")
        except json.JSONDecodeError:
            continue
    return None


def synchroniser():
    """Synchronise les missions terminees de l'inbox vers le suivi-optimus.

    Retourne (nombre_evenements_synchro, messages).
    """
    import sys
    sys.path.insert(0, str(REPERTOIRE_OUTIL_SUIVI.parent.parent / "data" / "commun"))

    evenements_inbox = lire_inbox()
    if not evenements_inbox:
        return 0, ["inbox vide"]

    synchronisees = set()
    if dernier_date_suivi():
        chemin_suivi = REPERTOIRE_OUTIL_SUIVI.parent.parent / "suivi-optimus.jsonl"
        if chemin_suivi.exists():
            try:
                lignes_suivi = chemin_suivi.read_text(encoding=ENCODAGE).splitlines()
                for ligne in reversed(lignes_suivi):
                    ligne = ligne.strip()
                    if not ligne:
                        continue
                    try:
                        d = json.loads(ligne)
                        mission = d.get("mission", "")
                        if mission:
                            synchronisees.add(mission)
                    except json.JSONDecodeError:
                        continue
            except OSError:
                pass

    nouveaux = []
    for ev in evenements_inbox:
        typ = ev.get("type", "")
        if typ not in TYPES_INTERESSANTS:
            continue
        date_ev = ev.get("date", "")
        if not date_ev:
            continue  # Date manquante : on ne peut pas comparer.
        # Determiner la mission et le theme.
        mission = ""
        theme = ""
        if typ == "fin-mission":
            mission = ev.get("mission", "")
            # Protection contre la duplication : si la mission est deja synchronisee, on skip.
            if mission in synchronisees:
                continue
            synchronisees.add(mission)
            bilan = ev.get("bilan", "")
            nouveaux.append(
                (
                    mission,
                    theme,
                    typ,
                    bilan or ev.get("detail", ""),
                    ev.get("date", ""),
                )
            )
        elif typ == "retour-lot":
            lot = ev.get("lot", [])
            bilan_consolide = ev.get("bilan_consolide", "")
            # Pour un retour-lot, on cree une entree par mission du lot.
            for m in lot:
                if m in synchronisees:
                    continue
                synchronisees.add(m)
                nouveaux.append(
                    (
                        m,
                        theme,
                        typ,
                        bilan_consolide,
                        ev.get("date", ""),
                    )
                )

    if not nouveaux:
        return 0, ["aucune mission a synchroniser"]

    messages = []
    for mission, theme, typ, detail, date_ev in nouveaux:
        # Ecrire dans suivi-optimus via subprocess (porte unique).
        try:
            termine = subprocess.run(
                [
                    sys.executable,
                    "main.py",
                    "noter",
                    "--mission", mission,
                    "--theme", theme or "SUIVI-OPTIMUS",
                    "--action", "fin",
                    "--detail", detail,
                    "--duree-s", "0",
                ],
                cwd=str(REPERTOIRE_OUTIL_SUIVI),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=30,
            )
            if termine.returncode == 0:
                messages.append("synchro : " + mission + " (" + typ + ")")
            else:
                messages.append(
                    "echec synchro : " + mission + " (code " + str(termine.returncode) + ")"
                )
                if termine.stderr:
                    messages.append("  " + termine.stderr.strip())
        except Exception as e:
            messages.append("echec synchro : " + mission + " (" + str(e) + ")")

    return len(nouveaux), messages


def noter_boot_check(messages_boot):
    """Note une entree 'decision' dans le suivi-optimus pour un demarrage du serveur."""
    import sys
    sys.path.insert(0, str(REPERTOIRE_OUTIL_SUIVI.parent.parent / "data" / "commun"))

    detail = (
        "Demarrage du serveur matrice (boot-check) : "
        + ("; ".join(messages_boot) if messages_boot else "aucune alerte")
    )
    try:
        termine = subprocess.run(
            [
                sys.executable,
                "main.py",
                "noter",
                "--mission", "",
                "--theme", "SUIVI-OPTIMUS",
                "--action", "decision",
                "--detail", detail,
                "--duree-s", "0",
            ],
            cwd=str(REPERTOIRE_OUTIL_SUIVI),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
        if termine.returncode == 0:
            return 0, ["boot-check note dans suivi-optimus"]
        else:
            return 1, ["echec boot-check note (code " + str(termine.returncode) + ")"]
    except Exception as e:
        return 1, ["echec boot-check note (" + str(e) + ")"]
