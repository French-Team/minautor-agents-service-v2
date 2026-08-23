# -*- coding: ascii -*-
"""logique_files.py - UNE tache : la logique des files d'attente et du
stop-dev pour le serveur MCP (protocole 14 - extrait v0.8.0)."""

import json
from datetime import datetime, timezone
from pathlib import Path

JARVIS_DIR = Path(__file__).parent.parent
FILES_DIR = JARVIS_DIR / "files"


def _chemin_file(nom):
    return FILES_DIR / f"{nom}.jsonl"


def mettre_en_attente(mission, contexte="", niveau="attente", agent=""):
    niveaux = {
        "attente": ("file-attente", "EN_ATTENTE", "ATTENTE"),
        "attention": ("file-asap", "SUIVANTE", "AT-1"),
        "urgent": ("file-attente", "PRIORITAIRE", "UR-1"),
    }
    if niveau not in niveaux:
        return f"ERREUR: niveau inconnu '{niveau}' (attente/attention/urgent)"
    file, statut, type_d = niveaux[niveau]
    entree = {
        "type": type_d,
        "mission": mission,
        "agent": agent,
        "contexte_avant": contexte,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "statut": statut,
    }
    chemin = _chemin_file(file)
    with open(chemin, "a", encoding="utf-8") as f:
        f.write(json.dumps(entree, ensure_ascii=False) + "\n")
    return (f"[JARVIS] Mission placee en {file} (statut: {statut}, "
            f"declencheur: [{niveau}]).\n  Mission: {mission}")


def stop_dev(raison):
    gelees = 0
    for nom in ("file-attente", "file-asap"):
        chemin = _chemin_file(nom)
        if not chemin.exists():
            continue
        lignes = [l for l in chemin.read_text(encoding="utf-8").splitlines()
                  if l.strip()]
        modifie = False
        for i, l in enumerate(lignes):
            try:
                e = json.loads(l)
            except ValueError:
                continue
            if e.get("statut") in ("EN_ATTENTE", "PREPAREE", "SUIVANTE",
                                   "PRIORITAIRE"):
                e["statut"] = "DEFCON5"
                lignes[i] = json.dumps(e, ensure_ascii=False)
                modifie = True
                gelees += 1
        if modifie:
            chemin.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    defcon = {"date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
              "niveau": 5, "raison": raison, "missions_gelees": gelees}
    with open(FILES_DIR / "defcon.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(defcon, ensure_ascii=False) + "\n")
    return (f"*** [STOP] DEFCON 5 - ARRET COMPLET DU DEV ***\n  Raison: {raison}\n"
            f"  Missions gelees: {gelees}")


def lister_files():
    result = []
    for nom in ("file-attente", "file-asap"):
        chemin = _chemin_file(nom)
        entrees = []
        if chemin.exists():
            for l in chemin.read_text(encoding="utf-8").splitlines():
                if not l.strip():
                    continue
                try:
                    e = json.loads(l)
                except ValueError:
                    continue
                if e.get("statut") not in (None, "VIDE"):
                    entrees.append(e)
        result.append(f"[{nom}] {len(entrees)} entree(s)")
        for e in entrees:
            result.append(f"  [{e.get('statut')}] {e.get('mission', '')[:70]} "
                          f"({e.get('date', '')})")
    return "\n".join(result)


def reprendre_mission(file="file-attente"):
    ordre = ["PRIORITAIRE", "SUIVANTE", "EN_ATTENTE", "PREPAREE"]
    fichiers = [("file-attente", _chemin_file("file-attente")),
                ("file-asap", _chemin_file("file-asap"))]
    if file != "file-attente":
        fichiers = [f for f in fichiers if f[0] == file]
    candidates = []
    for nom, chemin in fichiers:
        if not chemin.exists():
            continue
        lignes = [l for l in chemin.read_text(encoding="utf-8").splitlines()
                  if l.strip()]
        for i in range(len(lignes) - 1, -1, -1):
            try:
                e = json.loads(lignes[i])
            except ValueError:
                continue
            statut = e.get("statut")
            if statut in ordre:
                candidates.append((ordre.index(statut), len(candidates), nom,
                                   chemin, lignes, i, e))
    if not candidates:
        return "[JARVIS] Aucune mission en attente."
    _, _, nom, chemin, lignes, i, e = min(candidates,
                                          key=lambda c: (c[0], -c[1]))
    e["statut"] = "REPRISE"
    e["date_reprise"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    lignes[i] = json.dumps(e, ensure_ascii=False)
    chemin.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    sortie = [f"[JARVIS] Mission reprise depuis {nom} :",
              f"  Mission: {e.get('mission')}"]
    if e.get("contexte_avant"):
        sortie.append(f"  Contexte avant mise en attente: {e['contexte_avant']}")
    return "\n".join(sortie)
